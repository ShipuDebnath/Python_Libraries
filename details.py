"""
details.py - যেসব লাইব্রেরির পুরো ব্যাখ্যা, ইনস্টল, উদাহরণ ও প্রজেক্ট লেখা হয়েছে।

নতুন লাইব্রেরি যোগ করতে ফাইলের শেষে লেখো:

DETAILS["লাইব্রেরির-নাম"] = lib(
    about="কী কাজে লাগে…",
    install="pip install …",
    example='''…কোড…''',
    project_title="প্রজেক্টের নাম",
    project_about="প্রজেক্ট কী করে…",
    project_code='''…কোড…''',
)

নাম অবশ্যই libraries.json-এর নামের সাথে হুবহু মিলতে হবে।
"""


def lib(about, install, example, project_title, project_about, project_code):
    return dict(about=about, install=install, example=example,
                project_title=project_title, project_about=project_about,
                project_code=project_code)


def ex(title, about, code, hint=None, live=None, lang="python"):
    """একটা উদাহরণ-কার্ড।
    hint = কার্ডের নিচে ছোট টিপ
    live = ব্রাউজারে লাইভ চালানোর জন্য dict(cdn=[...], css=[...], js="...")
    lang = "python" বা "js"
    """
    return dict(title=title, about=about, code=code, hint=hint, live=live, lang=lang)


# ব্রাউজারে লাইভ ডেমোর জন্য CDN ঠিকানা
CDN = {
    "chartjs": ["https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"],
    "echarts": ["https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"],
    "plotly": ["https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"],
    "d3": ["https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"],
    "apex": ["https://cdn.jsdelivr.net/npm/apexcharts@3.49.0/dist/apexcharts.min.js"],
    "vega": ["https://cdn.jsdelivr.net/npm/vega@5.30.0/build/vega.min.js",
             "https://cdn.jsdelivr.net/npm/vega-lite@5.21.0/build/vega-lite.min.js",
             "https://cdn.jsdelivr.net/npm/vega-embed@6.26.0/build/vega-embed.min.js"],
    "plot": ["https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js",
             "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6.16/dist/plot.umd.min.js"],
    "uplot": ["https://cdn.jsdelivr.net/npm/uplot@1.6.30/dist/uPlot.iife.min.js"],
}
CDN_CSS = {"uplot": ["https://cdn.jsdelivr.net/npm/uplot@1.6.30/dist/uPlot.min.css"]}


def live(kind, js):
    return dict(cdn=CDN[kind], css=CDN_CSS.get(kind, []), js=js)


def jsex(kind, title, about, code, hint=None):
    """JavaScript লাইব্রেরির উদাহরণ: কোডটাই ব্রাউজারে লাইভ চলে (#app ডিভের ভেতরে)।"""
    return ex(title, about, code, hint=hint, live=live(kind, code), lang="js")


def jslib(name, about, install, examples, **manual):
    """JavaScript লাইব্রেরি: উদাহরণগুলো সরাসরি তালিকা হিসেবে।"""
    DETAILS[name] = dict(about=about, install=install, examples=list(examples), lang="js")
    if manual:
        man(name, **manual)


def more(name, *examples):
    """কোনো লাইব্রেরিতে আরো উদাহরণ যোগ করা: more("matplotlib", ex(...), ex(...))"""
    DETAILS[name].setdefault("more", []).extend(examples)


def man(name, tasks=None, caps=None, limits=None, alt="", level="", tag=""):
    """Field manual: কী কী কাজ, ক্ষমতা, সীমাবদ্ধতা, বিকল্প।"""
    DETAILS[name]["man"] = dict(tasks=tasks or [], caps=caps or [], limits=limits or [],
                                alt=alt, level=level, tag=tag)


def examples_of(d):
    """একটা লাইব্রেরির সব উদাহরণ ক্রমানুসারে: সহজ উদাহরণ, প্রজেক্ট, তারপর বাকিগুলো।"""
    if "examples" in d:
        return d["examples"] + d.get("more", [])
    out = [ex("সহজ উদাহরণ", "শুরু করার জন্য সবচেয়ে ছোট কোড।", d["example"]),
           ex(d["project_title"], d["project_about"], d["project_code"], hint="প্রজেক্ট")]
    return out + d.get("more", [])


DETAILS = {
    "requests": {
        "about": (
            "requests দিয়ে ইন্টারনেটের যেকোনো ওয়েবসাইট বা API-তে রিকোয়েস্ট পাঠানো যায়। "
            "ডেটা আনা (GET), ডেটা পাঠানো (POST), হেডার ও টাইমআউট সেট করা সব কাজ "
            "কয়েক লাইনে হয়ে যায়। পাইথনে সবচেয়ে বেশি ব্যবহৃত লাইব্রেরিগুলোর একটা।"
        ),
        "install": "pip install requests",
        "example": '''import requests

r = requests.get("https://api.github.com/users/octocat", timeout=10)
r.raise_for_status()          # ভুল হলে এখানেই error দেখাবে

data = r.json()               # JSON কে dict-এ রূপান্তর
print("নাম:", data["name"])
print("পাবলিক রিপো:", data["public_repos"])''',
        "project_title": "প্রকাশ্য আবহাওয়া API থেকে দৈনিক ডেটা সংগ্রাহক",
        "project_about": (
            "Open-Meteo-র ফ্রি API (কোনো key লাগে না) থেকে ঢাকার আগামী ৭ দিনের "
            "সর্বোচ্চ-সর্বনিম্ন তাপমাত্রা ও বৃষ্টি এনে weather.csv ফাইলে সেভ করে।"
        ),
        "project_code": '''import csv
import requests

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 23.81,            # ঢাকা
    "longitude": 90.41,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Dhaka",
}

r = requests.get(URL, params=params, timeout=15)
r.raise_for_status()
daily = r.json()["daily"]

with open("weather.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["date", "max_c", "min_c", "rain_mm"])
    for row in zip(daily["time"],
                   daily["temperature_2m_max"],
                   daily["temperature_2m_min"],
                   daily["precipitation_sum"]):
        w.writerow(row)
        print(*row)

print("weather.csv সেভ হয়েছে ✔")''',
    },
    "pandas": {
        "about": (
            "pandas হলো টেবিল আকারের ডেটা (Excel, CSV) নিয়ে কাজ করার সবচেয়ে জনপ্রিয় লাইব্রেরি। "
            "DataFrame নামের টেবিলে ডেটা রেখে ফিল্টার, সাজানো, গ্রুপ করে যোগফল/গড় বের করা, "
            "দুই টেবিল জোড়া লাগানো—সব সহজে করা যায়।"
        ),
        "install": "pip install pandas",
        "example": '''import pandas as pd

df = pd.DataFrame({
    "নাম":   ["রহিম", "করিম", "সুমি", "রিয়া"],
    "বয়স":   [22, 25, 21, 24],
    "নম্বর": [78, 85, 92, 66],
})

print(df)
print(df[df["নম্বর"] > 70])            # ফিল্টার
print(df.sort_values("নম্বর", ascending=False))
print("গড় নম্বর:", df["নম্বর"].mean())''',
        "project_title": "CSV survey থেকে অঞ্চলভিত্তিক সারাংশ",
        "project_about": (
            "একটা জরিপের CSV পড়ে প্রতিটা বিভাগের উত্তরদাতার সংখ্যা, গড় বয়স ও "
            "গড় সন্তুষ্টি স্কোর বের করে summary.csv-তে সেভ করে।"
        ),
        "project_code": '''import io
import pandas as pd

# আসল প্রজেক্টে: df = pd.read_csv("survey.csv")
csv_text = """region,age,satisfaction
Dhaka,25,4
Dhaka,31,5
Chattogram,28,3
Chattogram,40,4
Khulna,35,2
Khulna,22,4
Dhaka,45,3
"""
df = pd.read_csv(io.StringIO(csv_text))

summary = (
    df.groupby("region")
      .agg(people=("age", "count"),
           avg_age=("age", "mean"),
           avg_score=("satisfaction", "mean"))
      .round(1)
      .sort_values("avg_score", ascending=False)
)

print(summary)
summary.to_csv("summary.csv")
print("summary.csv সেভ হয়েছে ✔")''',
    },
    "numpy": {
        "about": (
            "NumPy পাইথনে দ্রুত সংখ্যা-হিসাবের ভিত্তি। এর array দিয়ে লক্ষ লক্ষ সংখ্যার উপর "
            "একসাথে যোগ-গুণ, গড়, ম্যাট্রিক্স হিসাব করা যায়, লুপ লিখতে হয় না। "
            "pandas, scikit-learn, Matplotlib সবই NumPy-র উপর তৈরি।"
        ),
        "install": "pip install numpy",
        "example": '''import numpy as np

a = np.array([1, 2, 3, 4, 5])
print(a * 2)            # [ 2  4  6  8 10]  লুপ ছাড়াই
print(a.mean(), a.sum(), a.max())

m = np.arange(1, 7).reshape(2, 3)   # 2x3 ম্যাট্রিক্স
print(m)
print(m.T)              # ট্রান্সপোজ
print(m + np.array([10, 20, 30]))   # broadcasting''',
        "project_title": "বিভিন্ন স্টেশনের মাসিক বৃষ্টিপাতের গড় গণনার টুল",
        "project_about": (
            "৩টা আবহাওয়া স্টেশনের ১২ মাসের বৃষ্টিপাত (mm) একটা 2D array-তে রেখে প্রতিটা "
            "স্টেশনের বার্ষিক মোট, মাসিক গড় আর সবচেয়ে বৃষ্টির মাস বের করে।"
        ),
        "project_code": '''import numpy as np

stations = ["Dhaka", "Sylhet", "Rajshahi"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# আসল ডেটা না থাকলে নমুনা ডেটা বানানো (সারি = স্টেশন, কলাম = মাস)
rng = np.random.default_rng(42)
monsoon = np.array([5, 20, 50, 120, 250, 350, 400, 330, 280, 150, 30, 10])
rain = np.clip(monsoon * rng.uniform(0.6, 1.6, size=(3, 1))
               + rng.normal(0, 20, size=(3, 12)), 0, None).round()

total = rain.sum(axis=1)
average = rain.mean(axis=1)
wettest = rain.argmax(axis=1)

for i, name in enumerate(stations):
    print(f"{name:9} মোট {total[i]:6.0f} mm | "
          f"গড় {average[i]:5.1f} mm | সবচেয়ে বৃষ্টি: {months[wettest[i]]}")

print("সব স্টেশনের সম্মিলিত মাসিক গড়:", rain.mean(axis=0).round(1))''',
    },
    "matplotlib": {
        "about": (
            "Matplotlib দিয়ে পাইথনে লাইন, বার, পাই, স্ক্যাটারসহ প্রায় সব ধরনের গ্রাফ আঁকা যায়। "
            "গ্রাফটাকে PNG, SVG বা PDF হিসেবে সেভ করে রিপোর্ট বা প্রেজেন্টেশনে ব্যবহার করা যায়।"
        ),
        "install": "pip install matplotlib",
        "example": '''import matplotlib.pyplot as plt

days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
temp = [31, 33, 32, 34, 35, 33, 30]

plt.plot(days, temp, marker="o")
plt.title("Weekly temperature")
plt.ylabel("°C")
plt.grid(alpha=0.3)
plt.show()''',
        "project_title": "বর্ষার বৃষ্টিপাতের PNG ও SVG গ্রাফ",
        "project_about": (
            "১২ মাসের বৃষ্টিপাতের বার চার্ট আঁকে, বর্ষার মাসগুলো (জুন–সেপ্টেম্বর) আলাদা রঙে দেখায়, "
            "আর গ্রাফটা rainfall.png ও rainfall.svg হিসেবে সেভ করে।"
        ),
        "project_code": '''import matplotlib
matplotlib.use("Agg")          # স্ক্রিন ছাড়া শুধু ফাইলে সেভ
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rain = [7, 28, 65, 150, 280, 330, 380, 310, 300, 170, 30, 10]
colors = ["#2e86de" if 5 <= i <= 8 else "#b2bec3" for i in range(12)]

fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(months, rain, color=colors)
ax.bar_label(bars, fontsize=8)
ax.set_title("Monthly rainfall – monsoon highlighted")
ax.set_ylabel("Rainfall (mm)")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()

fig.savefig("rainfall.png", dpi=200)
fig.savefig("rainfall.svg")
print("rainfall.png ও rainfall.svg সেভ হয়েছে ✔")''',
    },
    "flask": {
        "about": (
            "Flask হলো ছোট ও সহজ ওয়েব ফ্রেমওয়ার্ক। কয়েক লাইনেই একটা ওয়েব পেজ বা API চালু করা যায়। "
            "শেখার জন্য দারুণ, আবার ছোট-মাঝারি আসল প্রজেক্টেও ব্যবহার হয়।"
        ),
        "install": "pip install flask",
        "example": '''from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>আসসালামু আলাইকুম! এটা আমার Flask সাইট</h1>"

@app.route("/hello/<name>")
def hello(name):
    return f"হ্যালো, {name}!"

if __name__ == "__main__":
    app.run(debug=True)       # ব্রাউজারে খোলো: http://127.0.0.1:5000''',
        "project_title": "মাঠ পর্যবেক্ষণ লগের API",
        "project_about": (
            "মাঠে গিয়ে যা দেখা হলো (জায়গা, প্রজাতি, সংখ্যা) সেটা সেভ করার একটা REST API। "
            "GET দিয়ে সব লগ দেখা যায়, POST দিয়ে নতুন লগ যোগ করা যায়।"
        ),
        "project_code": '''from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
observations = []      # সহজ রাখতে মেমোরিতে; আসল প্রজেক্টে ডেটাবেস ব্যবহার করো

@app.get("/observations")
def list_observations():
    return jsonify(observations)

@app.post("/observations")
def add_observation():
    data = request.get_json(silent=True) or {}
    missing = [k for k in ("place", "species", "count") if k not in data]
    if missing:
        return jsonify(error=f"এগুলো লাগবে: {', '.join(missing)}"), 400

    item = {
        "id": len(observations) + 1,
        "place": data["place"],
        "species": data["species"],
        "count": int(data["count"]),
        "time": datetime.now().isoformat(timespec="seconds"),
    }
    observations.append(item)
    return jsonify(item), 201

if __name__ == "__main__":
    app.run(debug=True)

# টেস্ট করতে আরেকটা টার্মিনালে:
# curl -X POST http://127.0.0.1:5000/observations \\
#      -H "Content-Type: application/json" \\
#      -d '{"place": "Sundarbans", "species": "Kingfisher", "count": 3}'
# curl http://127.0.0.1:5000/observations''',
    },
}


# ==================================================================
# ব্যাচ ১ক: মেশিন লার্নিং, চার্ট, ওয়েব, স্ক্র্যাপিং
# ==================================================================

DETAILS["scikit-learn"] = lib(
    about=(
        "scikit-learn হলো ক্লাসিক মেশিন লার্নিংয়ের সবচেয়ে জনপ্রিয় লাইব্রেরি। "
        "classification (কোন শ্রেণিতে পড়ে), regression (সংখ্যা অনুমান), clustering (দল ভাগ) "
        "সব ধরনের মডেল একই নিয়মে চলে: fit() দিয়ে শেখাও, predict() দিয়ে অনুমান করো।"
    ),
    install="pip install scikit-learn",
    example='''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)         # ফুলের মাপ ও প্রজাতি
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)

model = DecisionTreeClassifier(max_depth=3)
model.fit(X_train, y_train)                # শেখানো

pred = model.predict(X_test)               # অনুমান
print("Accuracy:", accuracy_score(y_test, pred))''',
    project_title="আবহাওয়ার বৈশিষ্ট্য থেকে বৃষ্টির সম্ভাবনা শেখার ডেমো",
    project_about=(
        "আর্দ্রতা, বায়ুচাপ ও তাপমাত্রা থেকে পরদিন বৃষ্টি হবে কিনা শেখে "
        "(নমুনা ডেটা দিয়ে), মডেলের নির্ভুলতা দেখায় আর নতুন দিনের বৃষ্টির সম্ভাবনা % এ বলে।"
    ),
    project_code='''import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# নমুনা ডেটা: আর্দ্রতা (%), বায়ুচাপ (hPa), তাপমাত্রা (°C)
rng = np.random.default_rng(1)
n = 600
humidity = rng.uniform(40, 100, n)
pressure = rng.normal(1008, 6, n)
temp = rng.uniform(20, 38, n)
score = 0.08 * (humidity - 70) - 0.25 * (pressure - 1008) - 0.05 * (temp - 30)
rain = (score + rng.normal(0, 1, n) > 0).astype(int)

X = np.column_stack([humidity, pressure, temp])
X_train, X_test, y_train, y_test = train_test_split(X, rain, random_state=0)

model = make_pipeline(StandardScaler(), LogisticRegression())
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test),
                            target_names=["no rain", "rain"]))

today = [[80, 1006, 30]]          # আজকের মাপ
p = model.predict_proba(today)[0, 1]
print(f"আগামীকাল বৃষ্টির সম্ভাবনা: {p:.0%}")''',
)

DETAILS["seaborn"] = lib(
    about=(
        "seaborn হলো Matplotlib-এর উপর বানানো সহজ চার্ট লাইব্রেরি। pandas টেবিল দিয়ে এক লাইনে "
        "boxplot, histogram, heatmap, scatter-এর মতো পরিসংখ্যান চার্ট আঁকা যায়, "
        "আর ডিফল্ট রং ও স্টাইলও সুন্দর।"
    ),
    install="pip install seaborn",
    example='''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({"marks": np.random.default_rng(0).normal(65, 12, 200)})

sns.set_theme(style="whitegrid")
sns.histplot(data=df, x="marks", bins=20, kde=True)
plt.title("Exam marks distribution")
plt.savefig("marks.png", dpi=150)
print("marks.png সেভ হয়েছে ✔")''',
    project_title="দুই অঞ্চলের তাপমাত্রার boxplot",
    project_about=(
        "ঢাকা ও সিলেটের প্রতিদিনের তাপমাত্রা মাস অনুযায়ী পাশাপাশি boxplot-এ দেখায়, "
        "যাতে কোন মাসে কোথায় বেশি গরম আর কতটা ওঠানামা হয় এক নজরে বোঝা যায়।"
    ),
    project_code='''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# নমুনা ডেটা (আসল প্রজেক্টে: df = pd.read_csv("temperature.csv"))
rng = np.random.default_rng(7)
rows = []
for region, base in [("Dhaka", 30), ("Sylhet", 27)]:
    for month in ["Mar", "Apr", "May", "Jun"]:
        bump = {"Mar": 0, "Apr": 2, "May": 3, "Jun": 1.5}[month]
        for t in rng.normal(base + bump, 2, 30):
            rows.append({"region": region, "month": month, "temp": round(t, 1)})
df = pd.DataFrame(rows)

sns.set_theme(style="whitegrid")
ax = sns.boxplot(data=df, x="month", y="temp", hue="region",
                 palette=["#e17055", "#0984e3"])
ax.set(title="Daily temperature by month", xlabel="", ylabel="°C")
plt.tight_layout()
plt.savefig("temperature_boxplot.png", dpi=200)

print(df.groupby(["region", "month"])["temp"].median().unstack())
print("temperature_boxplot.png সেভ হয়েছে ✔")''',
)

DETAILS["pydantic"] = lib(
    about=(
        "pydantic দিয়ে ডেটার গঠন (কোন ফিল্ড কোন টাইপ) লিখে দিলে ইনপুট নিজে থেকেই যাচাই ও "
        "রূপান্তর হয়ে যায়। ভুল ডেটা এলে পরিষ্কার error দেয়। FastAPI এটার উপরেই চলে।"
    ),
    install="pip install pydantic",
    example='''from pydantic import BaseModel, ValidationError

class Student(BaseModel):
    name: str
    age: int
    email: str | None = None

s = Student(name="Rahim", age="21")   # "21" নিজে থেকে int হয়ে যায়
print(s)
print(s.model_dump())

try:
    Student(name="Karim", age="twenty")
except ValidationError as e:
    print(e)''',
    project_title="মাপজোক গ্রহণের API-তে unit ও range validator",
    project_about=(
        "সেন্সর থেকে আসা তাপমাত্রার রিডিং যাচাই করে: ইউনিট শুধু C বা F, মান স্বাভাবিক সীমার "
        "মধ্যে কিনা, আর F এলে নিজে থেকেই C-তে রূপান্তর করে। ভুল রিডিং আলাদা করে দেখায়।"
    ),
    project_code='''from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, model_validator

class Reading(BaseModel):
    station: str = Field(min_length=2)
    time: datetime
    unit: Literal["C", "F"]
    value: float

    @model_validator(mode="after")
    def to_celsius(self):
        if self.unit == "F":
            self.value = round((self.value - 32) * 5 / 9, 1)
            self.unit = "C"
        if not -10 <= self.value <= 55:
            raise ValueError(f"{self.value}°C স্বাভাবিক সীমার বাইরে")
        return self

incoming = [
    {"station": "Dhaka", "time": "2026-06-01T09:00", "unit": "C", "value": 31.5},
    {"station": "Sylhet", "time": "2026-06-01T09:00", "unit": "F", "value": 86},
    {"station": "Khulna", "time": "2026-06-01T09:00", "unit": "K", "value": 300},
    {"station": "Bogura", "time": "not-a-date", "unit": "C", "value": 30},
    {"station": "Rangpur", "time": "2026-06-01T09:00", "unit": "C", "value": 99},
]

good, bad = [], []
for raw in incoming:
    try:
        good.append(Reading(**raw))
    except ValidationError as e:
        bad.append((raw["station"], e.errors()[0]["msg"]))

for r in good:
    print("✔", r.station, r.value, "°C")
for station, msg in bad:
    print("✘", station, "→", msg)''',
)

DETAILS["starlette"] = lib(
    about=(
        "Starlette হলো হালকা ও দ্রুত async ওয়েব ফ্রেমওয়ার্ক (ASGI)। রাউট, JSON রেসপন্স, "
        "WebSocket, ব্যাকগ্রাউন্ড টাস্ক সব আছে। FastAPI আসলে Starlette-এর উপর বানানো।"
    ),
    install="pip install starlette uvicorn",
    example='''from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def home(request):
    return JSONResponse({"message": "Hello from Starlette"})

async def square(request):
    n = int(request.path_params["n"])
    return JSONResponse({"n": n, "square": n * n})

app = Starlette(routes=[
    Route("/", home),
    Route("/square/{n:int}", square),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)     # ব্রাউজারে: http://127.0.0.1:8000/square/7''',
    project_title="গবেষণার run status দেখানোর live endpoint",
    project_about=(
        "একটা লম্বা গবেষণা run-এর অগ্রগতি দুইভাবে দেখায়: /status থেকে JSON, আর "
        "/live WebSocket দিয়ে প্রতি মুহূর্তের আপডেট সরাসরি ব্রাউজারে।"
    ),
    project_code='''import asyncio
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, WebSocketRoute

state = {"step": 0, "total": 10, "status": "running"}

async def status(request):
    return JSONResponse(state)

async def live(websocket):
    await websocket.accept()
    while state["step"] < state["total"]:
        state["step"] += 1                       # আসলে এখানে তোমার কাজ চলবে
        await websocket.send_json(state)
        await asyncio.sleep(0.5)
    state["status"] = "done"
    await websocket.send_json(state)
    await websocket.close()

PAGE = """<h2>Run progress</h2><progress id=p max=10 value=0></progress> <span id=t></span>
<script>
const ws = new WebSocket(`ws://${location.host}/live`);
ws.onmessage = e => { const s = JSON.parse(e.data);
  p.value = s.step; t.textContent = `${s.step}/${s.total} – ${s.status}`; };
</script>"""

async def home(request):
    return HTMLResponse(PAGE)

app = Starlette(routes=[Route("/", home), Route("/status", status),
                        WebSocketRoute("/live", live)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)     # খোলো: http://127.0.0.1:8000''',
)

DETAILS["beautifulsoup4"] = lib(
    about=(
        "BeautifulSoup দিয়ে HTML বা XML পেজ থেকে দরকারি তথ্য (শিরোনাম, লিংক, টেবিল, দাম) "
        "সহজে খুঁজে বের করা যায়। সাধারণত requests দিয়ে পেজ এনে BeautifulSoup দিয়ে পড়া হয়।"
    ),
    install="pip install beautifulsoup4",
    example='''from bs4 import BeautifulSoup

html = """
<html><body>
  <h1>আমার ব্লগ</h1>
  <a href="/post-1">প্রথম পোস্ট</a>
  <a href="/post-2">দ্বিতীয় পোস্ট</a>
</body></html>
"""

soup = BeautifulSoup(html, "html.parser")
print("শিরোনাম:", soup.h1.text)
for a in soup.find_all("a"):
    print(a.text, "→", a["href"])''',
    project_title="লোকাল HTML থেকে বইয়ের শিরোনামের CSV",
    project_about=(
        "সেভ করা একটা বইয়ের তালিকার HTML পেজ পড়ে প্রতিটা বইয়ের নাম, লেখক ও দাম বের করে "
        "books.csv ফাইলে সেভ করে।"
    ),
    project_code='''import csv
from bs4 import BeautifulSoup

# আসল প্রজেক্টে: html = open("books.html", encoding="utf-8").read()
html = """
<div class="book"><h3>পথের পাঁচালী</h3><span class="author">বিভূতিভূষণ</span><span class="price">৳250</span></div>
<div class="book"><h3>দেবদাস</h3><span class="author">শরৎচন্দ্র</span><span class="price">৳180</span></div>
<div class="book"><h3>গীতাঞ্জলি</h3><span class="author">রবীন্দ্রনাথ</span><span class="price">৳300</span></div>
"""

soup = BeautifulSoup(html, "html.parser")
books = []
for card in soup.select("div.book"):
    books.append({
        "title": card.h3.get_text(strip=True),
        "author": card.select_one(".author").get_text(strip=True),
        "price": int(card.select_one(".price").text.strip("৳")),
    })

with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["title", "author", "price"])
    w.writeheader()
    w.writerows(books)

for b in books:
    print(b)
print(f"{len(books)}টা বই books.csv-তে সেভ হয়েছে ✔")''',
)

DETAILS["lxml"] = lib(
    about=(
        "lxml হলো খুব দ্রুত XML ও HTML পার্সার। XPath দিয়ে ঠিক কোন জায়গার ডেটা দরকার সেটা "
        "এক লাইনে বলে দেওয়া যায়। বড় XML ফাইল বা feed নিয়ে কাজে খুব কাজের।"
    ),
    install="pip install lxml",
    example='''from lxml import etree

xml = b"""
<library>
  <book year="1929"><title>Pather Panchali</title></book>
  <book year="1917"><title>Devdas</title></book>
</library>
"""

root = etree.fromstring(xml)
print(root.xpath("//title/text()"))            # সব শিরোনাম
print(root.xpath("//book[@year<1920]/title/text()"))  # শর্তসহ খোঁজা''',
    project_title="স্থানীয় আবহাওয়া XML feed-এর রূপান্তর",
    project_about=(
        "আবহাওয়া স্টেশনের XML feed পড়ে XPath দিয়ে প্রতিটা রিডিং বের করে, সবচেয়ে গরম "
        "স্টেশন খুঁজে বের করে আর পুরো ডেটা CSV-তে রূপান্তর করে।"
    ),
    project_code='''import csv
from lxml import etree

# আসল প্রজেক্টে: root = etree.parse("feed.xml").getroot()
feed = b"""<?xml version="1.0"?>
<weather updated="2026-06-01T09:00">
  <station id="DHK" name="Dhaka"><temp unit="C">31.4</temp><humidity>78</humidity></station>
  <station id="SYL" name="Sylhet"><temp unit="C">28.9</temp><humidity>88</humidity></station>
  <station id="RAJ" name="Rajshahi"><temp unit="C">34.1</temp><humidity>61</humidity></station>
</weather>"""

root = etree.fromstring(feed)
updated = root.get("updated")

rows = []
for st in root.xpath("//station"):
    rows.append({
        "id": st.get("id"),
        "name": st.get("name"),
        "temp_c": float(st.xpath("string(temp)")),
        "humidity": int(st.xpath("string(humidity)")),
        "updated": updated,
    })

with open("weather.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

hottest = max(rows, key=lambda r: r["temp_c"])
print("সবচেয়ে গরম:", hottest["name"], hottest["temp_c"], "°C")
print(f"{len(rows)}টা স্টেশন weather.csv-তে সেভ হয়েছে ✔")''',
)

DETAILS["playwright"] = lib(
    about=(
        "Playwright দিয়ে কোড লিখে ব্রাউজার (Chromium, Firefox, WebKit) চালানো যায়: পেজ খোলা, "
        "ক্লিক, টাইপ, স্ক্রিনশট। ওয়েবসাইট ঠিকমতো কাজ করছে কিনা অটোমেটিক টেস্ট করতে এটা সেরা।"
    ),
    install="pip install playwright\nplaywright install chromium",
    example='''from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()           # headless=False দিলে ব্রাউজার দেখা যাবে
    page = browser.new_page()
    page.goto("https://example.com")
    print("Title:", page.title())
    page.screenshot(path="example.png")
    browser.close()''',
    project_title="নিজের ক্যাটালগের search ও filter regression suite",
    project_about=(
        "একটা ছোট ক্যাটালগ পেজে সার্চ বক্স ঠিকমতো ফিল্টার করছে কিনা টেস্ট করে। "
        "কয়েকটা সার্চ শব্দ দিয়ে দেখে কতগুলো ফলাফল আসে, ভুল হলে জানায়।"
    ),
    project_code='''from playwright.sync_api import sync_playwright, expect

# আসল প্রজেক্টে: page.goto("https://তোমার-সাইট.github.io")
CATALOG = """
<input id="q" placeholder="search">
<ul id="list"><li>numpy</li><li>pandas</li><li>pydantic</li><li>flask</li></ul>
<script>
q.oninput = () => document.querySelectorAll("#list li").forEach(li =>
  li.hidden = !li.textContent.includes(q.value.toLowerCase()));
</script>
"""

CASES = [("p", 3), ("pandas", 1), ("flask", 1), ("zzz", 0), ("", 4)]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(CATALOG)
    items = page.locator("#list li:visible")

    failed = 0
    for text, expected in CASES:
        page.fill("#q", text)
        try:
            expect(items).to_have_count(expected, timeout=1000)
            print(f"✔ '{text}' → {expected}টা ফলাফল")
        except AssertionError:
            failed += 1
            print(f"✘ '{text}' → {items.count()}টা, আশা ছিল {expected}")
    page.screenshot(path="catalog.png")
    browser.close()

print("সব টেস্ট পাস ✔" if failed == 0 else f"{failed}টা টেস্ট ফেল")''',
)

DETAILS["watchdog"] = lib(
    about=(
        "watchdog একটা ফোল্ডার নজরে রাখে। নতুন ফাইল এলে, ফাইল বদলালে বা মুছলে সাথে সাথে "
        "তোমার কোড চালিয়ে দেয়। অটোমেশনের জন্য খুব কাজের।"
    ),
    install="pip install watchdog",
    example='''import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Printer(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)

observer = Observer()
observer.schedule(Printer(), path=".", recursive=False)
observer.start()
print("এই ফোল্ডার নজরে রাখছি… (বন্ধ করতে Ctrl+C)")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()''',
    project_title="ফোল্ডারে CSV এলেই preview তৈরি",
    project_about=(
        "inbox ফোল্ডারে কোনো CSV ফাইল রাখলেই সেটা পড়ে কয়টা সারি-কলাম আছে আর প্রথম কয়েকটা "
        "সারি দেখায়, আর পাশে একটা _preview.txt ফাইল বানিয়ে রাখে।"
    ),
    project_code='''import csv
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

INBOX = Path("inbox")
INBOX.mkdir(exist_ok=True)

def make_preview(path: Path):
    time.sleep(0.3)                          # ফাইল লেখা শেষ হওয়া পর্যন্ত অপেক্ষা
    with path.open(encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    lines = [f"ফাইল: {path.name}",
             f"কলাম ({len(header)}): {', '.join(header)}",
             f"সারি: {len(data)}", "প্রথম ৩ সারি:"]
    lines += ["  " + " | ".join(r) for r in data[:3]]
    text = "\\n".join(lines)
    path.with_name(path.stem + "_preview.txt").write_text(text, encoding="utf-8")
    print(text, "\\n")

class CsvHandler(FileSystemEventHandler):
    def on_created(self, event):
        p = Path(event.src_path)
        if p.suffix.lower() == ".csv":
            make_preview(p)

observer = Observer()
observer.schedule(CsvHandler(), str(INBOX))
observer.start()
print(f"'{INBOX}' ফোল্ডারে CSV রাখো… (বন্ধ করতে Ctrl+C)")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()''',
)


# ==================================================================
# ব্যাচ ১খ: ছবি ও কম্পিউটার ভিশন
# ==================================================================

DETAILS["opencv-python"] = lib(
    about=(
        "OpenCV হলো কম্পিউটার ভিশনের সবচেয়ে বড় লাইব্রেরি। ছবি বা ভিডিও পড়া, রং বদলানো, "
        "ব্লার, এজ খোঁজা, মুখ শনাক্ত করা, ক্যামেরা থেকে লাইভ ভিডিও প্রসেস করা সব করা যায়।"
    ),
    install="pip install opencv-python",
    example='''import cv2

img = cv2.imread("photo.jpg")                  # BGR রঙে পড়ে
print("মাপ (উচ্চতা, প্রস্থ, চ্যানেল):", img.shape)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # সাদা-কালো
blur = cv2.GaussianBlur(img, (15, 15), 0)      # ঝাপসা
small = cv2.resize(img, None, fx=0.5, fy=0.5)  # অর্ধেক মাপ

cv2.imwrite("gray.jpg", gray)
cv2.imwrite("blur.jpg", blur)
cv2.imwrite("small.jpg", small)
print("৩টা ছবি সেভ হয়েছে ✔")''',
    project_title="ছবির edge detection demo",
    project_about=(
        "একটা ছবির কিনারা (edge) খুঁজে বের করে Canny পদ্ধতিতে। আসল ছবি আর edge ছবি পাশাপাশি "
        "জোড়া লাগিয়ে edges.jpg সেভ করে, আর কয়টা আলাদা বস্তুর আউটলাইন পাওয়া গেল তা গোনে।"
    ),
    project_code='''import cv2
import numpy as np

img = cv2.imread("photo.jpg")
if img is None:
    raise SystemExit("photo.jpg পাওয়া যায়নি")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)       # noise কমানো
edges = cv2.Canny(gray, threshold1=50, threshold2=150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
big = [c for c in contours if cv2.contourArea(c) > 100]

outlined = img.copy()
cv2.drawContours(outlined, big, -1, (0, 0, 255), 2)

edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
side_by_side = np.hstack([outlined, edges_bgr])
cv2.imwrite("edges.jpg", side_by_side)

print(f"{len(big)}টা বস্তুর আউটলাইন পাওয়া গেছে")
print("edges.jpg সেভ হয়েছে ✔")''',
)

DETAILS["scikit-image"] = lib(
    about=(
        "scikit-image হলো বৈজ্ঞানিক ছবি বিশ্লেষণের লাইব্রেরি। ছবিকে ভাগ করা (segmentation), "
        "বস্তু গোনা, তাদের আকার মাপা, ফিল্টার লাগানো সব NumPy array দিয়েই হয়।"
    ),
    install="pip install scikit-image",
    example='''from skimage import data, filters, io, util

img = data.camera()                    # লাইব্রেরির সাথে আসা নমুনা ছবি
edges = filters.sobel(img)             # কিনারা খোঁজা
smooth = filters.gaussian(img, sigma=3)

io.imsave("edges.png", util.img_as_ubyte(edges / edges.max()))
io.imsave("smooth.png", util.img_as_ubyte(smooth))
print("ছবির মাপ:", img.shape, "→ edges.png ও smooth.png সেভ হয়েছে ✔")''',
    project_title="Microscope ছবিতে সাধারণ কণার area গণনা",
    project_about=(
        "একটা ছবিতে আলাদা আলাদা কণা (এখানে নমুনা হিসেবে মুদ্রা) খুঁজে বের করে প্রতিটার "
        "ক্ষেত্রফল মাপে, গড় আকার বলে আর প্রতিটা কণা লেবেলসহ ছবি সেভ করে।"
    ),
    project_code='''import numpy as np
from skimage import data, filters, measure, morphology, color, io, util

# আসল প্রজেক্টে: img = io.imread("microscope.png", as_gray=True)
img = data.coins()

thresh = filters.threshold_otsu(img)                 # অটো threshold
mask = img > thresh
mask = morphology.remove_small_objects(mask, max_size=150)
mask = morphology.closing(mask, morphology.disk(3))

labels = measure.label(mask)
props = measure.regionprops(labels)

areas = np.array([int(p.area) for p in props])
print(f"কণার সংখ্যা: {len(props)}")
print(f"গড় area: {areas.mean():.0f} px | ছোট: {areas.min()} | বড়: {areas.max()}")
for p in sorted(props, key=lambda p: p.area, reverse=True)[:5]:
    y, x = p.centroid
    print(f"  #{p.label:2}  area={int(p.area):5}  center=({x:.0f}, {y:.0f})")

overlay = color.label2rgb(labels, image=img, bg_label=0, alpha=0.4)
io.imsave("particles.png", util.img_as_ubyte(overlay))
print("particles.png সেভ হয়েছে ✔")''',
)

DETAILS["imageio"] = lib(
    about=(
        "imageio দিয়ে প্রায় সব ধরনের ছবি (PNG, JPG, GIF), এমনকি ভিডিও ফ্রেম সহজে পড়া ও লেখা যায়। "
        "ছবিগুলো NumPy array হিসেবে আসে, তাই প্রসেস করা সহজ।"
    ),
    install="pip install imageio",
    example='''import numpy as np
import imageio.v3 as iio

# একটা রঙিন gradient ছবি বানানো
h, w = 200, 300
x = np.linspace(0, 255, w, dtype=np.uint8)
img = np.dstack([np.tile(x, (h, 1)),
                 np.full((h, w), 120, np.uint8),
                 np.tile(x[::-1], (h, 1))])

iio.imwrite("gradient.png", img)
back = iio.imread("gradient.png")
print("সেভ করে আবার পড়া হলো:", back.shape, back.dtype)''',
    project_title="স্যাটেলাইট snapshots থেকে animated GIF",
    project_about=(
        "একের পর এক ছবি (এখানে একটা ঘূর্ণিঝড়ের নমুনা স্যাটেলাইট ছবি) জোড়া দিয়ে লুপ করা "
        "animated GIF বানায়। আসল প্রজেক্টে ফোল্ডারের সব ছবি নাম অনুযায়ী সাজিয়ে নেবে।"
    ),
    project_code='''import numpy as np
import imageio.v3 as iio

# আসল প্রজেক্টে:
# from pathlib import Path
# frames = [iio.imread(p) for p in sorted(Path("snapshots").glob("*.png"))]

size = 160
yy, xx = np.mgrid[0:size, 0:size]
frames = []
for t in range(24):
    cx, cy = 30 + t * 4, 120 - t * 3                  # ঝড় সরে যাচ্ছে
    angle = np.arctan2(yy - cy, xx - cx)
    r = np.hypot(xx - cx, yy - cy)
    cloud = np.clip(255 * np.exp(-r / 35) * (0.6 + 0.4 * np.sin(3 * angle + r / 6 - t)), 0, 255)
    sea = np.zeros((size, size, 3), np.uint8)
    sea[..., 2] = 90                                  # নীল সমুদ্র
    frame = sea.copy()
    for ch in range(3):
        frame[..., ch] = np.maximum(sea[..., ch], cloud).astype(np.uint8)
    frames.append(frame)

iio.imwrite("storm.gif", np.stack(frames), duration=120, loop=0)
print(f"{len(frames)} ফ্রেমের storm.gif সেভ হয়েছে ✔")''',
)

# ==================================================================
# ব্যাচ ১গ: PDF, Excel, Word, PowerPoint, OCR
# ==================================================================

DETAILS["pypdf"] = lib(
    about=(
        "pypdf দিয়ে PDF ফাইল পড়া, পৃষ্ঠা আলাদা করা, কয়েকটা PDF জোড়া লাগানো, পৃষ্ঠা ঘোরানো, "
        "লেখা বের করা আর পাসওয়ার্ড দেওয়া যায়। কোনো বাইরের প্রোগ্রাম লাগে না।"
    ),
    install="pip install pypdf",
    example='''from pypdf import PdfReader, PdfWriter

reader = PdfReader("document.pdf")
print("মোট পৃষ্ঠা:", len(reader.pages))
print("১ম পৃষ্ঠার লেখা:", reader.pages[0].extract_text())

# শুধু ১ম পৃষ্ঠা আলাদা ফাইলে
writer = PdfWriter()
writer.add_page(reader.pages[0])
writer.write("first_page.pdf")
print("first_page.pdf সেভ হয়েছে ✔")''',
    project_title="থিসিস appendix PDF merge tool",
    project_about=(
        "মূল থিসিস আর appendix PDF এক ফাইলে জোড়া লাগায়, প্রতিটা অংশের জন্য bookmark (সূচি) "
        "যোগ করে আর ফাইলের তথ্য (শিরোনাম, লেখক) বসিয়ে দেয়।"
    ),
    project_code='''from pypdf import PdfReader, PdfWriter

parts = [("Thesis", "thesis.pdf"), ("Appendix", "appendix.pdf")]

writer = PdfWriter()
for title, path in parts:
    start = len(writer.pages)
    reader = PdfReader(path)
    for page in reader.pages:
        writer.add_page(page)
    writer.add_outline_item(title, start)          # bookmark
    print(f"{path}: {len(reader.pages)} পৃষ্ঠা যোগ হলো")

writer.add_metadata({"/Title": "My Thesis (complete)", "/Author": "Your Name"})
with open("thesis_full.pdf", "wb") as f:
    writer.write(f)

print("মোট", len(writer.pages), "পৃষ্ঠার thesis_full.pdf সেভ হয়েছে ✔")''',
)

DETAILS["pdfplumber"] = lib(
    about=(
        "pdfplumber PDF-এর ভেতরের লেখা, শব্দের অবস্থান, লাইন আর টেবিল খুব নিখুঁতভাবে বের করে। "
        "রিপোর্ট বা বিল থেকে টেবিল তুলে Excel/CSV বানানোর জন্য সেরা।"
    ),
    install="pip install pdfplumber",
    example='''import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    print("মোট পৃষ্ঠা:", len(pdf.pages))
    page = pdf.pages[0]
    print(page.extract_text())

    words = page.extract_words()
    print("প্রথম ৫টা শব্দ ও অবস্থান:")
    for w in words[:5]:
        print(f"  {w['text']:10} x={w['x0']:.0f} y={w['top']:.0f}")''',
    project_title="বৃষ্টিপাতের report table-কে CSV-তে তোলা",
    project_about=(
        "PDF রিপোর্টের সব পৃষ্ঠা থেকে টেবিল খুঁজে বের করে rainfall.csv-তে সেভ করে, "
        "আর প্রতিটা স্টেশনের মোট বৃষ্টি হিসাব করে দেখায়।"
    ),
    project_code='''import csv
import pdfplumber

rows = []
with pdfplumber.open("report.pdf") as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        for table in page.extract_tables():
            print(f"পৃষ্ঠা {i}: {len(table)} সারির টেবিল পাওয়া গেছে")
            if not rows:
                rows.append(table[0])          # header একবারই
            rows.extend(table[1:])

if not rows:
    raise SystemExit("কোনো টেবিল পাওয়া যায়নি")

with open("rainfall.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

header, data = rows[0], rows[1:]
for r in data:
    total = sum(float(v) for v in r[1:] if v)
    print(f"{r[0]:10} মোট {total:.0f} mm")
print("rainfall.csv সেভ হয়েছে ✔")''',
)

DETAILS["reportlab"] = lib(
    about=(
        "ReportLab দিয়ে পাইথন কোড থেকেই সুন্দর PDF বানানো যায়: লেখা, টেবিল, চার্ট, ছবি, "
        "পৃষ্ঠা নম্বর সব। সার্টিফিকেট, ইনভয়েস, রিপোর্ট অটোমেটিক বানাতে কাজের।"
    ),
    install="pip install reportlab",
    example='''from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=A4)
width, height = A4

c.setFont("Helvetica-Bold", 28)
c.drawString(72, height - 100, "Hello, PDF!")
c.setFont("Helvetica", 14)
c.drawString(72, height - 130, "Made with Python + ReportLab")
c.line(72, height - 140, width - 72, height - 140)

c.save()
print("hello.pdf সেভ হয়েছে ✔")''',
    project_title="চার্টসহ মাসিক স্টেশন রিপোর্ট",
    project_about=(
        "একটা আবহাওয়া স্টেশনের মাসিক রিপোর্ট PDF বানায়: শিরোনাম, সারাংশ, বৃষ্টিপাতের বার "
        "চার্ট, রঙিন টেবিল আর প্রতি পৃষ্ঠার নিচে পৃষ্ঠা নম্বর।"
    ),
    project_code='''from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

station = "Dhaka"
weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
rain = [62, 110, 95, 48]
temp = [31.2, 30.4, 29.8, 31.9]

styles = getSampleStyleSheet()
story = [
    Paragraph(f"{station} Station – June 2026", styles["Title"]),
    Paragraph(f"Total rainfall: <b>{sum(rain)} mm</b> · "
              f"Average temperature: <b>{sum(temp)/len(temp):.1f} °C</b>",
              styles["Normal"]),
    Spacer(1, 0.6 * cm),
]

d = Drawing(16 * cm, 7 * cm)
chart = VerticalBarChart()
chart.x, chart.y, chart.width, chart.height = 40, 30, 15 * cm - 40, 6 * cm - 30
chart.data = [rain]
chart.categoryAxis.categoryNames = weeks
chart.valueAxis.valueMin = 0
chart.bars[0].fillColor = colors.HexColor("#2e86de")
d.add(chart)
story += [d, Spacer(1, 0.6 * cm)]

data = [["Week", "Rain (mm)", "Temp (°C)"]] + [[w, r, t] for w, r, t in zip(weeks, rain, temp)]
table = Table(data, colWidths=[5 * cm, 4 * cm, 4 * cm])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a5c")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef5f1")]),
    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
]))
story.append(table)

def page_number(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(A4[0] - 2 * cm, 1.5 * cm, f"Page {doc.page}")

SimpleDocTemplate("station_report.pdf", pagesize=A4).build(
    story, onFirstPage=page_number, onLaterPages=page_number)
print("station_report.pdf সেভ হয়েছে ✔")''',
)

DETAILS["openpyxl"] = lib(
    about=(
        "openpyxl দিয়ে Excel (.xlsx) ফাইল পড়া, লেখা, এডিট করা যায়: সেলে মান বসানো, ফর্মুলা, "
        "রং, ফন্ট, কলামের মাপ, একাধিক শিট সব। Excel খোলা ছাড়াই কাজ হয়।"
    ),
    install="pip install openpyxl",
    example='''from openpyxl import Workbook, load_workbook

wb = Workbook()
ws = wb.active
ws.title = "Shopping"
ws.append(["Item", "Qty", "Price"])
ws.append(["Rice", 5, 70])
ws.append(["Oil", 2, 180])
ws["D1"] = "Total"
ws["D2"] = "=B2*C2"
ws["D3"] = "=B3*C3"
wb.save("shopping.xlsx")

wb2 = load_workbook("shopping.xlsx")
for row in wb2["Shopping"].iter_rows(values_only=True):
    print(row)''',
    project_title="শিক্ষার্থীর নম্বরের format করা workbook",
    project_about=(
        "শিক্ষার্থীদের নম্বর দিয়ে সুন্দর Excel ফাইল বানায়: রঙিন হেডার, মোট ও গড়ের ফর্মুলা, "
        "৪০-এর নিচে লাল রং, ফ্রিজ করা হেডার আর মানানসই কলামের মাপ।"
    ),
    project_code='''from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill

students = [
    ("Rahim", 78, 65, 82), ("Karim", 35, 58, 61), ("Sumi", 92, 88, 95),
    ("Riya", 66, 39, 70), ("Tanvir", 55, 72, 48),
]
subjects = ["Bangla", "English", "Math"]

wb = Workbook()
ws = wb.active
ws.title = "Marks"
ws.append(["Name", *subjects, "Total", "Average"])

for i, (name, *marks) in enumerate(students, start=2):
    ws.append([name, *marks, f"=SUM(B{i}:D{i})", f"=ROUND(AVERAGE(B{i}:D{i}),1)"])

header_fill = PatternFill("solid", fgColor="1F7A5C")
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center")

last = len(students) + 1
ws.conditional_formatting.add(
    f"B2:D{last}",
    CellIsRule(operator="lessThan", formula=["40"],
               fill=PatternFill("solid", fgColor="F8D7DA"),
               font=Font(color="9C0006", bold=True)))

for col, width in zip("ABCDEF", [14, 10, 10, 10, 10, 10]):
    ws.column_dimensions[col].width = width
ws.freeze_panes = "B2"

wb.save("marks.xlsx")
print(f"{len(students)} জন শিক্ষার্থীর marks.xlsx সেভ হয়েছে ✔")''',
)

DETAILS["xlsxwriter"] = lib(
    about=(
        "XlsxWriter দিয়ে নতুন Excel ফাইল বানানো যায়, বিশেষ করে Excel-এর নিজস্ব চার্ট, ফর্মুলা, "
        "কন্ডিশনাল ফরম্যাটিংসহ। এটা শুধু লেখে, পুরোনো ফাইল পড়তে পারে না।"
    ),
    install="pip install xlsxwriter",
    example='''import xlsxwriter

wb = xlsxwriter.Workbook("budget.xlsx")
ws = wb.add_worksheet("Budget")
bold = wb.add_format({"bold": True})
money = wb.add_format({"num_format": "৳#,##0"})

ws.write_row("A1", ["Item", "Cost"], bold)
items = [("Rent", 12000), ("Food", 8000), ("Transport", 2500)]
for r, (name, cost) in enumerate(items, start=1):
    ws.write(r, 0, name)
    ws.write(r, 1, cost, money)
ws.write(len(items) + 1, 0, "Total", bold)
ws.write_formula(len(items) + 1, 1, f"=SUM(B2:B{len(items) + 1})", money)

wb.close()
print("budget.xlsx সেভ হয়েছে ✔")''',
    project_title="ঋতুভেদে বৃষ্টির চার্টসহ spreadsheet",
    project_about=(
        "১২ মাসের বৃষ্টিপাত দিয়ে Excel ফাইল বানায়, প্রতিটা মাসের ঋতু লেখে, ঋতুভিত্তিক মোট "
        "ফর্মুলায় হিসাব করে আর Excel-এর নিজস্ব কলাম চার্ট বসিয়ে দেয়।"
    ),
    project_code='''import xlsxwriter

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rain = [7, 28, 65, 150, 280, 330, 380, 310, 300, 170, 30, 10]
season = {"Dec": "Winter", "Jan": "Winter", "Feb": "Winter",
          "Mar": "Summer", "Apr": "Summer", "May": "Summer",
          "Jun": "Monsoon", "Jul": "Monsoon", "Aug": "Monsoon", "Sep": "Monsoon",
          "Oct": "Autumn", "Nov": "Autumn"}

wb = xlsxwriter.Workbook("rainfall_seasons.xlsx")
ws = wb.add_worksheet("Rainfall")
head = wb.add_format({"bold": True, "bg_color": "#1F7A5C", "font_color": "white"})

ws.write_row(0, 0, ["Month", "Season", "Rain (mm)"], head)
for i, m in enumerate(months, start=1):
    ws.write_row(i, 0, [m, season[m], rain[i - 1]])

ws.write_row(0, 4, ["Season", "Total (mm)"], head)
for j, s in enumerate(["Winter", "Summer", "Monsoon", "Autumn"], start=1):
    ws.write(j, 4, s)
    ws.write_formula(j, 5, f'=SUMIF($B$2:$B$13,E{j + 1},$C$2:$C$13)')

ws.conditional_format("C2:C13", {"type": "data_bar", "bar_color": "#74B9FF"})
ws.set_column("A:F", 12)

chart = wb.add_chart({"type": "column"})
chart.add_series({"name": "Rainfall", "categories": "=Rainfall!$A$2:$A$13",
                  "values": "=Rainfall!$C$2:$C$13", "fill": {"color": "#2E86DE"}})
chart.set_title({"name": "Monthly rainfall"})
chart.set_y_axis({"name": "mm"})
chart.set_legend({"none": True})
ws.insert_chart("H2", chart, {"x_scale": 1.3, "y_scale": 1.2})

wb.close()
print("rainfall_seasons.xlsx সেভ হয়েছে ✔ (Excel-এ খুললে চার্ট দেখা যাবে)")''',
)

DETAILS["python-docx"] = lib(
    about=(
        "python-docx দিয়ে Word (.docx) ফাইল বানানো ও এডিট করা যায়: শিরোনাম, অনুচ্ছেদ, "
        "বোল্ড-ইটালিক, টেবিল, ছবি, পৃষ্ঠা বিরতি সব। একই ধরনের অনেক চিঠি বা রিপোর্ট অটো বানাতে কাজের।"
    ),
    install="pip install python-docx",
    example='''from docx import Document

doc = Document()
doc.add_heading("আমার প্রথম Word ফাইল", level=1)

p = doc.add_paragraph("এটা পাইথন দিয়ে লেখা। ")
p.add_run("এই অংশ বোল্ড").bold = True
p.add_run(", আর এটা ইটালিক।").italic = True

doc.add_paragraph("প্রথম পয়েন্ট", style="List Bullet")
doc.add_paragraph("দ্বিতীয় পয়েন্ট", style="List Bullet")

doc.save("hello.docx")
print("hello.docx সেভ হয়েছে ✔")''',
    project_title="Template থেকে গবেষণা progress memo",
    project_about=(
        "গবেষণার অগ্রগতির তথ্য (কাজ, অবস্থা, পরের ধাপ) একটা dict-এ রেখে প্রতি সপ্তাহে "
        "একই ফরম্যাটের Word memo বানায়: শিরোনাম, তারিখ, সারাংশ আর কাজের টেবিল।"
    ),
    project_code='''from datetime import date
from docx import Document
from docx.shared import Pt, RGBColor

memo = {
    "project": "Monsoon Rainfall Study",
    "to": "Dr. Rahman",
    "from": "Your Name",
    "summary": "Data collection is 80% complete. The cleaning script is ready "
               "and first charts look consistent with last year's report.",
    "tasks": [
        ("Collect station data", "Done", "—"),
        ("Clean missing values", "In progress", "Finish Sylhet station"),
        ("Draft results chapter", "Not started", "Start next Monday"),
    ],
}

doc = Document()
doc.styles["Normal"].font.size = Pt(11)

doc.add_heading(f"Progress Memo – {memo['project']}", level=1)
info = doc.add_paragraph()
info.add_run("Date: ").bold = True
info.add_run(f"{date.today():%d %B %Y}\\n")
info.add_run("To: ").bold = True
info.add_run(f"{memo['to']}\\n")
info.add_run("From: ").bold = True
info.add_run(memo["from"])

doc.add_heading("Summary", level=2)
doc.add_paragraph(memo["summary"])

doc.add_heading("Tasks", level=2)
table = doc.add_table(rows=1, cols=3)
table.style = "Light Grid Accent 1"
for cell, text in zip(table.rows[0].cells, ["Task", "Status", "Next step"]):
    cell.text = text
colors = {"Done": "1F7A5C", "In progress": "C48A00", "Not started": "9C0006"}
for task, status, nxt in memo["tasks"]:
    row = table.add_row().cells
    row[0].text, row[2].text = task, nxt
    run = row[1].paragraphs[0].add_run(status)
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(colors[status])

name = f"memo_{date.today():%Y-%m-%d}.docx"
doc.save(name)
print(name, "সেভ হয়েছে ✔")''',
)

DETAILS["python-pptx"] = lib(
    about=(
        "python-pptx দিয়ে PowerPoint (.pptx) স্লাইড কোড থেকে বানানো যায়: শিরোনাম, বুলেট, ছবি, "
        "টেবিল, এমনকি PowerPoint-এর নিজস্ব চার্ট। প্রতি মাসের একই রিপোর্ট অটো বানাতে দারুণ।"
    ),
    install="pip install python-pptx",
    example='''from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])      # Title slide
slide.shapes.title.text = "Hello PowerPoint"
slide.placeholders[1].text = "Made with Python"

slide = prs.slides.add_slide(prs.slide_layouts[1])      # Title + content
slide.shapes.title.text = "Why Python?"
body = slide.placeholders[1].text_frame
body.text = "Easy to learn"
body.add_paragraph().text = "Huge library collection"
body.add_paragraph().text = "Automates boring work"

prs.save("hello.pptx")
print("hello.pptx সেভ হয়েছে ✔")''',
    project_title="মাসিক climate update slide deck",
    project_about=(
        "মাসের আবহাওয়ার ডেটা দিয়ে ৩ স্লাইডের PowerPoint বানায়: শিরোনাম, মূল তথ্যের বুলেট, "
        "আর স্টেশনভিত্তিক বৃষ্টির PowerPoint চার্ট (যেটা পরে PowerPoint-এই এডিট করা যায়)।"
    ),
    project_code='''from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt

month = "June 2026"
stations = {"Dhaka": 330, "Sylhet": 820, "Chattogram": 610, "Rajshahi": 250}
highlights = [
    f"Wettest station: {max(stations, key=stations.get)} ({max(stations.values())} mm)",
    f"Driest station: {min(stations, key=stations.get)} ({min(stations.values())} mm)",
    f"Average rainfall: {sum(stations.values()) / len(stations):.0f} mm",
]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)   # 16:9

s = prs.slides.add_slide(prs.slide_layouts[0])
s.shapes.title.text = "Climate Update"
s.placeholders[1].text = month

s = prs.slides.add_slide(prs.slide_layouts[1])
s.shapes.title.text = "Key points"
tf = s.placeholders[1].text_frame
tf.text = highlights[0]
for h in highlights[1:]:
    tf.add_paragraph().text = h
for p in tf.paragraphs:
    p.font.size = Pt(28)

s = prs.slides.add_slide(prs.slide_layouts[5])                    # Title only
s.shapes.title.text = "Rainfall by station (mm)"
data = CategoryChartData()
data.categories = list(stations)
data.add_series("Rainfall", list(stations.values()))
chart = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                           Inches(1), Inches(1.6), Inches(11.3), Inches(5.4), data).chart
chart.has_legend = False
chart.plots[0].has_data_labels = True

prs.save("climate_update.pptx")
print(f"{len(prs.slides)} স্লাইডের climate_update.pptx সেভ হয়েছে ✔")''',
)

DETAILS["pypdfium2"] = lib(
    about=(
        "pypdfium2 হলো Google Chrome-এর PDF ইঞ্জিন (PDFium)-এর পাইথন সংস্করণ। PDF-এর পৃষ্ঠাকে "
        "খুব দ্রুত ও নিখুঁতভাবে ছবিতে (PNG/JPG) রূপান্তর করে, লেখাও বের করতে পারে।"
    ),
    install="pip install pypdfium2",
    example='''import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")
print("মোট পৃষ্ঠা:", len(pdf))

page = pdf[0]
image = page.render(scale=2).to_pil()     # scale=2 মানে ২ গুণ রেজোলিউশন
image.save("page1.png")
print("page1.png সেভ হয়েছে ✔", image.size)

text = page.get_textpage().get_text_range()
print("লেখা:", text.strip())''',
    project_title="বড় PDF archive-এর thumbnail builder",
    project_about=(
        "একটা PDF-এর সব পৃষ্ঠার ছোট ছবি (thumbnail) বানিয়ে একটা গ্রিডে সাজিয়ে একটাই "
        "contact sheet ছবি তৈরি করে, যাতে এক নজরে পুরো ডকুমেন্ট দেখা যায়।"
    ),
    project_code='''import math
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

PDF = "document.pdf"
THUMB_W, COLS, GAP = 220, 4, 16

pdf = pdfium.PdfDocument(PDF)
thumbs = []
for i in range(len(pdf)):
    page = pdf[i]
    scale = THUMB_W / page.get_width()
    img = page.render(scale=scale).to_pil().convert("RGB")
    thumbs.append(img)
    print(f"পৃষ্ঠা {i + 1} রেন্ডার হলো")

thumb_h = max(t.height for t in thumbs)
rows = math.ceil(len(thumbs) / COLS)
sheet = Image.new("RGB", (COLS * (THUMB_W + GAP) + GAP,
                          rows * (thumb_h + GAP + 20) + GAP), "#eeeeee")
draw = ImageDraw.Draw(sheet)
for i, t in enumerate(thumbs):
    x = GAP + (i % COLS) * (THUMB_W + GAP)
    y = GAP + (i // COLS) * (thumb_h + GAP + 20)
    sheet.paste(t, (x, y))
    draw.text((x, y + t.height + 4), f"Page {i + 1}", fill="black")

sheet.save("thumbnails.png")
print(f"{len(thumbs)} পৃষ্ঠার thumbnails.png সেভ হয়েছে ✔")''',
)

DETAILS["pytesseract"] = lib(
    about=(
        "pytesseract হলো Tesseract OCR-এর পাইথন সংযোগ: ছবি বা স্ক্যান করা কাগজ থেকে লেখা পড়ে "
        "টেক্সটে রূপান্তর করে। বাংলাও পারে, তার জন্য Tesseract-এর 'ben' ভাষা ফাইল লাগে।"
    ),
    install=("pip install pytesseract pillow\n"
             "# এছাড়া Tesseract প্রোগ্রামটা আলাদা ইনস্টল করতে হবে:\n"
             "# Windows: github.com/UB-Mannheim/tesseract/wiki\n"
             "# Ubuntu:  sudo apt install tesseract-ocr tesseract-ocr-ben"),
    example='''import pytesseract
from PIL import Image

img = Image.open("scan.png")
text = pytesseract.image_to_string(img, lang="eng")   # বাংলার জন্য lang="ben"
print(text)''',
    project_title="স্ক্যান করা প্রশ্নপত্রের plaintext সংস্করণ",
    project_about=(
        "স্ক্যান করা প্রশ্নপত্রের ছবি আগে পরিষ্কার করে (সাদা-কালো, বড় করা), তারপর OCR চালিয়ে "
        "লেখা বের করে, কোন শব্দ কতটা নিশ্চিতভাবে পড়া গেছে দেখায় আর .txt ফাইলে সেভ করে।"
    ),
    project_code='''import pytesseract
from PIL import Image, ImageOps

SRC = "scan.png"
LANG = "eng"          # বাংলা প্রশ্নপত্র হলে "ben", দুটোই হলে "ben+eng"

img = Image.open(SRC)
img = ImageOps.grayscale(img)
img = img.resize((img.width * 2, img.height * 2))       # ছোট লেখা বড় করা
img = img.point(lambda p: 255 if p > 150 else 0)         # শুধু সাদা-কালো

text = pytesseract.image_to_string(img, lang=LANG)
data = pytesseract.image_to_data(img, lang=LANG, output_type=pytesseract.Output.DICT)
conf = [float(c) for c, w in zip(data["conf"], data["text"]) if w.strip() and float(c) >= 0]

out = SRC.rsplit(".", 1)[0] + ".txt"
with open(out, "w", encoding="utf-8") as f:
    f.write(text)

print(text.strip())
print("-" * 40)
print(f"শব্দ: {len(conf)} | গড় নিশ্চয়তা: {sum(conf) / len(conf):.0f}%")
low = [w for w, c in zip(data["text"], data["conf"]) if w.strip() and 0 <= float(c) < 60]
if low:
    print("যেসব শব্দ আবার দেখা দরকার:", ", ".join(low))
print(out, "সেভ হয়েছে ✔")''',
)


# ==================================================================
# ব্যাচ ১ঘ: গ্রাফ, বিজ্ঞান, সিস্টেম, টেস্টিং, নিরাপত্তা, CLI, লেখা, async
# ==================================================================

DETAILS["networkx"] = lib(
    about=(
        "NetworkX দিয়ে নেটওয়ার্ক বা গ্রাফ (বিন্দু আর তাদের সংযোগ) নিয়ে কাজ করা যায়: সবচেয়ে "
        "ছোট পথ খোঁজা, কোন বিন্দু সবচেয়ে গুরুত্বপূর্ণ, কোন অংশ বিচ্ছিন্ন, এসব হিসাব।"
    ),
    install="pip install networkx",
    example='''import networkx as nx

G = nx.Graph()
G.add_edges_from([("Rahim", "Karim"), ("Karim", "Sumi"),
                  ("Sumi", "Riya"), ("Rahim", "Riya"), ("Riya", "Tanvir")])

print("বন্ধুর সংখ্যা:", dict(G.degree()))
print("Rahim → Tanvir পথ:", nx.shortest_path(G, "Rahim", "Tanvir"))
print("সবচেয়ে বেশি সংযুক্ত:", max(G.degree, key=lambda x: x[1]))''',
    project_title="ক্যাম্পাস walkway connectivity model",
    project_about=(
        "ক্যাম্পাসের ভবনগুলোকে বিন্দু আর হাঁটার পথকে (দূরত্বসহ) সংযোগ ধরে সবচেয়ে ছোট পথ খোঁজে, "
        "কোন জায়গা দিয়ে সবচেয়ে বেশি মানুষ যায় বের করে, আর একটা পথ বন্ধ হলে কী হয় দেখায়।"
    ),
    project_code='''import networkx as nx

paths = [   # (থেকে, পর্যন্ত, দূরত্ব মিটার)
    ("Gate", "Library", 120), ("Gate", "Admin", 90), ("Admin", "Cafeteria", 60),
    ("Library", "Cafeteria", 70), ("Library", "Science", 150),
    ("Cafeteria", "Hall", 110), ("Science", "Hall", 80), ("Hall", "Gym", 140),
    ("Science", "Lab", 40),
]

G = nx.Graph()
G.add_weighted_edges_from(paths, weight="m")

route = nx.shortest_path(G, "Gate", "Lab", weight="m")
dist = nx.shortest_path_length(G, "Gate", "Lab", weight="m")
print("Gate → Lab:", " → ".join(route), f"({dist} m)")

hub = nx.betweenness_centrality(G, weight="m")
print("\\nসবচেয়ে ব্যস্ত মোড় (betweenness):")
for place, score in sorted(hub.items(), key=lambda x: -x[1])[:3]:
    print(f"  {place:10} {score:.2f}")

cut = nx.bridges(G)
print("\\nযে পথ বন্ধ হলে ক্যাম্পাস ভাগ হয়ে যাবে:", list(cut))

G.remove_edge("Library", "Science")
dist2 = nx.shortest_path_length(G, "Gate", "Lab", weight="m")
print(f"Library–Science পথ বন্ধ হলে Gate → Lab: {dist2} m (+{dist2 - dist} m)")''',
)

DETAILS["scipy"] = lib(
    about=(
        "SciPy হলো NumPy-র উপর বানানো বৈজ্ঞানিক হিসাবের বড় সংগ্রহ: সমীকরণ সমাধান, "
        "সর্বোচ্চ-সর্বনিম্ন খোঁজা (optimization), integration, signal ফিল্টার, পরিসংখ্যান টেস্ট।"
    ),
    install="pip install scipy",
    example='''import numpy as np
from scipy import integrate, optimize, stats

# ∫ x² dx, 0 থেকে 3
area, _ = integrate.quad(lambda x: x**2, 0, 3)
print("Integral:", area)

# f(x) = (x-2)² + 1 এর সর্বনিম্ন বিন্দু
res = optimize.minimize_scalar(lambda x: (x - 2)**2 + 1)
print("Minimum at x =", round(res.x, 4))

# দুই দলের নম্বরে কি আসল পার্থক্য আছে? (t-test)
a = [72, 75, 78, 80, 69, 74]
b = [81, 85, 79, 88, 84, 86]
t, p = stats.ttest_ind(a, b)
print(f"p-value = {p:.4f}", "→ পার্থক্য আছে" if p < 0.05 else "→ পার্থক্য নেই")''',
    project_title="Noise filter দিয়ে নদীর পানি মাপের signal পরিষ্কার",
    project_about=(
        "নদীর পানির উচ্চতার সেন্সর রিডিংয়ে প্রচুর noise থাকে। Butterworth low-pass ফিল্টার "
        "দিয়ে সেটা পরিষ্কার করে, সর্বোচ্চ জোয়ারের সময় খুঁজে বের করে আর আগে-পরের গ্রাফ সেভ করে।"
    ),
    project_code='''import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# নমুনা: ৪৮ ঘণ্টা, প্রতি ৫ মিনিটে এক রিডিং (জোয়ার-ভাটা + noise)
fs = 12                                   # ঘণ্টায় ১২টা রিডিং
t = np.arange(0, 48, 1 / fs)
true_level = 3 + 1.2 * np.sin(2 * np.pi * t / 12.4) + 0.02 * t
rng = np.random.default_rng(3)
raw = true_level + rng.normal(0, 0.25, t.size)
raw[rng.integers(0, t.size, 8)] += 1.5    # কিছু ভুল spike

despiked = signal.medfilt(raw, kernel_size=5)            # spike সরানো
b, a = signal.butter(N=4, Wn=0.5, btype="low", fs=fs)     # ২ ঘণ্টার কম তরঙ্গ বাদ
clean = signal.filtfilt(b, a, despiked)

peaks, _ = signal.find_peaks(clean, distance=fs * 10)
print("জোয়ারের সর্বোচ্চ সময় (ঘণ্টা):", np.round(t[peaks], 1))
print(f"noise আগে: {np.std(raw - true_level):.3f} m, "
      f"পরে: {np.std(clean - true_level):.3f} m")

plt.figure(figsize=(10, 4))
plt.plot(t, raw, lw=0.6, alpha=0.5, label="raw sensor")
plt.plot(t, clean, lw=2, label="filtered")
plt.plot(t[peaks], clean[peaks], "rv", label="high tide")
plt.xlabel("hours"); plt.ylabel("water level (m)"); plt.legend()
plt.tight_layout(); plt.savefig("river_level.png", dpi=150)
print("river_level.png সেভ হয়েছে ✔")''',
)

DETAILS["psutil"] = lib(
    about=(
        "psutil দিয়ে কম্পিউটারের CPU, RAM, ডিস্ক, নেটওয়ার্ক ব্যবহার আর কোন প্রোগ্রাম চলছে "
        "সব তথ্য পাওয়া যায়। Windows, Mac, Linux সবখানে একই কোড চলে।"
    ),
    install="pip install psutil",
    example='''import psutil

print("CPU core:", psutil.cpu_count())
print("CPU ব্যবহার:", psutil.cpu_percent(interval=1), "%")

mem = psutil.virtual_memory()
print(f"RAM: {mem.used / 1e9:.1f} / {mem.total / 1e9:.1f} GB ({mem.percent}%)")

disk = psutil.disk_usage("/")
print(f"Disk: {disk.percent}% ভরা")''',
    project_title="নিজের workstation-এর resource monitor",
    project_about=(
        "কয়েক সেকেন্ড ধরে প্রতি সেকেন্ডে CPU ও RAM ব্যবহার মাপে, টার্মিনালে ছোট বার দেখায়, "
        "সবচেয়ে বেশি RAM খাওয়া ৫টা প্রোগ্রাম বলে আর সব রিডিং CSV-তে সেভ করে।"
    ),
    project_code='''import csv
import time
from datetime import datetime
import psutil

SECONDS = 5
ALERT_CPU = 80

def bar(pct, width=20):
    filled = int(pct / 100 * width)
    return "█" * filled + "·" * (width - filled)

log = []
print("সময়      CPU                         RAM")
for _ in range(SECONDS):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    now = datetime.now().strftime("%H:%M:%S")
    log.append({"time": now, "cpu": cpu, "ram": ram})
    warn = "  ⚠ CPU বেশি!" if cpu > ALERT_CPU else ""
    print(f"{now}  {bar(cpu)} {cpu:5.1f}%  {bar(ram)} {ram:5.1f}%{warn}")

with open("resource_log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["time", "cpu", "ram"])
    w.writeheader()
    w.writerows(log)

procs = []
for p in psutil.process_iter(["pid", "name", "memory_info"]):
    if p.info["memory_info"]:
        procs.append((p.info["memory_info"].rss, p.info["pid"], p.info["name"]))
print("\\nসবচেয়ে বেশি RAM ব্যবহারকারী:")
for rss, pid, name in sorted(procs, reverse=True)[:5]:
    print(f"  {name:25} pid={pid:<7} {rss / 1e6:7.1f} MB")
print("resource_log.csv সেভ হয়েছে ✔")''',
)

DETAILS["pytest"] = lib(
    about=(
        "pytest দিয়ে খুব সহজে কোডের টেস্ট লেখা যায়: test_ দিয়ে শুরু হওয়া ফাংশনে শুধু assert লিখলেই "
        "হয়। কোড বদলানোর পর পুরোনো কিছু ভেঙেছে কিনা এক কমান্ডে জানা যায়।"
    ),
    install="pip install pytest",
    example='''# ফাইলের নাম দাও test_math.py, তারপর টার্মিনালে লেখো: pytest
import pytest

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("শূন্য দিয়ে ভাগ করা যায় না")
    return a / b

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 4) == 2.5

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)''',
    project_title="GIS coordinate converter-এর regression suite",
    project_about=(
        "দশমিক ডিগ্রি (23.8103) ↔ ডিগ্রি-মিনিট-সেকেন্ড (23°48'37\") রূপান্তরের ফাংশন আর তার "
        "টেস্ট। parametrize দিয়ে অনেক শহরের মান একসাথে পরীক্ষা হয়, ভুল ইনপুটও যাচাই হয়।"
    ),
    project_code='''# ফাইলের নাম দাও test_coords.py, তারপর চালাও: pytest -v
import pytest

def to_dms(deg: float) -> tuple[int, int, float]:
    if not -180 <= deg <= 180:
        raise ValueError("ডিগ্রি -180 থেকে 180 এর মধ্যে হতে হবে")
    sign = -1 if deg < 0 else 1
    deg = abs(deg)
    d = int(deg)
    m = int((deg - d) * 60)
    s = round((deg - d - m / 60) * 3600, 1)
    if s == 60.0:
        m, s = m + 1, 0.0
    return sign * d, m, s

def to_decimal(d: int, m: int, s: float) -> float:
    if not (0 <= m < 60 and 0 <= s < 60):
        raise ValueError("মিনিট ও সেকেন্ড 0–59 হতে হবে")
    sign = -1 if d < 0 else 1
    return round(sign * (abs(d) + m / 60 + s / 3600), 6)

# ---------------- টেস্ট ----------------
@pytest.mark.parametrize("city, deg, dms", [
    ("Dhaka",      23.8103, (23, 48, 37.1)),
    ("Sylhet",     24.8949, (24, 53, 41.6)),
    ("Equator",     0.0,    (0, 0, 0.0)),
    ("Buenos Aires", -34.6037, (-34, 36, 13.3)),
])
def test_to_dms(city, deg, dms):
    assert to_dms(deg) == dms

@pytest.mark.parametrize("deg", [23.8103, 90.4125, -34.6037, 0.5])
def test_round_trip(deg):
    assert to_decimal(*to_dms(deg)) == pytest.approx(deg, abs=1e-4)

@pytest.mark.parametrize("bad", [200, -181])
def test_out_of_range(bad):
    with pytest.raises(ValueError):
        to_dms(bad)

def test_bad_minutes():
    with pytest.raises(ValueError):
        to_decimal(23, 75, 0)''',
)

DETAILS["mypy"] = lib(
    about=(
        "mypy কোড না চালিয়েই type-এর ভুল ধরে। ফাংশনে type hint (যেমন age: int) লিখলে mypy "
        "দেখে কোথাও ভুল টাইপ পাঠানো হচ্ছে কিনা। বড় প্রজেক্টে বাগ আগেভাগে ধরা পড়ে।"
    ),
    install="pip install mypy",
    example='''# ফাইলের নাম দাও app.py, তারপর টার্মিনালে: mypy app.py

def greet(name: str, times: int) -> str:
    return ("Hello " + name + "! ") * times

print(greet("Rahim", 2))      # ঠিক আছে
print(greet("Karim", "3"))    # mypy ভুল ধরবে: "3" হলো str, int লাগবে

# mypy-র আউটপুট:
# app.py:7: error: Argument 2 to "greet" has incompatible type "str"; expected "int"''',
    project_title="API model-এ string ও integer type mismatch ধরা",
    project_about=(
        "একটা ছোট অর্ডার API-র data model-এ TypedDict ও dataclass দিয়ে টাইপ লেখা আছে। কোডে "
        "ইচ্ছা করে দুটো ভুল রাখা হয়েছে (দাম string, id ভুল টাইপ); mypy চালালে দুটোই ধরা পড়ে।"
    ),
    project_code='''# ফাইলের নাম দাও orders.py, তারপর: mypy --strict orders.py
from dataclasses import dataclass
from typing import TypedDict

class OrderIn(TypedDict):          # API তে যা আসে
    product_id: int
    quantity: int

@dataclass
class Product:
    id: int
    name: str
    price: float

CATALOG: dict[int, Product] = {
    1: Product(1, "Notebook", 45.0),
    2: Product(2, "Pen", "10"),            # ✘ ভুল ১: দাম string
}

def total(order: OrderIn) -> float:
    product = CATALOG[order["product_id"]]
    return product.price * order["quantity"]

def find(product_id: int) -> Product | None:
    return CATALOG.get(product_id)

print(total({"product_id": 1, "quantity": 3}))
print(find("2"))                            # ✘ ভুল ২: id হিসেবে string

# mypy-র আউটপুট মোটামুটি এমন হবে:
# orders.py:17: error: Argument 3 to "Product" has incompatible type "str"; expected "float"
# orders.py:28: error: Argument 1 to "find" has incompatible type "str"; expected "int"''',
)

DETAILS["cryptography"] = lib(
    about=(
        "cryptography হলো পাইথনের নির্ভরযোগ্য এনক্রিপশন লাইব্রেরি। Fernet দিয়ে সহজে ডেটা লক/আনলক "
        "করা যায়, আর digital signature দিয়ে প্রমাণ করা যায় ফাইলটা কেউ বদলায়নি।"
    ),
    install="pip install cryptography",
    example='''from cryptography.fernet import Fernet

key = Fernet.generate_key()          # এই key গোপন রাখতে হবে
f = Fernet(key)

secret = f.encrypt("আমার পাসওয়ার্ড: 1234".encode())
print("এনক্রিপ্টেড:", secret[:40], "...")

plain = f.decrypt(secret).decode()
print("ডিক্রিপ্টেড:", plain)''',
    project_title="লোকাল নথি encrypt এবং signature যাচাইয়ের টুল",
    project_about=(
        "একটা নথি পাসওয়ার্ড দিয়ে এনক্রিপ্ট করে (.enc), সাথে Ed25519 digital signature বানায়। "
        "পরে ডিক্রিপ্ট করে signature যাচাই করে, আর কেউ ফাইল বদলালে সেটা ধরে ফেলে।"
    ),
    project_code='''import base64
import os
from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

doc = Path("notes.txt")
doc.write_text("গবেষণার গোপন ফলাফল: নমুনা ৪২-এ সাফল্য।", encoding="utf-8")
password = "my-strong-password"

# ---- এনক্রিপ্ট + সাইন ----
salt = os.urandom(16)
data = doc.read_bytes()
token = Fernet(key_from_password(password, salt)).encrypt(data)
Path("notes.enc").write_bytes(salt + token)

signer = Ed25519PrivateKey.generate()
public_key = signer.public_key()
signature = signer.sign(data)
print("notes.enc ও signature তৈরি ✔")

# ---- ডিক্রিপ্ট + যাচাই ----
def open_and_verify(enc_path: str, pw: str, sig: bytes) -> str:
    raw = Path(enc_path).read_bytes()
    plain = Fernet(key_from_password(pw, raw[:16])).decrypt(raw[16:])
    public_key.verify(sig, plain)                  # বদলানো হলে error
    return plain.decode("utf-8")

print("খোলা হলো:", open_and_verify("notes.enc", password, signature))

tampered = bytearray(signature)
tampered[0] ^= 1
try:
    open_and_verify("notes.enc", password, bytes(tampered))
except InvalidSignature:
    print("✘ ভুল signature ধরা পড়েছে, নথি বিশ্বাসযোগ্য নয়")''',
)

DETAILS["pyjwt"] = lib(
    about=(
        "PyJWT দিয়ে JWT (JSON Web Token) বানানো ও যাচাই করা যায়। লগইনের পর ইউজারকে একটা সাইন "
        "করা token দেওয়া হয়, পরের রিকোয়েস্টে সেটা দেখে বোঝা যায় ইউজার কে আর token এখনো বৈধ কিনা।"
    ),
    install="pip install pyjwt",
    example='''import jwt

SECRET = "change-this-secret-at-least-32-bytes-long"   # আসল কাজে লম্বা গোপন key

token = jwt.encode({"user": "rahim", "role": "admin"}, SECRET, algorithm="HS256")
print("Token:", token)

data = jwt.decode(token, SECRET, algorithms=["HS256"])
print("ভেতরের তথ্য:", data)''',
    project_title="নিজের API-তে সঠিক issuer ও expiry যাচাই",
    project_about=(
        "API-র জন্য token বানায় যাতে issuer, audience আর মেয়াদ (exp) থাকে। তারপর যাচাই করে "
        "দেখায়: ঠিক token পাস করে, মেয়াদ শেষ বা অন্য issuer-এর token বাতিল হয়।"
    ),
    project_code='''from datetime import datetime, timedelta, timezone
import jwt

SECRET = "change-this-secret-at-least-32-bytes-long"
ISSUER = "https://api.my-site.com"
AUDIENCE = "my-mobile-app"

def make_token(user: str, minutes: int, issuer: str = ISSUER) -> str:
    now = datetime.now(timezone.utc)
    claims = {"sub": user, "iss": issuer, "aud": AUDIENCE,
              "iat": now, "exp": now + timedelta(minutes=minutes)}
    return jwt.encode(claims, SECRET, algorithm="HS256")

def check(token: str) -> str:
    try:
        c = jwt.decode(token, SECRET, algorithms=["HS256"],
                       issuer=ISSUER, audience=AUDIENCE,
                       options={"require": ["exp", "iss", "aud", "sub"]})
        return f"✔ বৈধ: ইউজার {c['sub']}"
    except jwt.ExpiredSignatureError:
        return "✘ মেয়াদ শেষ"
    except jwt.InvalidIssuerError:
        return "✘ অচেনা issuer"
    except jwt.InvalidAudienceError:
        return "✘ ভুল audience"
    except jwt.InvalidTokenError as e:
        return f"✘ অবৈধ token: {e}"

tests = {
    "ঠিক token":        make_token("rahim", 15),
    "মেয়াদ শেষ":        make_token("rahim", -1),
    "অন্য issuer":      make_token("rahim", 15, issuer="https://evil.example"),
    "বদলানো token":     make_token("rahim", 15)[:-3] + "abc",
}
for label, tok in tests.items():
    print(f"{label:14} → {check(tok)}")''',
)

DETAILS["click"] = lib(
    about=(
        "Click দিয়ে সুন্দর কমান্ড-লাইন প্রোগ্রাম (CLI) বানানো যায়: option, argument, "
        "subcommand, --help পেজ সব নিজে থেকেই তৈরি হয়। টার্মিনাল টুল বানাতে খুব জনপ্রিয়।"
    ),
    install="pip install click",
    example='''# hello.py   চালাও: python hello.py --name Rahim --count 3
import click

@click.command()
@click.option("--name", prompt="তোমার নাম", help="কাকে হ্যালো বলবে")
@click.option("--count", default=1, help="কতবার বলবে")
def hello(name, count):
    """একটা ছোট হ্যালো প্রোগ্রাম।"""
    for _ in range(count):
        click.secho(f"Hello, {name}!", fg="green")

if __name__ == "__main__":
    hello()''',
    project_title="ফাইল format converter-এর command suite",
    project_about=(
        "একটাই টুলে কয়েকটা subcommand: CSV → JSON, JSON → CSV আর ফাইলের তথ্য দেখা। "
        "প্রতিটা কমান্ডের নিজস্ব option আর --help আছে।"
    ),
    project_code='''# convert.py
#   python convert.py csv2json data.csv -o data.json --pretty
#   python convert.py json2csv data.json -o back.csv
#   python convert.py info data.csv
import csv
import json
from pathlib import Path
import click

@click.group()
def cli():
    """ফাইল রূপান্তরের ছোট টুলবক্স।"""

@cli.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--out", type=click.Path(), help="আউটপুট ফাইল")
@click.option("--pretty", is_flag=True, help="সুন্দর করে সাজানো JSON")
def csv2json(src, out, pretty):
    """CSV থেকে JSON।"""
    with open(src, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = out or Path(src).with_suffix(".json")
    Path(out).write_text(json.dumps(rows, ensure_ascii=False, indent=2 if pretty else None),
                         encoding="utf-8")
    click.secho(f"✔ {len(rows)} সারি → {out}", fg="green")

@cli.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--out", type=click.Path(), help="আউটপুট ফাইল")
def json2csv(src, out):
    """JSON (list of objects) থেকে CSV।"""
    rows = json.loads(Path(src).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise click.ClickException("JSON-এ object-এর list থাকতে হবে")
    out = out or Path(src).with_suffix(".csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    click.secho(f"✔ {len(rows)} সারি → {out}", fg="green")

@cli.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False))
def info(src):
    """ফাইলের মাপ ও সারির সংখ্যা।"""
    p = Path(src)
    lines = p.read_text(encoding="utf-8").count("\\n")
    click.echo(f"{p.name}: {p.stat().st_size} bytes, {lines} লাইন")

if __name__ == "__main__":
    cli()''',
)

DETAILS["pygments"] = lib(
    about=(
        "Pygments কোডকে রঙিন (syntax highlight) করে। ৫০০+ প্রোগ্রামিং ভাষা চেনে, আর আউটপুট দিতে "
        "পারে HTML, টার্মিনাল, ছবি বা LaTeX-এ। ব্লগ, ডকুমেন্টেশন সাইটে খুব ব্যবহৃত।"
    ),
    install="pip install pygments",
    example='''from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import PythonLexer

code = """def square(n):
    # সংখ্যার বর্গ
    return n * n

print(square(7))
"""

print(highlight(code, PythonLexer(), TerminalFormatter()))''',
    project_title="Library Atlas-এর highlighted example blocks",
    project_about=(
        "কয়েকটা কোড উদাহরণ (ভিন্ন ভিন্ন ভাষায়) নিয়ে লাইন নম্বরসহ রঙিন HTML পেজ বানায়, "
        "যেটা ব্রাউজারে খুললেই সুন্দর কোড ব্লক দেখা যায়।"
    ),
    project_code='''from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

examples = [
    ("numpy", "python", "import numpy as np\\na = np.arange(5)\\nprint(a * 2)"),
    ("D3.js", "javascript", "d3.select('body')\\n  .append('p')\\n  .text('Hello D3');"),
    ("SQL", "sql", "SELECT name, AVG(marks)\\nFROM students\\nGROUP BY name;"),
]

fmt = HtmlFormatter(style="monokai", linenos="table", cssclass="code")
blocks = []
for title, lang, code in examples:
    html = highlight(code, get_lexer_by_name(lang), fmt)
    blocks.append(f"<h2>{title} <small>({lang})</small></h2>{html}")

page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Highlighted examples</title>
<style>
body {{ font-family: system-ui; max-width: 760px; margin: 40px auto; background: #fafafa; }}
.code {{ border-radius: 8px; overflow: auto; }}
{fmt.get_style_defs(".code")}
</style></head><body><h1>Code examples</h1>{"".join(blocks)}</body></html>"""

with open("examples.html", "w", encoding="utf-8") as f:
    f.write(page)
print(f"{len(blocks)}টা ব্লকসহ examples.html সেভ হয়েছে ✔")''',
)

DETAILS["markdown-it-py"] = lib(
    about=(
        "markdown-it-py হলো Markdown লেখাকে HTML-এ রূপান্তরের নির্ভুল (CommonMark) লাইব্রেরি। "
        "নিজের নিয়ম বা plugin যোগ করা যায়, তাই ডকুমেন্টেশন টুল বানাতে কাজের।"
    ),
    install="pip install markdown-it-py",
    example='''from markdown_it import MarkdownIt

md = MarkdownIt()
text = """# শিরোনাম

এটা **বোল্ড**, এটা *ইটালিক*।

- আইটেম ১
- আইটেম ২
"""
print(md.render(text))''',
    project_title="নিজস্ব Markdown reference site-এর renderer",
    project_about=(
        "Markdown থেকে HTML বানায়, সাথে নিজস্ব নিয়ম: বাইরের লিংক নতুন ট্যাবে খোলে, প্রতিটা "
        "শিরোনামে id বসে আর সেই id দিয়ে স্বয়ংক্রিয় সূচিপত্র (table of contents) তৈরি হয়।"
    ),
    project_code='''import re
from markdown_it import MarkdownIt

md = MarkdownIt("commonmark").enable("table")
toc = []

def slug(text):
    return re.sub(r"[^\\w]+", "-", text.lower()).strip("-")

def heading_open(self, tokens, idx, options, env):
    token = tokens[idx]
    title = tokens[idx + 1].content
    token.attrSet("id", slug(title))
    toc.append((int(token.tag[1]), title))
    return self.renderToken(tokens, idx, options, env)

def link_open(self, tokens, idx, options, env):
    href = tokens[idx].attrGet("href") or ""
    if href.startswith("http"):
        tokens[idx].attrSet("target", "_blank")
        tokens[idx].attrSet("rel", "noopener")
    return self.renderToken(tokens, idx, options, env)

md.add_render_rule("heading_open", heading_open)
md.add_render_rule("link_open", link_open)

source = """# requests
Install with `pip install requests`.

## Basic usage
See the [official docs](https://requests.readthedocs.io).

## Status codes
| Code | Meaning |
|------|---------|
| 200  | OK      |
| 404  | Not found |
"""

body = md.render(source)
nav = "".join(f'<li style="margin-left:{(lvl - 1) * 16}px"><a href="#{slug(t)}">{t}</a></li>'
              for lvl, t in toc)
page = f"<html><meta charset=utf-8><body><nav><ul>{nav}</ul></nav>{body}</body></html>"
open("reference.html", "w", encoding="utf-8").write(page)

print(body)
print("সূচিপত্র:", [t for _, t in toc])
print("reference.html সেভ হয়েছে ✔")''',
)

DETAILS["mistune"] = lib(
    about=(
        "mistune হলো খুব দ্রুত Markdown পার্সার। এক লাইনে Markdown থেকে HTML হয়, আবার "
        "Markdown-কে গাছের মতো ডেটা (AST) হিসেবেও পাওয়া যায়।"
    ),
    install="pip install mistune",
    example='''import mistune

html = mistune.html("""
# আমার নোট
আজ **পাইথন** শিখলাম।

1. list
2. dict
""")
print(html)''',
    project_title="Notebook notes-এর lightweight HTML viewer",
    project_about=(
        "notes ফোল্ডারের সব .md ফাইল পড়ে একটা সুন্দর HTML পেজ বানায়, যেখানে বাঁ পাশে সব নোটের "
        "তালিকা আর ডানে প্রতিটা নোটের লেখা থাকে।"
    ),
    project_code='''from pathlib import Path
import mistune

NOTES = Path("notes")
render = mistune.create_markdown(plugins=["table", "strikethrough", "task_lists"])

sections, links = [], []
for f in sorted(NOTES.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    first = text.strip().splitlines()[0].lstrip("# ") if text.strip() else f.stem
    links.append(f'<a href="#{f.stem}">{first}</a>')
    sections.append(f'<section id="{f.stem}">{render(text)}</section>')

page = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>My notes</title>
<style>
body {{ margin: 0; display: flex; font-family: system-ui; }}
nav {{ width: 220px; padding: 20px; background: #1f2430; min-height: 100vh; }}
nav a {{ display: block; color: #cfd6e6; padding: 6px 0; text-decoration: none; }}
main {{ padding: 20px 40px; max-width: 760px; }}
section {{ border-bottom: 1px solid #ddd; padding-bottom: 20px; }}
code {{ background: #f1f1f1; padding: 2px 5px; border-radius: 4px; }}
</style></head><body>
<nav><h3 style="color:white">Notes</h3>{"".join(links)}</nav>
<main>{"".join(sections)}</main></body></html>"""

Path("notes.html").write_text(page, encoding="utf-8")
print(f"{len(sections)}টা নোট নিয়ে notes.html সেভ হয়েছে ✔")''',
)

DETAILS["anyio"] = lib(
    about=(
        "AnyIO দিয়ে async কোড লেখা যায় যা asyncio আর Trio দুই জায়গাতেই চলে। task group দিয়ে "
        "একসাথে অনেক কাজ চালানো, সময়সীমা দেওয়া আর বাতিল করা খুব নিরাপদ ও সহজ।"
    ),
    install="pip install anyio",
    example='''import anyio

async def worker(name, seconds):
    print(f"{name} শুরু")
    await anyio.sleep(seconds)
    print(f"{name} শেষ ({seconds}s)")

async def main():
    async with anyio.create_task_group() as tg:   # সব একসাথে চলে
        tg.start_soon(worker, "A", 1)
        tg.start_soon(worker, "B", 0.5)
        tg.start_soon(worker, "C", 0.8)
    print("সব কাজ শেষ")

anyio.run(main)''',
    project_title="Async backend বদলানো যায় এমন data fetcher",
    project_about=(
        "একসাথে অনেক স্টেশনের ডেটা আনে, কিন্তু একবারে সর্বোচ্চ ৩টা (CapacityLimiter), প্রতিটার "
        "সময়সীমা ১ সেকেন্ড; দেরি করলে বাদ। backend শুধু একটা লাইনে বদলানো যায় (asyncio/trio)।"
    ),
    project_code='''import random
import time
import anyio

STATIONS = ["Dhaka", "Sylhet", "Khulna", "Rajshahi", "Barishal", "Rangpur", "Cumilla"]
limit = anyio.CapacityLimiter(3)            # একসাথে সর্বোচ্চ ৩টা
results, timed_out = {}, []

async def fetch(station: str):
    # আসল প্রজেক্টে এখানে httpx.AsyncClient দিয়ে API কল হবে
    delay = random.uniform(0.2, 1.6)
    await anyio.sleep(delay)
    return round(random.uniform(25, 35), 1)

async def fetch_one(station: str):
    async with limit:
        with anyio.move_on_after(1.0) as scope:     # ১ সেকেন্ড সময়সীমা
            results[station] = await fetch(station)
        if scope.cancelled_caught:
            timed_out.append(station)

async def main():
    start = time.perf_counter()
    async with anyio.create_task_group() as tg:
        for s in STATIONS:
            tg.start_soon(fetch_one, s)
    took = time.perf_counter() - start
    for s, t in results.items():
        print(f"✔ {s:9} {t} °C")
    for s in timed_out:
        print(f"⏱ {s:9} সময় পার হয়ে গেছে")
    print(f"মোট সময়: {took:.1f}s (একটা একটা করে করলে অনেক বেশি লাগত)")

random.seed(4)
anyio.run(main, backend="asyncio")   # trio ইনস্টল থাকলে backend="trio"''',
)

DETAILS["joblib"] = lib(
    about=(
        "joblib দিয়ে একই কাজ কম্পিউটারের সব CPU core-এ ভাগ করে দ্রুত চালানো যায়, আর ভারী হিসাবের "
        "ফল ডিস্কে cache করে রাখা যায় যাতে পরের বার আবার হিসাব করতে না হয়। ML মডেল সেভ করতেও ব্যবহার হয়।"
    ),
    install="pip install joblib",
    example='''import time
from joblib import Parallel, delayed

def slow_square(n):
    time.sleep(0.2)          # ভারী কাজের ভান
    return n * n

start = time.time()
results = Parallel(n_jobs=4)(delayed(slow_square)(i) for i in range(8))
print(results)
print(f"সময়: {time.time() - start:.1f}s (একটা একটা করে লাগত ~1.6s)")''',
    project_title="Cross-validation trial parallel benchmark",
    project_about=(
        "কয়েকটা ML মডেল সেটিং cross-validation দিয়ে পরীক্ষা করে: একবার এক core-এ, একবার সব core-এ "
        "চালিয়ে সময় তুলনা করে, আর Memory cache থাকায় দ্বিতীয়বার চালালে সাথে সাথে ফল দেয়।"
    ),
    project_code='''import os
import time
from joblib import Memory, Parallel, delayed
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=1500, n_features=20, random_state=0)
settings = [(n, d) for n in (50, 100) for d in (4, 8, None)]

memory = Memory("cache_dir", verbose=0)

@memory.cache
def evaluate(n_trees, depth):
    model = RandomForestClassifier(n_estimators=n_trees, max_depth=depth,
                                   n_jobs=1, random_state=0)
    return cross_val_score(model, X, y, cv=5).mean()

def run(n_jobs):
    t = time.perf_counter()
    scores = Parallel(n_jobs=n_jobs)(delayed(evaluate.func)(n, d) for n, d in settings)
    return scores, time.perf_counter() - t

_, t1 = run(n_jobs=1)
scores, tall = run(n_jobs=-1)
print(f"১ core: {t1:.1f}s | সব core ({os.cpu_count()}টা): {tall:.1f}s")

for (n, d), s in sorted(zip(settings, scores), key=lambda x: -x[1]):
    print(f"  trees={n:3} depth={str(d):4} → accuracy {s:.3f}")

t = time.perf_counter()
[evaluate(n, d) for n, d in settings]          # প্রথমবার হিসাব + cache
first = time.perf_counter() - t
t = time.perf_counter()
[evaluate(n, d) for n, d in settings]          # দ্বিতীয়বার cache থেকে
print(f"cache ছাড়া: {first:.1f}s | cache থেকে: {time.perf_counter() - t:.3f}s")''',
)


# ==================================================================
# ব্যাচ ২: জনপ্রিয় লাইব্রেরি (AI, ওয়েব, ডেটা, CLI)
# ==================================================================

DETAILS["openai"] = lib(
    about=(
        "openai লাইব্রেরি দিয়ে পাইথন থেকে OpenAI-এর GPT মডেল ব্যবহার করা যায়: প্রশ্নের উত্তর, "
        "লেখা সারাংশ, অনুবাদ, কোড লেখা, ছবি বোঝা। platform.openai.com থেকে API key লাগে (টাকা লাগে)।"
    ),
    install="pip install openai\n# তারপর API key সেট করো:\n# Windows:  set OPENAI_API_KEY=sk-...\n# Mac/Linux: export OPENAI_API_KEY=sk-...",
    example='''from openai import OpenAI

client = OpenAI()          # OPENAI_API_KEY environment variable থেকে key নেয়

response = client.responses.create(
    model="gpt-4.1-mini",  # সর্বশেষ মডেলের নাম platform.openai.com/docs/models এ দেখে নাও
    input="পাইথন কী? দুই লাইনে বাংলায় বলো।",
)
print(response.output_text)''',
    project_title="বাংলা ক্লাস নোটের সারাংশ তৈরির অ্যাপ",
    project_about=(
        "notes ফোল্ডারের প্রতিটা ক্লাস নোট (.txt) পড়ে GPT দিয়ে বাংলায় মূল পয়েন্ট, কঠিন শব্দের "
        "মানে আর ৩টা অনুশীলনী প্রশ্ন বানায়, আর প্রতিটা নোটের পাশে _summary.md ফাইল সেভ করে।"
    ),
    project_code='''from pathlib import Path
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4.1-mini"

INSTRUCTIONS = """তুমি একজন যত্নশীল শিক্ষক। শিক্ষার্থীর ক্লাস নোট পড়ে বাংলায় লিখবে:
## মূল পয়েন্ট (৫টার বেশি নয়, বুলেটে)
## কঠিন শব্দ ও মানে
## অনুশীলনী প্রশ্ন (৩টা)
নোটে যা নেই তা বানিয়ে লিখবে না।"""

notes = sorted(Path("notes").glob("*.txt"))
if not notes:
    raise SystemExit("notes ফোল্ডারে .txt ফাইল রাখো")

for path in notes:
    text = path.read_text(encoding="utf-8")
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=f"ক্লাস নোট ({path.stem}):\\n\\n{text}",
    )
    out = path.with_name(path.stem + "_summary.md")
    out.write_text(f"# {path.stem}\\n\\n{response.output_text}", encoding="utf-8")
    print(f"✔ {path.name} → {out.name}")''',
)

DETAILS["anthropic"] = lib(
    about=(
        "anthropic লাইব্রেরি দিয়ে পাইথন থেকে Claude মডেল ব্যবহার করা যায়: লম্বা নথি পড়ে বিশ্লেষণ, "
        "প্রশ্নোত্তর, লেখা, কোড। console.anthropic.com থেকে API key লাগে (টাকা লাগে)।"
    ),
    install="pip install anthropic\n# তারপর API key সেট করো:\n# Windows:  set ANTHROPIC_API_KEY=sk-ant-...\n# Mac/Linux: export ANTHROPIC_API_KEY=sk-ant-...",
    example='''import anthropic

client = anthropic.Anthropic()     # ANTHROPIC_API_KEY থেকে key নেয়

message = client.messages.create(
    model="claude-sonnet-5-5",     # সর্বশেষ মডেলের নাম docs.claude.com এ দেখে নাও
    max_tokens=500,
    messages=[{"role": "user", "content": "পাইথনের list আর tuple-এর পার্থক্য বাংলায় বলো।"}],
)
print(message.content[0].text)''',
    project_title="গবেষণাপত্রের প্রশ্নোত্তর সহকারী",
    project_about=(
        "একটা গবেষণাপত্রের PDF পড়ে (pypdf দিয়ে) Claude-কে দেয়, তারপর টার্মিনালে প্রশ্ন করা যায়। "
        "Claude শুধু পেপার থেকে উত্তর দেয়, পৃষ্ঠা নম্বর বলে, আর আগের প্রশ্নগুলোও মনে রাখে।"
    ),
    project_code='''import anthropic
from pypdf import PdfReader

PDF = "paper.pdf"
client = anthropic.Anthropic()

reader = PdfReader(PDF)
paper = "\\n\\n".join(f"[Page {i}]\\n{p.extract_text()}"
                     for i, p in enumerate(reader.pages, start=1))

SYSTEM = f"""You help a student understand a research paper.
Answer ONLY from the paper below. Cite page numbers like (p. 3).
If the paper does not say, reply: "পেপারে এটা বলা নেই।"
Answer in the same language as the question.

<paper>
{paper}
</paper>"""

history = []
print(f"{PDF} লোড হলো ({len(reader.pages)} পৃষ্ঠা)। প্রশ্ন করো, বের হতে 'exit'।")
while True:
    q = input("\\nপ্রশ্ন: ").strip()
    if q.lower() in {"exit", "quit", ""}:
        break
    history.append({"role": "user", "content": q})
    reply = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=800,
        system=SYSTEM,
        messages=history,
    )
    answer = reply.content[0].text
    history.append({"role": "assistant", "content": answer})
    print("\\nউত্তর:", answer)''',
)

DETAILS["fastapi"] = lib(
    about=(
        "FastAPI দিয়ে খুব দ্রুত আধুনিক API বানানো যায়। ফাংশনে type hint লিখলেই ইনপুট যাচাই হয়, "
        "আর /docs ঠিকানায় নিজে থেকে একটা ইন্টারঅ্যাকটিভ ডকুমেন্টেশন পেজ তৈরি হয়ে যায়।"
    ),
    install='pip install "fastapi[standard]"',
    example='''# main.py   চালাও: fastapi dev main.py   তারপর খোলো http://127.0.0.1:8000/docs
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/square/{n}")
def square(n: int):                 # n সংখ্যা না হলে নিজে থেকেই error দেয়
    return {"n": n, "square": n * n}''',
    project_title="স্টেশনভেদে বৃষ্টির রেকর্ড ফেরত দেয় এমন REST API",
    project_about=(
        "আবহাওয়া স্টেশনের বৃষ্টির রেকর্ডের API: সব স্টেশন দেখা, একটা স্টেশনের রেকর্ড তারিখ দিয়ে "
        "ফিল্টার করা, নতুন রেকর্ড যোগ করা। ভুল ইনপুটে পরিষ্কার error, আর /docs-এ সব টেস্ট করা যায়।"
    ),
    project_code='''# main.py   চালাও: fastapi dev main.py   →  http://127.0.0.1:8000/docs
from datetime import date
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Rainfall API")

class Record(BaseModel):
    day: date
    rain_mm: float = Field(ge=0, le=1000)

RECORDS: dict[str, list[Record]] = {          # আসল প্রজেক্টে ডেটাবেস
    "dhaka": [Record(day=date(2026, 6, 1), rain_mm=12.5),
              Record(day=date(2026, 6, 2), rain_mm=40.0)],
    "sylhet": [Record(day=date(2026, 6, 1), rain_mm=88.2)],
}

@app.get("/stations")
def list_stations():
    return [{"station": s, "records": len(r),
             "total_mm": round(sum(x.rain_mm for x in r), 1)}
            for s, r in RECORDS.items()]

@app.get("/stations/{station}", response_model=list[Record])
def get_records(station: str,
                start: date | None = Query(None, description="এই তারিখ থেকে"),
                end: date | None = Query(None, description="এই তারিখ পর্যন্ত")):
    records = RECORDS.get(station.lower())
    if records is None:
        raise HTTPException(404, f"'{station}' নামে কোনো স্টেশন নেই")
    return [r for r in records
            if (start is None or r.day >= start) and (end is None or r.day <= end)]

@app.post("/stations/{station}", response_model=Record, status_code=201)
def add_record(station: str, record: Record):
    RECORDS.setdefault(station.lower(), []).append(record)
    return record''',
)

DETAILS["httpx"] = lib(
    about=(
        "httpx হলো requests-এর মতোই সহজ, কিন্তু আধুনিক HTTP লাইব্রেরি। এর বড় সুবিধা হলো async: "
        "একসাথে অনেকগুলো রিকোয়েস্ট পাঠানো যায়, তাই অনেক API থেকে ডেটা আনা অনেক দ্রুত হয়।"
    ),
    install="pip install httpx",
    example='''import httpx

r = httpx.get("https://api.github.com/repos/python/cpython", timeout=10)
r.raise_for_status()
repo = r.json()
print(repo["full_name"], "⭐", repo["stargazers_count"])''',
    project_title="একসঙ্গে কয়েকটি public sensor endpoint পর্যবেক্ষণ",
    project_about=(
        "কয়েকটা শহরের আবহাওয়া API একসাথে (async) কল করে, প্রতিটার উত্তর আসতে কত সময় লাগল, "
        "স্ট্যাটাস কোড আর বর্তমান তাপমাত্রা দেখায়; কোনোটা বন্ধ থাকলে বাকিগুলো থেমে থাকে না।"
    ),
    project_code='''import asyncio
import time
import httpx

URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {"Dhaka": (23.81, 90.41), "Sylhet": (24.89, 91.87),
          "Chattogram": (22.36, 91.78), "Rajshahi": (24.37, 88.60)}

async def check(client: httpx.AsyncClient, city: str, lat: float, lon: float):
    t = time.perf_counter()
    try:
        r = await client.get(URL, params={"latitude": lat, "longitude": lon,
                                          "current": "temperature_2m"})
        r.raise_for_status()
        temp = r.json()["current"]["temperature_2m"]
        return city, r.status_code, time.perf_counter() - t, f"{temp} °C"
    except httpx.HTTPError as e:
        return city, "ERR", time.perf_counter() - t, type(e).__name__

async def main():
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=10) as client:
        results = await asyncio.gather(*(check(client, c, *xy) for c, xy in CITIES.items()))
    print(f"{'City':12}{'Status':8}{'Time':>8}  Value")
    for city, status, took, value in results:
        print(f"{city:12}{str(status):8}{took:7.2f}s  {value}")
    print(f"মোট সময়: {time.perf_counter() - start:.2f}s (সব একসাথে চলেছে)")

asyncio.run(main())''',
)

DETAILS["sqlalchemy"] = lib(
    about=(
        "SQLAlchemy দিয়ে SQL ডেটাবেস (SQLite, PostgreSQL, MySQL) পাইথন class দিয়ে চালানো যায়। "
        "টেবিল = class, সারি = object। একই কোড প্রায় সব ডেটাবেসে চলে।"
    ),
    install="pip install sqlalchemy",
    example='''from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    marks: Mapped[int]

engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([Student(name="Rahim", marks=78), Student(name="Sumi", marks=92)])
    session.commit()
    for s in session.scalars(select(Student).where(Student.marks > 80)):
        print(s.name, s.marks)''',
    project_title="গ্রন্থাগারের বই ও ধার রেকর্ডের database layer",
    project_about=(
        "লাইব্রেরির বই, সদস্য আর ধারের রেকর্ড তিনটা সম্পর্কিত টেবিলে রাখে। বই ধার দেওয়া, ফেরত "
        "নেওয়া, কে কোন বই নিয়েছে আর কোন বইয়ের ফেরতের তারিখ পেরিয়ে গেছে সব কোয়েরি করা যায়।"
    ),
    project_code='''from datetime import date, timedelta
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    loans: Mapped[list["Loan"]] = relationship(back_populates="member")

class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    due: Mapped[date]
    returned: Mapped[bool] = mapped_column(default=False)
    book: Mapped[Book] = relationship(back_populates="loans")
    member: Mapped[Member] = relationship(back_populates="loans")

engine = create_engine("sqlite:///library.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def lend(session, book, member, days=14):
    busy = session.scalar(select(Loan).where(Loan.book_id == book.id, Loan.returned.is_(False)))
    if busy:
        raise ValueError(f"'{book.title}' এখন {busy.member.name}-এর কাছে")
    session.add(Loan(book=book, member=member, due=date.today() + timedelta(days=days)))

with Session(engine) as s:
    b1 = Book(title="Pather Panchali", author="Bibhutibhushan")
    b2 = Book(title="Gitanjali", author="Rabindranath")
    rahim, sumi = Member(name="Rahim"), Member(name="Sumi")
    s.add_all([b1, b2, rahim, sumi])
    s.flush()

    lend(s, b1, rahim, days=-3)          # ইতিমধ্যেই মেয়াদ পার (ডেমোর জন্য)
    lend(s, b2, sumi)
    try:
        lend(s, b1, sumi)
    except ValueError as e:
        print("✘", e)
    s.commit()

    print("\\nযেসব বইয়ের ফেরতের তারিখ পার হয়েছে:")
    late = select(Loan).where(Loan.returned.is_(False), Loan.due < date.today())
    for loan in s.scalars(late):
        print(f"  {loan.book.title} – {loan.member.name} (due {loan.due})")''',
)

DETAILS["streamlit"] = lib(
    about=(
        "Streamlit দিয়ে শুধু পাইথন লিখেই ডেটা অ্যাপ বা ড্যাশবোর্ড বানানো যায়: স্লাইডার, বাটন, ফাইল "
        "আপলোড, চার্ট, টেবিল সব এক লাইনে। HTML/CSS/JavaScript লাগে না।"
    ),
    install="pip install streamlit",
    example='''# app.py   চালাও: streamlit run app.py
import numpy as np
import pandas as pd
import streamlit as st

st.title("আমার প্রথম Streamlit অ্যাপ")
name = st.text_input("তোমার নাম", "Rahim")
st.write(f"হ্যালো, **{name}**! 👋")

n = st.slider("কতগুলো দিন?", 7, 60, 30)
df = pd.DataFrame({"temp": 30 + np.random.randn(n).cumsum() * 0.5})
st.line_chart(df)''',
    project_title="স্যাটেলাইট scene তুলনার upload dashboard",
    project_about=(
        "দুটো স্যাটেলাইট ছবি (আগে ও পরে) আপলোড করলে পাশাপাশি দেখায়, পার্থক্যের heat map বানায় "
        "আর কত শতাংশ এলাকা বদলেছে হিসাব করে। স্লাইডার দিয়ে পরিবর্তনের সীমা ঠিক করা যায়।"
    ),
    project_code='''# app.py   চালাও: streamlit run app.py
import numpy as np
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Scene compare", layout="wide")
st.title("🛰️ স্যাটেলাইট ছবি তুলনা")

c1, c2 = st.columns(2)
before = c1.file_uploader("আগের ছবি", type=["png", "jpg", "jpeg"])
after = c2.file_uploader("পরের ছবি", type=["png", "jpg", "jpeg"])

if before and after:
    a = Image.open(before).convert("L")
    b = Image.open(after).convert("L").resize(a.size)
    c1.image(a, caption="Before")
    c2.image(b, caption="After")

    threshold = st.slider("পরিবর্তনের সীমা (0–255)", 5, 120, 40)
    diff = np.abs(np.asarray(a, int) - np.asarray(b, int))
    changed = diff > threshold

    m1, m2, m3 = st.columns(3)
    m1.metric("পরিবর্তিত এলাকা", f"{changed.mean():.1%}")
    m2.metric("গড় পার্থক্য", f"{diff.mean():.1f}")
    m3.metric("ছবির মাপ", f"{a.size[0]}×{a.size[1]}")

    heat = np.zeros((*diff.shape, 3), np.uint8)
    heat[..., 0] = np.clip(diff * 2, 0, 255)          # লাল = বেশি পরিবর্তন
    heat[changed, 1] = 60
    st.image(heat, caption="পরিবর্তনের heat map")
else:
    st.info("শুরু করতে দুটো ছবি আপলোড করো।")''',
)

DETAILS["plotly"] = lib(
    about=(
        "Plotly দিয়ে ইন্টারঅ্যাকটিভ চার্ট বানানো যায়: মাউস রাখলে মান দেখায়, জুম, ঘোরানো যায়। "
        "চার্ট HTML ফাইল হিসেবে সেভ করে যে কাউকে পাঠানো যায়, ব্রাউজারেই খুলবে।"
    ),
    install="pip install plotly pandas",
    example='''import plotly.express as px

df = px.data.gapminder().query("year == 2007")      # plotly-র সাথে আসা নমুনা ডেটা
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=True,
                 title="Income vs life expectancy (2007)")
fig.write_html("gapminder.html")
print("gapminder.html সেভ হয়েছে ✔ (ব্রাউজারে খোলো)")''',
    project_title="বছরভেদে 3D তাপমাত্রা ঘাটতির explorer",
    project_about=(
        "বছর × মাস অনুযায়ী তাপমাত্রার বিচ্যুতি (anomaly) একটা ঘোরানো যায় এমন 3D surface-এ দেখায়, "
        "নিচে heatmap-ও দেয়, আর পুরোটা একটা HTML ফাইলে সেভ করে।"
    ),
    project_code='''import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

years = np.arange(1990, 2026)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# নমুনা ডেটা: ধীরে ধীরে উষ্ণতা + ঋতুর প্রভাব + noise
rng = np.random.default_rng(0)
trend = (years - years[0]) * 0.03
season = 0.3 * np.sin(np.linspace(0, 2 * np.pi, 12))
anomaly = trend[:, None] + season[None, :] + rng.normal(0, 0.25, (len(years), 12))

fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4],
                    specs=[[{"type": "surface"}, {"type": "heatmap"}]],
                    subplot_titles=("3D view (drag to rotate)", "Heatmap"))
fig.add_trace(go.Surface(z=anomaly, x=months, y=years, colorscale="RdBu_r",
                         cmid=0, showscale=False), row=1, col=1)
fig.add_trace(go.Heatmap(z=anomaly, x=months, y=years, colorscale="RdBu_r",
                         zmid=0, colorbar=dict(title="°C")), row=1, col=2)
fig.update_layout(title="Temperature anomaly by year and month",
                  height=600, scene=dict(zaxis_title="°C"))
fig.write_html("anomaly_explorer.html")

warmest = np.unravel_index(anomaly.argmax(), anomaly.shape)
print(f"সবচেয়ে উষ্ণ: {months[warmest[1]]} {years[warmest[0]]} "
      f"(+{anomaly.max():.2f} °C)")
print("anomaly_explorer.html সেভ হয়েছে ✔")''',
)

DETAILS["polars"] = lib(
    about=(
        "Polars হলো pandas-এর মতো টেবিল-ডেটার লাইব্রেরি, কিন্তু Rust-এ লেখা আর সব CPU core ব্যবহার "
        "করে বলে অনেক দ্রুত। lazy মোডে বিশাল ফাইলও কম মেমোরিতে প্রসেস করা যায়।"
    ),
    install="pip install polars",
    example='''import polars as pl

df = pl.DataFrame({
    "name": ["Rahim", "Karim", "Sumi", "Riya"],
    "dept": ["CSE", "EEE", "CSE", "EEE"],
    "marks": [78, 85, 92, 66],
})

print(df.filter(pl.col("marks") > 70))
print(df.group_by("dept").agg(pl.col("marks").mean().alias("avg_marks")))''',
    project_title="বড় Parquet ফাইল থেকে জেলাভিত্তিক পরিসংখ্যান",
    project_about=(
        "দশ লাখ সারির নমুনা আবহাওয়া ডেটা Parquet-এ সেভ করে, তারপর lazy scan দিয়ে পুরো ফাইল "
        "মেমোরিতে না এনেই জেলাভিত্তিক গড় তাপমাত্রা, মোট বৃষ্টি আর বৃষ্টির দিন গোনে।"
    ),
    project_code='''import time
import numpy as np
import polars as pl

# ১) নমুনা বড় ফাইল (আসল প্রজেক্টে তোমার নিজের .parquet থাকবে)
n = 1_000_000
rng = np.random.default_rng(0)
districts = np.array(["Dhaka", "Sylhet", "Khulna", "Rajshahi", "Barishal",
                      "Rangpur", "Chattogram", "Mymensingh"])
pl.DataFrame({
    "district": districts[rng.integers(0, len(districts), n)],
    "day": rng.integers(1, 366, n),
    "temp_c": rng.normal(29, 4, n).round(1),
    "rain_mm": rng.exponential(6, n).round(1),
}).write_parquet("weather.parquet")

# ২) lazy query: দরকারি কলামই শুধু পড়া হবে
t = time.perf_counter()
summary = (
    pl.scan_parquet("weather.parquet")
      .filter(pl.col("temp_c").is_between(-5, 50))
      .group_by("district")
      .agg(
          pl.col("temp_c").mean().round(2).alias("avg_temp"),
          pl.col("rain_mm").sum().round(0).alias("total_rain"),
          (pl.col("rain_mm") > 10).sum().alias("rainy_days"),
          pl.len().alias("rows"),
      )
      .sort("total_rain", descending=True)
      .collect()
)
print(summary)
print(f"{n:,} সারি প্রসেস হলো {time.perf_counter() - t:.2f}s-এ")
summary.write_csv("district_summary.csv")''',
)

DETAILS["rich"] = lib(
    about=(
        "Rich দিয়ে টার্মিনালের আউটপুট সুন্দর করা যায়: রঙিন লেখা, টেবিল, প্রগ্রেস বার, প্যানেল, "
        "কোড হাইলাইট, সুন্দর error message। CLI টুলকে প্রফেশনাল দেখাতে সেরা।"
    ),
    install="pip install rich",
    example='''from rich import print
from rich.table import Table
from rich.console import Console

print("[bold green]সফল![/] ফাইল সেভ হয়েছে :white_check_mark:")

table = Table(title="ফলাফল")
table.add_column("নাম")
table.add_column("নম্বর", justify="right")
table.add_row("Rahim", "78")
table.add_row("Sumi", "[bold]92[/]")
Console().print(table)''',
    project_title="সেন্সর ফলের readable terminal report",
    project_about=(
        "কয়েকটা সেন্সর একে একে পড়ার সময় প্রগ্রেস বার দেখায়, তারপর রঙিন টেবিলে ফলাফল দেয় (সীমার "
        "বাইরে হলে লাল), আর শেষে একটা সারাংশ প্যানেল দেখায়।"
    ),
    project_code='''import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

console = Console()
SENSORS = {"Temp-01": (20, 35, "°C"), "Temp-02": (20, 35, "°C"),
           "Humidity-A": (30, 90, "%"), "Pressure-X": (990, 1030, "hPa"),
           "Soil-M1": (10, 60, "%")}

random.seed(5)
readings = []
for name in track(SENSORS, description="সেন্সর পড়া হচ্ছে…"):
    low, high, unit = SENSORS[name]
    span = high - low
    value = round(random.uniform(low - span * 0.15, high + span * 0.15), 1)
    readings.append((name, value, low, high, unit))
    time.sleep(0.3)

table = Table(title="Sensor report", header_style="bold cyan")
table.add_column("Sensor")
table.add_column("Value", justify="right")
table.add_column("Range", justify="center")
table.add_column("Status")

bad = 0
for name, value, low, high, unit in readings:
    ok = low <= value <= high
    bad += not ok
    table.add_row(name, f"{value} {unit}", f"{low}–{high}",
                  "[green]✔ OK[/]" if ok else "[bold red]✘ OUT[/]")

console.print(table)
style = "green" if bad == 0 else "red"
console.print(Panel(f"{len(readings)}টা সেন্সর পড়া হলো · {bad}টা সীমার বাইরে",
                    title="Summary", border_style=style))''',
)

DETAILS["typer"] = lib(
    about=(
        "Typer দিয়ে শুধু type hint দেওয়া পাইথন ফাংশন থেকেই কমান্ড-লাইন টুল বানানো যায়। "
        "--help, ইনপুট যাচাই, রঙিন error সব নিজে থেকে হয়। Click-এর উপর বানানো, লেখা আরো সহজ।"
    ),
    install="pip install typer",
    example='''# hello.py   চালাও: python hello.py Rahim --times 2
import typer

def main(name: str, times: int = 1, loud: bool = False):
    """কাউকে হ্যালো বলে।"""
    msg = f"Hello, {name}!"
    for _ in range(times):
        typer.echo(msg.upper() if loud else msg)

if __name__ == "__main__":
    typer.run(main)''',
    project_title="বৃষ্টির CSV summarize করার CLI",
    project_about=(
        "বৃষ্টির CSV ফাইলের জন্য দুটো কমান্ড: summary (মোট, গড়, সবচেয়ে বৃষ্টির দিন) আর top "
        "(সবচেয়ে বেশি বৃষ্টির N দিন)। কলামের নাম ও কয়টা দেখাবে option দিয়ে বদলানো যায়।"
    ),
    project_code='''# rain.py
#   python rain.py summary rain.csv
#   python rain.py top rain.csv --n 5 --column rain_mm
import csv
from pathlib import Path
import typer

app = typer.Typer(help="বৃষ্টির CSV বিশ্লেষণ টুল")

def load(path: Path, column: str) -> list[tuple[str, float]]:
    if not path.exists():
        typer.secho(f"ফাইল পাওয়া যায়নি: {path}", fg=typer.colors.RED)
        raise typer.Exit(1)
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows or column not in rows[0]:
        typer.secho(f"'{column}' কলাম নেই", fg=typer.colors.RED)
        raise typer.Exit(1)
    first = list(rows[0])[0]
    return [(r[first], float(r[column] or 0)) for r in rows]

@app.command()
def summary(path: Path, column: str = "rain_mm"):
    """মোট, গড় ও সবচেয়ে বৃষ্টির দিন।"""
    data = load(path, column)
    values = [v for _, v in data]
    day, most = max(data, key=lambda x: x[1])
    typer.echo(f"দিন: {len(values)}")
    typer.echo(f"মোট: {sum(values):.1f} mm | গড়: {sum(values) / len(values):.1f} mm")
    typer.echo(f"বৃষ্টিহীন দিন: {sum(v == 0 for v in values)}")
    typer.secho(f"সবচেয়ে বেশি: {day} ({most} mm)", fg=typer.colors.CYAN)

@app.command()
def top(path: Path, n: int = 3, column: str = "rain_mm"):
    """সবচেয়ে বেশি বৃষ্টির n দিন।"""
    for day, v in sorted(load(path, column), key=lambda x: -x[1])[:n]:
        typer.echo(f"{day:12} {'█' * int(v // 5)} {v}")

if __name__ == "__main__":
    app()''',
)

DETAILS["transformers"] = lib(
    about=(
        "Hugging Face Transformers দিয়ে হাজার হাজার তৈরি (pretrained) AI মডেল কয়েক লাইনে চালানো "
        "যায়: লেখার অনুভূতি বোঝা, অনুবাদ, সারাংশ, প্রশ্নোত্তর, ছবি চেনা। প্রথমবার মডেল ডাউনলোড হয়।"
    ),
    install="pip install transformers torch",
    example='''from transformers import pipeline

classifier = pipeline("sentiment-analysis")      # প্রথমবার মডেল ডাউনলোড হবে
print(classifier("I love learning Python!"))
print(classifier("This movie was a waste of time."))
# [{'label': 'POSITIVE', 'score': 0.99...}]''',
    project_title="ইংরেজি রিভিউয়ের sentiment classifier",
    project_about=(
        "একটা CSV-র সব প্রোডাক্ট রিভিউ একসাথে (batch) বিশ্লেষণ করে প্রতিটাকে positive/negative "
        "লেবেল দেয়, কম নিশ্চিত ফলগুলো 'review' হিসেবে চিহ্নিত করে আর নতুন CSV-তে সেভ করে।"
    ),
    project_code='''import csv
from collections import Counter
from transformers import pipeline

MODEL = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("sentiment-analysis", model=MODEL)

# আসল প্রজেক্টে: reviews = [r["text"] for r in csv.DictReader(open("reviews.csv"))]
reviews = [
    "Battery lasts two full days, amazing value.",
    "Stopped working after a week. Very disappointed.",
    "It's okay, nothing special.",
    "Fast delivery and the quality is great!",
    "The screen scratches far too easily.",
]

results = classifier(reviews, batch_size=8, truncation=True)

rows, counts = [], Counter()
for text, r in zip(reviews, results):
    label = r["label"].lower() if r["score"] >= 0.8 else "needs review"
    counts[label] += 1
    rows.append({"review": text, "label": label, "score": round(r["score"], 3)})
    print(f"{label:13} {r['score']:.2f}  {text}")

with open("reviews_labeled.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["review", "label", "score"])
    w.writeheader()
    w.writerows(rows)

print("\\nসারাংশ:", dict(counts))
print("reviews_labeled.csv সেভ হয়েছে ✔")''',
)

DETAILS["gradio"] = lib(
    about=(
        "Gradio দিয়ে কয়েক লাইনে যেকোনো পাইথন ফাংশন বা AI মডেলের জন্য ওয়েব ইন্টারফেস বানানো যায়: "
        "টেক্সট বক্স, ছবি আপলোড, মাইক্রোফোন। share=True দিলে অন্যদেরও লিংক পাঠানো যায়।"
    ),
    install="pip install gradio",
    example='''# app.py   চালাও: python app.py  → ব্রাউজারে http://127.0.0.1:7860
import gradio as gr

def greet(name, times):
    return ("Hello " + name + "! ") * int(times)

demo = gr.Interface(
    fn=greet,
    inputs=[gr.Textbox(label="নাম"), gr.Slider(1, 5, step=1, label="কতবার")],
    outputs=gr.Textbox(label="ফলাফল"),
    title="Hello app",
)
demo.launch()''',
    project_title="ছবি আপলোড করে classifier ফল দেখার ডেমো",
    project_about=(
        "একটা ছবি আপলোড বা ক্যামেরা দিয়ে তুললে Hugging Face-এর ViT মডেল দিয়ে চিনে সেরা ৩টা "
        "সম্ভাব্য নাম % সহ দেখায়। কয়েকটা উদাহরণ ছবি থাকলে এক ক্লিকে চেষ্টা করা যায়।"
    ),
    project_code='''# app.py   চালাও: python app.py
# pip install gradio transformers torch pillow
import gradio as gr
from transformers import pipeline

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify(image):
    if image is None:
        return {}
    preds = classifier(image, top_k=3)
    return {p["label"]: float(p["score"]) for p in preds}

demo = gr.Interface(
    fn=classify,
    inputs=gr.Image(type="pil", label="ছবি দাও", sources=["upload", "webcam"]),
    outputs=gr.Label(num_top_classes=3, label="মডেল যা ভাবছে"),
    title="🖼️ ছবি চেনার ডেমো",
    description="যেকোনো ছবি দাও, মডেল বলবে এটা কী হতে পারে।",
    # examples=["cat.jpg", "car.jpg"],   # ফোল্ডারে ছবি থাকলে চালু করো
)

if __name__ == "__main__":
    demo.launch()          # share=True দিলে পাবলিক লিংক পাবে''',
)


# ==================================================================
# ব্যাচ ৩: ওয়েব, অটোমেশন, ডিপ লার্নিং, NLP, ডেটাবেস
# ==================================================================

DETAILS["django"] = lib(
    about=(
        "Django হলো পূর্ণাঙ্গ ওয়েব ফ্রেমওয়ার্ক: ডেটাবেস (ORM), লগইন সিস্টেম, অ্যাডমিন প্যানেল, "
        "ফর্ম, নিরাপত্তা সব আগে থেকেই তৈরি। বড় ওয়েবসাইট দ্রুত বানাতে সবচেয়ে জনপ্রিয় পাইথন ফ্রেমওয়ার্ক।"
    ),
    install="pip install django",
    example='''# app.py  – এক ফাইলের ছোট Django সাইট
# চালাও: python app.py runserver   → http://127.0.0.1:8000
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

settings.configure(
    DEBUG=True,
    SECRET_KEY="dev-only-secret",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
)

def home(request):
    return HttpResponse("<h1>Hello Django!</h1><a href='/hello/Rahim/'>Say hello</a>")

def hello(request, name):
    return HttpResponse(f"<h2>হ্যালো, {name}!</h2>")

urlpatterns = [
    path("", home),
    path("hello/<str:name>/", hello),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)''',
    project_title="কোর্স রেজিস্ট্রেশন পোর্টাল",
    project_about=(
        "শিক্ষার্থীরা লগইন করে কোর্সের তালিকা দেখে, সিট খালি থাকলে রেজিস্টার করে। একই কোর্সে দুবার "
        "নেওয়া যায় না, আর অ্যাডমিন প্যানেল থেকে কোর্স যোগ ও কারা নিয়েছে দেখা যায়। নিচে কোন ফাইলে কী লিখতে হবে দেওয়া আছে।"
    ),
    project_code='''# ধাপ ১ – টার্মিনালে:
#   django-admin startproject portal
#   cd portal
#   python manage.py startapp courses
#   portal/settings.py এর INSTALLED_APPS-এ "courses" যোগ করো

# ===== courses/models.py =====
from django.conf import settings
from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    seats = models.PositiveIntegerField(default=30)

    def seats_left(self):
        return self.seats - self.enrollments.count()

    def __str__(self):
        return f"{self.code} – {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["student", "course"],
                                               name="one_enrollment_per_course")]

# ===== courses/admin.py =====
from django.contrib import admin
from .models import Course, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "seats", "seats_left"]

admin.site.register(Enrollment)

# ===== courses/views.py =====
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Enrollment

@login_required
def course_list(request):
    mine = set(Enrollment.objects.filter(student=request.user)
                                 .values_list("course_id", flat=True))
    return render(request, "courses/list.html",
                  {"courses": Course.objects.all(), "mine": mine})

@login_required
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        if course.seats_left() <= 0:
            messages.error(request, f"{course.code}: সিট নেই")
        else:
            _, created = Enrollment.objects.get_or_create(student=request.user, course=course)
            messages.success(request, f"{course.code}: রেজিস্ট্রেশন সফল" if created
                             else f"{course.code}: আগেই নেওয়া আছে")
    return redirect("course_list")

# ===== courses/urls.py =====
from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("<int:pk>/enroll/", views.enroll, name="enroll"),
]

# ===== portal/urls.py =====
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("courses.urls")),
]

# ===== courses/templates/courses/list.html =====
# {% for m in messages %}<p>{{ m }}</p>{% endfor %}
# <h1>Courses</h1>
# {% for c in courses %}
#   <p>{{ c }} – {{ c.seats_left }} seats left
#   {% if c.id in mine %} ✔ enrolled
#   {% else %}
#     <form method="post" action="{% url 'enroll' c.id %}">{% csrf_token %}
#       <button>Enroll</button></form>
#   {% endif %}</p>
# {% endfor %}

# ধাপ ২ – টার্মিনালে:
#   python manage.py makemigrations && python manage.py migrate
#   python manage.py createsuperuser
#   python manage.py runserver   → /admin থেকে কোর্স যোগ করো, তারপর / খোলো
# (লগইন পেজের জন্য templates/registration/login.html বানাতে হবে)''',
)

DETAILS["selenium"] = lib(
    about=(
        "Selenium দিয়ে কোড লিখে আসল ব্রাউজার (Chrome, Firefox, Edge) চালানো যায়: পেজ খোলা, ফর্ম পূরণ, "
        "বাটনে ক্লিক। ওয়েবসাইট টেস্ট করা আর একঘেয়ে ব্রাউজারের কাজ অটোমেট করতে ব্যবহার হয়।"
    ),
    install="pip install selenium\n# Chrome ইনস্টল থাকলেই হবে, driver নিজে থেকে ঠিক হয়ে যায়",
    example='''from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
print("Title:", driver.title)

heading = driver.find_element(By.TAG_NAME, "h1")
print("Heading:", heading.text)

driver.save_screenshot("example.png")
driver.quit()''',
    project_title="কোর্স সাইটের login form smoke test",
    project_about=(
        "একটা লগইন ফর্ম ঠিকমতো কাজ করছে কিনা পরীক্ষা করে: সঠিক পাসওয়ার্ডে ড্যাশবোর্ড আসে কিনা, "
        "ভুল পাসওয়ার্ডে error দেখায় কিনা, খালি ফর্মে কী হয়। প্রতিটার পাস/ফেল আর স্ক্রিনশট রাখে।"
    ),
    project_code='''from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# আসল প্রজেক্টে: URL = "https://তোমার-কোর্স-সাইট/login"
DEMO = Path("login_demo.html")
DEMO.write_text("""<form id=f><input id=user><input id=pass type=password>
<button id=go>Login</button></form><p id=msg></p>
<script>f.onsubmit = e => { e.preventDefault();
  if (!user.value || !pass.value) msg.textContent = "Please fill all fields";
  else if (user.value == "student" && pass.value == "secret123")
    document.body.innerHTML = "<h1 id=dash>Dashboard</h1>";
  else msg.textContent = "Wrong username or password"; };</script>""")
URL = DEMO.resolve().as_uri()

CASES = [
    ("সঠিক লগইন", "student", "secret123", (By.ID, "dash"), "Dashboard"),
    ("ভুল পাসওয়ার্ড", "student", "nope", (By.ID, "msg"), "Wrong"),
    ("খালি ফর্ম", "", "", (By.ID, "msg"), "fill all"),
]

opts = Options()
opts.add_argument("--headless=new")
driver = webdriver.Chrome(options=opts)
passed = 0
try:
    for i, (label, user, pw, locator, expect) in enumerate(CASES, 1):
        driver.get(URL)
        driver.find_element(By.ID, "user").send_keys(user)
        driver.find_element(By.ID, "pass").send_keys(pw)
        driver.find_element(By.ID, "go").click()
        try:
            WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element(locator, expect))
            passed += 1
            print(f"✔ {label}")
        except TimeoutException:
            driver.save_screenshot(f"fail_{i}.png")
            print(f"✘ {label} – fail_{i}.png দেখো")
finally:
    driver.quit()

print(f"{passed}/{len(CASES)} টেস্ট পাস")''',
)

DETAILS["scrapy"] = lib(
    about=(
        "Scrapy হলো বড় আকারের ওয়েব স্ক্র্যাপিং ফ্রেমওয়ার্ক। অনেক পেজ একসাথে দ্রুত পড়ে, লিংক ধরে "
        "এগোয়, robots.txt মানে, আর ফল সরাসরি JSON/CSV-তে সেভ করে। শুধু অনুমতি থাকা সাইটে ব্যবহার করো।"
    ),
    install="pip install scrapy",
    example='''# quotes.py   চালাও: scrapy runspider quotes.py -O quotes.json
# quotes.toscrape.com হলো স্ক্র্যাপিং অনুশীলনের জন্য বানানো সাইট
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for q in response.css("div.quote"):
            yield {
                "text": q.css("span.text::text").get(),
                "author": q.css("small.author::text").get(),
                "tags": q.css("a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)''',
    project_title="নিজের ব্লগে ভাঙা article link ও title inventory",
    project_about=(
        "নিজের ব্লগের প্রতিটা পেজ ঘুরে প্রতিটা আর্টিকেলের শিরোনাম, ঠিকানা আর স্ট্যাটাস লিখে রাখে; "
        "কোন লিংক ভাঙা (404/500) আর কোন পেজ থেকে সেটা এসেছে সেটা আলাদা করে দেখায়।"
    ),
    project_code='''# blog_audit.py   চালাও: scrapy runspider blog_audit.py
# START পরিবর্তন করে নিজের সাইটের ঠিকানা দাও
from urllib.parse import urlparse
import scrapy

START = "https://your-blog.github.io/"

class BlogAudit(scrapy.Spider):
    name = "blog_audit"
    start_urls = [START]
    allowed_domains = [urlparse(START).netloc]
    handle_httpstatus_list = [404, 410, 500, 503]      # ভাঙা পেজও আমাদের কাছে আসুক
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.5,                          # সার্ভারের উপর চাপ কম
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "FEEDS": {"inventory.csv": {"format": "csv", "overwrite": True}},
    }

    def parse(self, response):
        broken = response.status >= 400
        yield {
            "url": response.url,
            "status": response.status,
            "title": None if broken else (response.css("title::text").get() or "").strip(),
            "found_on": response.meta.get("from", "-"),
            "broken": broken,
        }
        if broken or "text/html" not in response.headers.get("Content-Type", b"").decode():
            return
        for href in response.css("a::attr(href)").getall():
            if href.startswith(("mailto:", "tel:", "#")):
                continue
            yield response.follow(href, self.parse, meta={"from": response.url})

# চালানো শেষে inventory.csv খুলে broken = True সারিগুলো দেখো''',
)

DETAILS["tensorflow"] = lib(
    about=(
        "TensorFlow হলো Google-এর ডিপ লার্নিং ফ্রেমওয়ার্ক। নিউরাল নেটওয়ার্ক বানানো, ট্রেইন করা, আর "
        "মোবাইল (TF Lite), ব্রাউজার বা সার্ভারে চালানো যায়। এর ভেতরে Keras API দিয়ে মডেল বানানো সবচেয়ে সহজ।"
    ),
    install="pip install tensorflow",
    example='''import tensorflow as tf

a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0], [1.0]])
print(tf.matmul(a, b))            # ম্যাট্রিক্স গুণ

# স্বয়ংক্রিয় derivative: y = x² এর ঢাল x = 3 এ
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2
print("dy/dx =", tape.gradient(y, x).numpy())   # 6.0

print("GPU আছে?", tf.config.list_physical_devices("GPU"))''',
    project_title="উদ্ভিদের পাতার ধরন শনাক্তের অ্যাপ",
    project_about=(
        "ফোল্ডারে রাখা পাতার ছবি (প্রতি ধরনের জন্য আলাদা ফোল্ডার) দিয়ে আগে থেকে শেখা MobileNetV2 "
        "মডেলকে নতুন করে শেখায় (transfer learning)। কম ছবিতেই ভালো ফল দেয়, মডেল সেভ করে আর নতুন ছবি চেনে।"
    ),
    project_code='''# ফোল্ডার এভাবে সাজাও:
# leaves/
#   mango/   *.jpg
#   guava/   *.jpg
#   neem/    *.jpg
import numpy as np
import tensorflow as tf

IMG = (160, 160)
train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    "leaves", validation_split=0.2, subset="both", seed=42,
    image_size=IMG, batch_size=32)
classes = train_ds.class_names
print("ধরন:", classes)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(500).prefetch(AUTOTUNE)
val_ds = val_ds.cache().prefetch(AUTOTUNE)

augment = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
])
base = tf.keras.applications.MobileNetV2(input_shape=IMG + (3,),
                                         include_top=False, weights="imagenet")
base.trainable = False                     # আগের শেখা জ্ঞান স্থির রাখা

inputs = tf.keras.Input(shape=IMG + (3,))
x = augment(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = tf.keras.layers.Dense(len(classes), activation="softmax")(x)
model = tf.keras.Model(inputs, outputs)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(train_ds, validation_data=val_ds, epochs=8,
          callbacks=[tf.keras.callbacks.EarlyStopping(patience=2,
                                                      restore_best_weights=True)])
model.save("leaf_model.keras")

def predict(path):
    img = tf.keras.utils.load_img(path, target_size=IMG)
    arr = np.expand_dims(tf.keras.utils.img_to_array(img), 0)
    probs = model.predict(arr, verbose=0)[0]
    best = int(np.argmax(probs))
    return classes[best], float(probs[best])

# label, conf = predict("test_leaf.jpg")
# print(f"এটা সম্ভবত {label} ({conf:.0%})")''',
)

DETAILS["keras"] = lib(
    about=(
        "Keras হলো নিউরাল নেটওয়ার্ক বানানোর সবচেয়ে সহজ API: লেয়ার একটার পর একটা সাজাও, compile করো, "
        "fit করো। Keras 3 একই কোড TensorFlow, PyTorch বা JAX যেকোনোটার উপর চালাতে পারে।"
    ),
    install="pip install keras tensorflow",
    example='''import numpy as np
import keras
from keras import layers

# শেখাও: y = 2x + 1
x = np.linspace(-1, 1, 200).reshape(-1, 1)
y = 2 * x + 1 + np.random.normal(0, 0.05, x.shape)

model = keras.Sequential([keras.Input(shape=(1,)), layers.Dense(1)])
model.compile(optimizer=keras.optimizers.SGD(0.1), loss="mse")
model.fit(x, y, epochs=50, verbose=0)

w, b = model.layers[0].get_weights()
print(f"শিখেছে: y = {w[0][0]:.2f}x + {b[0]:.2f}")
print("x=3 হলে:", model.predict(np.array([[3.0]]), verbose=0)[0][0])''',
    project_title="হাতের লেখা অঙ্ক শ্রেণিবিন্যাস ডেমো",
    project_about=(
        "MNIST ডেটাসেটের ৬০,০০০ হাতে লেখা অঙ্কের ছবি দিয়ে একটা ছোট CNN ট্রেইন করে (~৯৯% নির্ভুল), "
        "টেস্ট সেটে যাচাই করে, কোন অঙ্ক বেশি ভুল হয় দেখায় আর মডেল সেভ করে।"
    ),
    project_code='''import numpy as np
import keras
from keras import layers

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train[..., None].astype("float32") / 255.0      # (60000, 28, 28, 1)
x_test = x_test[..., None].astype("float32") / 255.0

model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),
])
model.summary()

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(x_train, y_train, batch_size=128, epochs=5, validation_split=0.1)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"টেস্ট নির্ভুলতা: {acc:.2%}")

pred = model.predict(x_test, verbose=0).argmax(axis=1)
wrong = pred != y_test
for digit in range(10):
    mask = y_test == digit
    print(f"  অঙ্ক {digit}: ভুল {wrong[mask].mean():.1%}")

model.save("digits.keras")
print("digits.keras সেভ হয়েছে ✔")''',
)

DETAILS["xgboost"] = lib(
    about=(
        "XGBoost হলো টেবিল-ডেটায় (Excel/CSV-র মতো) অনুমান করার জন্য সবচেয়ে শক্তিশালী মডেলগুলোর একটা। "
        "অনেকগুলো decision tree একটার পর একটা ভুল শুধরে শেখে। Kaggle প্রতিযোগিতায় খুব জনপ্রিয়।"
    ),
    install="pip install xgboost scikit-learn",
    example='''from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

model = XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.1)
model.fit(X_train, y_train)
print("Accuracy:", model.score(X_test, y_test))''',
    project_title="বাস্তব তথ্য দিয়ে বাড়িভাড়া অনুমানের মডেল",
    project_about=(
        "এলাকা, আয়তন, রুম, তলা, লিফট আছে কিনা এসব থেকে মাসিক বাড়িভাড়া অনুমান করে। কোন তথ্য ভাড়ায় "
        "সবচেয়ে বেশি প্রভাব ফেলে দেখায় আর নতুন একটা ফ্ল্যাটের ভাড়া অনুমান করে। নিজের CSV দিয়ে বদলে নিও।"
    ),
    project_code='''import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# আসল প্রজেক্টে: df = pd.read_csv("rent.csv")  (একই কলাম নাম রাখো)
rng = np.random.default_rng(0)
n = 2000
areas = ["Gulshan", "Dhanmondi", "Mirpur", "Uttara", "Mohammadpur"]
premium = {"Gulshan": 2.2, "Dhanmondi": 1.6, "Uttara": 1.3, "Mirpur": 1.0, "Mohammadpur": 1.05}
df = pd.DataFrame({
    "area": rng.choice(areas, n),
    "sqft": rng.integers(600, 2500, n),
    "rooms": rng.integers(1, 5, n),
    "floor": rng.integers(1, 15, n),
    "lift": rng.integers(0, 2, n),
})
df["rent"] = (df["sqft"] * 14 * df["area"].map(premium)
              + df["rooms"] * 1500 + df["lift"] * 3000 + df["floor"] * 150
              + rng.normal(0, 2500, n)).round(-2)

df["area"] = df["area"].astype("category")
X, y = df.drop(columns="rent"), df["rent"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = XGBRegressor(n_estimators=600, learning_rate=0.05, max_depth=5,
                     enable_categorical=True, tree_method="hist",
                     early_stopping_rounds=30)
model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"গড় ভুল: ৳{mae:,.0f} (গড় ভাড়া ৳{y.mean():,.0f})")

imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\\nকোন তথ্য কতটা গুরুত্বপূর্ণ:")
print(imp.round(3))

flat = pd.DataFrame([{"area": "Dhanmondi", "sqft": 1400, "rooms": 3, "floor": 6, "lift": 1}])
flat["area"] = pd.Categorical(flat["area"], categories=X["area"].cat.categories)
print(f"\\nনতুন ফ্ল্যাটের আনুমানিক ভাড়া: ৳{model.predict(flat)[0]:,.0f}")''',
)

DETAILS["spacy"] = lib(
    about=(
        "spaCy হলো দ্রুত ও আধুনিক NLP লাইব্রেরি: বাক্য ভাঙা, শব্দের পদ (noun, verb) চেনা, মানুষ-স্থান-"
        "প্রতিষ্ঠানের নাম খুঁজে বের করা (NER)। আসল প্রজেক্টে ব্যবহারের জন্য বানানো।"
    ),
    install="pip install spacy\npython -m spacy download en_core_web_sm",
    example='''import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Rahim moved from Sylhet to London in 2019 to work at Google.")

for token in doc[:6]:
    print(f"{token.text:8} {token.pos_:6} lemma={token.lemma_}")

print("\\nনাম পাওয়া গেছে:")
for ent in doc.ents:
    print(f"  {ent.text:10} → {ent.label_}")     # PERSON, GPE, DATE, ORG''',
    project_title="ইংরেজি field note থেকে শহরের নামের index",
    project_about=(
        "কয়েকটা ইংরেজি ফিল্ড নোট পড়ে সব জায়গার নাম (শহর/দেশ) খুঁজে বের করে, কোনটা কতবার এসেছে "
        "আর কোন নোটের কোন বাক্যে আছে সেই সূচি (index) বানিয়ে CSV-তে সেভ করে।"
    ),
    project_code='''import csv
from collections import Counter, defaultdict
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")

# আসল প্রজেক্টে: notes = {p.stem: p.read_text() for p in Path("notes").glob("*.txt")}
notes = {
    "day1": "We left Dhaka early and reached Sylhet by noon. Tea gardens near Srimangal were busy.",
    "day2": "Rain stopped work in Sylhet. A team from Chittagong joined us in the afternoon.",
    "day3": "Back in Dhaka. Samples will be shipped to Kolkata and later to London.",
}

count = Counter()
where = defaultdict(list)
for name, text in notes.items():
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            place = ent.text.strip()
            count[place] += 1
            where[place].append((name, ent.sent.text.strip()))

with open("place_index.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["place", "mentions", "note", "sentence"])
    for place, n in count.most_common():
        for note, sent in where[place]:
            w.writerow([place, n, note, sent])

for place, n in count.most_common():
    notes_list = sorted({note for note, _ in where[place]})
    print(f"{place:12} {n}× → {', '.join(notes_list)}")
print("place_index.csv সেভ হয়েছে ✔")''',
)

DETAILS["nltk"] = lib(
    about=(
        "NLTK হলো ভাষা প্রক্রিয়াকরণ (NLP) শেখার ক্লাসিক লাইব্রেরি: শব্দ ভাঙা, মূল শব্দ বের করা "
        "(stemming), শব্দের পদ, শব্দের ঘনত্ব, WordNet অভিধান। শেখা ও গবেষণার জন্য দারুণ।"
    ),
    install="pip install nltk",
    example='''import nltk
nltk.download("punkt_tab", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

text = "Python is easy to learn. Students love building small projects."
sentences = nltk.sent_tokenize(text)
words = nltk.word_tokenize(sentences[1])

print("বাক্য:", sentences)
print("শব্দ:", words)
print("পদ:", nltk.pos_tag(words))''',
    project_title="শব্দের গঠন শেখার ছোট NLP notebook",
    project_about=(
        "একটা অনুচ্ছেদ নিয়ে ধাপে ধাপে দেখায়: শব্দ ভাঙা, stopword বাদ দেওয়া, stemming বনাম "
        "lemmatization-এর পার্থক্য, সবচেয়ে বেশি আসা শব্দ, আর WordNet থেকে একটা শব্দের মানে ও সমার্থক শব্দ।"
    ),
    project_code='''import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer

for pkg in ["punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger_eng"]:
    nltk.download(pkg, quiet=True)

text = """Researchers were studying how rivers flooded the villages.
The studies showed that flooding happens faster when forests are cut.
Villagers are building better houses and studying the warnings."""

words = [w.lower() for w in nltk.word_tokenize(text) if w.isalpha()]
stop = set(stopwords.words("english"))
content = [w for w in words if w not in stop]
print(f"মোট শব্দ {len(words)}, stopword বাদে {len(content)}")

stemmer, lemmatizer = PorterStemmer(), WordNetLemmatizer()
def wn_pos(tag):
    return {"V": wordnet.VERB, "J": wordnet.ADJ, "R": wordnet.ADV}.get(tag[0], wordnet.NOUN)

print(f"\\n{'word':12}{'stem':12}lemma")
for word, tag in nltk.pos_tag(sorted(set(content)))[:12]:
    print(f"{word:12}{stemmer.stem(word):12}{lemmatizer.lemmatize(word, wn_pos(tag))}")

freq = nltk.FreqDist(lemmatizer.lemmatize(w, wordnet.VERB) for w in content)
print("\\nসবচেয়ে বেশি:", freq.most_common(5))

syn = wordnet.synsets("flood")[0]
print("\\n'flood' এর মানে:", syn.definition())
print("সমার্থক:", sorted({l.name() for s in wordnet.synsets("flood") for l in s.lemmas()})[:8])''',
)

DETAILS["langchain"] = lib(
    about=(
        "LangChain দিয়ে বড় ভাষা মডেল (GPT, Claude ইত্যাদি) দিয়ে অ্যাপ বানানো যায়: প্রম্পট, নিজের "
        "ডকুমেন্ট থেকে খুঁজে উত্তর দেওয়া (RAG), টুল ব্যবহার করা এজেন্ট। মডেল বদলানো খুব সহজ।"
    ),
    install="pip install langchain langchain-openai\n# OPENAI_API_KEY সেট করো",
    example='''from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4.1-mini")      # Claude: "anthropic:claude-sonnet-5-5"

reply = model.invoke("পাইথনে list comprehension কী? এক লাইনের উদাহরণ দাও।")
print(reply.content)''',
    project_title="সিলেবাস থেকে সূত্র দেখিয়ে উত্তর দেওয়া চ্যাটবট",
    project_about=(
        "কোর্সের সিলেবাস টুকরো করে embedding দিয়ে সার্চযোগ্য করে। প্রশ্ন করলে সবচেয়ে মিলে যাওয়া "
        "অংশগুলো খুঁজে শুধু সেখান থেকে উত্তর দেয়, আর কোন অংশ থেকে উত্তর এসেছে [১], [২] দিয়ে দেখায়।"
    ),
    project_code='''from langchain.chat_models import init_chat_model
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# আসল প্রজেক্টে: syllabus = open("syllabus.txt", encoding="utf-8").read()
syllabus = """CSE101 Introduction to Programming.
Assessment: Midterm 30%, Final 40%, Assignments 20%, Attendance 10%.
Late assignments lose 10% per day and are not accepted after 3 days.
Week 1-3: variables, loops, functions. Week 4-6: lists, dictionaries, files.
Office hours: Sunday and Tuesday, 2-4 pm, Room 402.
Plagiarism results in zero marks for the assignment."""

splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)
chunks = splitter.create_documents([syllabus])
store = InMemoryVectorStore.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"))
model = init_chat_model("openai:gpt-4.1-mini", temperature=0)

def ask(question: str) -> str:
    hits = store.similarity_search(question, k=3)
    context = "\\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(hits, 1))
    prompt = f"""Answer using ONLY the syllabus excerpts below.
Cite excerpts like [1]. If the answer is not there, say you don't know.
Answer in the language of the question.

{context}

Question: {question}"""
    return model.invoke(prompt).content

print("সিলেবাস চ্যাটবট – বের হতে 'exit'")
while (q := input("\\nপ্রশ্ন: ").strip()) and q.lower() != "exit":
    print("উত্তর:", ask(q))''',
)

DETAILS["pymongo"] = lib(
    about=(
        "PyMongo দিয়ে পাইথন থেকে MongoDB ডেটাবেস ব্যবহার করা যায়। MongoDB-তে টেবিলের বদলে JSON-এর মতো "
        "document রাখা হয়, তাই ভিন্ন ভিন্ন গঠনের ডেটা রাখা সহজ।"
    ),
    install="pip install pymongo\n# MongoDB লোকালি চালাও, অথবা MongoDB Atlas-এর ফ্রি ক্লাস্টার ব্যবহার করো",
    example='''from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")   # Atlas হলে সেখানকার URI
db = client["school"]

db.students.insert_one({"name": "Rahim", "marks": 78, "subjects": ["Math", "Physics"]})
db.students.insert_many([{"name": "Sumi", "marks": 92}, {"name": "Riya", "marks": 66}])

for s in db.students.find({"marks": {"$gt": 70}}, {"_id": 0}):
    print(s)''',
    project_title="ফিল্ড নোটের document archive",
    project_about=(
        "মাঠ পর্যবেক্ষণের নোট (জায়গা, তারিখ, প্রজাতির তালিকা, মন্তব্য) document হিসেবে রাখে। টেক্সট "
        "সার্চ করা যায়, তারিখ দিয়ে ফিল্টার করা যায়, আর aggregation দিয়ে কোন প্রজাতি কোথায় কতবার দেখা গেছে বের হয়।"
    ),
    project_code='''from datetime import datetime
from pymongo import ASCENDING, MongoClient, TEXT

client = MongoClient("mongodb://localhost:27017")
notes = client["fieldwork"]["notes"]
notes.drop()                                   # ডেমোর জন্য পরিষ্কার শুরু

notes.insert_many([
    {"site": "Sundarbans", "date": datetime(2026, 3, 2), "observer": "Rahim",
     "sightings": [{"species": "Kingfisher", "count": 3}, {"species": "Spotted deer", "count": 12}],
     "remarks": "High tide in the morning, kingfishers near the canal."},
    {"site": "Ratargul", "date": datetime(2026, 3, 9), "observer": "Sumi",
     "sightings": [{"species": "Kingfisher", "count": 1}, {"species": "Water snake", "count": 2}],
     "remarks": "Water level rising after rain."},
    {"site": "Sundarbans", "date": datetime(2026, 4, 1), "observer": "Sumi",
     "sightings": [{"species": "Spotted deer", "count": 7}],
     "remarks": "Dry season, deer close to the river bank."},
])

notes.create_index([("date", ASCENDING)])
notes.create_index([("remarks", TEXT)])

print("'river' বা 'canal' লেখা আছে এমন নোট:")
for n in notes.find({"$text": {"$search": "river canal"}}, {"site": 1, "date": 1, "_id": 0}):
    print(f"  {n['site']:11} {n['date']:%d %b}")

print("\\nমার্চ মাসের নোট:", notes.count_documents(
    {"date": {"$gte": datetime(2026, 3, 1), "$lt": datetime(2026, 4, 1)}}))

pipeline = [
    {"$unwind": "$sightings"},
    {"$group": {"_id": {"species": "$sightings.species", "site": "$site"},
                "total": {"$sum": "$sightings.count"}, "visits": {"$sum": 1}}},
    {"$sort": {"total": -1}},
]
print("\\nপ্রজাতি ও জায়গা অনুযায়ী মোট:")
for r in notes.aggregate(pipeline):
    print(f"  {r['_id']['species']:13} @ {r['_id']['site']:11} {r['total']:3} ({r['visits']} বার)")''',
)


# ==================================================================
# ডেটা ভিজুয়ালাইজেশন: Matplotlib ও seaborn-এর আরো উদাহরণ + field manual
# ==================================================================

more("matplotlib",
    ex("টীকাসহ লাইন চার্ট",
       "দুটো শহরের মাসিক তাপমাত্রা, সর্বোচ্চ বিন্দুতে তীর দিয়ে টীকা আর ছায়া দেওয়া পরিসর।",
       '''import numpy as np
import matplotlib.pyplot as plt

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
dhaka = [19, 22, 27, 30, 31, 30, 29, 29, 29, 28, 24, 20]
sylhet = [18, 20, 24, 26, 27, 28, 28, 28, 28, 26, 22, 19]
x = np.arange(12)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(x, dhaka, marker="o", lw=2.5, color="#7c3aed", label="Dhaka")
ax.plot(x, sylhet, marker="s", lw=2.5, color="#0d9488", label="Sylhet")
ax.fill_between(x, sylhet, dhaka, color="#7c3aed", alpha=0.08)

peak = int(np.argmax(dhaka))
ax.annotate(f"Peak {dhaka[peak]}°C", xy=(peak, dhaka[peak]), xytext=(peak + 1.5, 33),
            arrowprops=dict(arrowstyle="->", color="#444"), fontsize=11)

ax.set_xticks(x, months)
ax.set_ylabel("Average temperature (°C)")
ax.set_title("Monthly temperature", loc="left", fontsize=14, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
ax.legend(frameon=False)
plt.tight_layout()
plt.show()'''),

    ex("গ্রুপ করা বার চার্ট",
       "তিন বিষয়ে চার জন শিক্ষার্থীর নম্বর পাশাপাশি বার দিয়ে তুলনা, বারের মাথায় মান লেখা।",
       '''import numpy as np
import matplotlib.pyplot as plt

students = ["Rahim", "Karim", "Sumi", "Riya"]
marks = {"Bangla": [78, 65, 92, 70], "English": [65, 58, 88, 74], "Math": [82, 61, 95, 69]}
colors = ["#7c3aed", "#0284c7", "#e11d48"]

x = np.arange(len(students))
width = 0.26
fig, ax = plt.subplots(figsize=(9, 4.5))
for i, (subject, values) in enumerate(marks.items()):
    bars = ax.bar(x + (i - 1) * width, values, width, label=subject, color=colors[i])
    ax.bar_label(bars, fontsize=8, padding=2)

ax.set_xticks(x, students)
ax.set_ylim(0, 105)
ax.set_ylabel("Marks")
ax.set_title("Marks by subject", loc="left", fontweight="bold")
ax.legend(ncols=3, frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()'''),

    ex("বাবল স্ক্যাটার ও colorbar",
       "দেশের আয় বনাম আয়ু; বৃত্তের মাপ = জনসংখ্যা, রং = মহাদেশ। লগ স্কেলের x-অক্ষ।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)
n = 60
income = 10 ** rng.uniform(2.8, 4.8, n)
life = 50 + 7 * np.log10(income) + rng.normal(0, 2.5, n)
pop = rng.uniform(5, 300, n)
region = rng.integers(0, 4, n)

fig, ax = plt.subplots(figsize=(9, 5))
sc = ax.scatter(income, life, s=pop * 3, c=region, cmap="viridis",
                alpha=0.7, edgecolor="white", linewidth=0.8)
ax.set_xscale("log")
ax.set_xlabel("Income per person (log scale)")
ax.set_ylabel("Life expectancy (years)")
ax.set_title("Income vs life expectancy", loc="left", fontweight="bold")

cbar = fig.colorbar(sc, ax=ax, ticks=[0, 1, 2, 3])
cbar.ax.set_yticklabels(["Asia", "Africa", "Europe", "Americas"])
for size in [50, 150, 300]:
    ax.scatter([], [], s=size * 3, color="gray", alpha=0.4, label=f"{size} M")
ax.legend(title="Population", frameon=False, labelspacing=1.4, loc="lower right")
ax.grid(alpha=0.25)
plt.tight_layout()
plt.show()'''),

    ex("হিস্টোগ্রাম ও গড়-মধ্যমা রেখা",
       "পরীক্ষার নম্বরের বণ্টন, গড় ও মধ্যমা আলাদা দাগে, আর প্রতিটা ঘরে কতজন সেটা।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(0)
marks = np.clip(np.concatenate([rng.normal(62, 10, 300), rng.normal(85, 5, 80)]), 0, 100)

fig, ax = plt.subplots(figsize=(9, 4.5))
counts, bins, patches = ax.hist(marks, bins=20, color="#a78bfa", edgecolor="white")
for c, p in zip(counts, patches):
    if p.get_x() >= 80:
        p.set_facecolor("#7c3aed")              # A+ অংশ আলাদা রঙে

ax.axvline(marks.mean(), color="#e11d48", ls="--", lw=2, label=f"Mean {marks.mean():.1f}")
ax.axvline(np.median(marks), color="#0d9488", ls=":", lw=2.5, label=f"Median {np.median(marks):.1f}")
ax.set_xlabel("Marks")
ax.set_ylabel("Students")
ax.set_title("Exam marks distribution (dark = 80+)", loc="left", fontweight="bold")
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()'''),

    ex("ডোনাট চার্ট",
       "মাসিক খরচ কোন খাতে কত শতাংশ, মাঝখানে মোট টাকা।",
       '''import matplotlib.pyplot as plt

labels = ["Rent", "Food", "Transport", "Study", "Internet", "Other"]
amount = [12000, 8000, 2500, 3000, 1000, 1500]
colors = ["#7c3aed", "#0284c7", "#0d9488", "#d97706", "#e11d48", "#94a3b8"]

fig, ax = plt.subplots(figsize=(6.5, 6.5))
wedges, texts, autotexts = ax.pie(
    amount, labels=labels, colors=colors, autopct="%1.0f%%", startangle=90,
    pctdistance=0.8, wedgeprops=dict(width=0.38, edgecolor="white", linewidth=2))
for t in autotexts:
    t.set_color("white")
    t.set_fontweight("bold")

ax.text(0, 0.06, f"Tk {sum(amount):,}", ha="center", fontsize=20, fontweight="bold")
ax.text(0, -0.12, "per month", ha="center", color="gray")
ax.set_title("Monthly budget", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("মানসহ হিটম্যাপ",
       "সপ্তাহের দিন × ঘণ্টা অনুযায়ী লাইব্রেরিতে কতজন এসেছে; প্রতিটা ঘরে সংখ্যা লেখা।",
       '''import numpy as np
import matplotlib.pyplot as plt

days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
hours = [f"{h}:00" for h in range(9, 18)]
rng = np.random.default_rng(1)
visits = (rng.poisson(20, (7, 9)) + np.array([0, 5, 10, 15, 8, 20, 25, 12, 4])).astype(int)
visits[6] //= 3                                   # শুক্রবার কম

fig, ax = plt.subplots(figsize=(10, 4.8))
im = ax.imshow(visits, cmap="magma_r")
ax.set_xticks(range(len(hours)), hours, rotation=45)
ax.set_yticks(range(len(days)), days)
for i in range(len(days)):
    for j in range(len(hours)):
        v = visits[i, j]
        ax.text(j, i, v, ha="center", va="center",
                color="white" if v > visits.max() * 0.6 else "black", fontsize=9)
fig.colorbar(im, ax=ax, label="Visitors")
ax.set_title("Library visitors by day and hour", loc="left", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("কনট্যুর ম্যাপ",
       "একটা পাহাড়ি এলাকার উচ্চতা: রঙিন ভরাট কনট্যুর, ওপরে উচ্চতার রেখা ও লেবেল।",
       '''import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 200)
y = np.linspace(-2, 2, 160)
X, Y = np.meshgrid(x, y)
Z = (np.exp(-((X - 1) ** 2 + Y ** 2)) * 900
     + np.exp(-((X + 1.4) ** 2 + (Y - 0.6) ** 2) * 2) * 600
     + 100 * np.sin(X) * np.cos(Y) + 200)

fig, ax = plt.subplots(figsize=(9, 5))
filled = ax.contourf(X, Y, Z, levels=15, cmap="terrain")
lines = ax.contour(X, Y, Z, levels=8, colors="black", linewidths=0.6, alpha=0.6)
ax.clabel(lines, fmt="%d m", fontsize=8)
fig.colorbar(filled, ax=ax, label="Elevation (m)")
ax.plot(1, 0, "r^", ms=12)
ax.text(1.1, 0.1, "Summit", color="darkred", fontweight="bold")
ax.set_title("Terrain elevation", loc="left", fontweight="bold")
ax.set_aspect("equal")
plt.tight_layout()
plt.show()'''),

    ex("3D সারফেস",
       "একটা গাণিতিক ঢেউ 3D-তে, নিচে তার ছায়া-কনট্যুর।",
       '''import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4, 4, 80)
X, Y = np.meshgrid(x, x)
R = np.sqrt(X ** 2 + Y ** 2) + 1e-9
Z = np.sin(R * 1.6) / R

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection="3d")
ax.plot_surface(X, Y, Z, cmap="plasma", rstride=2, cstride=2, linewidth=0, antialiased=True)
ax.contourf(X, Y, Z, zdir="z", offset=-0.6, cmap="plasma", alpha=0.6)
ax.set_zlim(-0.6, 1.6)
ax.view_init(elev=28, azim=-55)
ax.set_title("sin(r)/r surface", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("পোলার উইন্ড রোজ",
       "কোন দিক থেকে কত বাতাস আসে: ১৬ দিকের পোলার বার চার্ট, গতি অনুযায়ী স্তূপ করা।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(4)
direction = np.concatenate([rng.normal(200, 30, 600), rng.normal(60, 25, 250)]) % 360
speed = rng.gamma(2.2, 2.2, direction.size)

sectors = 16
edges = np.linspace(0, 360, sectors + 1)
speed_bins = [0, 3, 6, 10, 40]
labels = ["0-3", "3-6", "6-10", "10+ m/s"]
colors = ["#c4b5fd", "#8b5cf6", "#6d28d9", "#2e1065"]

theta = np.deg2rad(edges[:-1] + 360 / sectors / 2)
width = np.deg2rad(360 / sectors) * 0.92
fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw=dict(projection="polar"))
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
bottom = np.zeros(sectors)
for lo, hi, lab, col in zip(speed_bins[:-1], speed_bins[1:], labels, colors):
    m = (speed >= lo) & (speed < hi)
    counts, _ = np.histogram(direction[m], bins=edges)
    ax.bar(theta, counts, width=width, bottom=bottom, color=col, label=lab, edgecolor="white")
    bottom += counts
ax.set_xticks(np.deg2rad([0, 90, 180, 270]), ["N", "E", "S", "W"])
ax.legend(loc="lower left", bbox_to_anchor=(-0.12, -0.08), frameon=False, title="Speed")
ax.set_title("Wind rose", fontweight="bold", pad=18)
plt.tight_layout()
plt.show()'''),

    ex("এক পাতায় ড্যাশবোর্ড",
       "subplot_mosaic দিয়ে চারটা চার্ট এক ছবিতে: ট্রেন্ড, ভাগ, বণ্টন আর KPI সংখ্যা।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
days = np.arange(1, 31)
sales = 200 + days * 6 + rng.normal(0, 25, 30).cumsum() * 0.6
channels = {"Shop": 42, "Online": 38, "Phone": 20}
order_size = rng.gamma(3, 120, 400)

fig, axd = plt.subplot_mosaic([["trend", "trend", "kpi"], ["share", "dist", "dist"]],
                              figsize=(11, 6), layout="constrained")
ax = axd["trend"]
ax.plot(days, sales, color="#7c3aed", lw=2.5)
ax.fill_between(days, sales, sales.min() - 20, color="#7c3aed", alpha=0.12)
ax.set_title("Daily sales (June)", loc="left", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)

ax = axd["kpi"]
ax.axis("off")
ax.text(0.5, 0.68, f"{sales.sum():,.0f}", ha="center", fontsize=30, fontweight="bold", color="#140e29")
ax.text(0.5, 0.48, "units this month", ha="center", color="gray")
growth = (sales[-7:].mean() / sales[:7].mean() - 1) * 100
arrow, color = ("▲", "#0d9488") if growth >= 0 else ("▼", "#e11d48")
ax.text(0.5, 0.25, f"{arrow} {abs(growth):.0f}% vs week 1", ha="center", color=color, fontsize=13, fontweight="bold")

ax = axd["share"]
ax.barh(list(channels), list(channels.values()), color=["#7c3aed", "#0284c7", "#0d9488"])
ax.set_title("Sales channel (%)", loc="left", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)

ax = axd["dist"]
ax.hist(order_size, bins=30, color="#e11d48", alpha=0.75, edgecolor="white")
ax.set_title("Order size (Tk)", loc="left", fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)

fig.suptitle("Shop dashboard", fontsize=16, fontweight="bold")
plt.show()'''),
)

man("matplotlib",
    level="শুরু থেকে মাঝারি",
    tag="পাইথনের মূল চার্ট লাইব্রেরি: প্রায় যেকোনো 2D/3D চার্ট, প্রকাশনার মানের ছবি।",
    tasks=["রিপোর্ট ও থিসিসের জন্য PNG/SVG/PDF গ্রাফ", "লাইন, বার, পাই, হিস্টোগ্রাম, স্ক্যাটার",
           "হিটম্যাপ, কনট্যুর, 3D সারফেস, পোলার চার্ট", "এক ছবিতে অনেকগুলো চার্টের ড্যাশবোর্ড",
           "ছোট অ্যানিমেশন (FuncAnimation) ও GIF"],
    caps=["figure ও axes দিয়ে প্রতিটা অংশ নিজের মতো নিয়ন্ত্রণ", "শত শত colormap, স্টাইল শিট (plt.style.use)",
          "টীকা, তীর, টেক্সট, LaTeX-ধাঁচের গাণিতিক লেখা", "pandas, seaborn, scikit-image সবাই এর উপর চার্ট আঁকে"],
    limits=["ডিফল্টে ইন্টারঅ্যাকটিভ ওয়েব চার্ট নয়; এর জন্য Plotly বা Bokeh ভালো",
            "বাংলা লেখা দেখাতে বাংলা ফন্ট সেট করতে হয় (rcParams['font.family'])",
            "লাখ লাখ বিন্দুতে ধীর হয়ে যায়; Datashader বিবেচনা করো"],
    alt="seaborn, plotly, bokeh, altair, plotnine",
)

more("seaborn",
    ex("দলভিত্তিক বণ্টন (KDE)",
       "তিন বিভাগের শিক্ষার্থীদের নম্বরের মসৃণ বণ্টন একসাথে, আলাদা রঙে।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(2)
df = pd.DataFrame({
    "marks": np.concatenate([rng.normal(68, 9, 200), rng.normal(75, 7, 200), rng.normal(60, 12, 200)]),
    "dept": ["CSE"] * 200 + ["EEE"] * 200 + ["BBA"] * 200,
})

sns.set_theme(style="white")
plt.figure(figsize=(9, 4.5))
sns.kdeplot(data=df, x="marks", hue="dept", fill=True, alpha=0.35, linewidth=2,
            palette=["#7c3aed", "#0284c7", "#e11d48"])
sns.despine()
plt.title("Marks distribution by department", loc="left", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("ভায়োলিন প্লট",
       "সপ্তাহের প্রতিদিন ঘুমের ঘণ্টার বণ্টন; ভেতরে কোয়ার্টাইল দাগ।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(5)
days = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
base = [7.5, 6.6, 6.4, 6.5, 6.3, 6.8, 8.2]
df = pd.DataFrame([(d, rng.normal(b, 0.9)) for d, b in zip(days, base) for _ in range(80)],
                  columns=["day", "sleep"])

sns.set_theme(style="whitegrid")
plt.figure(figsize=(9, 4.5))
sns.violinplot(data=df, x="day", y="sleep", hue="day", palette="Purples", inner="quart", legend=False)
plt.ylabel("Hours of sleep")
plt.xlabel("")
plt.title("Sleep by day of week", loc="left", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("রিগ্রেশন রেখাসহ স্ক্যাটার",
       "পড়ার ঘণ্টা বনাম নম্বর; সাথে সবচেয়ে মানানসই সরলরেখা আর ৯৫% আস্থার ছায়া।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)
hours = rng.uniform(0, 10, 120)
df = pd.DataFrame({"study_hours": hours,
                   "marks": np.clip(40 + 5 * hours + rng.normal(0, 7, 120), 0, 100)})

sns.set_theme(style="ticks")
g = sns.jointplot(data=df, x="study_hours", y="marks", kind="reg", height=6,
                  color="#7c3aed", marginal_kws=dict(bins=15))
r = df.corr().iloc[0, 1]
g.ax_joint.text(0.3, 95, f"r = {r:.2f}", fontsize=12, fontweight="bold")
g.figure.suptitle("Study hours vs marks", y=1.02, fontweight="bold")
plt.show()'''),

    ex("কোরিলেশন হিটম্যাপ",
       "আবহাওয়ার ভ্যারিয়েবলগুলো একে অপরের সাথে কতটা সম্পর্কিত; শুধু নিচের ত্রিভুজ দেখানো।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(9)
n = 365
temp = rng.normal(28, 4, n)
humidity = 90 - 1.2 * temp + rng.normal(0, 5, n)
rain = np.clip(0.8 * humidity - 40 + rng.normal(0, 8, n), 0, None)
wind = rng.gamma(2, 2, n)
pressure = 1010 - 0.3 * rain + rng.normal(0, 3, n)
df = pd.DataFrame(dict(temp=temp, humidity=humidity, rain=rain, wind=wind, pressure=pressure))

corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.set_theme(style="white")
plt.figure(figsize=(7, 5.5))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            vmin=-1, vmax=1, square=True, linewidths=1, cbar_kws=dict(shrink=0.8))
plt.title("Weather variable correlations", loc="left", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("পেয়ারপ্লট",
       "চারটা মাপের প্রতিটা জোড়ার সম্পর্ক একসাথে; প্রজাতি অনুযায়ী রং।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
rows = []
for species, (bl, bd, fl) in {"Adelie": (39, 18, 190), "Gentoo": (47, 15, 217),
                              "Chinstrap": (49, 18.5, 196)}.items():
    for _ in range(70):
        rows.append(dict(species=species, bill_length=rng.normal(bl, 2.5),
                         bill_depth=rng.normal(bd, 1), flipper=rng.normal(fl, 6),
                         mass=rng.normal(fl * 22 - 600, 300)))
df = pd.DataFrame(rows)

sns.set_theme(style="ticks")
g = sns.pairplot(df, hue="species", palette=["#7c3aed", "#0d9488", "#e11d48"],
                 corner=True, plot_kws=dict(alpha=0.7, s=25), height=2.2)
g.figure.suptitle("Penguin measurements (sample data)", y=1.02, fontweight="bold")
plt.show()'''),

    ex("আস্থার ব্যবধানসহ বার চার্ট",
       "catplot দিয়ে বিভাগ ও লিঙ্গ অনুযায়ী গড় নম্বর; কালো দাগ = ৯৫% আস্থার ব্যবধান।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(12)
rows = [dict(dept=d, gender=g, marks=rng.normal(m + (3 if g == "F" else 0), 9))
        for d, m in [("CSE", 70), ("EEE", 66), ("BBA", 72), ("ENG", 68)]
        for g in ["F", "M"] for _ in range(40)]
df = pd.DataFrame(rows)

sns.set_theme(style="whitegrid")
g = sns.catplot(data=df, kind="bar", x="dept", y="marks", hue="gender",
                palette=["#e11d48", "#0284c7"], errorbar=("ci", 95),
                height=4.5, aspect=1.7, alpha=0.85)
g.set_axis_labels("", "Average marks")
g.figure.suptitle("Average marks by department and gender", x=0.05, ha="left", fontweight="bold")
plt.show()'''),

    ex("সোয়ার্ম + বক্স প্লট",
       "প্রতিটা বিন্দু আলাদা দেখা যায় এমন swarm প্লট, পেছনে হালকা বক্স প্লট।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(13)
df = pd.DataFrame({
    "method": np.repeat(["Lecture", "Video", "Group study", "Practice"], 45),
    "score": np.concatenate([rng.normal(m, 8, 45) for m in (64, 67, 72, 79)]),
})

sns.set_theme(style="whitegrid")
plt.figure(figsize=(9, 4.8))
sns.boxplot(data=df, x="method", y="score", color="#ede9fe", width=0.55, showfliers=False)
sns.swarmplot(data=df, x="method", y="score", hue="method", size=4,
              palette=["#a78bfa", "#8b5cf6", "#7c3aed", "#5b21b6"], legend=False)
plt.xlabel("")
plt.ylabel("Test score")
plt.title("Which study method works best?", loc="left", fontweight="bold")
plt.tight_layout()
plt.show()'''),

    ex("টাইম সিরিজ ও ছায়া পরিসর",
       "তিন বছরের দৈনিক বায়ুমান (AQI): প্রতিদিনের গড় রেখা আর বছরের পর বছর ছড়ানোর ছায়া।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(14)
rows = []
for year in [2024, 2025, 2026]:
    for month in range(1, 13):
        base = 220 - 140 * np.sin((month - 1) / 11 * np.pi)   # শীতে দূষণ বেশি
        for _ in range(20):
            rows.append(dict(month=month, year=str(year), aqi=base + rng.normal(0, 30) - (year - 2024) * 8))
df = pd.DataFrame(rows)

sns.set_theme(style="darkgrid")
plt.figure(figsize=(9, 4.5))
sns.lineplot(data=df, x="month", y="aqi", hue="year", errorbar="sd",
             palette=["#c4b5fd", "#8b5cf6", "#4c1d95"], linewidth=2.5)
plt.ylim(0, 320)
plt.axhspan(150, 320, color="#e11d48", alpha=0.07)
plt.text(1.2, 160, "Unhealthy", color="#e11d48")
plt.xticks(range(1, 13), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
plt.title("Dhaka air quality by month", loc="left", fontweight="bold")
plt.ylabel("AQI")
plt.tight_layout()
plt.show()'''),
)

man("seaborn",
    level="শুরু থেকে মাঝারি",
    tag="pandas টেবিল থেকে এক লাইনে সুন্দর পরিসংখ্যান চার্ট।",
    tasks=["দলভিত্তিক বণ্টন তুলনা (hist, kde, violin, box)", "দুই ভ্যারিয়েবলের সম্পর্ক ও রিগ্রেশন রেখা",
           "কোরিলেশন হিটম্যাপ", "অনেকগুলো ভ্যারিয়েবলের পেয়ারপ্লট", "আস্থার ব্যবধানসহ গড়ের তুলনা"],
    caps=["hue, col, row দিয়ে এক লাইনে দলভিত্তিক চার্ট", "নিজে থেকে গড়, আস্থার ব্যবধান, KDE হিসাব",
          "সুন্দর থিম ও রঙের প্যালেট (set_theme, color_palette)", "Matplotlib-এর উপর বানানো, তাই সব কিছু পরে বদলানো যায়"],
    limits=["ইন্টারঅ্যাকটিভ নয় (জুম/হোভার নেই)", "খুব বিশেষ ধরনের চার্টে Matplotlib-এ নামতে হয়",
            "load_dataset() নমুনা ডেটা আনতে ইন্টারনেট লাগে"],
    alt="matplotlib, plotly, plotnine, altair",
)


# ==================================================================
# JavaScript চার্ট লাইব্রেরি – সাইটের ভেতরেই লাইভ চলে
# ==================================================================

jslib("Chart.js",
    about=("Chart.js হলো সবচেয়ে জনপ্রিয় সহজ JavaScript চার্ট লাইব্রেরি। Canvas-এ বার, লাইন, পাই, "
           "রাডার চার্ট আঁকে, মোবাইলে নিজে থেকে মাপ বদলায়, হোভার করলে মান দেখায়।"),
    install='npm install chart.js\n<!-- অথবা HTML-এ: <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->',
    examples=[
        jsex("chartjs", "বৃষ্টি (বার) + তাপমাত্রা (লাইন)",
             "একই চার্টে দুই ধরনের ডেটা, দুই পাশে দুটো আলাদা অক্ষ।",
             '''const box = document.getElementById("app");
const canvas = document.createElement("canvas");
box.append(canvas);

new Chart(canvas, {
  type: "bar",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    datasets: [
      { label: "Rain (mm)", data: [7,28,65,150,280,330,380,310,300,170,30,10],
        backgroundColor: "rgba(124,58,237,.55)", borderRadius: 6, yAxisID: "y" },
      { type: "line", label: "Temp (°C)", data: [19,22,27,30,31,30,29,29,29,28,24,20],
        borderColor: "#e11d48", backgroundColor: "#e11d48", tension: 0.35, yAxisID: "y1" }
    ]
  },
  options: {
    maintainAspectRatio: false,
    interaction: { mode: "index", intersect: false },
    plugins: { title: { display: true, text: "Dhaka – rain and temperature" } },
    scales: {
      y:  { title: { display: true, text: "mm" } },
      y1: { position: "right", grid: { drawOnChartArea: false }, title: { display: true, text: "°C" } }
    }
  }
});''', hint="মাউস রাখো মান দেখতে, লেজেন্ডে চাপলে ডেটা লুকায়"),
        jsex("chartjs", "ডোনাট চার্ট",
             "মাসিক খরচের ভাগ; লেজেন্ডে চাপলে অংশ সরে যায় আর বাকিগুলো নতুন করে ভাগ হয়।",
             '''const canvas = document.createElement("canvas");
document.getElementById("app").append(canvas);

new Chart(canvas, {
  type: "doughnut",
  data: {
    labels: ["Rent", "Food", "Transport", "Study", "Internet", "Other"],
    datasets: [{
      data: [12000, 8000, 2500, 3000, 1000, 1500],
      backgroundColor: ["#7c3aed","#0284c7","#0d9488","#d97706","#e11d48","#94a3b8"],
      borderWidth: 3, hoverOffset: 14
    }]
  },
  options: {
    maintainAspectRatio: false,
    cutout: "62%",
    plugins: {
      legend: { position: "right" },
      title: { display: true, text: "Monthly budget (Tk)" }
    }
  }
});''', hint="লেজেন্ডের নামে চাপ দাও"),
        jsex("chartjs", "রাডার চার্ট",
             "দুই শিক্ষার্থীর ছয়টা দক্ষতা একসাথে তুলনা।",
             '''const canvas = document.createElement("canvas");
document.getElementById("app").append(canvas);

new Chart(canvas, {
  type: "radar",
  data: {
    labels: ["Python", "Math", "English", "Design", "Teamwork", "Writing"],
    datasets: [
      { label: "Rahim", data: [85, 70, 60, 45, 80, 55],
        borderColor: "#7c3aed", backgroundColor: "rgba(124,58,237,.2)" },
      { label: "Sumi", data: [65, 90, 80, 75, 60, 85],
        borderColor: "#0d9488", backgroundColor: "rgba(13,148,136,.2)" }
    ]
  },
  options: {
    maintainAspectRatio: false,
    scales: { r: { suggestedMin: 0, suggestedMax: 100 } }
  }
});'''),
    ],
    level="শুরু", tag="সহজ, সুন্দর Canvas চার্ট; কয়েক লাইনে বার, লাইন, পাই, রাডার।",
    tasks=["ওয়েবসাইট বা ড্যাশবোর্ডে ছোট-মাঝারি চার্ট", "বার + লাইন মেশানো চার্ট", "পাই, ডোনাট, রাডার, বাবল চার্ট",
           "রিয়েল-টাইমে ডেটা আপডেট (chart.update())"],
    caps=["৮ ধরনের মূল চার্ট, মেশানো যায়", "নিজে থেকে responsive আর animated", "plugin দিয়ে বাড়ানো যায় (zoom, annotation)"],
    limits=["হাজার হাজার বিন্দুতে ধীর; বড় ডেটায় uPlot বা ECharts ভালো", "ম্যাপ বা 3D নেই"],
    alt="Apache ECharts, ApexCharts, Plotly.js",
)

jslib("Apache ECharts",
    about=("Apache ECharts হলো খুব শক্তিশালী চার্ট লাইব্রেরি: সাধারণ চার্ট থেকে ক্যালেন্ডার হিটম্যাপ, "
           "Sankey, ম্যাপ, গেজ সব। বড় ডেটা দ্রুত আঁকে, জুম, টুলবক্স আর ছবি সেভ করার বাটন আগে থেকেই আছে।"),
    install='npm install echarts\n<!-- অথবা: <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script> -->',
    examples=[
        jsex("echarts", "জুম করা যায় এমন বার চার্ট",
             "৬০ দিনের বিক্রি; নিচের স্লাইডার দিয়ে সময়ের পরিসর বদলাও, টুলবক্সে ছবি সেভ।",
             '''const chart = echarts.init(document.getElementById("app"));
let seed = 3;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

const days = [], sales = [];
for (let i = 1; i <= 60; i++) {
  days.push("Day " + i);
  sales.push(Math.round(200 + i * 4 + rand() * 120));
}

chart.setOption({
  title: { text: "Daily sales", left: "center" },
  tooltip: { trigger: "axis" },
  toolbox: { feature: { dataZoom: {}, restore: {}, saveAsImage: {} } },
  xAxis: { type: "category", data: days },
  yAxis: { type: "value" },
  dataZoom: [{ type: "inside", start: 0, end: 50 }, { type: "slider", start: 0, end: 50 }],
  series: [{
    type: "bar", data: sales, itemStyle: { color: "#7c3aed", borderRadius: [4, 4, 0, 0] },
    markLine: { data: [{ type: "average", name: "Average" }] }
  }]
});
window.addEventListener("resize", () => chart.resize());''', hint="নিচের স্লাইডার টানো, চাকা ঘুরিয়ে জুম করো"),
        jsex("echarts", "ক্যালেন্ডার হিটম্যাপ",
             "সারা বছর প্রতিদিন কত ঘণ্টা পড়া হয়েছে – GitHub-এর contribution গ্রাফের মতো।",
             '''const chart = echarts.init(document.getElementById("app"));
let seed = 11;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

const data = [];
const start = Date.UTC(2026, 0, 1);
for (let i = 0; i < 365; i++) {
  const day = new Date(start + i * 86400000).toISOString().slice(0, 10);
  const weekend = [5, 6].includes(new Date(start + i * 86400000).getUTCDay());
  data.push([day, Math.round(rand() * (weekend ? 3 : 8))]);
}

chart.setOption({
  title: { text: "Study hours in 2026", left: "center" },
  tooltip: { formatter: p => p.value[0] + ": " + p.value[1] + " h" },
  visualMap: { min: 0, max: 8, orient: "horizontal", left: "center", bottom: 10,
               inRange: { color: ["#f3e8ff", "#7c3aed", "#2e1065"] } },
  calendar: { range: "2026", top: 60, left: 40, right: 20, cellSize: ["auto", 16] },
  series: [{ type: "heatmap", coordinateSystem: "calendar", data }]
});
window.addEventListener("resize", () => chart.resize());'''),
        jsex("echarts", "নাইটিঙ্গেল রোজ চার্ট",
             "পাইয়ের মতো, কিন্তু প্রতিটা ভাগের ব্যাসার্ধ মানের সমান – বড় পার্থক্য সহজে চোখে পড়ে।",
             '''const chart = echarts.init(document.getElementById("app"));

chart.setOption({
  title: { text: "Visitors by division", left: "center" },
  tooltip: { trigger: "item", formatter: "{b}: {c} ({d}%)" },
  legend: { bottom: 0 },
  series: [{
    type: "pie", roseType: "area", radius: [20, "70%"], center: ["50%", "48%"],
    itemStyle: { borderRadius: 6 },
    data: [
      { value: 40, name: "Dhaka" }, { value: 32, name: "Chattogram" },
      { value: 25, name: "Sylhet" }, { value: 20, name: "Khulna" },
      { value: 16, name: "Rajshahi" }, { value: 12, name: "Barishal" },
      { value: 9, name: "Rangpur" }, { value: 7, name: "Mymensingh" }
    ]
  }]
});
window.addEventListener("resize", () => chart.resize());'''),
    ],
    level="মাঝারি", tag="বড় ও সমৃদ্ধ চার্ট লাইব্রেরি: ক্যালেন্ডার, Sankey, ম্যাপ, গেজ, জুম, টুলবক্স।",
    tasks=["ইন্টারঅ্যাকটিভ ড্যাশবোর্ড", "ক্যালেন্ডার হিটম্যাপ, Sankey, গেজ, ট্রি-ম্যাপ", "লাখ বিন্দুর স্ক্যাটার (WebGL এক্সটেনশন)",
           "জুম, ছবি সেভ, ডেটা ভিউ টুলবক্স"],
    caps=["৪০+ ধরনের চার্ট", "dataZoom, visualMap, brush দিয়ে ইন্টারঅ্যাকশন", "Canvas বা SVG দুইভাবেই আঁকে", "pyecharts দিয়ে পাইথন থেকেও ব্যবহার"],
    limits=["ফাইলের আকার বড় (~১ MB); শুধু দরকারি অংশ বেছে বিল্ড করা যায়", "অপশন অনেক, শিখতে সময় লাগে"],
    alt="Chart.js, Plotly.js, ApexCharts",
)

jslib("Plotly.js",
    about=("Plotly.js দিয়ে ব্রাউজারে বৈজ্ঞানিক মানের ইন্টারঅ্যাকটিভ চার্ট: 3D সারফেস, কনট্যুর, ম্যাপ, "
           "সানবার্স্ট। জুম, ঘোরানো, হোভার, ছবি ডাউনলোড সব নিজে থেকেই আছে। Python-এর Plotly এটাই ব্যবহার করে।"),
    install='npm install plotly.js-dist-min\n<!-- অথবা: <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script> -->',
    examples=[
        jsex("plotly", "ঘোরানো যায় এমন 3D সারফেস",
             "sin(r)/r ঢেউ; মাউস দিয়ে টেনে ঘোরাও, স্ক্রল করে জুম।",
             '''const n = 60, xs = [], z = [];
for (let i = 0; i < n; i++) xs.push(-8 + (16 * i) / (n - 1));
for (const y of xs) {
  z.push(xs.map(x => {
    const r = Math.hypot(x, y) + 1e-9;
    return Math.sin(r) / r;
  }));
}

Plotly.newPlot("app", [{
  type: "surface", x: xs, y: xs, z, colorscale: "Viridis",
  contours: { z: { show: true, usecolormap: true, project: { z: true } } }
}], {
  title: "sin(r) / r",
  margin: { l: 0, r: 0, t: 40, b: 0 },
  scene: { camera: { eye: { x: 1.6, y: 1.6, z: 0.9 } } }
}, { responsive: true });''', hint="টেনে ঘোরাও"),
        jsex("plotly", "রেঞ্জ স্লাইডারসহ টাইম সিরিজ",
             "দুই বছরের দৈনিক তাপমাত্রা; নিচের ছোট চার্টে টেনে যেকোনো সময়ে জুম করা যায়।",
             '''const dates = [], dhaka = [], sylhet = [];
const start = Date.UTC(2025, 0, 1);
for (let i = 0; i < 730; i++) {
  dates.push(new Date(start + i * 86400000).toISOString().slice(0, 10));
  const season = Math.sin(((i % 365) / 365) * 2 * Math.PI - 1.4);
  dhaka.push(+(27 + 6 * season + Math.sin(i * 1.7) * 1.5).toFixed(1));
  sylhet.push(+(25 + 5 * season + Math.cos(i * 1.3) * 1.5).toFixed(1));
}

Plotly.newPlot("app", [
  { x: dates, y: dhaka, name: "Dhaka", line: { color: "#7c3aed" } },
  { x: dates, y: sylhet, name: "Sylhet", line: { color: "#0d9488" } }
], {
  title: "Daily temperature (°C)",
  hovermode: "x unified",
  margin: { t: 40, r: 10 },
  xaxis: { rangeslider: { visible: true },
           rangeselector: { buttons: [
             { count: 1, label: "1m", step: "month", stepmode: "backward" },
             { count: 6, label: "6m", step: "month", stepmode: "backward" },
             { step: "all", label: "all" } ] } }
}, { responsive: true });''', hint="উপরের 1m / 6m বাটনে চাপো"),
        jsex("plotly", "সানবার্স্ট",
             "খরচের খাত → উপখাত, স্তরে স্তরে; কোনো অংশে চাপলে সেটা বড় হয়ে খোলে।",
             '''Plotly.newPlot("app", [{
  type: "sunburst",
  labels:  ["Total", "Home", "Food", "Travel", "Rent", "Bills", "Market", "Restaurant", "Bus", "Rickshaw"],
  parents: ["", "Total", "Total", "Total", "Home", "Home", "Food", "Food", "Travel", "Travel"],
  values:  [0, 0, 0, 0, 12000, 2500, 6000, 2000, 1500, 1000],
  branchvalues: "remainder",
  marker: { colors: ["#fff", "#7c3aed", "#0d9488", "#d97706"] }
}], {
  title: "Where the money goes",
  margin: { t: 40, l: 0, r: 0, b: 0 }
}, { responsive: true });''', hint="কোনো অংশে চাপো"),
    ],
    level="মাঝারি", tag="ব্রাউজারে 3D, বৈজ্ঞানিক আর ইন্টারঅ্যাকটিভ চার্ট।",
    tasks=["3D সারফেস ও স্ক্যাটার", "রেঞ্জ স্লাইডারসহ টাইম সিরিজ", "সানবার্স্ট, ট্রিম্যাপ, ফানেল", "কনট্যুর ও হিটম্যাপ", "ম্যাপে ডেটা"],
    caps=["৪০+ চার্ট টাইপ, 3D সহ", "জুম, প্যান, হোভার, PNG ডাউনলোড আগে থেকে", "Python/R-এর Plotly একই JSON ব্যবহার করে"],
    limits=["পূর্ণ বিল্ড বড় (~৩.৫ MB); 'basic' বিল্ড ছোট", "খুব বেশি ডেটায় WebGL টাইপ (scattergl) দরকার"],
    alt="Apache ECharts, D3.js, Vega-Lite",
)

jslib("D3.js",
    about=("D3.js দিয়ে ডেটাকে সরাসরি SVG বা Canvas-এর আকৃতির সাথে জুড়ে দেওয়া যায়। তৈরি চার্ট নেই, কিন্তু "
           "স্কেল, অক্ষ, অ্যানিমেশন, ফোর্স লেআউট সব টুকরো আছে, তাই যেকোনো নতুন ধরনের ভিজুয়ালাইজেশন বানানো যায়।"),
    install='npm install d3\n<!-- অথবা: <script src="https://cdn.jsdelivr.net/npm/d3@7"></script> -->',
    examples=[
        jsex("d3", "অ্যানিমেটেড সাজানো বার চার্ট",
             "বাটনে চাপলে বারগুলো অ্যানিমেশন করে নতুন ক্রমে সাজে; ডেটা binding ও transition-এর ক্লাসিক উদাহরণ।",
             '''const data = [
  { name: "Dhaka", v: 23 }, { name: "Chattogram", v: 9 }, { name: "Khulna", v: 5 },
  { name: "Rajshahi", v: 4 }, { name: "Sylhet", v: 4 }, { name: "Rangpur", v: 3 },
  { name: "Barishal", v: 2 }, { name: "Mymensingh", v: 2.5 }
];
const app = d3.select("#app");
const btn = app.append("button").text("Sort ↓")
  .style("position", "absolute").style("right", "12px").style("top", "10px");
const W = 640, H = 380, m = { t: 40, r: 20, b: 40, l: 50 };
const svg = app.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%").style("height", "100%");

const x = d3.scaleBand().domain(data.map(d => d.name)).range([m.l, W - m.r]).padding(0.2);
const y = d3.scaleLinear().domain([0, 25]).nice().range([H - m.b, m.t]);
const color = d3.scaleSequential(d3.interpolatePurples).domain([-5, 25]);

const xAxis = svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x));
svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));
svg.append("text").attr("x", m.l).attr("y", 24).attr("font-weight", 700).text("Population (millions)");

const bars = svg.selectAll("rect").data(data, d => d.name).join("rect")
  .attr("x", d => x(d.name)).attr("width", x.bandwidth()).attr("rx", 4)
  .attr("y", H - m.b).attr("height", 0).attr("fill", d => color(d.v));
bars.transition().duration(900).delay((d, i) => i * 80)
  .attr("y", d => y(d.v)).attr("height", d => y(0) - y(d.v));

let sorted = false;
btn.on("click", () => {
  sorted = !sorted;
  btn.text(sorted ? "Original" : "Sort ↓");
  const order = sorted ? [...data].sort((a, b) => b.v - a.v) : data;
  x.domain(order.map(d => d.name));
  const t = svg.transition().duration(750);
  bars.transition(t).delay((d, i) => i * 40).attr("x", d => x(d.name));
  xAxis.transition(t).call(d3.axisBottom(x));
});''', hint="Sort বাটনে চাপো"),
        jsex("d3", "ফোর্স-ডিরেক্টেড নেটওয়ার্ক",
             "বন্ধুত্বের নেটওয়ার্ক; বিন্দুগুলো নিজে থেকে জায়গা খুঁজে নেয়, মাউস দিয়ে টেনে সরানো যায়।",
             '''const nodes = ["Rahim","Karim","Sumi","Riya","Tanvir","Nila","Arif","Mitu","Sakib","Joya","Rafi","Tania"]
  .map((id, i) => ({ id, group: i % 3 }));
const pairs = [[0,1],[0,2],[1,2],[2,3],[3,4],[4,5],[5,3],[6,7],[7,8],[8,6],[6,0],[9,10],[10,11],[11,9],[9,4],[1,7]];
const links = pairs.map(([a, b]) => ({ source: nodes[a].id, target: nodes[b].id }));

const W = 640, H = 400;
const svg = d3.select("#app").append("svg").attr("viewBox", [0, 0, W, H])
  .style("width", "100%").style("height", "100%");
const color = d3.scaleOrdinal(["#7c3aed", "#0d9488", "#e11d48"]);

const sim = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(70))
  .force("charge", d3.forceManyBody().strength(-220))
  .force("center", d3.forceCenter(W / 2, H / 2));

const link = svg.append("g").attr("stroke", "#c4b5fd").attr("stroke-width", 2)
  .selectAll("line").data(links).join("line");
const node = svg.append("g").selectAll("g").data(nodes).join("g").style("cursor", "grab")
  .call(d3.drag()
    .on("start", (e, d) => { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on("end", (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));
node.append("circle").attr("r", 13).attr("fill", d => color(d.group)).attr("stroke", "#fff").attr("stroke-width", 2);
node.append("text").text(d => d.id).attr("x", 16).attr("y", 4).attr("font-size", 12);

sim.on("tick", () => {
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${d.x},${d.y})`);
});''', hint="যেকোনো বিন্দু টেনে সরাও"),
        jsex("d3", "ক্রসহেয়ার টুলটিপসহ লাইন চার্ট",
             "মাউস যেখানে, সেই দিনের মান একটা উল্লম্ব দাগ আর বিন্দু দিয়ে দেখায়।",
             '''const W = 640, H = 380, m = { t: 30, r: 20, b: 35, l: 45 };
const data = d3.range(90).map(i => ({
  day: i + 1,
  aqi: Math.round(150 + 60 * Math.sin(i / 9) + 25 * Math.sin(i / 2.3))
}));

const svg = d3.select("#app").append("svg").attr("viewBox", [0, 0, W, H])
  .style("width", "100%").style("height", "100%");
const x = d3.scaleLinear().domain([1, 90]).range([m.l, W - m.r]);
const y = d3.scaleLinear().domain([0, d3.max(data, d => d.aqi)]).nice().range([H - m.b, m.t]);

svg.append("g").attr("transform", `translate(0,${H - m.b})`).call(d3.axisBottom(x));
svg.append("g").attr("transform", `translate(${m.l},0)`).call(d3.axisLeft(y));
svg.append("path").datum(data).attr("fill", "rgba(124,58,237,.12)")
  .attr("d", d3.area().x(d => x(d.day)).y0(y(0)).y1(d => y(d.aqi)).curve(d3.curveMonotoneX));
svg.append("path").datum(data).attr("fill", "none").attr("stroke", "#7c3aed").attr("stroke-width", 2.5)
  .attr("d", d3.line().x(d => x(d.day)).y(d => y(d.aqi)).curve(d3.curveMonotoneX));

const rule = svg.append("line").attr("stroke", "#140e29").attr("y1", m.t).attr("y2", H - m.b).style("opacity", 0);
const dot = svg.append("circle").attr("r", 5).attr("fill", "#e11d48").style("opacity", 0);
const label = svg.append("text").attr("font-weight", 700).style("opacity", 0);

svg.on("pointermove", e => {
  const [px] = d3.pointer(e);
  const d = data[Math.max(0, Math.min(89, Math.round(x.invert(px)) - 1))];
  rule.attr("x1", x(d.day)).attr("x2", x(d.day)).style("opacity", 0.4);
  dot.attr("cx", x(d.day)).attr("cy", y(d.aqi)).style("opacity", 1);
  label.attr("x", x(d.day) + 8).attr("y", y(d.aqi) - 10).text(`Day ${d.day}: AQI ${d.aqi}`).style("opacity", 1);
}).on("pointerleave", () => { rule.style("opacity", 0); dot.style("opacity", 0); label.style("opacity", 0); });''',
             hint="চার্টের উপর মাউস নাড়াও"),
    ],
    level="উন্নত", tag="ডেটা দিয়ে SVG/Canvas চালানো: যেকোনো কাস্টম ভিজুয়ালাইজেশন।",
    tasks=["কাস্টম ও অ্যানিমেটেড চার্ট", "ফোর্স নেটওয়ার্ক, ট্রি, Sankey", "মানচিত্র (d3-geo)", "স্ক্রলিটেলিং ও ডেটা জার্নালিজম"],
    caps=["scale, axis, shape, transition, force – সব আলাদা মডিউল", "যেকোনো DOM/SVG উপাদান ডেটার সাথে জোড়া", "জুম, ড্র্যাগ, ব্রাশ"],
    limits=["তৈরি চার্ট নেই – সব নিজে বানাতে হয়", "শিখতে সময় লাগে", "সাধারণ চার্টের জন্য Chart.js বা Observable Plot সহজ"],
    alt="Observable Plot, Vega-Lite, Apache ECharts",
)

jslib("ApexCharts",
    about=("ApexCharts দিয়ে আধুনিক দেখতে SVG চার্ট বানানো যায়: এরিয়া, বার, রেডিয়াল গেজ, হিটম্যাপ। "
           "জুম, টুলবার, annotation আর সুন্দর অ্যানিমেশন আগে থেকেই আছে।"),
    install='npm install apexcharts\n<!-- অথবা: <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script> -->',
    examples=[
        jsex("apex", "জুমসহ এরিয়া চার্ট ও annotation",
             "ওয়েবসাইটের দৈনিক ভিজিটর; একটা বিশেষ দিনে annotation, টুলবারে জুম আর ডাউনলোড।",
             '''const visits = [];
for (let i = 0; i < 60; i++) {
  visits.push([Date.UTC(2026, 5, 1) + i * 86400000,
               Math.round(400 + i * 12 + 120 * Math.sin(i / 3) + (i === 41 ? 900 : 0))]);
}

new ApexCharts(document.getElementById("app"), {
  chart: { type: "area", height: "100%", zoom: { enabled: true }, toolbar: { show: true } },
  series: [{ name: "Visitors", data: visits }],
  xaxis: { type: "datetime" },
  colors: ["#7c3aed"],
  dataLabels: { enabled: false },
  stroke: { curve: "smooth", width: 2.5 },
  fill: { type: "gradient", gradient: { opacityFrom: 0.5, opacityTo: 0.05 } },
  title: { text: "Website visitors" },
  annotations: { xaxis: [{ x: visits[41][0], borderColor: "#e11d48",
                           label: { text: "Post went viral", style: { background: "#e11d48", color: "#fff" } } }] }
}).render();''', hint="চার্টে টেনে জুম করো"),
        jsex("apex", "রেডিয়াল গেজ",
             "তিনটা লক্ষ্যের অগ্রগতি % – গোল রিং আকারে, মাঝে গড়।",
             '''new ApexCharts(document.getElementById("app"), {
  chart: { type: "radialBar", height: "100%" },
  series: [82, 64, 45],
  labels: ["Course", "Project", "Thesis"],
  colors: ["#7c3aed", "#0d9488", "#e11d48"],
  plotOptions: {
    radialBar: {
      hollow: { size: "35%" },
      track: { background: "#f3e8ff" },
      dataLabels: {
        name: { fontSize: "16px" },
        value: { fontSize: "22px", formatter: v => v + "%" },
        total: { show: true, label: "Average", formatter: w =>
          Math.round(w.globals.series.reduce((a, b) => a + b, 0) / w.globals.series.length) + "%" }
      }
    }
  },
  legend: { show: true, position: "bottom" }
}).render();'''),
    ],
    level="শুরু থেকে মাঝারি", tag="আধুনিক, অ্যানিমেটেড SVG চার্ট; ড্যাশবোর্ডের জন্য দারুণ।",
    tasks=["অ্যাডমিন ড্যাশবোর্ড", "রেডিয়াল গেজ ও প্রগ্রেস", "annotation দেওয়া টাইম সিরিজ", "হিটম্যাপ ও ক্যান্ডেলস্টিক"],
    caps=["জুম, প্যান, টুলবার, CSV/PNG ডাউনলোড", "annotation (রেখা, বিন্দু, লেবেল)", "React/Vue র‍্যাপার আছে"],
    limits=["SVG বলে খুব বেশি বিন্দুতে ধীর", "3D বা ম্যাপ নেই"],
    alt="Chart.js, Apache ECharts",
)

jslib("Vega-Lite",
    about=("Vega-Lite-এ কোড না লিখে JSON-এ বলে দাও: কোন কলাম x, কোনটা y, কোনটা রং – চার্ট নিজে তৈরি হয়। "
           "এক চার্টে নির্বাচন করলে আরেক চার্ট বদলায় (linked view)। Python-এর Altair এটাই তৈরি করে।"),
    install='npm install vega vega-lite vega-embed\n<!-- অথবা CDN থেকে vega, vega-lite, vega-embed তিনটাই -->',
    examples=[
        jsex("vega", "ব্রাশ দিয়ে লিংক করা দুটো চার্ট",
             "উপরের স্ক্যাটারে মাউস দিয়ে একটা এলাকা বাছাই করো – নিচের বার চার্ট শুধু সেই অংশের হিসাব দেখাবে।",
             '''const data = [];
let seed = 5;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (const [dept, base] of [["CSE", 70], ["EEE", 62], ["BBA", 66]]) {
  for (let i = 0; i < 40; i++) {
    const hours = rand() * 10;
    data.push({ dept, hours: +hours.toFixed(1), marks: Math.round(base - 15 + hours * 4 + rand() * 12) });
  }
}

vegaEmbed("#app", {
  $schema: "https://vega.github.io/schema/vega-lite/v5.json",
  data: { values: data },
  vconcat: [{
    width: "container", height: 190,
    params: [{ name: "brush", select: "interval" }],
    mark: { type: "point", filled: true, size: 60 },
    encoding: {
      x: { field: "hours", type: "quantitative", title: "Study hours" },
      y: { field: "marks", type: "quantitative", scale: { zero: false } },
      color: { condition: { param: "brush", field: "dept", type: "nominal" }, value: "#ddd" }
    }
  }, {
    width: "container", height: 90,
    transform: [{ filter: { param: "brush" } }],
    mark: "bar",
    encoding: {
      y: { field: "dept", type: "nominal", title: null },
      x: { aggregate: "count", title: "Students selected" },
      color: { field: "dept", type: "nominal", legend: null }
    }
  }]
}, { actions: false });''', hint="উপরের চার্টে টেনে আয়তক্ষেত্র আঁকো"),
        jsex("vega", "স্তূপ করা বার চার্ট",
             "মাস অনুযায়ী বিদ্যুতের উৎস; শুধু JSON-এ x, y, রং বলে দেওয়া হয়েছে।",
             '''const months = ["Jan","Feb","Mar","Apr","May","Jun"];
const mix = { Gas: [60,58,55,52,50,49], Coal: [15,16,18,20,21,22], Solar: [3,4,5,6,7,8], Import: [10,10,11,11,12,12] };
const values = [];
for (const [source, arr] of Object.entries(mix)) {
  arr.forEach((v, i) => values.push({ month: months[i], source, share: v }));
}

vegaEmbed("#app", {
  $schema: "https://vega.github.io/schema/vega-lite/v5.json",
  title: "Electricity by source (TWh, sample)",
  width: "container", height: 300,
  data: { values },
  mark: { type: "bar", cornerRadiusEnd: 3 },
  encoding: {
    x: { field: "month", type: "ordinal", sort: months, title: null },
    y: { field: "share", type: "quantitative", stack: "zero", title: "TWh" },
    color: { field: "source", type: "nominal",
             scale: { range: ["#7c3aed", "#475569", "#d97706", "#0d9488"] } },
    tooltip: [{ field: "source" }, { field: "share" }]
  }
}, { actions: false });'''),
    ],
    level="শুরু থেকে মাঝারি", tag="JSON লিখলেই চার্ট: গ্রামার অব গ্রাফিক্স, linked selection।",
    tasks=["ডেটা এক্সপ্লোরেশন", "এক চার্টে বাছাই করে আরেক চার্ট ফিল্টার", "ফ্যাসেট (ছোট ছোট অনেক চার্ট)", "নোটবুক ও রিপোর্টে এম্বেড"],
    caps=["encoding: x, y, color, size, shape, tooltip", "params দিয়ে brush, click, slider", "Altair (Python) এর আউটপুট এটাই"],
    limits=["খুব কাস্টম ডিজাইনে সীমাবদ্ধ", "বড় ডেটা পুরোটা ব্রাউজারে যায়"],
    alt="Observable Plot, D3.js, Plotly.js",
)

jslib("Observable Plot",
    about=("Observable Plot হলো D3-এর নির্মাতাদের বানানো সংক্ষিপ্ত চার্ট লাইব্রেরি: Plot.dot, Plot.line, Plot.barY "
           "এর মতো 'mark' দিয়ে এক-দুই লাইনে পরিসংখ্যান চার্ট। টুলটিপ (tip) নিজে থেকে।"),
    install='npm install @observablehq/plot\n<!-- CDN: আগে d3, তারপর @observablehq/plot -->',
    examples=[
        jsex("plot", "টুলটিপসহ স্ক্যাটার ও ট্রেন্ড",
             "উচ্চতা বনাম ওজন; লিঙ্গ অনুযায়ী রং, প্রতিটা দলের জন্য রিগ্রেশন রেখা।",
             '''let seed = 9;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const people = d3.range(160).map(i => {
  const sex = i % 2 ? "F" : "M";
  const height = (sex === "M" ? 168 : 155) + (rand() - 0.5) * 22;
  return { sex, height: +height.toFixed(1), weight: +(height * 0.9 - 88 + (rand() - 0.5) * 18).toFixed(1) };
});

const chart = Plot.plot({
  width: 640, height: 380, grid: true,
  color: { legend: true, range: ["#7c3aed", "#e11d48"] },
  x: { label: "Height (cm)" }, y: { label: "Weight (kg)" },
  marks: [
    Plot.dot(people, { x: "height", y: "weight", stroke: "sex", r: 3.5, tip: true }),
    Plot.linearRegressionY(people, { x: "height", y: "weight", stroke: "sex" })
  ]
});
document.getElementById("app").append(chart);''', hint="বিন্দুর উপর মাউস রাখো"),
        jsex("plot", "হিস্টোগ্রাম (binX)",
             "নম্বরের বণ্টন – কাঁচা ডেটা দিলে Plot নিজেই ঘরে ভাগ করে গোনে।",
             '''let seed = 21;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const normal = () => Math.sqrt(-2 * Math.log(rand())) * Math.cos(2 * Math.PI * rand());
const marks = d3.range(500).map(() => ({ score: Math.max(0, Math.min(100, 65 + normal() * 12)) }));

document.getElementById("app").append(Plot.plot({
  width: 640, height: 360,
  y: { grid: true, label: "Students" },
  x: { label: "Marks" },
  marks: [
    Plot.rectY(marks, Plot.binX({ y: "count" }, { x: "score", thresholds: 25, fill: "#7c3aed", tip: true })),
    Plot.ruleX([d3.mean(marks, d => d.score)], { stroke: "#e11d48", strokeWidth: 2, strokeDasharray: "4 3" }),
    Plot.ruleY([0])
  ]
}));'''),
    ],
    level="শুরু", tag="এক-দুই লাইনে পরিসংখ্যান চার্ট; D3-এর সহজ রূপ।",
    tasks=["দ্রুত ডেটা এক্সপ্লোরেশন", "হিস্টোগ্রাম, বক্স, স্ক্যাটার, রিগ্রেশন", "ফ্যাসেট চার্ট", "টুলটিপসহ রিপোর্ট চার্ট"],
    caps=["mark + transform (binX, groupY, windowY…)", "স্বয়ংক্রিয় স্কেল ও লেজেন্ড", "SVG আউটপুট, যেকোনো পেজে বসানো যায়"],
    limits=["অ্যানিমেশন ও জটিল ইন্টারঅ্যাকশন কম", "3D নেই"],
    alt="Vega-Lite, D3.js, Chart.js",
)

jslib("uPlot",
    about=("uPlot হলো খুব ছোট (~৫০ KB) আর খুব দ্রুত টাইম-সিরিজ চার্ট। লাখ লাখ বিন্দুও এক পলকে আঁকে, "
           "তাই সেন্সর ডেটা, মনিটরিং ড্যাশবোর্ডের জন্য আদর্শ।"),
    install='npm install uplot\n<!-- CDN: uPlot.iife.min.js + uPlot.min.css -->',
    examples=[
        jsex("uplot", "৫০,০০০ বিন্দুর সেন্সর ডেটা",
             "তিনটা সেন্সরের ৫০ হাজার রিডিং একসাথে, তবু তাৎক্ষণিক; টেনে জুম, ডাবল-ক্লিকে রিসেট।",
             '''const n = 50000, t0 = Date.UTC(2026, 0, 1) / 1000;
const xs = new Float64Array(n), a = new Float64Array(n), b = new Float64Array(n), c = new Float64Array(n);
for (let i = 0; i < n; i++) {
  xs[i] = t0 + i * 60;                       // প্রতি মিনিটে একটা রিডিং
  a[i] = 25 + 5 * Math.sin(i / 1440 * 2 * Math.PI) + Math.sin(i / 7) * 0.8;
  b[i] = 22 + 4 * Math.sin(i / 1440 * 2 * Math.PI + 1) + Math.cos(i / 5) * 0.8;
  c[i] = 18 + 3 * Math.sin(i / 1440 * 2 * Math.PI + 2) + Math.sin(i / 3) * 0.6;
}

const app = document.getElementById("app");
const t = performance.now();
const plot = new uPlot({
  title: "50,000 sensor readings",
  width: app.clientWidth, height: app.clientHeight - 30,
  scales: { x: { time: true } },
  series: [
    {},
    { label: "Room A °C", stroke: "#7c3aed", width: 1 },
    { label: "Room B °C", stroke: "#0d9488", width: 1 },
    { label: "Room C °C", stroke: "#e11d48", width: 1 }
  ]
}, [xs, a, b, c], app);
const info = document.createElement("div");
info.style.cssText = "position:absolute;right:10px;top:6px;font:12px monospace;color:#6b6288";
info.textContent = "drawn in " + Math.round(performance.now() - t) + " ms";
app.append(info);
window.addEventListener("resize", () => plot.setSize({ width: app.clientWidth, height: app.clientHeight - 30 }));''',
             hint="টেনে জুম, ডাবল-ক্লিকে রিসেট"),
    ],
    level="মাঝারি", tag="ক্ষুদ্র ও অতি-দ্রুত টাইম-সিরিজ চার্ট।",
    tasks=["সেন্সর ও IoT ডেটা", "সার্ভার মনিটরিং ড্যাশবোর্ড", "লাইভ স্ট্রিমিং চার্ট", "লাখ বিন্দুর লাইন চার্ট"],
    caps=["~৫০ KB, কোনো নির্ভরতা নেই", "লাখ লাখ বিন্দু মিলিসেকেন্ডে", "জুম, কার্সর, সিঙ্ক করা একাধিক চার্ট"],
    limits=["শুধু লাইন/এরিয়া/বার ধরনের চার্ট", "সাজসজ্জার অপশন কম"],
    alt="Chart.js, Plotly.js, Apache ECharts",
)

# ---------- Python লাইব্রেরি, যাদের আউটপুট ব্রাউজারেও একই চার্ট ----------

more("plotly",
    ex("রেঞ্জ স্লাইডারসহ লাইন চার্ট",
       "দুই বছরের দৈনিক তাপমাত্রা, নিচে রেঞ্জ স্লাইডার। ডানে একই চার্ট ব্রাউজারে লাইভ (Plotly Python ভেতরে plotly.js-ই চালায়)।",
       '''import math
from datetime import date, timedelta
import plotly.graph_objects as go

start = date(2025, 1, 1)
dates, dhaka, sylhet = [], [], []
for i in range(730):
    dates.append(start + timedelta(days=i))
    season = math.sin((i % 365) / 365 * 2 * math.pi - 1.4)
    dhaka.append(round(27 + 6 * season + math.sin(i * 1.7) * 1.5, 1))
    sylhet.append(round(25 + 5 * season + math.cos(i * 1.3) * 1.5, 1))

fig = go.Figure()
fig.add_scatter(x=dates, y=dhaka, name="Dhaka", line_color="#7c3aed")
fig.add_scatter(x=dates, y=sylhet, name="Sylhet", line_color="#0d9488")
fig.update_layout(title="Daily temperature (°C)", hovermode="x unified")
fig.update_xaxes(rangeslider_visible=True,
                 rangeselector=dict(buttons=[
                     dict(count=1, label="1m", step="month", stepmode="backward"),
                     dict(count=6, label="6m", step="month", stepmode="backward"),
                     dict(step="all", label="all")]))
fig.write_html("temperature.html")   # ব্রাউজারে খোলো
fig.show()''',
       hint="লাইভ চার্ট: plotly.js দিয়ে একই ডেটা",
       live=live("plotly", '''const dates = [], dhaka = [], sylhet = [];
const start = Date.UTC(2025, 0, 1);
for (let i = 0; i < 730; i++) {
  dates.push(new Date(start + i * 86400000).toISOString().slice(0, 10));
  const season = Math.sin(((i % 365) / 365) * 2 * Math.PI - 1.4);
  dhaka.push(+(27 + 6 * season + Math.sin(i * 1.7) * 1.5).toFixed(1));
  sylhet.push(+(25 + 5 * season + Math.cos(i * 1.3) * 1.5).toFixed(1));
}
Plotly.newPlot("app", [
  { x: dates, y: dhaka, name: "Dhaka", line: { color: "#7c3aed" } },
  { x: dates, y: sylhet, name: "Sylhet", line: { color: "#0d9488" } }
], { title: "Daily temperature (°C)", hovermode: "x unified", margin: { t: 40, r: 10 },
  xaxis: { rangeslider: { visible: true }, rangeselector: { buttons: [
    { count: 1, label: "1m", step: "month", stepmode: "backward" },
    { count: 6, label: "6m", step: "month", stepmode: "backward" },
    { step: "all", label: "all" } ] } } }, { responsive: true });''')),
    ex("ঘোরানো যায় এমন 3D সারফেস",
       "sin(r)/r সারফেস, নিচে কনট্যুরের ছায়া। ব্রাউজারে মাউস দিয়ে ঘোরানো যায়।",
       '''import numpy as np
import plotly.graph_objects as go

x = np.linspace(-8, 8, 60)
X, Y = np.meshgrid(x, x)
R = np.hypot(X, Y) + 1e-9
Z = np.sin(R) / R

fig = go.Figure(go.Surface(x=x, y=x, z=Z, colorscale="Viridis",
                           contours_z=dict(show=True, usecolormap=True, project_z=True)))
fig.update_layout(title="sin(r) / r", margin=dict(l=0, r=0, t=40, b=0),
                  scene_camera=dict(eye=dict(x=1.6, y=1.6, z=0.9)))
fig.write_html("surface.html")
fig.show()''',
       hint="লাইভ চার্ট: টেনে ঘোরাও",
       live=live("plotly", '''const n = 60, xs = [], z = [];
for (let i = 0; i < n; i++) xs.push(-8 + (16 * i) / (n - 1));
for (const y of xs) z.push(xs.map(x => { const r = Math.hypot(x, y) + 1e-9; return Math.sin(r) / r; }));
Plotly.newPlot("app", [{ type: "surface", x: xs, y: xs, z, colorscale: "Viridis",
  contours: { z: { show: true, usecolormap: true, project: { z: true } } } }],
  { title: "sin(r) / r", margin: { l: 0, r: 0, t: 40, b: 0 },
    scene: { camera: { eye: { x: 1.6, y: 1.6, z: 0.9 } } } }, { responsive: true });''')),
)

man("plotly",
    level="শুরু থেকে মাঝারি",
    tag="ইন্টারঅ্যাকটিভ চার্ট: হোভার, জুম, ঘোরানো; HTML ফাইলে সেভ করে যে কাউকে পাঠানো যায়।",
    tasks=["ইন্টারঅ্যাকটিভ HTML রিপোর্ট", "3D সারফেস ও স্ক্যাটার", "টাইম সিরিজ রেঞ্জ স্লাইডারসহ", "ম্যাপ ও choropleth", "Dash দিয়ে পুরো ওয়েব ড্যাশবোর্ড"],
    caps=["plotly.express: এক লাইনে চার্ট", "graph_objects: সব কিছু নিজে নিয়ন্ত্রণ", "write_html / write_image (kaleido দিয়ে PNG)", "Jupyter-এ সরাসরি ইন্টারঅ্যাকটিভ"],
    limits=["HTML ফাইল বড় হয় (plotly.js ভেতরে থাকে); include_plotlyjs='cdn' দিলে ছোট", "PNG সেভ করতে kaleido আলাদা ইনস্টল"],
    alt="Plotly.js, bokeh, altair, matplotlib",
)

DETAILS["altair"] = dict(
    about=("Altair দিয়ে পাইথনে ঘোষণামূলক (declarative) চার্ট বানানো যায়: কোন কলাম x, কোনটা y, কোনটা রং – "
           "শুধু এটুকু বললেই হয়। আউটপুট হলো Vega-Lite JSON, তাই চার্টগুলো ব্রাউজারে ইন্টারঅ্যাকটিভ।"),
    install="pip install altair pandas",
    examples=[
        ex("ব্রাশ দিয়ে লিংক করা চার্ট",
           "উপরের স্ক্যাটারে এলাকা বাছাই করলে নিচের বার চার্ট শুধু সেই শিক্ষার্থীদের গোনে। লাইভ চার্টটা ঠিক এই কোড থেকে তৈরি হওয়া Vega-Lite।",
           '''import random
import altair as alt
import pandas as pd

random.seed(5)
rows = []
for dept, base in [("CSE", 70), ("EEE", 62), ("BBA", 66)]:
    for _ in range(40):
        hours = random.random() * 10
        rows.append(dict(dept=dept, hours=round(hours, 1),
                         marks=round(base - 15 + hours * 4 + random.random() * 12)))
df = pd.DataFrame(rows)

brush = alt.selection_interval()
points = alt.Chart(df).mark_point(filled=True, size=60).encode(
    x=alt.X("hours:Q", title="Study hours"),
    y=alt.Y("marks:Q", scale=alt.Scale(zero=False)),
    color=alt.condition(brush, "dept:N", alt.value("#ddd")),
).add_params(brush).properties(width=500, height=190)

bars = alt.Chart(df).mark_bar().encode(
    y=alt.Y("dept:N", title=None),
    x=alt.X("count():Q", title="Students selected"),
    color=alt.Color("dept:N", legend=None),
).transform_filter(brush).properties(width=500, height=90)

chart = points & bars            # & মানে উপরে-নিচে
chart.save("linked.html")''',
           hint="লাইভ: উপরের চার্টে টেনে আয়তক্ষেত্র আঁকো",
           live=live("vega", '''const data = [];
let seed = 5;
const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (const [dept, base] of [["CSE", 70], ["EEE", 62], ["BBA", 66]]) {
  for (let i = 0; i < 40; i++) {
    const hours = rand() * 10;
    data.push({ dept, hours: +hours.toFixed(1), marks: Math.round(base - 15 + hours * 4 + rand() * 12) });
  }
}
vegaEmbed("#app", { $schema: "https://vega.github.io/schema/vega-lite/v5.json", data: { values: data },
  vconcat: [{ width: "container", height: 190, params: [{ name: "brush", select: "interval" }],
    mark: { type: "point", filled: true, size: 60 },
    encoding: { x: { field: "hours", type: "quantitative", title: "Study hours" },
      y: { field: "marks", type: "quantitative", scale: { zero: false } },
      color: { condition: { param: "brush", field: "dept", type: "nominal" }, value: "#ddd" } } },
  { width: "container", height: 90, transform: [{ filter: { param: "brush" } }], mark: "bar",
    encoding: { y: { field: "dept", type: "nominal", title: null },
      x: { aggregate: "count", title: "Students selected" },
      color: { field: "dept", type: "nominal", legend: null } } }] }, { actions: false });''')),
        ex("স্তূপ করা বার ও টুলটিপ",
           "মাস অনুযায়ী বিদ্যুতের উৎস; শুধু encode() দিয়ে x, y, রং, টুলটিপ বলে দেওয়া।",
           '''import altair as alt
import pandas as pd

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
mix = {"Gas": [60, 58, 55, 52, 50, 49], "Coal": [15, 16, 18, 20, 21, 22],
       "Solar": [3, 4, 5, 6, 7, 8], "Import": [10, 10, 11, 11, 12, 12]}
df = pd.DataFrame([dict(month=m, source=s, share=v)
                   for s, vals in mix.items() for m, v in zip(months, vals)])

chart = alt.Chart(df, title="Electricity by source (TWh, sample)").mark_bar(cornerRadiusEnd=3).encode(
    x=alt.X("month:O", sort=months, title=None),
    y=alt.Y("share:Q", stack="zero", title="TWh"),
    color=alt.Color("source:N", scale=alt.Scale(range=["#7c3aed", "#475569", "#d97706", "#0d9488"])),
    tooltip=["source", "share"],
).properties(width=500, height=300)

chart.save("energy.html")
print(chart.to_json()[:300], "...")     # ভেতরে আসলে Vega-Lite JSON''',
           hint="লাইভ: বারের উপর মাউস রাখো",
           live=live("vega", '''const months = ["Jan","Feb","Mar","Apr","May","Jun"];
const mix = { Gas: [60,58,55,52,50,49], Coal: [15,16,18,20,21,22], Solar: [3,4,5,6,7,8], Import: [10,10,11,11,12,12] };
const values = [];
for (const [source, arr] of Object.entries(mix)) arr.forEach((v, i) => values.push({ month: months[i], source, share: v }));
vegaEmbed("#app", { $schema: "https://vega.github.io/schema/vega-lite/v5.json",
  title: "Electricity by source (TWh, sample)", width: "container", height: 300, data: { values },
  mark: { type: "bar", cornerRadiusEnd: 3 },
  encoding: { x: { field: "month", type: "ordinal", sort: months, title: null },
    y: { field: "share", type: "quantitative", stack: "zero", title: "TWh" },
    color: { field: "source", type: "nominal", scale: { range: ["#7c3aed", "#475569", "#d97706", "#0d9488"] } },
    tooltip: [{ field: "source" }, { field: "share" }] } }, { actions: false });''')),
    ],
)
man("altair",
    level="শুরু থেকে মাঝারি",
    tag="পাইথনে ঘোষণামূলক চার্ট; আউটপুট Vega-Lite, তাই ব্রাউজারে ইন্টারঅ্যাকটিভ।",
    tasks=["pandas ডেটার দ্রুত এক্সপ্লোরেশন", "লিংক করা ইন্টারঅ্যাকটিভ চার্ট", "ফ্যাসেট চার্ট", "HTML/PNG/SVG রিপোর্ট"],
    caps=["encode(): x, y, color, size, tooltip", "selection_interval / point দিয়ে ইন্টারঅ্যাকশন", "চার্ট জোড়া: | পাশাপাশি, & উপরে-নিচে, + স্তর"],
    limits=["ডিফল্টে ৫০০০ সারির বেশি ডেটায় সতর্কতা (alt.data_transformers)", "PNG সেভে vl-convert লাগে"],
    alt="Vega-Lite, plotly, matplotlib",
)


# ==================================================================
# শোকেস: জটিল ও সুন্দর চার্ট (Matplotlib, seaborn, NetworkX)
# ==================================================================

SHOW = "শোকেস"

more("matplotlib",
    ex("রিজলাইন: মাসভিত্তিক তাপমাত্রা",
       "১২ মাসের দৈনিক তাপমাত্রার বণ্টন একটার পেছনে আরেকটা পাহাড়ের মতো সাজানো; অন্ধকার পটভূমি আর plasma রঙে। KDE শুধু NumPy দিয়ে হিসাব করা।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
means = [18, 21, 26, 29, 30, 29.5, 29, 29, 28.5, 27, 23, 19]
spread = [3.2, 3.4, 3.0, 2.6, 2.4, 1.8, 1.5, 1.5, 1.7, 2.2, 2.8, 3.1]
grid = np.linspace(8, 40, 400)

def kde(x, grid, bw=0.9):
    z = (grid[:, None] - x[None, :]) / bw
    return np.exp(-0.5 * z ** 2).sum(1) / (len(x) * bw * np.sqrt(2 * np.pi))

bg = "#0f0c1d"
fig, ax = plt.subplots(figsize=(10, 9), facecolor=bg)
ax.set_facecolor(bg)
cmap = plt.get_cmap("plasma")
gap = 0.11

for i, (m, mu, sd) in enumerate(zip(months, means, spread)):
    temps = np.concatenate([rng.normal(mu, sd, 280), rng.normal(mu + sd * 1.3, sd * 0.6, 60)])
    y = kde(temps, grid)
    base = (11 - i) * gap
    color = cmap(0.15 + 0.75 * (mu - 18) / 12)
    ax.fill_between(grid, base, base + y, color=color, alpha=0.92, zorder=20 - i)
    ax.plot(grid, base + y, color="white", lw=1.2, zorder=20 - i)
    ax.plot(grid, np.full_like(grid, base), color=bg, lw=2, zorder=20 - i)
    ax.text(9, base + 0.02, m, color="white", fontsize=11, fontweight="bold", zorder=30)
    ax.text(39.5, base + 0.02, f"{temps.mean():.1f}°", color="#e9e5ff", fontsize=10,
            ha="right", zorder=30)

ax.set_xlim(8, 40)
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(colors="#b9b3d6")
ax.set_xlabel("Daily temperature (°C)", color="#b9b3d6", fontsize=11)
fig.text(0.07, 0.94, "A year of heat in Dhaka", color="white", fontsize=22, fontweight="bold")
fig.text(0.07, 0.915, "Distribution of daily temperatures by month (sample data)",
         color="#b9b3d6", fontsize=12)
plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.07)
plt.show()''', hint=SHOW),

    ex("বৃত্তাকার বার চার্ট",
       "১২ মাসের বৃষ্টি একটা ঘড়ির মতো বৃত্তে; বারের রং মান অনুযায়ী, লেবেলগুলো বৃত্তের বাইরে ঘুরিয়ে বসানো, মাঝে বছরের মোট।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rain = np.array([7, 28, 65, 150, 280, 330, 380, 310, 300, 170, 30, 10])

n = len(rain)
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
width = 2 * np.pi / n * 0.82
inner = 210                                   # মাঝের ফাঁকা বৃত্ত
norm = colors.Normalize(rain.min(), rain.max())
cmap = plt.get_cmap("cool")

fig = plt.figure(figsize=(8.5, 8.5), facecolor="#faf7ff")
ax = fig.add_subplot(projection="polar", facecolor="#faf7ff")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
bars = ax.bar(theta, rain, width=width, bottom=inner,
              color=[cmap(norm(v)) for v in rain], edgecolor="white", linewidth=2)

for t, v, m in zip(theta, rain, months):
    angle = np.degrees(t)
    rot = 90 - angle if angle <= 180 else 270 - angle
    align = "left" if angle <= 180 else "right"
    ax.text(t, inner + v + 18, f"{m}  {v}", rotation=rot, rotation_mode="anchor",
            ha=align, va="center", fontsize=10.5, color="#2e1065", fontweight="bold")

for r in (100, 200, 300):
    ax.plot(np.linspace(0, 2 * np.pi, 200), np.full(200, inner + r),
            color="#7c3aed", lw=0.6, alpha=0.25, ls="--")
ax.text(0, 0, f"{rain.sum():,}\\nmm / year", ha="center", va="center",
        fontsize=18, fontweight="bold", color="#140e29", linespacing=1.4)
ax.set_ylim(0, inner + rain.max() + 90)
ax.set_axis_off()
fig.suptitle("Monsoon in a circle", fontsize=20, fontweight="bold", color="#140e29", y=0.96)
plt.show()''', hint=SHOW),

    ex("স্ট্রিমগ্রাফ",
       "২০ বছরে কোন গানের ধারা কত জনপ্রিয় – মাঝখান ঘিরে ঢেউয়ের মতো স্তূপ (baseline='wiggle'), প্রতিটা স্রোতের ভেতরেই তার নাম।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
years = np.linspace(2005, 2025, 241)
genres = ["Folk", "Band", "Hip-hop", "Pop", "Classical", "Indie", "EDM"]
palette = ["#0d9488", "#0284c7", "#7c3aed", "#db2777", "#d97706", "#65a30d", "#e11d48"]

def smooth(y, k=21):
    w = np.hanning(k)
    return np.convolve(np.pad(y, k, mode="edge"), w / w.sum(), mode="same")[k:-k]

layers = []
for i in range(len(genres)):
    peak = 2006 + i * 2.9 + rng.uniform(-1, 1)
    width = rng.uniform(2.2, 4)
    base = rng.uniform(0.2, 0.5)
    y = (base + rng.uniform(4, 7) * np.exp(-((years - peak) / width) ** 2)
         + 1.5 * np.exp(-((years - peak - 6) / 3) ** 2) + rng.normal(0, 0.3, years.size))
    layers.append(np.clip(smooth(y), 0.05, None))
layers = np.array(layers)

fig, ax = plt.subplots(figsize=(12, 5.5), facecolor="white")
polys = ax.stackplot(years, layers, baseline="wiggle", colors=palette,
                     edgecolor="white", linewidth=0.8, alpha=0.95)

for poly, layer, name in zip(polys, layers, genres):
    k = int(np.argmax(layer))                       # স্রোত যেখানে সবচেয়ে মোটা
    path = poly.get_paths()[0].vertices
    near = path[np.abs(path[:, 0] - years[k]) < (years[1] - years[0]) * 1.5]
    if len(near) >= 2:
        ax.text(years[k], near[:, 1].mean(), name, ha="center", va="center", color="white",
                fontsize=10 + layer[k] * 1.4, fontweight="bold")

ax.set_xlim(years[0], years[-1])
ax.set_xticks(range(2005, 2026, 5), [str(y) for y in range(2005, 2026, 5)])
ax.set_yticks([])
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#bbb")
ax.set_title("Twenty years of listening", loc="left", fontsize=20, fontweight="bold", pad=30)
ax.text(0, 1.02, "Share of streams by genre (sample data)", transform=ax.transAxes,
        color="#666", fontsize=11, va="bottom")
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("উষ্ণায়নের স্ট্রাইপ ও বিচ্যুতি",
       "উপরে বিখ্যাত 'warming stripes' – প্রতিটা দাগ এক বছর; নিচে একই ডেটা বার চার্টে, রং বিচ্যুতি অনুযায়ী, সাথে ১০ বছরের চলমান গড়।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

rng = np.random.default_rng(1)
years = np.arange(1901, 2026)
trend = 0.000065 * (years - 1900) ** 2 - 0.35
anomaly = trend + 0.12 * np.sin((years - 1900) / 9) + rng.normal(0, 0.11, years.size)
rolling = np.convolve(anomaly, np.ones(10) / 10, mode="valid")
norm = TwoSlopeNorm(vmin=-0.7, vcenter=0, vmax=1.1)
cmap = plt.get_cmap("RdBu_r")

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12, 7.5), height_ratios=[1, 1.6],
                                  facecolor="white")
top.imshow(anomaly[None, :], aspect="auto", cmap=cmap, norm=norm,
           extent=[years[0] - 0.5, years[-1] + 0.5, 0, 1])
top.set_axis_off()
top.set_title("Warming stripes, 1901–2025", loc="left", fontsize=20, fontweight="bold")

bottom.bar(years, anomaly, color=cmap(norm(anomaly)), width=0.85)
bottom.plot(years[9:], rolling, color="#140e29", lw=2.5, label="10-year average")
bottom.axhline(0, color="#999", lw=0.8)
bottom.set_xlim(years[0] - 1, years[-1] + 1)
bottom.set_ylabel("Temperature anomaly (°C)")
for s in ("top", "right"):
    bottom.spines[s].set_visible(False)
hot = int(np.argmax(anomaly))
bottom.annotate(f"Warmest: {years[hot]} (+{anomaly[hot]:.2f}°C)",
                xy=(years[hot], anomaly[hot]), xytext=(1960, anomaly[hot] + 0.1),
                arrowprops=dict(arrowstyle="->", color="#444"), fontsize=11)
bottom.legend(frameon=False, loc="upper left")
fig.text(0.125, 0.02, "Sample data shaped like a real temperature record", color="#888", fontsize=9)
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.show()''', hint=SHOW),

    ex("নিয়ন গ্লো লাইন চার্ট",
       "অন্ধকার পটে জ্বলজ্বলে রেখা: প্রতিটা লাইন কয়েকবার মোটা-স্বচ্ছ করে আঁকা, নিচে ঝাপসা আলো, শেষ বিন্দুতে নাম ও মান।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(5)
days = np.arange(60)
series = {
    "Python":     ("#22d3ee", 50 + np.cumsum(rng.normal(0.6, 2.0, 60))),
    "JavaScript": ("#f472b6", 48 + np.cumsum(rng.normal(0.3, 2.2, 60))),
    "Rust":       ("#a3e635", 20 + np.cumsum(rng.normal(0.5, 1.4, 60))),
}

bg = "#0b0820"
fig, ax = plt.subplots(figsize=(11, 5.8), facecolor=bg)
ax.set_facecolor(bg)

for name, (color, y) in series.items():
    for lw, alpha in [(22, 0.03), (16, 0.05), (10, 0.08), (6, 0.14), (2.6, 1)]:
        ax.plot(days, y, color=color, lw=lw, alpha=alpha, solid_capstyle="round")
    ax.scatter(days[-1], y[-1], s=90, color=color, zorder=5, edgecolor="white", linewidth=1.5)
    ax.text(days[-1] + 1.2, y[-1], f"{name}\\n{y[-1]:.0f}", color=color, va="center",
            fontsize=11, fontweight="bold")

ax.grid(color="#2a2350", lw=0.7)
ax.set_xlim(0, 68)
ax.tick_params(colors="#8b85b1")
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xlabel("Day", color="#8b85b1")
ax.set_title("Search interest, last 60 days", loc="left", color="white",
             fontsize=20, fontweight="bold", pad=16)
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("হেক্সবিন ঘনত্ব ও মার্জিনাল হিস্টোগ্রাম",
       "২০,০০০ বিন্দুর ঘনত্ব ছয়কোণা ঘরে; উপরে ও ডানে দুই অক্ষের আলাদা বণ্টন; নিজের বানানো বেগুনি colormap, GridSpec লেআউট।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

rng = np.random.default_rng(3)
n = 20000
x = np.concatenate([rng.normal(30, 6, n // 2), rng.normal(48, 5, n // 2)])
y = 0.9 * x + rng.normal(0, 7, n) + np.where(x > 40, 8, 0)
cmap = LinearSegmentedColormap.from_list("violet", ["#faf7ff", "#c4b5fd", "#7c3aed", "#2e1065", "#0b0820"])

fig = plt.figure(figsize=(9, 9), facecolor="white")
gs = fig.add_gridspec(2, 2, width_ratios=(5, 1.1), height_ratios=(1.1, 5),
                      wspace=0.04, hspace=0.04)
ax = fig.add_subplot(gs[1, 0])
top = fig.add_subplot(gs[0, 0], sharex=ax)
right = fig.add_subplot(gs[1, 1], sharey=ax)

hb = ax.hexbin(x, y, gridsize=45, cmap=cmap, mincnt=1, linewidths=0.2, edgecolors="white")
top.hist(x, bins=70, color="#7c3aed", alpha=0.85)
right.hist(y, bins=70, color="#0d9488", alpha=0.85, orientation="horizontal")
for a in (top, right):
    a.axis("off")

r = np.corrcoef(x, y)[0, 1]
ax.text(0.03, 0.95, f"r = {r:.2f}\\nn = {n:,}", transform=ax.transAxes, va="top",
        fontsize=13, fontweight="bold", color="#140e29",
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#e9d5ff"))
ax.set_xlabel("Age")
ax.set_ylabel("Monthly spending (×100 Tk)")
cax = ax.inset_axes([0.6, 0.1, 0.35, 0.03])
cb = fig.colorbar(hb, cax=cax, orientation="horizontal")
cax.xaxis.set_label_position("top")
cb.set_label("People per cell", labelpad=4)
fig.suptitle("Who spends how much?", x=0.12, ha="left", fontsize=20, fontweight="bold", y=0.95)
plt.show()''', hint=SHOW),

    ex("ছোট ছোট অনেক চার্ট (small multiples)",
       "১২টা শহর, প্রতিটার আলাদা প্যানেল; প্যানেলে সব শহর ধূসর পটভূমিতে, শুধু সেই শহরটা রঙিন – তুলনা খুব সহজ।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(9)
cities = ["Dhaka", "Delhi", "Cairo", "Lagos", "Tokyo", "Paris",
          "Moscow", "Sydney", "Lima", "Toronto", "Nairobi", "Oslo"]
base = [26, 25, 22, 27, 16, 12, 6, 18, 19, 8, 19, 6]
amp = [5, 9, 7, 2, 10, 8, 14, -5, -3, 13, 2, 9]
m = np.arange(12)
temps = {c: b + a * np.sin((m - 3.5) / 12 * 2 * np.pi) + rng.normal(0, 0.6, 12)
         for c, b, a in zip(cities, base, amp)}
colors = plt.get_cmap("turbo")(np.linspace(0.08, 0.92, 12))

fig, axes = plt.subplots(3, 4, figsize=(13, 8.5), sharex=True, sharey=True, facecolor="white")
for ax, city, color in zip(axes.flat, cities, colors):
    for other in cities:
        ax.plot(m, temps[other], color="#d6d3e0", lw=1)
    ax.plot(m, temps[city], color=color, lw=3)
    ax.fill_between(m, temps[city], -10, color=color, alpha=0.12)
    ax.set_title(city, loc="left", fontsize=13, fontweight="bold", color=color)
    ax.text(11, temps[city][-1], f"{temps[city].mean():.0f}°", ha="right", va="bottom",
            fontsize=10, color="#444")
    ax.set_ylim(-10, 38)
    ax.set_xticks([0, 3, 6, 9], ["Jan", "Apr", "Jul", "Oct"])
    ax.grid(axis="y", color="#eee")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
fig.suptitle("Monthly temperature in 12 cities (°C)", x=0.06, ha="left",
             fontsize=20, fontweight="bold")
fig.text(0.06, 0.915, "Each panel highlights one city against all the others (sample data)",
         color="#666", fontsize=11)
plt.tight_layout(rect=(0, 0, 1, 0.92))
plt.show()''', hint=SHOW),

    ex("আলো-ছায়ার 3D ভূখণ্ড",
       "LightSource দিয়ে পাহাড়ে সূর্যের আলো আর ছায়া, gist_earth রঙ, নিচে উচ্চতার কনট্যুর প্রজেকশন।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

n = 160
x = np.linspace(-3, 3, n)
X, Y = np.meshgrid(x, x)
Z = (1.6 * np.exp(-((X - 0.8) ** 2 + (Y - 0.5) ** 2) * 1.2)
     + 1.1 * np.exp(-((X + 1.2) ** 2 + (Y + 0.9) ** 2) * 1.8)
     + 0.6 * np.exp(-((X + 0.5) ** 2 + (Y - 1.6) ** 2) * 2.5)
     + 0.04 * np.sin(X * 4) * np.cos(Y * 3))

ls = LightSource(azdeg=315, altdeg=35)
rgb = ls.shade(Z, cmap=plt.get_cmap("terrain"), vert_exag=0.6, blend_mode="soft", vmin=-0.4, vmax=2)

fig = plt.figure(figsize=(11, 8), facecolor="#f8fafc")
ax = fig.add_subplot(projection="3d", facecolor="#f8fafc")
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                linewidth=0, antialiased=False, shade=False)
ax.set_zlim(-0.3, 2)
ax.view_init(elev=32, azim=-60)
ax.set_box_aspect((1, 1, 0.45))
ax.set_axis_off()
ax.set_title("Shaded relief of an imaginary island", fontsize=18, fontweight="bold", pad=0)
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("জলবায়ু স্পাইরাল",
       "১৯৮০–২০২৫ প্রতিটা বছর এক পাক; বছর যত এগোয় রং তত উষ্ণ আর বৃত্ত তত বাইরে। ১.৫°C ও ২°C সীমা লাল বৃত্তে।",
       '''import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(12)
years = np.arange(1980, 2026)
months = np.arange(12)
theta = np.linspace(0, 2 * np.pi, 12, endpoint=False)
offset = 1.0

bg = "#07051a"
fig = plt.figure(figsize=(9, 9), facecolor=bg)
ax = fig.add_subplot(projection="polar", facecolor=bg)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
cmap = plt.get_cmap("inferno")

for i in range(len(years)):
    anom = 0.15 + 0.028 * i + 0.12 * np.sin(theta * 2 + i) + rng.normal(0, 0.06, 12)
    t = np.linspace(0, 2 * np.pi, 241)                       # মসৃণ বক্ররেখা
    r = np.interp(t, np.r_[theta, 2 * np.pi], np.r_[anom, anom[0]], period=2 * np.pi)
    k = np.hanning(25)
    k /= k.sum()
    r = np.convolve(np.r_[r[-12:], r, r[:12]], k, mode="same")[12:-12] + offset
    ax.plot(t, r, color=cmap(0.2 + 0.75 * i / len(years)), lw=1.5, alpha=0.9)

for level, label in [(1.5, "1.5°C"), (2.0, "2.0°C")]:
    ax.plot(np.linspace(0, 2 * np.pi, 300), np.full(300, level + offset), color="#ef4444", lw=1.4)
    ax.text(np.radians(20), level + offset + 0.06, label, color="#ef4444", fontsize=11, fontweight="bold")

ax.set_xticks(theta, ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], color="#cfc8f5", fontsize=11)
ax.set_yticks([])
ax.set_ylim(0, 3.3)
ax.spines["polar"].set_visible(False)
ax.grid(color="#2a2350")
ax.text(0, 0, f"{years[0]}\\n–\\n{years[-1]}", ha="center", va="center",
        color="white", fontsize=18, fontweight="bold")
fig.subplots_adjust(top=0.86, bottom=0.05)
fig.suptitle("Climate spiral", color="white", fontsize=22, fontweight="bold", y=0.975)
fig.text(0.5, 0.925, "Monthly temperature anomaly, one loop per year (sample data)",
         ha="center", color="#a09ac4", fontsize=11)
plt.show()''', hint=SHOW),

    ex("ডাম্বেল চার্ট: আগে বনাম এখন",
       "১৪টা জেলার সাক্ষরতার হার ২০০০ আর ২০২৫-এ; প্রতিটা সারিতে দুই বিন্দু ও তাদের মাঝে রঙিন রেখা, পরিবর্তন অনুযায়ী সাজানো।",
       '''import numpy as np
import matplotlib.pyplot as plt

districts = ["Dhaka", "Chattogram", "Sylhet", "Khulna", "Rajshahi", "Barishal", "Rangpur",
             "Mymensingh", "Cumilla", "Bogura", "Jessore", "Noakhali", "Dinajpur", "Pabna"]
before = np.array([62, 55, 41, 52, 47, 50, 39, 37, 49, 44, 51, 46, 40, 43])
after = np.array([88, 82, 71, 80, 76, 79, 72, 68, 81, 74, 80, 78, 73, 72])
order = np.argsort(after - before)
districts = [districts[i] for i in order]
before, after = before[order], after[order]
y = np.arange(len(districts))

fig, ax = plt.subplots(figsize=(10, 8), facecolor="white")
for yi, b, a in zip(y, before, after):
    ax.plot([b, a], [yi, yi], color="#c4b5fd", lw=5, solid_capstyle="round", zorder=1)
    ax.text(a + 1.2, yi, f"+{a - b}", va="center", fontsize=10, color="#7c3aed", fontweight="bold")
ax.scatter(before, y, s=140, color="#94a3b8", zorder=2, label="2000", edgecolor="white", linewidth=1.5)
ax.scatter(after, y, s=140, color="#7c3aed", zorder=3, label="2025", edgecolor="white", linewidth=1.5)

ax.set_yticks(y, districts, fontsize=11)
ax.set_xlim(30, 96)
ax.set_xlabel("Literacy rate (%)")
ax.grid(axis="x", color="#eee")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.legend(ncols=2, frameon=False, loc="lower left", fontsize=11)
ax.set_title("Literacy rose everywhere – fastest at the top", loc="left",
             fontsize=18, fontweight="bold", pad=14)
fig.text(0.02, 0.01, "Sample data for illustration", color="#999", fontsize=9)
plt.tight_layout()
plt.show()''', hint=SHOW),
)

more("seaborn",
    ex("ক্লাস্টার হিটম্যাপ ও ডেনড্রোগ্রাম",
       "৩০টা জিনের ১৬টা নমুনায় প্রকাশ; মিল অনুযায়ী সারি-কলাম নিজে থেকে সাজানো, পাশে গাছের মতো ডেনড্রোগ্রাম আর নমুনার দলের রঙ। (scipy লাগে)",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rng = np.random.default_rng(4)
samples = [f"S{i:02d}" for i in range(1, 17)]
groups = np.repeat(["Control", "Drug A", "Drug B", "Drug C"], 4)
genes = [f"GENE{i:02d}" for i in range(1, 31)]
data = rng.normal(0, 1, (30, 16))
data[:8, 4:8] += 2.5        # Drug A তে কিছু জিন বাড়ে
data[8:16, 8:12] += 2.2     # Drug B
data[16:22, 12:] -= 2.0     # Drug C তে কিছু কমে
data[22:, :4] += 1.6
df = pd.DataFrame(data, index=genes, columns=samples)

lut = dict(zip(["Control", "Drug A", "Drug B", "Drug C"], ["#94a3b8", "#7c3aed", "#0d9488", "#e11d48"]))
col_colors = pd.Series(groups, index=samples).map(lut)

g = sns.clustermap(df, cmap="vlag", center=0, col_colors=col_colors, figsize=(10, 10),
                   dendrogram_ratio=(0.14, 0.12), linewidths=0.4, linecolor="white",
                   cbar_pos=(0.02, 0.86, 0.025, 0.1), cbar_kws=dict(label="z-score"))
g.ax_heatmap.set_xlabel("")
g.ax_heatmap.tick_params(labelsize=8)
for name, color in lut.items():
    g.ax_col_dendrogram.bar(0, 0, color=color, label=name, linewidth=0)
g.ax_col_dendrogram.legend(ncols=4, loc="center", bbox_to_anchor=(0.5, 1.12), frameon=False)
g.figure.suptitle("Gene expression clusters", x=0.55, y=1.04, fontsize=18, fontweight="bold")
plt.show()''', hint=SHOW),

    ex("রিজ প্লট (FacetGrid)",
       "seaborn-এর FacetGrid দিয়ে ১০টা দলের বণ্টন একটার উপর আরেকটা; সারিগুলো একটু করে ঢাকা পড়ে (hspace ঋণাত্মক), cubehelix রঙ।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
rng = np.random.default_rng(10)
labels = [f"Batch {c}" for c in "ABCDEFGHIJ"]
x = np.concatenate([rng.normal(i * 0.55, 1 + (i % 3) * 0.15, 400) for i in range(10)])
df = pd.DataFrame(dict(x=x, g=np.repeat(labels, 400)))

pal = sns.cubehelix_palette(10, rot=-0.25, light=0.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=12, height=0.62, palette=pal)
g.map(sns.kdeplot, "x", bw_adjust=0.6, clip_on=False, fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=0.6)
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

def label(x, color, label):
    ax = plt.gca()
    ax.text(0, 0.2, label, fontweight="bold", color=color, ha="left", va="center",
            transform=ax.transAxes)
g.map(label, "x")

g.figure.subplots_adjust(hspace=-0.3)
g.set_titles("")
g.set(yticks=[], ylabel="", xlabel="Measured value")
g.despine(bottom=True, left=True)
g.figure.suptitle("Ten production batches", x=0.12, ha="left", y=1.0, fontsize=18, fontweight="bold")
plt.show()''', hint=SHOW),

    ex("অন্ধকার পটে মসৃণ ঘনত্ব",
       "হাজার বিন্দুর স্ক্যাটার, তার নিচে 2D হিস্টোগ্রাম (mako), উপরে সাদা KDE কনট্যুর – seaborn-এর তিনটা স্তর একসাথে।",
       '''import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="dark")
rng = np.random.default_rng(2)
n = 6000
mean, cov = [0, 0], [(2, 0.9), (0.9, 1)]
x, y = rng.multivariate_normal(mean, cov, n).T
x2, y2 = rng.multivariate_normal([3.5, 2.5], [(0.6, -0.3), (-0.3, 0.5)], n // 3).T
x, y = np.r_[x, x2], np.r_[y, y2]

f, ax = plt.subplots(figsize=(9, 7.5))
sns.scatterplot(x=x, y=y, s=4, color=".15", linewidth=0)
sns.histplot(x=x, y=y, bins=60, pthresh=0.08, cmap="mako")
sns.kdeplot(x=x, y=y, levels=6, color="w", linewidths=1.2)
ax.set(xlabel="Feature 1", ylabel="Feature 2")
ax.set_title("Two overlapping populations", loc="left", fontsize=18, fontweight="bold")
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("দুই দলের জয়েন্ট KDE",
       "jointplot(kind='kde', hue=...) – মাঝে দুই দলের ভরাট কনট্যুর, উপরে-ডানে তাদের আলাদা বণ্টন।",
       '''import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="ticks")
rng = np.random.default_rng(6)
a = rng.multivariate_normal([165, 60], [[40, 25], [25, 60]], 500)
b = rng.multivariate_normal([175, 74], [[45, 30], [30, 80]], 500)
df = pd.DataFrame(np.vstack([a, b]), columns=["height", "weight"])
df["group"] = ["Group A"] * 500 + ["Group B"] * 500

g = sns.jointplot(data=df, x="height", y="weight", hue="group", kind="kde",
                  fill=True, alpha=0.55, levels=8, height=8,
                  palette=["#7c3aed", "#e11d48"])
g.set_axis_labels("Height (cm)", "Weight (kg)", fontsize=12)
g.figure.suptitle("Height and weight in two groups", y=1.02, fontsize=18, fontweight="bold")
plt.show()''', hint=SHOW),
)

more("networkx",
    ex("কমিউনিটি রঙে নেটওয়ার্ক",
       "বিখ্যাত Karate Club নেটওয়ার্ক (লাইব্রেরির ভেতরেই থাকে): মডুলারিটি দিয়ে কমিউনিটি খুঁজে রঙ, বিন্দুর মাপ = সংযোগ সংখ্যা, অন্ধকার পটে আলোকিত।",
       '''import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

G = nx.karate_club_graph()
communities = greedy_modularity_communities(G)
palette = ["#22d3ee", "#f472b6", "#a3e635", "#fbbf24", "#a78bfa"]
color = {n: palette[i % len(palette)] for i, c in enumerate(communities) for n in c}

pos = nx.spring_layout(G, seed=7, k=0.35)
deg = dict(G.degree())
bg = "#0b0820"
fig, ax = plt.subplots(figsize=(10, 8.5), facecolor=bg)
ax.set_facecolor(bg)

same = [(u, v) for u, v in G.edges if color[u] == color[v]]
cross = [(u, v) for u, v in G.edges if color[u] != color[v]]
nx.draw_networkx_edges(G, pos, edgelist=cross, edge_color="#4b4470", width=0.8, alpha=0.6, ax=ax)
nx.draw_networkx_edges(G, pos, edgelist=same, edge_color=[color[u] for u, v in same],
                       width=1.6, alpha=0.55, ax=ax)
nodes = list(G.nodes)
sizes = [80 + deg[n] * 55 for n in nodes]
nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=[s * 2.2 for s in sizes],
                       node_color=[color[n] for n in nodes], alpha=0.15, ax=ax)   # আলোর আভা
nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=sizes,
                       node_color=[color[n] for n in nodes], edgecolors="white", linewidths=1.2, ax=ax)
hubs = sorted(deg, key=deg.get, reverse=True)[:5]
nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in hubs}, font_color="#0b0820",
                        font_weight="bold", font_size=10, ax=ax)

ax.set_axis_off()
ax.set_title(f"Karate club: {len(communities)} communities found", color="white",
             fontsize=18, fontweight="bold", loc="left")
plt.tight_layout()
plt.show()''', hint=SHOW),
)


# ==================================================================
# শোকেস ২: ML, বিজ্ঞান, ছবি প্রসেসিং, ডেটা
# ==================================================================

more("scikit-learn",
    ex("ক্লাসিফায়ারের সিদ্ধান্ত-সীমার তুলনা",
       "৩টা ডেটাসেট × ৫টা মডেল: প্রতিটা মডেল জায়গাটাকে কীভাবে দুই রঙে ভাগ করে আর টেস্টে কত নম্বর পায়। scikit-learn-এর বিখ্যাত ছবির নিজস্ব সংস্করণ।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_circles, make_classification, make_moons
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_classification(n_features=2, n_redundant=0, n_informative=2,
                           random_state=1, n_clusters_per_class=1)
X += 2 * np.random.default_rng(2).uniform(size=X.shape)
datasets = [make_moons(noise=0.3, random_state=0),
            make_circles(noise=0.2, factor=0.5, random_state=1), (X, y)]
models = {
    "Nearest neighbors": KNeighborsClassifier(3),
    "Linear SVM": SVC(kernel="linear", C=0.025),
    "RBF SVM": SVC(gamma=2, C=1),
    "Random forest": RandomForestClassifier(max_depth=5, n_estimators=50, random_state=0),
    "Neural net": MLPClassifier(alpha=1, max_iter=1500, random_state=0),
}
cm = plt.get_cmap("PuOr")
dots = ListedColormap(["#7c3aed", "#d97706"])

fig, axes = plt.subplots(3, 6, figsize=(17, 8.5), facecolor="white")
for r, (X, y) in enumerate(datasets):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=42)
    ax = axes[r, 0]
    ax.scatter(X_tr[:, 0], X_tr[:, 1], c=y_tr, cmap=dots, edgecolors="white", s=26)
    ax.scatter(X_te[:, 0], X_te[:, 1], c=y_te, cmap=dots, alpha=0.5, edgecolors="white", s=26)
    if r == 0:
        ax.set_title("Input data", fontweight="bold")
    for c, (name, model) in enumerate(models.items(), start=1):
        ax = axes[r, c]
        clf = make_pipeline(StandardScaler(), model).fit(X_tr, y_tr)
        score = clf.score(X_te, y_te)
        DecisionBoundaryDisplay.from_estimator(clf, X, cmap=cm, alpha=0.75, ax=ax, eps=0.5)
        ax.scatter(X_tr[:, 0], X_tr[:, 1], c=y_tr, cmap=dots, edgecolors="white", s=22)
        ax.scatter(X_te[:, 0], X_te[:, 1], c=y_te, cmap=dots, edgecolors="black", s=22, alpha=0.6)
        ax.text(0.95, 0.06, f"{score:.2f}", transform=ax.transAxes, ha="right", fontsize=13,
                fontweight="bold", bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.8))
        if r == 0:
            ax.set_title(name, fontweight="bold")
for ax in axes.flat:
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
fig.suptitle("How five classifiers split the same data", x=0.02, ha="left",
             fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("ক্লাস্টারিং পদ্ধতির তুলনা",
       "৩ ধরনের আকৃতির ডেটায় K-Means, DBSCAN, Agglomerative আর Gaussian Mixture – কোনটা কোথায় ঠিকমতো দল চেনে, অন্ধকার পটে।",
       '''import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
blobs, _ = make_blobs(n_samples=700, centers=4, cluster_std=[0.9, 0.6, 1.2, 0.5], random_state=8)
moons, _ = make_moons(n_samples=700, noise=0.06, random_state=1)
aniso, _ = make_blobs(n_samples=700, centers=3, random_state=170)
aniso = aniso @ np.array([[0.6, -0.64], [-0.41, 0.85]])
data = {"Blobs": (blobs, 4), "Moons": (moons, 2), "Stretched": (aniso, 3)}

palette = np.array(["#22d3ee", "#f472b6", "#a3e635", "#fbbf24", "#a78bfa", "#fb7185"])
bg = "#0b0820"
fig, axes = plt.subplots(3, 4, figsize=(15, 11), facecolor=bg)
for r, (dname, (X, k)) in enumerate(data.items()):
    X = StandardScaler().fit_transform(X)
    algos = {
        "K-Means": KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X),
        "DBSCAN": DBSCAN(eps=0.3 if dname != "Blobs" else 0.25, min_samples=8).fit_predict(X),
        "Agglomerative": AgglomerativeClustering(
            n_clusters=k, linkage="single" if dname == "Moons" else "ward").fit_predict(X),
        "Gaussian mixture": GaussianMixture(n_components=k, covariance_type="full",
                                            random_state=0).fit(X).predict(X),
    }
    for c, (aname, labels) in enumerate(algos.items()):
        ax = axes[r, c]
        ax.set_facecolor(bg)
        colors = np.where(labels >= 0, palette[labels % len(palette)], "#4b4470")   # -1 = noise
        ax.scatter(X[:, 0], X[:, 1], c=colors, s=9, linewidths=0)
        n = len(set(labels) - {-1})
        ax.text(0.97, 0.04, f"{n} clusters", transform=ax.transAxes, ha="right",
                color="#cfc8f5", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#2a2350")
        if r == 0:
            ax.set_title(aname, color="white", fontweight="bold", fontsize=13)
        if c == 0:
            ax.set_ylabel(dname, color="white", fontsize=13, fontweight="bold")
fig.suptitle("Same points, four ways to find groups", color="white", x=0.02, ha="left",
             fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("হাতে লেখা অঙ্কের t-SNE ম্যাপ",
       "৬৪ মাত্রার ১৭৯৭টা অঙ্কের ছবি t-SNE দিয়ে ২ মাত্রায় নামানো – একই অঙ্ক নিজে থেকে এক জায়গায় জড়ো হয়; প্রতিটা দলের মাঝে একটা আসল ছবি।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE

digits = load_digits()
emb = TSNE(n_components=2, init="pca", perplexity=35, random_state=0).fit_transform(digits.data)
colors = plt.get_cmap("tab10")

fig, ax = plt.subplots(figsize=(11, 9.5), facecolor="white")
for d in range(10):
    pts = emb[digits.target == d]
    ax.scatter(pts[:, 0], pts[:, 1], s=14, color=colors(d), alpha=0.75, linewidths=0)
    cx, cy = np.median(pts, axis=0)
    idx = np.where(digits.target == d)[0][0]
    img = OffsetImage(digits.images[idx], zoom=3.2, cmap="gray_r")
    ax.add_artist(AnnotationBbox(img, (cx, cy), frameon=True,
                                 bboxprops=dict(edgecolor=colors(d), linewidth=2.5, boxstyle="round,pad=0.2")))
    ax.text(cx, cy - 6.5, str(d), ha="center", fontsize=16, fontweight="bold", color=colors(d))

ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("1,797 handwritten digits, organised by t-SNE", loc="left",
             fontsize=20, fontweight="bold", pad=30)
ax.text(0, 1.015, "Each dot is one 8×8 image; nobody told the algorithm which digit is which",
        transform=ax.transAxes, color="#666", fontsize=11, va="bottom")
plt.tight_layout()
plt.show()''', hint=SHOW),
)

more("scipy",
    ex("Lorenz attractor",
       "solve_ivp দিয়ে বিখ্যাত বিশৃঙ্খল (chaotic) সমীকরণ সমাধান; পথটা সময় অনুযায়ী রং বদলায় (LineCollection), অন্ধকার পটে প্রজাপতির ডানা।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.integrate import solve_ivp

def lorenz(t, s, sigma=10, rho=28, beta=8 / 3):
    x, y, z = s
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

t = np.linspace(0, 60, 30000)
sol = solve_ivp(lorenz, (0, 60), [1, 1, 1], t_eval=t, rtol=1e-9, atol=1e-9)
x, y, z = sol.y

bg = "#05030f"
fig, ax = plt.subplots(figsize=(11, 8.5), facecolor=bg)
ax.set_facecolor(bg)
points = np.column_stack([x, z])
segs = np.stack([points[:-1], points[1:]], axis=1)
for lw, alpha in [(4, 0.05), (1.6, 0.15), (0.6, 0.9)]:
    lc = LineCollection(segs, cmap="plasma", linewidth=lw, alpha=alpha)
    lc.set_array(t[:-1])
    ax.add_collection(lc)
ax.autoscale()
ax.set_axis_off()
ax.set_title("The Lorenz attractor", color="white", fontsize=22, fontweight="bold", loc="left")
ax.text(0, 0.985, "x–z projection of 60 seconds of chaos, coloured by time",
        transform=ax.transAxes, color="#a09ac4", fontsize=11)
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("Voronoi ও Delaunay শিল্প",
       "৩০০টা এলোমেলো বিন্দু থেকে Voronoi কোষ (প্রতিটা কোষ = নিকটতম বিন্দুর এলাকা), আকার অনুযায়ী রং, উপরে Delaunay ত্রিভুজের জাল।",
       '''import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from scipy.spatial import Delaunay, Voronoi

rng = np.random.default_rng(11)
pts = np.vstack([rng.uniform(0, 1, (220, 2)),
                 rng.normal([0.68, 0.38], 0.08, (80, 2))])           # একটা ঘন এলাকা
far = np.array([[-5, -5], [-5, 6], [6, -5], [6, 6]])                # ধারের কোষ বন্ধ রাখতে
vor = Voronoi(np.vstack([pts, far]))

polys, areas = [], []
for i in range(len(pts)):
    region = vor.regions[vor.point_region[i]]
    if -1 in region or not region:
        continue
    poly = vor.vertices[region]                      # অক্ষের বাইরে অংশ নিজে থেকেই কাটা পড়ে
    x, y = poly[:, 0], poly[:, 1]
    polys.append(poly)
    areas.append(0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))))
areas = np.array(areas)

fig, ax = plt.subplots(figsize=(10, 10), facecolor="#0b0820")
ax.set_facecolor("#0b0820")
pc = PolyCollection(polys, array=np.log(areas + 1e-6), cmap="magma_r",
                    edgecolors="#0b0820", linewidths=1.6)
ax.add_collection(pc)
tri = Delaunay(pts)
ax.triplot(pts[:, 0], pts[:, 1], tri.simplices, color="white", lw=0.35, alpha=0.35)
ax.scatter(pts[:, 0], pts[:, 1], s=6, color="white", zorder=3)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_axis_off()
ax.set_title("Voronoi cells and Delaunay mesh", color="white", fontsize=20, fontweight="bold", loc="left")
plt.tight_layout()
plt.show()''', hint=SHOW),
)

more("numpy",
    ex("Mandelbrot ফ্র্যাক্টাল",
       "শুধু NumPy array দিয়ে লুপ ছাড়াই Mandelbrot সেট; 'smooth colouring' দিয়ে রঙের স্তরগুলো মসৃণ, একটা সুন্দর অংশে জুম করা।",
       '''import numpy as np
import matplotlib.pyplot as plt

W, H, max_iter = 1400, 900, 300
cx, cy, span = -0.743643887, 0.131825904, 0.012
x = np.linspace(cx - span, cx + span, W)
y = np.linspace(cy - span * H / W, cy + span * H / W, H)
C = x[None, :] + 1j * y[:, None]

Z = np.zeros_like(C)
smooth = np.zeros(C.shape)
alive = np.ones(C.shape, dtype=bool)
for i in range(max_iter):
    Z[alive] = Z[alive] ** 2 + C[alive]
    escaped = alive & (np.abs(Z) > 4)
    smooth[escaped] = i + 1 - np.log2(np.log(np.abs(Z[escaped])))
    alive &= ~escaped

smooth[alive] = 0
img = np.where(alive, np.nan, np.sqrt(smooth))

fig, ax = plt.subplots(figsize=(14, 9), facecolor="black")
ax.imshow(img, cmap="twilight_shifted", extent=[x[0], x[-1], y[0], y[-1]], origin="lower",
          interpolation="bilinear")
ax.set_facecolor("black")
ax.set_axis_off()
ax.text(0.015, 0.03, "Mandelbrot set · Seahorse valley · 300 iterations", transform=ax.transAxes,
        color="white", fontsize=13, fontweight="bold")
plt.subplots_adjust(0, 0, 1, 1)
plt.show()''', hint=SHOW),

    ex("রিঅ্যাকশন-ডিফিউশন প্যাটার্ন",
       "Gray-Scott মডেল: দুই রাসায়নিক ছড়ায় আর বিক্রিয়া করে – শুধু দুইটা সংখ্যা (f, k) বদলালে দাগ, রেখা বা গোলকধাঁধা তৈরি হয়, প্রকৃতির মতো।",
       '''import numpy as np
import matplotlib.pyplot as plt

def gray_scott(f, k, n=200, steps=8000, seed=0):
    rng = np.random.default_rng(seed)
    U = np.ones((n, n))
    V = np.zeros((n, n))
    for _ in range(12):                                 # কয়েকটা বীজ
        x, y = rng.integers(20, n - 20, 2)
        U[x - 5:x + 5, y - 5:y + 5] = 0.5
        V[x - 5:x + 5, y - 5:y + 5] = 0.25
    Du, Dv = 0.16, 0.08
    for _ in range(steps):
        Lu = np.roll(U, 1, 0) + np.roll(U, -1, 0) + np.roll(U, 1, 1) + np.roll(U, -1, 1) - 4 * U
        Lv = np.roll(V, 1, 0) + np.roll(V, -1, 0) + np.roll(V, 1, 1) + np.roll(V, -1, 1) - 4 * V
        uvv = U * V * V
        U += Du * Lu - uvv + f * (1 - U)
        V += Dv * Lv + uvv - (f + k) * V
    return V

patterns = [("Spots", 0.0367, 0.0649, "magma"), ("Stripes", 0.042, 0.059, "viridis"),
            ("Maze", 0.029, 0.057, "cividis"), ("Coral", 0.0545, 0.062, "inferno")]
fig, axes = plt.subplots(1, 4, figsize=(16, 4.8), facecolor="#0b0820")
for ax, (name, f, k, cmap) in zip(axes, patterns):
    ax.imshow(gray_scott(f, k), cmap=cmap, interpolation="bicubic")
    ax.set_title(f"{name}\\nf={f}, k={k}", color="white", fontsize=12, fontweight="bold")
    ax.set_axis_off()
fig.suptitle("Turing patterns from two simple equations", color="white",
             fontsize=18, fontweight="bold", x=0.01, ha="left")
plt.tight_layout(rect=(0, 0, 1, 0.9))
plt.show()''', hint=SHOW),
)

more("scikit-image",
    ex("কয়েন সেগমেন্টেশনের ধাপ",
       "একটা ছবি থেকে বস্তু আলাদা করার পুরো পথ: আসল → এজ ম্যাপ → watershed সেগমেন্ট → রঙিন লেবেল ও নম্বরসহ ফল, চারটা প্যানেলে।",
       '''import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import data, filters, measure, morphology, segmentation, color

coins = data.coins()
elevation = filters.sobel(coins)                         # কিনারার উঁচু-নিচু
markers = np.zeros_like(coins)
markers[coins < 30] = 1                                  # পটভূমি
markers[coins > 150] = 2                                 # কয়েন
seg = segmentation.watershed(elevation, markers)
mask = ndi.binary_fill_holes(seg == 2)
mask = morphology.remove_small_objects(mask, max_size=60)
labels = measure.label(mask)

fig, axes = plt.subplots(1, 4, figsize=(18, 5.2), facecolor="white")
axes[0].imshow(coins, cmap="gray")
axes[0].set_title("1 · Original", fontweight="bold", loc="left")
axes[1].imshow(elevation, cmap="magma")
axes[1].set_title("2 · Sobel elevation map", fontweight="bold", loc="left")
axes[2].imshow(segmentation.mark_boundaries(coins, labels, color=(0.49, 0.23, 0.93), mode="thick"))
axes[2].set_title("3 · Watershed boundaries", fontweight="bold", loc="left")
axes[3].imshow(color.label2rgb(labels, image=coins, bg_label=0, alpha=0.45))
for r in measure.regionprops(labels):
    y, x = r.centroid
    axes[3].text(x, y, str(r.label), color="white", ha="center", va="center",
                 fontsize=9, fontweight="bold")
axes[3].set_title(f"4 · {labels.max()} coins labelled", fontweight="bold", loc="left")
for ax in axes:
    ax.set_axis_off()
fig.suptitle("From pixels to objects", fontsize=20, fontweight="bold", x=0.01, ha="left")
plt.tight_layout()
plt.show()''', hint=SHOW),

    ex("ফিল্টার গ্যালারি",
       "একটা ছবিতে ছয়টা ভিন্ন ফিল্টার: এজ, হিস্টোগ্রাম সমতা, ঘূর্ণি (swirl), পোস্টারাইজ, রং উল্টানো ও HSV রং ঘোরানো।",
       '''import numpy as np
import matplotlib.pyplot as plt
from skimage import color, data, exposure, filters, transform, util

img = data.astronaut()
gray = color.rgb2gray(img)

hsv = color.rgb2hsv(img)
hsv[..., 0] = (hsv[..., 0] + 0.45) % 1.0
hue_shift = color.hsv2rgb(hsv)
poster = (np.floor(img / 64) * 64 + 32).astype(np.uint8)
edges = filters.sobel(gray)

panels = [
    ("Original", img, None),
    ("Sobel edges", edges, "magma"),
    ("Adaptive equalisation", exposure.equalize_adapthist(img, clip_limit=0.03), None),
    ("Swirl", transform.swirl(img, center=(220, 260), strength=8, radius=220), None),
    ("Posterise (4 levels)", poster, None),
    ("Hue rotated", hue_shift, None),
]
fig, axes = plt.subplots(2, 3, figsize=(15, 10.5), facecolor="white")
for ax, (title, im, cmap) in zip(axes.flat, panels):
    ax.imshow(im, cmap=cmap)
    ax.set_title(title, fontsize=14, fontweight="bold", loc="left")
    ax.set_axis_off()
fig.suptitle("One photo, six filters", fontsize=22, fontweight="bold", x=0.01, ha="left")
plt.tight_layout()
plt.show()''', hint=SHOW),
)

more("opencv-python",
    ex("কার্টুন, পেন্সিল স্কেচ ও অয়েল পেইন্ট",
       "OpenCV-র ছবি-স্টাইলের ফাংশন: bilateral filter + adaptive threshold দিয়ে কার্টুন, pencilSketch, stylization আর detailEnhance – একটা বিড়ালের ছবিতে। (নমুনা ছবির জন্য scikit-image লাগে)",
       '''import cv2
import matplotlib.pyplot as plt
from skimage import data            # শুধু নমুনা ছবির জন্য; নিজের ছবি হলে cv2.imread("cat.jpg")

img = cv2.cvtColor(data.chelsea(), cv2.COLOR_RGB2BGR)

# কার্টুন: রং মসৃণ করা + মোটা কালো কিনারা
smooth = img.copy()
for _ in range(5):
    smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=40, sigmaSpace=9)
gray = cv2.medianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 7)
edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)
cartoon = cv2.bitwise_and(smooth, smooth, mask=edges)

sketch_gray, sketch_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.06)
painting = cv2.stylization(img, sigma_s=80, sigma_r=0.45)
detail = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.2)

panels = [("Original", img), ("Cartoon", cartoon), ("Pencil sketch", sketch_gray),
          ("Coloured pencil", sketch_color), ("Oil painting", painting), ("Detail enhance", detail)]
fig, axes = plt.subplots(2, 3, figsize=(15, 8.6), facecolor="white")
for ax, (title, im) in zip(axes.flat, panels):
    shown = im if im.ndim == 2 else cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    ax.imshow(shown, cmap="gray" if im.ndim == 2 else None)
    ax.set_title(title, fontsize=14, fontweight="bold", loc="left")
    ax.set_axis_off()
fig.suptitle("Photo effects with OpenCV", fontsize=22, fontweight="bold", x=0.01, ha="left")
plt.tight_layout()
plt.show()''', hint=SHOW),
)

more("pandas",
    ex("স্টক চার্ট: চলমান গড়, বলিঙ্গার ব্যান্ড ও ভলিউম",
       "pandas-এর rolling() দিয়ে ২০ ও ৫০ দিনের গড়, বলিঙ্গার ব্যান্ড, সবচেয়ে বড় পতনের এলাকা চিহ্নিত, নিচে রঙিন ভলিউম বার।",
       '''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(21)
dates = pd.bdate_range("2025-01-01", periods=320)
ret = rng.normal(0.0006, 0.017, len(dates))
ret[150:190] -= 0.006                                   # একটা পতনের সময়
df = pd.DataFrame({"close": 100 * np.exp(np.cumsum(ret)),
                   "volume": rng.gamma(4, 2.5e5, len(dates))}, index=dates)

df["ma20"] = df["close"].rolling(20).mean()
df["ma50"] = df["close"].rolling(50).mean()
std = df["close"].rolling(20).std()
df["upper"], df["lower"] = df["ma20"] + 2 * std, df["ma20"] - 2 * std
peak = df["close"].cummax()
drawdown = df["close"] / peak - 1
trough = drawdown.idxmin()
start = df.loc[:trough, "close"].idxmax()

fig, (ax, axv) = plt.subplots(2, 1, figsize=(13, 7.5), sharex=True,
                              height_ratios=[3.2, 1], facecolor="white")
ax.fill_between(df.index, df["lower"], df["upper"], color="#7c3aed", alpha=0.10, label="Bollinger band")
ax.plot(df.index, df["close"], color="#140e29", lw=1.6, label="Close")
ax.plot(df.index, df["ma20"], color="#7c3aed", lw=1.4, label="20-day average")
ax.plot(df.index, df["ma50"], color="#d97706", lw=1.8, label="50-day average")
ax.axvspan(start, trough, color="#e11d48", alpha=0.08)
ax.annotate(f"Max drawdown {drawdown.min():.0%}", xy=(trough, df.loc[trough, "close"]),
            xytext=(-60, 45), textcoords="offset points", ha="right",
            arrowprops=dict(arrowstyle="->", color="#e11d48"), color="#e11d48", fontweight="bold")
ax.legend(frameon=False, ncols=4, loc="upper left")
ax.set_ylabel("Price")
ax.grid(color="#eee")

up = df["close"].diff() >= 0
axv.bar(df.index, df["volume"], color=np.where(up, "#0d9488", "#e11d48"), width=1.0)
axv.set_ylabel("Volume")
for a in (ax, axv):
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
ax.set_title("Sample stock: trend, volatility and volume", loc="left", fontsize=20, fontweight="bold")
plt.tight_layout()
plt.show()''', hint=SHOW),
)
