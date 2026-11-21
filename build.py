"""
build.py - পাইথন লাইব্রেরি গাইড ওয়েবসাইট বানায় (index.html)।

- libraries.json      : Atlas থেকে নেওয়া ৬৪৫টা লাইব্রেরির তালিকা
- DETAILS (নিচে)       : যেসব লাইব্রেরির পুরো ব্যাখ্যা ও কোড উদাহরণ লেখা হয়েছে

নতুন লাইব্রেরি সম্পূর্ণ করতে DETAILS-এ ওই লাইব্রেরির নাম দিয়ে একটা এন্ট্রি যোগ করো।
বাকিগুলো সাইটে নিজে থেকেই "শীঘ্রই আসছে" (placeholder) হিসেবে দেখাবে।

চালাও:  python build.py
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE_TITLE = "পাইথন লাইব্রেরি গাইড"

# ------------------------------------------------------------------
# সম্পূর্ণ লাইব্রেরি (নাম অবশ্যই libraries.json-এর নামের সাথে মিলতে হবে)
# ------------------------------------------------------------------
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
# ------------------------------------------------------------------


def load_libraries():
    libs = json.loads((ROOT / "libraries.json").read_text(encoding="utf-8"))
    names = {lib["name"].lower() for lib in libs}
    for key in DETAILS:
        if key.lower() not in names:
            raise SystemExit(f"DETAILS-এর '{key}' নামটা libraries.json-এ নেই")
    for lib in libs:
        extra = DETAILS.get(lib["name"]) or DETAILS.get(lib["name"].lower())
        lib["full"] = bool(extra)
        if extra:
            lib.update(extra)
    # সম্পূর্ণগুলো আগে দেখাবে
    libs.sort(key=lambda x: (not x["full"], x["id"]))
    return libs


TEMPLATE = r"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="৬৪৫টা পাইথন ও জাভাস্ক্রিপ্ট লাইব্রেরি – কোনটা কী কাজে লাগে, উদাহরণ ও প্রজেক্টসহ">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#f6f4ef;--card:#fff;--ink:#1d1f24;--muted:#61656f;--line:#e4e0d6;
  --py:#2f6fdb;--js:#c48a00;--accent:#1f7a5c;--accent-soft:#e3f2ec;--code:#16181d;
  --font:"Hind Siliguri","Noto Sans Bengali",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Consolas,monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font);background:var(--bg);color:var(--ink);line-height:1.6;font-size:16px}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
header.hero{padding-top:44px;padding-bottom:26px}
.eyebrow{font:600 .78rem var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
h1{font-size:clamp(1.9rem,6vw,3rem);line-height:1.15;margin:8px 0 10px;font-weight:700}
.lead{color:var(--muted);max-width:640px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 14px}
.stat b{font-size:1.25rem;display:block;line-height:1.2}
.stat span{font-size:.8rem;color:var(--muted)}
.controls{position:sticky;top:0;z-index:5;background:var(--bg);padding:12px 0;border-bottom:1px solid var(--line)}
.controls .row{display:grid;grid-template-columns:1fr;gap:8px}
@media(min-width:760px){.controls .row{grid-template-columns:2fr 1.4fr 1fr 1fr}}
input,select{width:100%;font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink)}
input:focus,select:focus{outline:2px solid var(--accent);outline-offset:1px}
.count{font-size:.85rem;color:var(--muted);margin:14px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;padding-bottom:40px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;cursor:pointer;
  text-align:left;font:inherit;color:inherit;display:flex;flex-direction:column;gap:6px;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.06)}
.card.full{border-color:var(--accent);box-shadow:inset 4px 0 0 var(--accent)}
.card h3{font:600 1.05rem var(--mono);word-break:break-word}
.card p{font-size:.92rem;color:var(--muted)}
.meta{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.tag{font:600 .7rem var(--mono);padding:2px 8px;border-radius:99px;border:1px solid currentColor}
.tag.python{color:var(--py)}.tag.javascript{color:var(--js)}
.badge{font-size:.72rem;padding:2px 8px;border-radius:99px;background:var(--accent-soft);color:var(--accent);font-weight:600}
.badge.soon{background:#eee;color:#888}
.cat{font-size:.75rem;color:var(--muted)}
.more{text-align:center;padding-bottom:40px}
.more button,.btn{font:inherit;font-weight:600;padding:10px 20px;border-radius:10px;border:1px solid var(--accent);background:var(--card);color:var(--accent);cursor:pointer}
/* detail */
dialog{margin:auto;border:none;border-radius:18px;width:min(860px,96vw);max-height:92vh;padding:0;background:var(--bg);color:var(--ink)}
dialog::backdrop{background:rgba(20,22,28,.55)}
.d-head{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--line);padding:16px 18px;display:flex;gap:12px;align-items:flex-start}
.d-head h2{font:700 1.4rem var(--mono);word-break:break-word}
.close{margin-left:auto;border:none;background:#eee;border-radius:50%;width:36px;height:36px;font-size:1.2rem;cursor:pointer;flex:none}
.d-body{padding:18px;display:flex;flex-direction:column;gap:18px}
.d-body h4{font-size:1rem;margin-bottom:6px}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
pre{background:var(--code);color:#e8e6e3;border-radius:10px;padding:14px;overflow:auto;font:13px/1.55 var(--mono);position:relative}
.codewrap{position:relative}
.copy{position:absolute;top:8px;right:8px;font:600 .72rem var(--mono);padding:4px 10px;border-radius:6px;border:1px solid #444;background:#24272e;color:#ddd;cursor:pointer;z-index:1}
.ideas{display:flex;flex-direction:column;gap:6px;margin-top:6px}
.ideas li{list-style:none;padding:8px 10px;border-radius:8px;background:var(--bg);font-size:.92rem}
.ideas li.done{background:var(--accent-soft);font-weight:600}
.soonbox{border:2px dashed var(--line);border-radius:12px;padding:18px;text-align:center;color:var(--muted)}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tabs button{font:inherit;font-size:.9rem;padding:6px 14px;border-radius:99px;border:1px solid var(--line);background:var(--card);cursor:pointer}
.tabs button[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:#fff}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:30px 0 40px}
</style>
</head>
<body>
<header class="hero wrap">
  <div class="eyebrow">Library Atlas · Python & JS</div>
  <h1>__TITLE__</h1>
  <p class="lead">কোন লাইব্রেরি কী কাজে লাগে, কীভাবে ইনস্টল করতে হয়, কোড উদাহরণ আর কী প্রজেক্ট বানানো যায়, সব এক জায়গায়। যেকোনো কার্ডে চাপ দিলে বিস্তারিত দেখা যাবে।</p>
  <div class="stats">
    <div class="stat"><b id="s-total"></b><span>মোট লাইব্রেরি</span></div>
    <div class="stat"><b id="s-full"></b><span>সম্পূর্ণ উদাহরণসহ</span></div>
    <div class="stat"><b id="s-cat"></b><span>ক্যাটাগরি</span></div>
  </div>
</header>

<div class="controls"><div class="wrap row">
  <input id="q" type="search" placeholder="🔍 লাইব্রেরি বা কাজ খোঁজো… (যেমন: pdf, chart)">
  <select id="cat"><option value="">সব ক্যাটাগরি</option></select>
  <select id="kind"><option value="">Python + JS</option><option value="python">শুধু Python</option><option value="javascript">শুধু JavaScript</option></select>
  <select id="status"><option value="">সব অবস্থা</option><option value="full">✅ সম্পূর্ণ</option><option value="soon">⏳ শীঘ্রই আসছে</option></select>
</div></div>

<main class="wrap">
  <div class="count" id="count"></div>
  <div class="grid" id="grid"></div>
  <div class="more"><button id="more" hidden>আরো দেখাও</button></div>
</main>

<dialog id="dlg"><div id="dlg-in"></div></dialog>

<footer>© __YEAR__ · Python দিয়ে বানানো 🐍 · তালিকা: Library Atlas</footer>

<script>
const LIBS = __DATA__;
const PAGE = 60;
let shown = PAGE;
const $ = s => document.querySelector(s);
const bn = n => String(n).replace(/\d/g, d => "০১২৩৪৫৬৭৮৯"[d]);
function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v; else if (k.startsWith("on")) e[k] = v; else e.setAttribute(k, v);
  }
  for (const k of kids) if (k != null) e.append(k);
  return e;
}

const cats = [...new Set(LIBS.map(l => l.category))];
cats.forEach(c => $("#cat").append(el("option", {value: c}, c)));
$("#s-total").textContent = bn(LIBS.length);
$("#s-full").textContent = bn(LIBS.filter(l => l.full).length);
$("#s-cat").textContent = bn(cats.length);

function filtered() {
  const q = $("#q").value.trim().toLowerCase();
  const c = $("#cat").value, k = $("#kind").value, s = $("#status").value;
  return LIBS.filter(l =>
    (!c || l.category === c) && (!k || l.kind === k) &&
    (!s || (s === "full") === l.full) &&
    (!q || (l.name + " " + l.purpose + " " + l.category + " " + l.ideas.slice(0, 3).join(" ")).toLowerCase().includes(q)));
}

function render() {
  const list = filtered(), grid = $("#grid");
  grid.replaceChildren();
  list.slice(0, shown).forEach(l => {
    grid.append(el("button", {class: "card" + (l.full ? " full" : ""), type: "button", onclick: () => open(l)},
      el("div", {class: "meta"},
        el("span", {class: "tag " + l.kind}, l.kind === "python" ? "Python" : "JS"),
        el("span", {class: "badge" + (l.full ? "" : " soon")}, l.full ? "✅ সম্পূর্ণ" : "⏳ শীঘ্রই")),
      el("h3", {}, l.name),
      el("p", {}, l.purpose),
      el("span", {class: "cat"}, l.category)));
  });
  $("#count").textContent = bn(list.length) + "টা লাইব্রেরি পাওয়া গেছে";
  $("#more").hidden = list.length <= shown;
}

function codeBlock(code) {
  const btn = el("button", {class: "copy", type: "button"}, "কপি");
  btn.onclick = () => navigator.clipboard.writeText(code).then(() => {
    btn.textContent = "✔ কপি হয়েছে"; setTimeout(() => btn.textContent = "কপি", 1500);
  });
  return el("div", {class: "codewrap"}, btn, el("pre", {}, el("code", {}, code)));
}

function open(l) {
  const body = el("div", {class: "d-body"});
  body.append(el("div", {class: "box"}, el("h4", {}, "কী কাজে লাগে"),
    el("p", {}, l.full ? l.about : l.purpose)));

  if (l.full) {
    body.append(el("div", {}, el("h4", {}, "📦 ইনস্টল"), codeBlock(l.install)));
    const panel = el("div");
    const tabs = el("div", {class: "tabs", role: "tablist"});
    const views = {
      "🧩 সহজ উদাহরণ": () => [codeBlock(l.example)],
      "🚀 প্রজেক্ট": () => [el("div", {class: "box"}, el("h4", {}, l.project_title), el("p", {}, l.project_about)), codeBlock(l.project_code)],
    };
    Object.keys(views).forEach((name, i) => {
      const b = el("button", {type: "button", role: "tab", "aria-selected": i === 0 ? "true" : "false"}, name);
      b.onclick = () => { tabs.querySelectorAll("button").forEach(x => x.setAttribute("aria-selected", "false"));
        b.setAttribute("aria-selected", "true"); panel.replaceChildren(...views[name]()); };
      tabs.append(b);
    });
    panel.append(...views["🧩 সহজ উদাহরণ"]());
    body.append(tabs, panel);
  } else {
    body.append(el("div", {class: "soonbox"}, "⏳ এই লাইব্রেরির ব্যাখ্যা, ইনস্টল কমান্ড ও কোড উদাহরণ শীঘ্রই আসছে।"));
  }

  if (l.ideas.length) {
    const ul = el("ul", {class: "ideas"});
    l.ideas.slice(0, 12).forEach((t, i) =>
      ul.append(el("li", {class: l.full && i === 0 ? "done" : ""}, (l.full && i === 0 ? "✅ " : "💡 ") + t)));
    const extra = l.ideas.length > 12 ? el("p", {class: "cat"}, "+ আরো " + bn(l.ideas.length - 12) + "টা আইডিয়া") : null;
    body.append(el("div", {class: "box"}, el("h4", {}, "কী বানানো যায়"), ul, extra));
  }

  $("#dlg-in").replaceChildren(
    el("div", {class: "d-head"},
      el("div", {},
        el("div", {class: "meta"}, el("span", {class: "tag " + l.kind}, l.kind === "python" ? "Python" : "JavaScript"),
          el("span", {class: "cat"}, l.category)),
        el("h2", {}, l.name)),
      el("button", {class: "close", type: "button", "aria-label": "বন্ধ", onclick: () => $("#dlg").close()}, "×")),
    body);
  $("#dlg").showModal();
  $("#dlg").scrollTop = 0;
}

$("#dlg").addEventListener("click", e => { if (e.target.id === "dlg") e.target.close(); });
["#q", "#cat", "#kind", "#status"].forEach(s => $(s).addEventListener("input", () => { shown = PAGE; render(); }));
$("#more").onclick = () => { shown += PAGE; render(); };
render();
</script>
</body>
</html>
"""


def build():
    libs = load_libraries()
    data = json.dumps(libs, ensure_ascii=False).replace("</", "<\\/")
    page = (TEMPLATE.replace("__TITLE__", SITE_TITLE)
                    .replace("__YEAR__", str(date.today().year))
                    .replace("__DATA__", data))
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    full = sum(l["full"] for l in libs)
    print(f"index.html তৈরি হয়েছে ✔  ({len(libs)}টা লাইব্রেরি, {full}টা সম্পূর্ণ)")


if __name__ == "__main__":
    build()
