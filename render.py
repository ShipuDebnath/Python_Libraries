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
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
from details import DETAILS, examples_of  # noqa: E402

OUT = ROOT / "outputs.json"
PY = sys.executable
CHROME = shutil.which("google-chrome") or shutil.which("chromium")

# ইন্টারনেট, API key বা আলাদা সার্ভার লাগে – এখানে চালানো হয় না
NEEDS_NET = {
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
}
NEEDS_NET_EX = {("playwright", 0): "ইন্টারনেট লাগে"}
SERVER_TESTS = {
    ("flask", 0): 'c = app.test_client()\nprint("GET /  →", c.get("/").status_code, c.get("/").get_data(as_text=True))\nprint("GET /hello/Rahim →", c.get("/hello/Rahim").get_data(as_text=True))',
    ("flask", 1): 'c = app.test_client()\nr = c.post("/observations", json={"place": "Sundarbans", "species": "Kingfisher", "count": 3})\nprint("POST /observations →", r.status_code, r.get_json())\nr = c.post("/observations", json={"place": "X"})\nprint("POST (ভুল ডেটা) →", r.status_code, r.get_json())\nprint("GET /observations →", c.get("/observations").get_json())',
    ("starlette", 0): 'from starlette.testclient import TestClient\nc = TestClient(app)\nprint("GET / →", c.get("/").json())\nprint("GET /square/7 →", c.get("/square/7").json())',
    ("starlette", 1): 'from starlette.testclient import TestClient\nc = TestClient(app)\nprint("GET /status →", c.get("/status").json())\nwith c.websocket_connect("/live") as ws:\n    for _ in range(11):\n        msg = ws.receive_json()\n        print("ws →", msg)',
}
CMDS = {
    ("pytest", 0): [PY, "-m", "pytest", "-v", "main.py"],
    ("pytest", 1): [PY, "-m", "pytest", "-v", "main.py"],
    ("mypy", 0): [PY, "-m", "mypy", "main.py"],
    ("mypy", 1): [PY, "-m", "mypy", "--strict", "main.py"],
    ("click", 0): [PY, "main.py", "--name", "Rahim", "--count", "2"],
    ("click", 1): ["bash", "-c", f"{PY} main.py --help && echo && {PY} main.py csv2json data.csv --pretty && cat data.json && echo && {PY} main.py info data.csv"],
}

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
    try:
        md.distribution(name)
        return True
    except md.PackageNotFoundError:
        return False


def fixtures(name, d):
    """কিছু উদাহরণ ইনপুট ফাইল আশা করে – নমুনা ফাইল বানানো।"""
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
    if name == "click":
        (d / "data.csv").write_text("name,marks\nRahim,78\nKarim,85\n", encoding="utf-8")


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


def image_file(path):
    from PIL import Image, ImageSequence
    img = Image.open(path)
    if getattr(img, "is_animated", False):
        frames = [f.convert("RGB") for f in ImageSequence.Iterator(img)][:40]
        w = min(frames[0].width, 600)
        frames = [f.resize((w, round(f.height * w / f.width))) for f in frames]
        buf = io.BytesIO()
        frames[0].save(buf, "WEBP", save_all=True, append_images=frames[1:],
                       duration=img.info.get("duration", 100), loop=0, quality=70)
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return to_webp(img)


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


def html_preview(path):
    if not CHROME:
        return []
    from PIL import Image
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1000, "height": 700})
        pg.goto(path.resolve().as_uri())
        pg.wait_for_timeout(300)
        png = pg.screenshot(full_page=True)
        b.close()
    return [to_webp(Image.open(io.BytesIO(png)), 1000)]


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NOISE = ("platform ", "cachedir:", "rootdir:", "plugins:")


def clean_text(s, limit_lines=45, limit_chars=3500):
    s = ANSI.sub("", s.replace("\r", ""))
    lines = [ln for ln in s.splitlines()
             if ("Warning" not in ln or "error" in ln.lower()) and not ln.startswith(NOISE)]
    s = "\n".join(lines).strip()
    if len(lines) > limit_lines:
        s = "\n".join(lines[:limit_lines]) + f"\n… (আরো {len(lines) - limit_lines} লাইন)"
    return s[:limit_chars]


def run_one(name, i, code):
    d = Path(tempfile.mkdtemp(prefix="ex_"))
    try:
        fixtures(name, d)
        before = {p.name for p in d.iterdir()}
        env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8", PYTHONWARNINGS="ignore")
        if (name, i) in SERVER_TESTS:
            code = code.replace('if __name__ == "__main__":', "if False:") + "\n\n" + SERVER_TESTS[(name, i)]
        if name == "playwright" and CHROME:
            code = code.replace("p.chromium.launch()", f'p.chromium.launch(executable_path="{CHROME}")')
        (d / "main.py").write_text(code, encoding="utf-8")
        (d / "__runner.py").write_text(RUNNER, encoding="utf-8")

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
            cmd = CMDS.get((name, i), [PY, "__runner.py"])
            r = subprocess.run(cmd, cwd=d, env=env, capture_output=True, text=True, timeout=240)
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
                    elif ext == ".pdf":
                        images += pdf_pages(f)
                    elif ext in OFFICE_EXT:
                        images += office_preview(f, d)
                    elif ext in (".html", ".htm"):
                        images += html_preview(f)
                except Exception as e:  # প্রিভিউ না হলে শুধু ফাইলের নাম থাকবে
                    print(f"    preview failed for {f.name}: {e}")
                if len(images) >= 3:
                    break
        return dict(status="ok" if ok else "error", text=clean_text(out), images=images[:3],
                    files=[p.name for p in produced][:8])
    except subprocess.TimeoutExpired:
        return dict(status="error", text="সময়সীমা পার হয়ে গেছে", images=[], files=[])
    finally:
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
            t = time.time()
            res = run_one(name, i, e["code"])
            res["hash"] = h
            outputs[key] = res
            print(f"{res['status']:5} {key:28} {len(res['images'])} img  {time.time() - t:4.1f}s")
            OUT.write_text(json.dumps(outputs, ensure_ascii=False), encoding="utf-8")
    OUT.write_text(json.dumps(outputs, ensure_ascii=False), encoding="utf-8")
    print(f"outputs.json: {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
