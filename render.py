"""
render.py - details.py-র প্রতিটা উদাহরণ চালিয়ে তার আউটপুট (চার্টের ছবি, তৈরি হওয়া
ফাইলের প্রিভিউ, টার্মিনালের লেখা) outputs.json-এ জমা করে। build.py সেটা সাইটে বসায়।

    python render.py                 # যেগুলোর কোড বদলেছে শুধু সেগুলো
    python render.py matplotlib      # নির্দিষ্ট লাইব্রেরি
    python render.py --force         # সব আবার

দরকার: যেসব লাইব্রেরির উদাহরণ চালাবে সেগুলো ইনস্টল থাকতে হবে।
ঐচ্ছিক: LibreOffice (Word/Excel/PowerPoint প্রিভিউ), Playwright + Chrome (HTML প্রিভিউ)।
"""
import base64
import hashlib
import importlib.metadata as md
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import atexit
import glob
import socket
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from details import DETAILS, examples_of  # noqa: E402

OUT = ROOT / "outputs.json"
PY = sys.executable
CHROME = shutil.which("google-chrome") or shutil.which("chromium")

# ভারী/পরস্পরবিরোধী ডিপেন্ডেন্সির লাইব্রেরি আলাদা venv-এ (না থাকলে সাধারণ python)
VENV = {"bpy": "/opt/venv-bpy", "graph-tool": "/opt/venv-gt", "graspologic": "/opt/venv-gsp", "docling": "/opt/venv-docling", "marker-pdf": "/opt/venv-marker", "surya-ocr": "/opt/venv-marker",
        "paddleocr": "/opt/venv-paddle", "poliastro": "/opt/venv-poli", "deepchem": "/opt/venv-dc", "fenicsx (dolfinx)": "/opt/venv-fem", "pychrono": "/opt/venv-chrono", "genesis-world": "/opt/venv-gen",
        "apache-airflow": "/opt/venv-airflow", "prefect": "/opt/venv-prefect", "dagster": "/opt/venv-dagster", "dbt-core": "/opt/venv-dbt",
        "mlflow": "/opt/venv-mlflow", "dvc": "/opt/venv-dvc", "bentoml": "/opt/venv-bento", "litserve": "/opt/venv-lit",
        "py5": "/opt/venv-py5", "sketchpy": "/opt/venv-skp"}
TIMEOUT = {"warp-lang": 900, "brax": 900, "fipy": 600, "fenicsx (dolfinx)": 900, "pybullet": 600, "pydrake": 900, "PyFoam / fluidfoam": 900, "pychrono": 900, "genesis-world": 1500, "pymunk": 600, "mesa": 600, "simpy": 600, "mujoco": 300, "pymol": 600, "scanpy": 900, "deepchem": 1200, "pydeseq2": 600, "ase": 900, "igv-notebook": 600, "mdanalysis": 600, "rdkit": 300, "pymatgen": 300, "bpy": 1200, "mitsuba (mitsuba3)": 900, "open3d": 600, "taichi": 600, "pyvista": 600, "vtk": 600, "vedo": 600, "pymeshlab": 600, "rerun-sdk": 600, "torchgeo": 1800, "whitebox": 900, "satpy": 900, "osmnx": 600, "pysal": 600, "geoviews": 600, "leafmap": 400, "lonboard": 400, "stackstac": 1200, "xarray": 600, "rasterio": 600, "gdal (osgeo)": 600, "rioxarray": 900, "pystac-client": 300, "cartopy": 600, "quarto": 900, "docling": 900, "marker-pdf": 1500, "surya-ocr": 900, "paddleocr": 600, "easyocr": 600, "unstructured": 600,
           "segment-anything": 900, "ultralytics": 900, "timm": 600, "supervision": 600, "kornia": 600,
           "flair": 900, "stanza": 900, "pyvips": 600,
           "numba": 600, "ortools": 300, "tox": 900, "nox": 900, "nuitka": 1200, "pyinstaller": 900, "uv": 600, "poetry": 600, "hatch": 600, "pdm": 600,
           "pyright": 300, "ty": 300, "cython": 300, "mypyc": 300, "pylint": 300, "ruff": 300, "apache-airflow": 600, "prefect": 600, "dagster": 600, "dbt-core": 600, "mlflow": 600,
           "bentoml": 600, "litserve": 300, "ray[serve]": 600, "docker": 600, "aws-cdk-lib": 300, "dvc": 300, "wandb": 300, "rebound": 600, "lightkurve": 900, "astroquery": 600, "sunpy": 600, "astropy": 300, "poliastro": 600, "colour-science": 300, "sketchpy": 300}
# বাংলা লেখা PDF-এ বসাতে ফন্ট (উদাহরণগুলো BN_FONT env পড়ে)
for _f in ("/usr/local/share/fonts/bn/NotoSansBengali-Regular.ttf", "/usr/share/fonts/truetype/noto/NotoSansBengali-Regular.ttf"):
    if os.path.exists(_f):
        os.environ.setdefault("BN_FONT", _f)
        os.environ.setdefault("BN_FONT_BOLD", _f.replace("Regular", "Bold"))
        break


EXTRA_BIN = {"poetry": "/opt/venv-pkg/bin", "hatch": "/opt/venv-pkg/bin", "pdm": "/opt/venv-pkg/bin",
             "uv": os.path.expanduser("~/.local/bin")}


def py_for(name):
    v = VENV.get(name)
    return f"{v}/bin/python" if v and os.path.exists(f"{v}/bin/python") else PY

# ইন্টারনেট, API key বা আলাদা সার্ভার লাগে – এখানে চালানো হয় না
NEEDS_NET = {
    "gsplat": "NVIDIA GPU + CUDA লাগে (rasterization কার্নেল CUDA-তে)", "nerfstudio": "NVIDIA GPU + CUDA আর বহু ছবির ডেটাসেট লাগে (প্রশিক্ষণ কয়েক ঘণ্টা)",
    "earthengine-api": "Google Earth Engine অ্যাকাউন্ট, Cloud প্রজেক্ট ও অনুমোদন (earthengine authenticate) লাগে",
    "cupy": "NVIDIA GPU + CUDA লাগে", "kubernetes": "চালু Kubernetes ক্লাস্টার লাগে (এখানে kind/k3s চালানো যায়নি)", "sagemath": "SageMath আলাদা বিশাল ব্যবস্থা (conda/ডকার) – pip-এ নেই",
    "requests": "ইন্টারনেট লাগে", "httpx": "ইন্টারনেট লাগে",
    "openai": "OpenAI API key লাগে", "anthropic": "Anthropic API key লাগে",
    "langchain": "API key লাগে", "transformers": "মডেল ডাউনলোড করতে ইন্টারনেট লাগে",
    "gradio": "ব্রাউজারে চলা অ্যাপ", "streamlit": "ব্রাউজারে চলা অ্যাপ (streamlit run)",
    "pymongo": "MongoDB সার্ভার লাগে", "scrapy": "ইন্টারনেট লাগে",
    "selenium": "ইন্টারনেট/ব্রাউজার লাগে", "django": "সার্ভার হিসেবে চলে",
    "tensorflow": "ডেটা ডাউনলোড ও লম্বা ট্রেনিং", "keras": "ডেটা ডাউনলোড ও লম্বা ট্রেনিং",
    "spacy": "ভাষা মডেল ডাউনলোড লাগে", "nltk": "ডেটা ডাউনলোড লাগে",
    "onnxruntime": "PyTorch আর একটা .onnx মডেল ফাইল লাগে",
    "sentence-transformers": "মডেল ডাউনলোড লাগে", "llama-index": "API key লাগে",
    "litellm": "API key লাগে", "ollama": "Ollama অ্যাপ ও মডেল লাগে",
    "llama-cpp-python": ".gguf মডেল ফাইল লাগে", "peft": "মডেল ডাউনলোড ও GPU লাগে",
    "diffusers": "GPU ও মডেল ডাউনলোড লাগে", "chromadb": "embedding মডেল ডাউনলোড লাগে",
    "tiktoken": "encoding ফাইল ডাউনলোড লাগে",
    "litestar": "সার্ভার হিসেবে চলে (uvicorn)", "quart": "সার্ভার হিসেবে চলে",
    "tornado": "সার্ভার হিসেবে চলে", "sanic": "সার্ভার হিসেবে চলে",
    "pyramid": "সার্ভার হিসেবে চলে", "bottle": "সার্ভার হিসেবে চলে",
    "fasthtml": "ব্রাউজারে চলা অ্যাপ", "strawberry-graphql": "এখানে ইনস্টল নেই; নিজের কম্পিউটারে চালালে data ছাপবে",
    "graphene": "এখানে ইনস্টল নেই; নিজের কম্পিউটারে চালালে data ছাপবে",
    "ariadne": "এখানে ইনস্টল নেই; নিজের কম্পিউটারে চালালে data ছাপবে",
    "grpcio": ".proto থেকে কোড তৈরি ও সার্ভার লাগে",
    "aiohttp": "ইন্টারনেট/সার্ভার লাগে", "curl_cffi": "ইন্টারনেট লাগে", "zeep": "ইন্টারনেট লাগে",
    "bravado": "ইন্টারনেট লাগে", "websockets": "সার্ভার ও ক্লায়েন্ট আলাদা চলে",
    "python-socketio": "সার্ভার হিসেবে চলে", "twisted": "সার্ভার হিসেবে চলে",
    "netmiko": "নেটওয়ার্ক ডিভাইস লাগে", "napalm": "নেটওয়ার্ক ডিভাইস লাগে",
    "celery": "Redis ও worker লাগে", "dramatiq": "Redis ও worker লাগে", "taskiq": "Redis ও worker লাগে",
    "huey": "worker প্রসেস লাগে", "rq": "Redis ও worker লাগে", "pyzmq": "দুটো আলাদা প্রসেস লাগে",
    "pika": "RabbitMQ সার্ভার লাগে", "confluent-kafka": "Kafka সার্ভার লাগে",
    "pymysql": "MySQL সার্ভার লাগে", "aiomysql": "MySQL সার্ভার লাগে",
    "motor": "MongoDB সার্ভার লাগে", "beanie": "MongoDB সার্ভার লাগে",
    "azure-sdk": "Azure অ্যাকাউন্ট লাগে", "google-cloud-*": "Google Cloud অ্যাকাউন্ট লাগে",
    "reflex": "Node.js-সহ reflex init করা প্রজেক্ট লাগে",
    "pyautogui": "আসল স্ক্রিন/মাউস লাগে – সার্ভারে ডিসপ্লে নেই",
    "dgl": "DGL-এর wheel Python 3.13 + নতুন PyTorch-এর জন্য নেই (উন্নয়ন ২০২৪-এ থেমেছে) – Python ≤3.12 আর PyTorch ≤2.4-এ চালাও",
    "pycaret": "পাইথন ৩.১১ পর্যন্ত ও পুরনো scikit-learn লাগে – আলাদা venv-এ চালাও",
    "mlx": "শুধু Apple Silicon (M1/M2/M3…) Mac-এ চলে",
}
NEEDS_NET_EX = {
    ("volatility3", 1): "প্রশিক্ষণ-মেমরি-ইমেজ (কয়েক GB) লাগে – নিজের কম্পিউটারে চালাও",
    ("pulumi", 1): "Pulumi CLI আর নিজের AWS অ্যাকাউন্ট লাগে", ("wandb", 1): "W&B সার্ভার/অ্যাকাউন্ট লাগে (sweep অনলাইনে চলে)",("playwright", 0): "ইন্টারনেট লাগে", ("boto3", 0): "AWS অ্যাকাউন্ট লাগে",
                ("surya-ocr", 2): "Surya 2 OCR মডেল চালাতে NVIDIA GPU (vLLM) বা llama.cpp সার্ভার লাগে – এখানে নেই"}
# libraries.json-এর নাম ≠ pip প্যাকেজের নাম
DIST = {"wgpu (wgpu-py)": "wgpu", "mitsuba (mitsuba3)": "mitsuba", "libigl (igl)": "libigl", "p5 (p5py)": "p5", "gdal (osgeo)": "gdal", "quarto": "quarto-cli", "python-markdown": "markdown", "ponyorm": "pony", "redis-py": "redis", "valkey-py": "valkey", "psycopg (psycopg3)": "psycopg",
        "django-orm": "django", "boto3": "moto", "ray[tune]": "ray", "torch (PyTorch)": "torch",
        "pytorch-lightning": "lightning", "pymupdf (fitz)": "pymupdf", "av (PyAV)": "av", "pillow (PIL)": "pillow", "segment-anything": "segment_anything", "presidio": "presidio-analyzer", "python-igraph": "igraph", "Skyfield (JS)": "skyfield", "ray[serve]": "ray", "ansible": "ansible-core", "mypyc": "mypy",
        "pymol": "pymol-open-source-whl", "Box2D (pybox2d)": "Box2D", "warp-lang": "warp-lang", "fenicsx (dolfinx)": "fenics-dolfinx", "pydrake": "drake", "PyFoam / fluidfoam": "fluidfoam", "genesis-world": "genesis-world", "openbabel": "openbabel-wheel", "mdanalysis": "MDAnalysis"}
# এগুলোর জন্য লোকাল সার্ভার চালু করা হয় (থাকলে); না থাকলে skip
SERVICES = {"psycopg (psycopg3)": "postgres", "psycopg2": "postgres", "asyncpg": "postgres",
            "redis-py": "redis", "valkey-py": "redis", "neo4j": "neo4j", "fabric": "sshd", "paramiko": "sshd", "docker": "docker"}
SERVICE_REASON = {"postgres": "PostgreSQL সার্ভার লাগে", "redis": "Redis/Valkey সার্ভার লাগে", "neo4j": "Neo4j সার্ভার লাগে",
                  "sshd": "SSH সার্ভার লাগে", "docker": "Docker daemon লাগে"}
SERVER_TESTS = {
    ("flask", 0): 'c = app.test_client()\nprint("GET /  →", c.get("/").status_code, c.get("/").get_data(as_text=True))\nprint("GET /hello/Rahim →", c.get("/hello/Rahim").get_data(as_text=True))',
    ("flask", 1): 'c = app.test_client()\nr = c.post("/observations", json={"place": "Sundarbans", "species": "Kingfisher", "count": 3})\nprint("POST /observations →", r.status_code, r.get_json())\nr = c.post("/observations", json={"place": "X"})\nprint("POST (ভুল ডেটা) →", r.status_code, r.get_json())\nprint("GET /observations →", c.get("/observations").get_json())',
    ("starlette", 0): 'from starlette.testclient import TestClient\nc = TestClient(app)\nprint("GET / →", c.get("/").json())\nprint("GET /square/7 →", c.get("/square/7").json())',
    ("starlette", 1): 'from starlette.testclient import TestClient\nc = TestClient(app)\nprint("GET /status →", c.get("/status").json())\nwith c.websocket_connect("/live") as ws:\n    for _ in range(11):\n        msg = ws.receive_json()\n        print("ws →", msg)',
}
HTML_WAIT = {}          # ফাইলের নাম → কত ms অপেক্ষা (CDN-নির্ভর HTML-এর জন্য)
HTML_WAIT.update({"divisions_map.html": 9000, "survey_map.html": 9000, "leafmap_basic.html": 6000, "haor_field.html": 9000, "trips_hex.html": 7000, "flows.html": 7000,
    "survey_points.html": 9000, "upazila_3d.html": 8000, "kepler_trips.html": 12000, "kepler_timeline.html": 12000, "stations_geoviews.html": 6000, "era5_april_geoviews.html": 6000})
HTML_WAIT.update({"stations_map.html": 4500, "rain_choropleth.html": 5000})
HTML_WAIT.update({"water_3d.html": 4000, "hemoglobin_grid.html": 7000, "ubiquitin_ngl.html": 10000, "adk_open.html": 7000, "molstar_4hhb.html": 12000,
    "molstar_ubiquitin.html": 12000, "igv_hbb.html": 9000, "igv_toy.html": 7000})
HTML_WAIT.update({"site_preview.html": 4000, "ndvi_lecture.html": 2500, "sylhet_rain.html": 1500})
APP_NOTE = "▶ অ্যাপটা আসলে চালিয়ে ব্রাউজারে তোলা স্ক্রিনশট (নিজের কম্পিউটারে চালালে http://127.0.0.1:পোর্ট খোলো)\n"
# (lib, উদাহরণ) → ওয়েব-অ্যাপ সার্ভার চালিয়ে স্ক্রিনশট
APPS = {
    ("rerun-sdk", 0): dict(port=9090, wait=25000, width=1300, height=800, path="/?url=rerun%2Bhttp%3A%2F%2F127.0.0.1%3A9877%2Fproxy", log=True),
    ("rerun-sdk", 1): dict(port=9090, wait=25000, width=1300, height=800, path="/?url=rerun%2Bhttp%3A%2F%2F127.0.0.1%3A9877%2Fproxy", log=True),
    ("dash", 0): dict(port=8050, wait=5000, steps=[("click", "#division"), ("click", "text=Dhaka"), ("shot", "1500")]),
    ("dash", 1): dict(port=8050, wait=6000, height=900, steps=[("click", "#bar g.point path >> nth=7"), ("shot", "2000")]),
    ("panel", 0): dict(port=5006, wait=6000),
    ("panel", 1): dict(port=5006, wait=8000, height=900),
    ("nicegui", 0): dict(port=8080, wait=3000, steps=[("fill", "input", "Rahim"), ("click", "text=চাপো"),
                                                       ("click", "text=চাপো"), ("shot", "800")]),
    ("nicegui", 1): dict(port=8080, wait=6000, height=900, steps=[("click", ".q-toggle >> nth=2"), ("shot", "6000")]),
    ("shiny", 0): dict(port=8000, wait=4000),
    ("shiny", 1): dict(port=8000, wait=6000, height=900),
    ("solara", 0): dict(port=8765, wait=6000, cmd=[PY, "-m", "solara", "run", "main.py", "--port", "8765", "--production", "--no-open"],
                        steps=[("click", "text=৳50,000"), ("shot", "1500")]),
    ("solara", 1): dict(port=8765, wait=7000, height=900,
                        cmd=[PY, "-m", "solara", "run", "main.py", "--port", "8765", "--production", "--no-open"]),
    ("dash-cytoscape", 0): dict(port=8050, wait=5000),
    ("dash-cytoscape", 1): dict(port=8050, wait=5000, height=660),
}
HTML_WAIT.update({"rivers.html": 5000, "writers.html": 9000, "karate_widget.html": 8000})
HTML_WAIT.update({"notebook.html": 7000, "explorer.html": 7000, "profile.html": 7000,
                  "bmi_widgets.html": 6000, "loan_app.html": 6000})
HTML_WAIT.update({"dhaka_rain_animated.svg": 5500})
BIO_LIBS = {"biopython", "biotite", "rdkit", "openbabel", "py3Dmol", "nglview", "pymol", "ipymolstar", "scanpy", "anndata", "pydeseq2", "scikit-bio",
            "ete3", "igv-notebook", "mdanalysis", "mdtraj", "pysam", "ase", "pymatgen", "deepchem"}
AUDIO_LIBS = {"librosa", "torchaudio", "pydub", "sounddevice", "soundfile", "pyaudio", "essentia", "speechrecognition", "openai-whisper", "faster-whisper",
              "pedalboard", "pyo", "music21", "pretty_midi", "mido", "demucs", "kokoro", "coqui-tts", "piper-tts", "bark", "pyannote.audio"}
# মাইক্রোফোনের উদাহরণ: সাউন্ড-কার্ড নেই → /etc/asound.conf-এ ALSA file-প্লাগইন /tmp/claude-0/mic.raw (FLEURS-এর বাংলা কথা) পড়ে
TIMEOUT.update({"torchaudio": 600, "essentia": 600, "openai-whisper": 900, "faster-whisper": 900, "demucs": 1200, "coqui-tts": 900, "piper-tts": 300, "pedalboard": 300})   # ৬ সেকেন্ডের লুপের শেষ দিকে
NEEDS_NET.update({"kokoro": "kokoro-র বর্তমান সংস্করণ পাইথন ৩.১৩-এ চলে না (numpy 1.26-এ আটকানো), মডেল ~৩৩০ MB – নিজের কম্পিউটারে (পাইথন ≤৩.১২) চালাও",
                  "bark": "মডেল ~৫ GB আর GPU বাঞ্ছনীয় (CPU-তে কয়েক মিনিট) – নিজের GPU-যন্ত্রে চালাও",
                  "pyannote.audio": "Hugging Face-এর gated মডেল – শর্ত মেনে ব্যক্তিগত HF_TOKEN লাগে"})
W8 = "/tmp/claude-0/weights"
LIB_ENV = {"vispy": {"EGL_PLATFORM": "surfaceless"}, "pyrender": {"PYOPENGL_PLATFORM": "egl"}, "ete3": {"QT_QPA_PLATFORM": "offscreen"}, "PyFoam / fluidfoam": {"WM_PROJECT_DIR": "/usr/share/openfoam", "WM_PROJECT": "OpenFOAM", "WM_PROJECT_VERSION": "v1912"}, "mujoco": {"MUJOCO_GL": "egl"}, "genesis-world": {"PYOPENGL_PLATFORM": "egl"}, "pymol": {"QT_QPA_PLATFORM": "offscreen"}}
LIB_ENV.update({"openai-whisper": {"WHISPER_DIR": W8 + "/whisper"}, "faster-whisper": {"FW_DIR": W8 + "/fw"},
                "coqui-tts": {"TTS_HOME": W8 + "/tts", "COQUI_TOS_AGREED": "1"}, "piper-tts": {"PIPER_DIR": W8 + "/piper"}})
XVFB = ["xvfb-run", "-a", "-s", "-screen 0 1600x1200x24"]
CMDS = {
    ("py5", 0): XVFB + ["/opt/venv-py5/bin/python", "__runner.py"],
    ("py5", 1): XVFB + ["/opt/venv-py5/bin/python", "__runner.py"],
    ("py5", 2): XVFB + ["/opt/venv-py5/bin/python", "__runner.py"],
    ("p5 (p5py)", 0): XVFB + [PY, "__runner.py"],
    ("p5 (p5py)", 1): XVFB + [PY, "__runner.py"],
    ("sketchpy", 1): XVFB + ["/opt/venv-skp/bin/python", "__runner.py"],
    ("PyOpenGL", 0): XVFB + [PY, "__runner.py"],
    ("PyOpenGL", 1): XVFB + [PY, "__runner.py"],
    ("mpi4py", 0): ["mpirun", "--allow-run-as-root", "--oversubscribe", "-n", "4", PY, "main.py"],
    ("mpi4py", 1): ["mpirun", "--allow-run-as-root", "--oversubscribe", "-n", "4", PY, "main.py"],
    ("marimo", 0): [PY, "-m", "marimo", "export", "html", "main.py", "-o", "notebook.html", "-f", "--no-include-code"],
    ("marimo", 1): [PY, "-m", "marimo", "export", "html", "main.py", "-o", "notebook.html", "-f", "--no-include-code"],
    ("pytest", 0): [PY, "-m", "pytest", "-v", "main.py"],
    ("pytest", 1): [PY, "-m", "pytest", "-v", "main.py"],
    ("mypy", 0): [PY, "-m", "mypy", "main.py"],
    ("mypy", 1): [PY, "-m", "mypy", "--strict", "main.py"],
    ("click", 0): [PY, "main.py", "--name", "Rahim", "--count", "2"],
    ("invoke", 0): ["bash", "-c", f"cp main.py tasks.py && {PY} -m invoke --list && echo && {PY} -m invoke build --version 2.1 && echo && cat build/report.txt"],
    ("invoke", 1): ["bash", "-c", f"cp main.py tasks.py && {PY} -m invoke sample && echo '$ invoke reports' && {PY} -m invoke reports && "
                    f"echo '$ invoke reports   (আবার)' && {PY} -m invoke reports && echo '$ Sylhet.csv-এ জুলাইয়ের মান বদলানো হলো' && sed -i 's/^7,.*/7,999/' data/Sylhet.csv && "
                    f"echo '$ invoke reports --dry' && {PY} -m invoke reports --dry && echo '$ invoke reports' && {PY} -m invoke reports && cat reports/Sylhet.md"],
    ("click", 1): ["bash", "-c", f"{PY} main.py --help && echo && {PY} main.py csv2json data.csv --pretty && cat data.json && echo && {PY} main.py info data.csv"],
}

# ---- রোবটিক্স/IoT বিভাগ: আসল বোর্ড নেই – MicroPython-এর unix-port, gpiozero-র MockFactory, সফটওয়্যার-I²C-চিপ, pty, mosquitto, ROS 2 (robostack)
EXTRA_BIN["micropython"] = "/usr/bin"
for _i in range(4): CMDS[("micropython", _i)] = ["micropython", "main.py"]
VENV.update({"rclpy (ROS 2)": "/opt/venv-ros"})                 # micromamba robostack-jazzy, python 3.14, NOT system-site
DIST.update({"circuitpython": "adafruit-blinka", "pyusb": "pyusb", "paho-mqtt": "paho-mqtt"})
SERVICES.update({"paho-mqtt": "mosquitto"}); SERVICE_REASON.update({"mosquitto": "MQTT ব্রোকার (mosquitto) লাগে"})
ROB_LIBS = {"circuitpython", "adafruit-blinka", "micropython", "gpiozero", "pyserial", "pyusb", "rclpy (ROS 2)", "bleak", "paho-mqtt", "pymavlink"}
NEEDS_NET.update({"RPi.GPIO": "আসল Raspberry Pi লাগে – RPi.GPIO অন্য যন্ত্রে import-ই হয় না (Pi 5-এ rpi-lgpio)"})
TIMEOUT.update({"rclpy (ROS 2)": 300, "paho-mqtt": 180, "pymavlink": 180})
LIB_ENV["rclpy (ROS 2)"] = {"AMENT_PREFIX_PATH": "/opt/venv-ros", "ROS_DISTRO": "jazzy", "ROS_AUTOMATIC_DISCOVERY_RANGE": "LOCALHOST", "ROS_DOMAIN_ID": "42", "RCUTILS_LOGGING_SEVERITY_THRESHOLD": "WARN"}
NEEDS_NET_EX.update({("bleak", 0): "ব্লুটুথ-অ্যাডাপ্টার আর নিজের BLE-থার্মোমিটার লাগে – নিজের কম্পিউটারে চালাও"})

# ---- গেম বিভাগ: ডেমো-মোডে নিজে খেলে; pygame (SDL dummy), arcade/pyglet headless, pyxel/renpy Xvfb-তে, panda3d/ursina offscreen
DIST.update({"pygame / pygame-ce": "pygame-ce", "pyyaml (yaml)": "PyYAML", "web3.py": "web3"})
TIMEOUT.update({"xy": 600, "py-solc-x": 600, "web3.py": 600, "bitcoinlib": 300})
VENV.update({"arcade": "/opt/venv-arcade"})                 # arcade pymunk 6.9 আর pillow 11 বেঁধে দেয় → আলাদা venv (system-site)
for _i in range(4):
    CMDS[("pyxel", _i)] = XVFB + [PY, "__runner.py"]
TIMEOUT.update({"arcade": 600, "pyglet": 300, "pyxel": 300, "pygame / pygame-ce": 300})
EXTRA_BIN["renpy"] = "/opt/renpy-8.5.2-sdk"                    # SDK (pip নয়) – installed() দেখে /opt/renpy-8.5.2-sdk/renpy আছে কিনা
LIB_ENV["renpy"] = {"RENPY_SDK": "/opt/renpy-8.5.2-sdk"}
for _i in range(4):
    CMDS[("renpy", _i)] = XVFB + [PY, "__runner.py"]
TIMEOUT.update({"renpy": 600, "panda3d": 300, "ursina": 300})
NOISE_GAME = ("findfont: Failed to find font weight", "\x1b[93mwarning: No monitors", "warning: No monitors", "pw.conf", "ALSOFT", "ALSA lib", "AL lib", "Failed to initialize audio device")

# ---- কোয়ান্টাম/রসায়ন/প্রকৌশল-CAD বিভাগ: সব স্থানীয় সিমুলেশন (Aer, cirq, default.qubit, qutip, pyscf, cantera, CoolProp, OCCT, ngspice)
DIST.update({"cirq": "cirq-core", "python-control": "control", "pyspice": "PySpice", "coolprop": "CoolProp"})
TIMEOUT.update({"pyscf": 900, "cantera": 900, "pennylane": 600, "qiskit": 600, "cadquery": 600, "build123d": 600, "qutip": 600})

# ---- ডেস্কটপ GUI বিভাগ: আসল অ্যাপ চালিয়ে (Qt offscreen, বাকিরা Xvfb-তে) ATLAS_DEMO=1 দিয়ে নিজে-নিজে ক্লিক + স্ক্রিনশট
GUI_X = ["tkinter (stdlib)", "customtkinter", "dearpygui", "kivy", "wxPython", "toga", "PyGObject", "pywebview"]
VENV.update({n: "/opt/venv-gui" for n in GUI_X})                 # /usr/bin/python3.12 --system-site-packages (apt-এর tk, wx, gtk3, webkit2)
DIST.update({"toga": "toga-core", "PyGObject": "pygobject"})
for _n in GUI_X:
    LIB_ENV[_n] = {"ATLAS_DEMO": "1", "KIVY_NO_ARGS": "1", "KIVY_NO_CONSOLELOG": "1", "NO_AT_BRIDGE": "1"}
    for _i in range(4):
        CMDS[(_n, _i)] = XVFB + ["/opt/venv-gui/bin/python", "__runner.py"]
for _n in ("PySide6", "PyQt6"):
    LIB_ENV[_n] = {"ATLAS_DEMO": "1", "QT_QPA_PLATFORM": "offscreen"}
LIB_ENV["flet"] = {"ATLAS_DEMO": "1"}
APPS.update({("flet", 0): dict(port=8550, wait=5500, width=820, height=620, log=True, steps=[("shot", "3200"), ("shot", "3400")]),
             ("flet", 1): dict(port=8550, wait=9000, width=1000, height=640, log=True, steps=[("shot", "3500"), ("shot", "3000")])})
GUI_LIBS = set(GUI_X) | {"PySide6", "PyQt6", "flet"}
TIMEOUT.update({n: 300 for n in GUI_LIBS})

# ---- পরিমাণগত ফাইন্যান্স বিভাগ (ভারী/সংঘাতপূর্ণ নির্ভরতা আলাদা venv-এ, সব NOT system-site)
DIST.update({"quantlib": "QuantLib", "pyportfolioopt": "PyPortfolioOpt", "ta-lib": "TA-Lib", "zipline (zipline-reloaded)": "zipline-reloaded"})
VENV.update({"vectorbt": "/opt/venv-vbt", "zipline (zipline-reloaded)": "/opt/venv-zip", "openbb": "/opt/venv-obb", "pandas-ta": "/opt/venv-pta"})
TIMEOUT.update({"arch": 900, "linearmodels": 900, "quantlib": 600, "vectorbt": 600, "zipline (zipline-reloaded)": 900, "openbb": 600, "riskfolio-lib": 600, "quantstats": 600, "backtrader": 600})
# ---- অ্যানিমেশন বিভাগ
ANIM_LIBS = {"manim (manimgl)", "moviepy", "gizeh", "celluloid", "vapory", "lottie", "drawbot"}
DIST.update({"manim (manimgl)": "manim", "drawbot": "drawbot-skia"})
TIMEOUT.update({"manim (manimgl)": 900, "moviepy": 900, "vapory": 900, "lottie": 600, "drawbot": 600, "celluloid": 600, "gizeh": 600})
CMDS[("manim (manimgl)", 4)] = ["env", "TQDM_DISABLE=1", "PYTHONWARNINGS=ignore"] + XVFB + [
    "/opt/venv-mgl/bin/manimgl", "main.py", "InscribedAngle", "-w", "--video_dir", ".", "-r", "1280x720", "--log-level", "ERROR"]

RUNNER = r'''
import os, runpy, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.show = lambda *a, **k: None
try:
    runpy.run_path("main.py", run_name="__main__")
finally:
    for i, n in enumerate(plt.get_fignums()):
        plt.figure(n).savefig(f"__fig{i}.png", dpi=150, bbox_inches="tight", facecolor="auto")
'''

IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
OFFICE_EXT = {".docx", ".xlsx", ".pptx"}


def installed(name):
    if "stdlib" in name or name.startswith("xml."):
        return True
    if name in EXTRA_BIN:
        return os.path.exists(os.path.join(EXTRA_BIN[name], name))
    if py_for(name) != PY:
        mod = {"graph-tool": "import graph_tool", "poliastro": "import poliastro", "pychrono": "import pychrono", "fenicsx (dolfinx)": "import dolfinx", "sketchpy": "import tkinter, turtle, cv2", "rclpy (ROS 2)": "import rclpy"}.get(name)          # conda-প্যাকেজে pip-মেটাডেটা নেই
        code = mod or f"import importlib.metadata as m; m.distribution({DIST.get(name, name)!r})"
        return subprocess.run([py_for(name), "-c", code], capture_output=True).returncode == 0
    for dist in (DIST.get(name, name), name + "-binary"):      # psycopg2 → psycopg2-binary
        try:
            md.distribution(dist)
            return True
        except md.PackageNotFoundError:
            pass
    return False


_svc = {}


def _wait_port(port, secs=15):
    for _ in range(secs * 10):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.1)
    return False


def service(kind):
    """লোকাল PostgreSQL বা Redis একবার চালু করে দরকারি env ফেরত দেয়; চালানো না গেলে None।"""
    if kind in _svc:
        return _svc[kind]
    env = None
    try:
        if kind == "postgres":
            bins = sorted(glob.glob("/usr/lib/postgresql/*/bin"), reverse=True)
            initdb = shutil.which("initdb") or (bins and os.path.join(bins[0], "initdb"))
            if initdb and os.path.exists(initdb):
                pg_ctl = os.path.join(os.path.dirname(initdb), "pg_ctl")
                data = Path(tempfile.mkdtemp(prefix="pg_"))
                as_user = []
                if hasattr(os, "geteuid") and os.geteuid() == 0:      # root হলে postgres ইউজার দিয়ে
                    as_user = ["runuser", "-u", "postgres", "--"]
                    shutil.chown(data, "postgres")
                subprocess.run(as_user + [initdb, "-D", str(data), "-U", "postgres", "--auth=trust"],
                               capture_output=True, check=True)
                subprocess.run(as_user + [pg_ctl, "-D", str(data), "-l", str(data / "server.log"), "-w",
                                          "-o", "-p 54329 -k /tmp -c listen_addresses=127.0.0.1", "start"],
                               capture_output=True, check=True)
                atexit.register(lambda: subprocess.run(as_user + [pg_ctl, "-D", str(data), "-m", "fast", "stop"],
                                                       capture_output=True))
                env = {"DATABASE_URL": "postgresql://postgres@127.0.0.1:54329/postgres"}
        elif kind == "neo4j":                 # /opt/neo4j-community-* (Java লাগে) – শুধু এই রেন্ডারের জন্য, পাসওয়ার্ড এলোমেলো
            homes = sorted(glob.glob("/opt/neo4j-community-*"))
            if homes:
                home = homes[-1]
                pw = "atlas-" + os.urandom(6).hex()
                data = Path(tempfile.mkdtemp(prefix="neo_"))
                nenv = dict(os.environ, NEO4J_HOME=home, NEO4J_CONF=str(data))
                over = {"server.directories.data": f"{data}/data", "server.directories.logs": f"{data}/logs",
                        "server.bolt.listen_address": "127.0.0.1:7697", "server.http.enabled": "false",
                        "server.https.enabled": "false", "server.memory.heap.max_size": "1g",
                        "server.memory.pagecache.size": "256m"}
                base = [l for l in Path(home, "conf", "neo4j.conf").read_text().splitlines()
                        if l.split("=", 1)[0].strip() not in over]
                conf = "\n".join(base + [f"{k}={v}" for k, v in over.items()]) + "\n"
                (data / "neo4j.conf").write_text(conf)
                subprocess.run([f"{home}/bin/neo4j-admin", "dbms", "set-initial-password", pw], env=nenv,
                               capture_output=True, check=True)
                p = subprocess.Popen([f"{home}/bin/neo4j", "console"], env=nenv,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                atexit.register(p.terminate)
                if _wait_port(7697, 120):
                    time.sleep(3)
                    env = {"NEO4J_URI": "bolt://127.0.0.1:7697", "NEO4J_USER": "neo4j", "NEO4J_PASSWORD": pw}
        elif kind == "sshd":                  # শুধু রেন্ডারের জন্য: 127.0.0.1:2222-এ এলোমেলো চাবির SSH সার্ভার
            sshd = shutil.which("sshd") or "/usr/sbin/sshd"
            if os.path.exists(sshd):
                d = Path(tempfile.mkdtemp(prefix="ssh_"))
                subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(d / "host_key")], check=True)
                subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(d / "client_key")], check=True)
                user = os.environ.get("USER") or "root"
                home = Path(os.path.expanduser("~")); (home / ".ssh").mkdir(mode=0o700, exist_ok=True)
                ak = home / ".ssh" / "authorized_keys"
                pub = (d / "client_key.pub").read_text()
                ak.write_text((ak.read_text() if ak.exists() else "") + pub); ak.chmod(0o600)
                (d / "sshd_config").write_text(f"Port 2222\nListenAddress 127.0.0.1\nHostKey {d}/host_key\nPidFile {d}/sshd.pid\n"
                                               "PermitRootLogin prohibit-password\nPasswordAuthentication no\nUsePAM no\n"
                                               "StrictModes no\nSubsystem sftp internal-sftp\n")
                os.makedirs("/run/sshd", exist_ok=True)
                p = subprocess.Popen([sshd, "-D", "-f", str(d / "sshd_config")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                def _stop(p=p, ak=ak, pub=pub):
                    p.terminate(); ak.write_text(ak.read_text().replace(pub, ""))
                atexit.register(_stop)
                if _wait_port(2222):
                    env = {"SSH_HOST": "127.0.0.1", "SSH_PORT": "2222", "SSH_USER": user, "SSH_KEY": str(d / "client_key")}
        elif kind == "docker":                # daemon চলছে না হলে চালু করা
            if shutil.which("dockerd"):
                if subprocess.run(["docker", "info"], capture_output=True).returncode != 0:
                    subprocess.Popen(["dockerd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    for _ in range(60):
                        time.sleep(1)
                        if subprocess.run(["docker", "info"], capture_output=True).returncode == 0:
                            break
                if subprocess.run(["docker", "info"], capture_output=True).returncode == 0:
                    env = {"DOCKER_HOST": "unix:///var/run/docker.sock"}
        elif kind == "mosquitto":             # শুধু রেন্ডারের জন্য: 127.0.0.1:18830-এ MQTT ব্রোকার
            mq = shutil.which("mosquitto") or "/usr/sbin/mosquitto"
            if os.path.exists(mq):
                d = Path(tempfile.mkdtemp(prefix="mq_")); (d / "m.conf").write_text("listener 18830 127.0.0.1\nallow_anonymous true\npersistence false\nsys_interval 1\n")
                p = subprocess.Popen([mq, "-c", str(d / "m.conf")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                atexit.register(p.terminate)
                if _wait_port(18830):
                    env = {"MQTT_HOST": "127.0.0.1", "MQTT_PORT": "18830"}
        elif kind == "redis":
            rs = shutil.which("valkey-server") or shutil.which("redis-server")
            if rs:
                p = subprocess.Popen([rs, "--port", "63799", "--save", "", "--appendonly", "no"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                atexit.register(p.terminate)
                if _wait_port(63799):
                    env = {"REDIS_URL": "redis://127.0.0.1:63799/0", "VALKEY_URL": "valkey://127.0.0.1:63799/0"}
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"    {kind} চালু হলো না: {e}")
    _svc[kind] = env
    return env


def fixtures(name, d):
    """কিছু উদাহরণ ইনপুট ফাইল আশা করে – নমুনা ফাইল বানানো।"""
    if name == "sketchpy":                               # নমুনা ছবি: scikit-image-এর বিড়াল
        from skimage import data
        from PIL import Image as _Im
        _Im.fromarray(data.chelsea()).save(d / "photo.jpg")
    if name == "opencv-python":
        import numpy as np
        import cv2
        img = np.full((260, 360, 3), 245, np.uint8)
        cv2.circle(img, (110, 130), 70, (200, 90, 60), -1)
        cv2.rectangle(img, (200, 60), (330, 200), (60, 160, 40), -1)
        cv2.putText(img, "Py", (125, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 20, 20), 2)
        cv2.imwrite(str(d / "photo.jpg"), img)
    if name in ("pypdf", "pypdfium2", "pdfplumber"):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
        for fn, pages in [("document.pdf", 3), ("thesis.pdf", 2), ("appendix.pdf", 2)]:
            c = canvas.Canvas(str(d / fn), pagesize=A4)
            for i in range(pages):
                c.setFillColorRGB(0.49, 0.23, 0.93)
                c.rect(0, 770, 600, 72, fill=1, stroke=0)
                c.setFillColorRGB(1, 1, 1)
                c.setFont("Helvetica-Bold", 26)
                c.drawString(60, 795, f"{fn} - page {i + 1}")
                c.setFillColorRGB(0.2, 0.2, 0.2)
                c.setFont("Helvetica", 13)
                for k in range(18):
                    c.drawString(60, 720 - k * 22, f"Line {k + 1}: sample text for the PDF demo.")
                c.showPage()
            c.save()
        data = [["Station", "Jun", "Jul", "Aug"], ["Dhaka", "330", "380", "310"],
                ["Sylhet", "820", "790", "640"], ["Rajshahi", "250", "300", "270"]]
        t = Table(data)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)]))
        SimpleDocTemplate(str(d / "report.pdf"), pagesize=A4).build(
            [Paragraph("Rainfall report 2026", getSampleStyleSheet()["Title"]), t])
    if name == "pytesseract":
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (900, 260), "white")
        dr = ImageDraw.Draw(img)
        try:
            f = ImageFont.truetype("DejaVuSans.ttf", 40)
        except OSError:
            f = ImageFont.load_default(size=40)
        dr.text((30, 30), "1. What is Python?", fill="black", font=f)
        dr.text((30, 110), "2. Write a loop that prints 1 to 10.", fill="black", font=f)
        img.save(d / "scan.png")
    if name == "mistune":
        (d / "notes").mkdir()
        (d / "notes" / "python.md").write_text("# Python\n\n- list\n- **dict**\n- [x] loops\n", encoding="utf-8")
        (d / "notes" / "git.md").write_text("# Git\n\nSave work: `git commit -m 'msg'`\n", encoding="utf-8")
    if name == "pyxlsb":
        xlsb_fixture(d)
    if name in ("ultralytics", "supervision", "segment-anything"):    # আগে নামানো মডেল-ওজন (প্রতিবার নামানো এড়াতে)
        for w in Path("/tmp/claude-0/weights").glob("*.p*"):
            (d / w.name).symlink_to(w)
    if Path("/tmp/claude-0/gis").exists():          # বাংলাদেশের প্রশাসনিক সীমানা (geoBoundaries) আগে নামানো – উদাহরণ নিজেও নামাতে পারে
        for f in Path("/tmp/claude-0/gis").glob("bd_ADM*.geojson"):
            if not (d / f.name).exists():
                (d / f.name).symlink_to(f)
    W = Path("/tmp/claude-0/weights")
    if name in AUDIO_LIBS and (W / "fleurs").exists():          # FLEURS বাংলা ক্লিপ আগে নামানো (প্রতিবার না নামিয়ে)
        (d / "fleurs").symlink_to(W / "fleurs")
        for f in ("jfk.flac",):
            if (W / "audio" / f).exists(): (d / f).symlink_to(W / "audio" / f)
    if name in BIO_LIBS and (W / "bio").exists():               # NCBI/RCSB থেকে আগে নামানো নমুনা (উদাহরণ নিজেও নামাতে পারে)
        for f in (W / "bio").iterdir():
            if f.is_file() and not (d / f.name).exists():
                (d / f.name).symlink_to(f)
        if name == "scanpy" and (W / "bio" / "data").exists():
            (d / "data").symlink_to(W / "bio" / "data")
    if name in ROB_LIBS and (W / "rob").exists():
        for f in (W / "rob").iterdir():
            if not (d / f.name).exists(): (d / f.name).symlink_to(f)
    if (name in ANIM_LIBS or name in GUI_LIBS) and (W / "anim").exists():              # ERA5 ঢাকা-বৃষ্টি আর variable font আগে নামানো
        for f in (W / "anim").iterdir():
            if not (d / f.name).exists(): (d / f.name).symlink_to(f)
    if name == "skyfield" and Path("/tmp/claude-0/weights/de421.bsp").exists():   # JPL ephemeris আগে নামানো
        (d / "de421.bsp").symlink_to("/tmp/claude-0/weights/de421.bsp")
    if name == "click":
        (d / "data.csv").write_text("name,marks\nRahim,78\nKarim,85\n", encoding="utf-8")


def write_xlsb(path, sheets):
    """খুব ছোট .xlsb (Excel Binary) লেখক – শুধু ডেমো ফাইল বানাতে (BIFF12 রেকর্ড)।"""
    import struct
    import zipfile

    def rec(rid, data=b""):
        idb = struct.pack("<H", rid) if rid > 0x7F else bytes([rid])
        n, ln = len(data), b""
        while True:
            b = n & 0x7F
            n >>= 7
            ln += bytes([b | (0x80 if n else 0)])
            if not n:
                break
        return idb + ln + data

    def wstr(t):
        return struct.pack("<I", len(t)) + t.encode("utf-16-le")

    sst, sidx = [], {}
    def si(t):
        if t not in sidx:
            sidx[t] = len(sst)
            sst.append(t)
        return sidx[t]

    sheet_bins = []
    for name, rows in sheets.items():
        ncol = max(len(r) for r in rows)
        b = rec(0x0181) + rec(0x0194, struct.pack("<4I", 0, len(rows) - 1, 0, ncol - 1)) + rec(0x0191)
        for r, row in enumerate(rows):
            b += rec(0x0000, struct.pack("<I", r) + b"\0" * 13)
            for c, v in enumerate(row):
                if v is None:
                    continue
                if isinstance(v, str):
                    b += rec(0x07, struct.pack("<III", c, 0, si(v)))
                else:
                    b += rec(0x05, struct.pack("<IId", c, 0, float(v)))
        sheet_bins.append(b + rec(0x0192) + rec(0x0182))
    book = rec(0x0183) + rec(0x018F)
    for k, name in enumerate(sheets, 1):
        book += rec(0x019C, struct.pack("<II", 0, k) + wstr(f"rId{k}") + wstr(name))
    book += rec(0x0190) + rec(0x0184)
    sstb = rec(0x019F, struct.pack("<II", len(sst), len(sst))) + b"".join(rec(0x13, b"\0" + wstr(t)) for t in sst) + rec(0x01A0)
    rels = "".join(f'<Relationship Id="rId{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                   f'Target="worksheets/sheet{k}.bin"/>' for k in range(1, len(sheets) + 1))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("xl/workbook.bin", book)
        z.writestr("xl/_rels/workbook.bin.rels",
                   '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   + rels + "</Relationships>")
        z.writestr("xl/sharedStrings.bin", sstb)
        for k, b in enumerate(sheet_bins, 1):
            z.writestr(f"xl/worksheets/sheet{k}.bin", b)


def xlsb_fixture(d):
    import datetime as dt
    import random
    rnd = random.Random(7)
    branches = {"Dhaka": 1.6, "Chattogram": 1.2, "Sylhet": 0.9, "Rajshahi": 0.7, "Khulna": 0.8}
    books = {"Gitanjali": 250, "Himu": 200, "Feluda Samagra": 950, "Lalsalu": 180, "Pather Panchali": 320, "Agnibeena": 140}
    base = dt.date(1899, 12, 30)
    rows = [["তারিখ", "শাখা", "বই", "কপি", "দাম", "ছাড় %"]]
    day = dt.date(2026, 1, 1)
    while day <= dt.date(2026, 6, 30):
        for br, w in branches.items():
            for _ in range(rnd.randint(1, 3)):
                bk = rnd.choice(list(books))
                boost = 1.8 if day.month == 2 else 1.0          # ফেব্রুয়ারি – বইমেলা
                rows.append([(day - base).days, br, bk, max(1, int(rnd.gauss(6 * w * boost, 2))), books[bk],
                             rnd.choice([0, 0, 0, 10, 15, 25])])
        day += dt.timedelta(days=1)
    targets = [["শাখা", "ম্যানেজার", "ছয় মাসের লক্ষ্য (৳)"]] + [[b, m, t] for b, m, t in [
        ("Dhaka", "Sumi", 1_400_000), ("Chattogram", "Rafiq", 1_000_000), ("Sylhet", "Nabila", 700_000),
        ("Rajshahi", "Tanvir", 600_000), ("Khulna", "Mitu", 650_000)]]
    write_xlsb(d / "sales_2026.xlsb", {"বিক্রি": rows, "লক্ষ্য": targets})


def to_webp(img, max_w=1500):
    from PIL import Image
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    if img.width > max_w:
        img = img.resize((max_w, round(img.height * max_w / img.width)), Image.LANCZOS)
    if img.height > 2000:
        img = img.crop((0, 0, img.width, 2000))
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=86, method=5)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


ANIM_W, ANIM_MAX = 720, 120          # চলমান প্রিভিউ: চওড়া ৭২০ px, সর্বোচ্চ ১২০ ফ্রেম (দরকারে সমান ফাঁকে বাদ, গতি আসল সময়ের মতোই)
VID_EXT = {".mp4", ".webm", ".mov", ".mkv", ".avi"}


def anim_webp(frames, durations):
    """ফ্রেম-তালিকা → animated WebP (loop)। durations ms-এ, প্রতি ফ্রেমের।"""
    import io as _io
    if len(frames) > ANIM_MAX:                  # সমান ফাঁকে বাছাই, প্রতিটার সময় যোগ করে আসল গতি রাখি
        step = len(frames) / ANIM_MAX
        idx = [int(k * step) for k in range(ANIM_MAX)]
        durations = [sum(durations[idx[k]:(idx[k + 1] if k + 1 < len(idx) else len(frames))]) for k in range(len(idx))]
        frames = [frames[k] for k in idx]
    w = min(frames[0].width, ANIM_W)
    frames = [f.convert("RGB").resize((w, round(f.height * w / f.width))) if f.width != w else f.convert("RGB") for f in frames]
    buf = _io.BytesIO()
    frames[0].save(buf, "WEBP", save_all=True, append_images=frames[1:], duration=[max(20, int(x)) for x in durations],
                   loop=0, quality=74, method=4)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def image_file(path):
    from PIL import Image, ImageSequence
    img = Image.open(path)
    if getattr(img, "is_animated", False):
        frames, durs = [], []
        for f in ImageSequence.Iterator(img):
            frames.append(f.convert("RGB")); durs.append(f.info.get("duration", img.info.get("duration", 100)) or 100)
        return anim_webp(frames, durs)
    return to_webp(img)


def video_file(path):
    """ভিডিও → animated WebP (প্রথম ১২ সেকেন্ড, ≤১৫ fps)।"""
    from PIL import Image
    import tempfile
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                               capture_output=True, text=True).stdout.strip() or 0)
    T = min(dur, 12.0) if dur > 0 else 12.0
    fps = min(15.0, ANIM_MAX / T)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-v", "error", "-t", f"{T}", "-i", str(path), "-vf", f"fps={fps},scale={ANIM_W}:-2:flags=lanczos",
                        f"{td}/f%04d.png"], check=True)
        frames = [Image.open(p).convert("RGB") for p in sorted(Path(td).glob("f*.png"))]
    return anim_webp(frames, [1000 / fps] * len(frames))


def trim(img, pad=28):
    """চারপাশের সাদা জায়গা কেটে শুধু কনটেন্ট রাখা।"""
    from PIL import Image, ImageChops
    rgb = img.convert("RGB")
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255)))
    box = diff.point(lambda v: 255 if v > 12 else 0).getbbox()
    if not box:
        return img
    l, t, r, b = box
    return rgb.crop((max(0, l - pad), max(0, t - pad), min(rgb.width, r + pad), min(rgb.height, b + pad)))


def pdf_pages(path, n=2, crop=False):
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(str(path))
    pages = []
    for i in range(min(n, len(pdf))):
        img = pdf[i].render(scale=2.2 if crop else 1.4).to_pil()
        pages.append(to_webp(trim(img) if crop else img, 1000 if crop else 800))
    return pages


def office_preview(path, d):
    soffice = shutil.which("soffice")
    if not soffice:
        return []
    out = d / "__office"
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out), str(path)],
                   capture_output=True, timeout=120)
    pdf = out / (path.stem + ".pdf")
    return pdf_pages(pdf, 1, crop=True) if pdf.exists() else []


def app_screens(spec, d, env):
    """ওয়েব-অ্যাপ (Dash, Panel, NiceGUI, Shiny…) সার্ভার চালিয়ে ব্রাউজারে স্ক্রিনশট – আসল আউটপুট।
    spec = dict(port, cmd=None, path="/", wait=ms, steps=[(action, selector, value?), ...])"""
    from PIL import Image
    from playwright.sync_api import sync_playwright
    cmd = spec.get("cmd") or [PY, "main.py"]
    p = subprocess.Popen(cmd, cwd=d, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         start_new_session=True)
    shots, log = [], ""
    try:
        import socket as _s
        up = False
        for _ in range(900):                       # ৯০ সেকেন্ড পর্যন্ত অপেক্ষা
            if p.poll() is not None:
                break
            with _s.socket() as s:
                if s.connect_ex(("127.0.0.1", spec["port"])) == 0:
                    up = True
                    break
            time.sleep(0.1)
        if not up:
            raise RuntimeError("সার্ভার চালু হয়নি")
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=CHROME) if CHROME else pw.chromium.launch()
            pg = b.new_page(viewport={"width": spec.get("width", 1200), "height": spec.get("height", 760)},
                            ignore_https_errors=True)
            pg.goto(f"http://127.0.0.1:{spec['port']}{spec.get('path', '/')}", wait_until="domcontentloaded", timeout=60000)
            pg.wait_for_timeout(spec.get("wait", 4000))
            shots.append(pg.screenshot())
            for step in spec.get("steps", []):
                act, sel, *val = step
                try:
                    loc = pg.locator(sel).first
                    if act == "click":
                        loc.click(force=True, timeout=8000)      # চার্টের ওপরের স্তর থাকলেও ঠিক জায়গায় ক্লিক
                        pg.wait_for_timeout(400)
                    elif act == "fill":
                        loc.fill(val[0], timeout=8000)
                    elif act == "select":
                        loc.select_option(val[0], timeout=8000)
                    elif act == "press":
                        loc.press(val[0], timeout=8000)
                    elif act == "shot":
                        pg.wait_for_timeout(int(sel))
                        shots.append(pg.screenshot())
                except Exception as e:                          # একটা ধাপ ব্যর্থ হলেও আগের ছবি থাকবে
                    print(f"    step {step} failed: {str(e)[:120]}")
            b.close()
    finally:
        try:
            os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            log = p.communicate(timeout=10)[0] or ""
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            log = p.communicate()[0] or ""
    return [Image.open(io.BytesIO(s)) for s in shots], log


def html_preview(path):
    if not CHROME:
        return []
    from PIL import Image
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1000, "height": 700}, ignore_https_errors=True)
        if path.suffix.lower() == ".svg":                # Textual-এর SVG: অনলাইন ফন্ট বাদ (অফলাইনে screenshot আটকে যায়)
            svg = re.sub(r"@font-face\s*\{[^}]*\}", "", path.read_text(encoding="utf-8"))
            pg.set_viewport_size({"width": 1600, "height": 1400})
            pg.set_content("<html><body style='margin:0;background:#fff'>" + svg + "</body></html>")
        else:
            pg.goto(path.resolve().as_uri())
        pg.wait_for_timeout(HTML_WAIT.get(path.name, 300))       # CDN থেকে JS এলে একটু বেশি সময়
        if path.suffix.lower() == ".svg" and pg.locator("svg").count():
            png = pg.locator("svg").first.screenshot()           # শুধু SVG-র নিজের মাপটুকু
        else:
            png = pg.screenshot(full_page=True)
        b.close()
    return [to_webp(Image.open(io.BytesIO(png)), 1000)]


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NOISE = ("platform ", "cachedir:", "rootdir:", "plugins:", "[Open3D INFO]", "[Open3D WARNING] GLFW", "Using 'soft' CircularBuffer", "FEngine ", "Vulkan device driver", "Selected physical device", "Backend feature level", "Picked up JAVA_TOOL_OPTIONS", "Picked up _JAVA_OPTIONS", "WARNING: could not determine DPI", "WxPython is not found", "Pyo will use a minimal", "This toolkit has limited", "maintained or updated", "GUI features, you should", "http://www.wxpython.org", "Neither WxPython nor Tkinter", "Pyo's GUI features are", "consider installing WxPython")


NOISE += NOISE_GAME + ("[E][", "[W][", "package_folder:", "asset_folder:", ":display:", ":audio:", "Known pipe types")
NOISE += ("qt.text.font.db:", "This plugin does not support propagateSizeHints", "qt.qpa.", "Gtk-WARNING", "Gtk-Message", "(main.py:", "[INFO   ] ", "[WARNING] [Deps", "Fontconfig warning")
BLENDER_LOG = re.compile(r"^(\d\d:\d\d[.:]\d+\s+(\|\s*INFO|render\s+\|)|INFO Draco|Info: Saved)")


def clean_text(s, limit_lines=45, limit_chars=3500):
    s = ANSI.sub("", s.replace("\r", ""))
    lines = [ln for ln in s.splitlines()
             if ("Warning" not in ln or "error" in ln.lower()) and not ln.startswith(NOISE) and not BLENDER_LOG.match(ln)]
    s = "\n".join(lines).strip()
    if len(lines) > limit_lines:
        s = "\n".join(lines[:limit_lines]) + f"\n… (আরো {len(lines) - limit_lines} লাইন)"
    return s[:limit_chars]


MIC_LIBS = {"sounddevice", "pyaudio", "speechrecognition"}
MIC_WAV = "/tmp/claude-0/mic16.wav"            # FLEURS-এর তিনটে বাংলা বাক্য, মাঝে ২ সে নীরবতা


def mic_start():
    """সাউন্ড-কার্ড নেই: PulseAudio-র null-sink বানিয়ে তার monitor-কে ডিফল্ট ‘মাইক্রোফোন’ করি আর সেখানে আসল রেকর্ডিং বাজাই।
    (/etc/asound.conf-এ ALSA default = pulse; কোডে কিছু বদলাতে হয় না)"""
    if not (shutil.which("pulseaudio") and os.path.exists(MIC_WAV)):
        return None
    if subprocess.run(["pactl", "info"], capture_output=True).returncode != 0:
        subprocess.run(["pulseaudio", "-D", "--exit-idle-time=-1"], capture_output=True)
        time.sleep(1.5)
    if "vmic" not in subprocess.run(["pactl", "list", "short", "sinks"], capture_output=True, text=True).stdout:
        subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=vmic"], capture_output=True)
    subprocess.run(["pactl", "set-default-source", "vmic.monitor"], capture_output=True)
    subprocess.run(["pactl", "set-default-sink", "vmic"], capture_output=True)
    return subprocess.Popen(["bash", "-c", f"for i in 1 2 3 4 5 6 7 8; do paplay -d vmic {MIC_WAV}; done"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def run_one(name, i, code, extra_env=None):
    d = Path(tempfile.mkdtemp(prefix="ex_"))
    mic = None
    try:
        fixtures(name, d)
        if name in MIC_LIBS:
            mic = mic_start()
        before = {p.name for p in d.iterdir()}
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8", PYTHONWARNINGS="ignore", **(extra_env or {}))
        env.update(LIB_ENV.get(name, {}))                        # GPU-ছাড়া অফস্ক্রিন OpenGL (EGL) ইত্যাদি
        if name == "whitebox" and os.path.exists("/opt/wbt/bin/whitebox_tools"):   # conda-forge-এর WhiteboxTools বাইনারি
            env["WBT_DIR"] = "/opt/wbt/bin"
        if name in EXTRA_BIN:                                    # আলাদা venv-এর CLI (poetry, hatch, pdm)
            env["PATH"] = EXTRA_BIN[name] + os.pathsep + env.get("PATH", "")
        if py_for(name) != PY:                                   # venv-এর CLI টুল (poetry, dvc…) PATH-এ
            env["PATH"] = os.path.dirname(py_for(name)) + os.pathsep + env.get("PATH", "")
        if (name, i) in SERVER_TESTS:
            code = code.replace('if __name__ == "__main__":', "if False:") + "\n\n" + SERVER_TESTS[(name, i)]
        if name == "playwright" and CHROME:
            code = code.replace("p.chromium.launch()", f'p.chromium.launch(executable_path="{CHROME}")')
        (d / "main.py").write_text(code, encoding="utf-8")
        (d / "__runner.py").write_text(RUNNER, encoding="utf-8")

        if (name, i) in APPS:
            imgs, log = app_screens(APPS[(name, i)], d, env)
            from PIL import Image as _I
            return dict(status="ok", text=APP_NOTE + clean_text(APPS[(name, i)].get("log") and log or "", 12),
                        images=[to_webp(im) for im in imgs[:3]], files=[])
        if name == "watchdog":
            p = subprocess.Popen([PY, "main.py"], cwd=d, env=env, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(1.5)
            target = d / "inbox" if i == 1 else d
            target.mkdir(exist_ok=True)
            (target / "marks.csv").write_text("name,marks\nRahim,78\nKarim,85\nSumi,92\nRiya,66\n", encoding="utf-8")
            time.sleep(1.5)
            p.send_signal(signal.SIGINT)
            out, _ = p.communicate(timeout=10)
            ok = True
        else:
            cmd = CMDS.get((name, i), [py_for(name), "__runner.py"])
            r = subprocess.run(cmd, cwd=d, env=env, capture_output=True, text=True, timeout=TIMEOUT.get(name, 240))
            out = r.stdout + ("\n" + r.stderr if r.returncode != 0 else "")
            ok = r.returncode == 0 or name == "mypy"      # mypy ভুল পেলে 1 দেয়, সেটাই উদ্দেশ্য

        from PIL import Image
        images = [to_webp(Image.open(f)) for f in sorted(d.glob("__fig*.png"))]
        produced = sorted(p for p in d.iterdir()
                          if p.name not in before and not p.name.startswith(("__", ".")) and p.name != "main.py"
                          and p.is_file())
        if not images:
            for f in produced:
                ext = f.suffix.lower()
                try:
                    if ext in IMG_EXT:
                        images.append(image_file(f))
                    elif ext in VID_EXT:
                        images.append(video_file(f))
                    elif ext == ".pdf":
                        images += pdf_pages(f)
                    elif ext in OFFICE_EXT:
                        images += office_preview(f, d)
                    elif ext in (".html", ".htm", ".svg"):
                        images += html_preview(f)
                except Exception as e:  # প্রিভিউ না হলে শুধু ফাইলের নাম থাকবে
                    print(f"    preview failed for {f.name}: {e}")
                if len(images) >= 3:
                    break
        return dict(status="ok" if ok else "error", text=clean_text(out), images=images[:3],
                    files=[p.name for p in produced][:8])
    except subprocess.TimeoutExpired:
        return dict(status="error", text="সময়সীমা পার হয়ে গেছে", images=[], files=[])
    except RuntimeError as e:
        return dict(status="error", text=str(e), images=[], files=[])
    finally:
        if mic is not None:
            try:
                os.killpg(mic.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        shutil.rmtree(d, ignore_errors=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    outputs = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    names = args or list(DETAILS)
    for name in names:
        for i, e in enumerate(examples_of(DETAILS[name])):
            if e.get("lang") == "js":
                continue                                  # JS উদাহরণ ব্রাউজারে লাইভ চলে
            key = f"{name}::{i}"
            h = hashlib.sha1(e["code"].encode()).hexdigest()[:12]
            old = outputs.get(key)
            if old and old.get("hash") == h and not force and old["status"] in ("ok", "skip"):
                continue
            reason = NEEDS_NET_EX.get((name, i)) or NEEDS_NET.get(name)
            if reason:
                outputs[key] = dict(hash=h, status="skip", reason=reason, text="", images=[], files=[])
                continue
            if not installed(name):
                outputs[key] = dict(hash=h, status="skip", reason="এখানে ইনস্টল নেই", text="", images=[], files=[])
                continue
            extra = None
            if name in SERVICES:
                extra = service(SERVICES[name])
                if extra is None:
                    outputs[key] = dict(hash=h, status="skip", reason=SERVICE_REASON[SERVICES[name]],
                                        text="", images=[], files=[])
                    continue
            t = time.time()
            res = run_one(name, i, e["code"], extra)
            res["hash"] = h
            outputs[key] = res
            print(f"{res['status']:5} {key:28} {len(res['images'])} img  {time.time() - t:4.1f}s")
            OUT.write_text(json.dumps(outputs, ensure_ascii=False), encoding="utf-8")
    OUT.write_text(json.dumps(outputs, ensure_ascii=False), encoding="utf-8")
    print(f"outputs.json: {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
