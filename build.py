"""
build.py - "Python Library Atlas" ওয়েবসাইট বানায় (index.html)।

ফাইলগুলো:
- libraries.json : Atlas থেকে নেওয়া ৬৪৫টা লাইব্রেরির তালিকা
- details.py     : যেসব লাইব্রেরির ব্যাখ্যা, উদাহরণ ও field manual লেখা হয়েছে
- outputs.json   : render.py দিয়ে চালানো উদাহরণের আউটপুট (চার্টের ছবি, টার্মিনালের লেখা)

চালাও:  python build.py            → index.html + img/ ফোল্ডার (GitHub Pages-এর জন্য)
        python build.py --inline   → সব ছবি index.html-এর ভেতরে (একটা ফাইলেই সব)
"""

import json
import os
import re
import shutil
from datetime import date
from pathlib import Path

from details import DETAILS, examples_of
try:                                    # পাইথন প্লেগ্রাউন্ডের রানটাইম (একবারই পেজে বসে)
    from details import PYODIDE, PYPLAY_JS, PYPLAY_RUNNER, PYPLAY_SQL
    PYRT = dict(tpl=PYPLAY_JS, runner=PYPLAY_RUNNER, sqlpy=PYPLAY_SQL, index=PYODIDE)
except ImportError:
    PYRT = None

ROOT = Path(__file__).parent
SITE_TITLE = "Python Library Atlas"
FIRST_CATEGORY = "চার্ট, পরিসংখ্যান ও ডেটা ভিজুয়ালাইজেশন"   # এটা সবার আগে দেখাবে

PALETTE = ["#7c3aed", "#0284c7", "#0d9488", "#e11d48", "#d97706", "#4f46e5", "#db2777",
           "#059669", "#0891b2", "#9333ea", "#ea580c", "#15803d", "#be185d", "#6d28d9",
           "#c2410c", "#b45309", "#475569", "#57534e"]


def slug(name, used):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "lib"
    base, n = s, 2
    while s in used:
        s, n = f"{base}-{n}", n + 1
    used.add(s)
    return s


def slim_live(lv):
    """পাইথন প্লেগ্রাউন্ডে কোড আবার না রেখে শুধু সেটিং (কোড তো উদাহরণেই আছে)।"""
    if lv and "py" in lv:
        p = lv["py"]
        return dict(cdn=lv["cdn"], py=dict(pip=p["pip"], sql=p["sql"], pre=p["pre"]))
    return lv


def load():
    libs = json.loads((ROOT / "libraries.json").read_text(encoding="utf-8"))
    outputs_path = ROOT / "outputs.json"
    outputs = json.loads(outputs_path.read_text(encoding="utf-8")) if outputs_path.exists() else {}
    # GitHub-এর ওয়েব-আপলোডে এক ফাইল সর্বোচ্চ ২৫ MB → বড় outputs.json ভাগ করে outputs/part-*.json-এ রাখা যায়।
    # দুটোই থাকলে ভাগগুলো (নতুন) জেতে; পুরোনো hash না মিললে সেই আউটপুট এমনিতেই বাদ পড়ে।
    for part in sorted((ROOT / "outputs").glob("part-*.json")):
        outputs.update(json.loads(part.read_text(encoding="utf-8")))
    names = {l["name"] for l in libs}
    for key in DETAILS:
        if key not in names:
            raise SystemExit(f"details.py-র '{key}' নামটা libraries.json-এ নেই")

    import hashlib
    used, out = set(), []
    for l in libs:
        d = DETAILS.get(l["name"])
        item = dict(id=slug(l["name"], used), name=l["name"], cat=l["category"], kind=l["kind"],
                    tag=l["purpose"], ideas=l["ideas"][:12], nIdeas=len(l["ideas"]), full=bool(d), ex=[])
        if d:
            m = d.get("man", {})
            item.update(about=d["about"], install=d["install"], tag=m.get("tag") or l["purpose"],
                        man=dict(level=m.get("level", ""), tasks=m.get("tasks") or l["ideas"][:6],
                                 caps=m.get("caps", []), limits=m.get("limits", []), alt=m.get("alt", "")))
            for i, e in enumerate(examples_of(d)):
                o = outputs.get(f"{l['name']}::{i}")
                h = hashlib.sha1(e["code"].encode()).hexdigest()[:12]
                if o and o.get("hash") != h:
                    o = None                                   # কোড বদলেছে, পুরোনো আউটপুট বাদ
                item["ex"].append(dict(t=e["title"], d=e["about"], hint=e.get("hint"), code=e["code"],
                                       lang=e.get("lang", "python"), live=slim_live(e.get("live")),
                                       out=None if e.get("lang") == "js" else
                                       o and {k: o.get(k) for k in ("status", "text", "images", "files", "reason")}))
        item["ex"].sort(key=lambda e: e.get("hint") != "শোকেস")   # শোকেস আগে
        out.append(item)

    cat_order = []
    for l in out:
        if l["cat"] not in cat_order:
            cat_order.append(l["cat"])
    done = {c: sum(l["full"] for l in out if l["cat"] == c) for c in cat_order}
    original = {c: i for i, c in enumerate(cat_order)}
    cat_order.sort(key=lambda c: (c != FIRST_CATEGORY, -done[c], original[c]))

    cats = []
    for i, c in enumerate(cat_order):
        members = [l for l in out if l["cat"] == c]
        cats.append(dict(id=f"c{i + 1:02d}", name=c, col=PALETTE[i % len(PALETTE)],
                         blurb=", ".join(l["name"] for l in members[:4]) + (" …" if len(members) > 4 else "")))
    cid = {c["name"]: c["id"] for c in cats}
    for l in out:
        l["cat"] = cid[l["cat"]]
    order = {c["id"]: i for i, c in enumerate(cats)}
    out.sort(key=lambda l: (order[l["cat"]], not l["full"], -len(l["ex"])))
    return cats, out


def export_images(libs, inline=False):
    """outputs.json-এর ছবিগুলো img/ ফোল্ডারে আলাদা ফাইল হিসেবে লেখা।
    (ছবি HTML-এর ভেতরে data: হিসেবে থাকলে অনেক ব্রাউজার/প্রিভিউ সেগুলো দেখায় না)"""
    import base64
    import hashlib
    if inline:
        return 0
    folder = ROOT / "img"
    folder.mkdir(exist_ok=True)
    keep = set()
    for l in libs:
        for e in l["ex"]:
            o = e["out"]
            if not o or not o.get("images"):
                continue
            paths = []
            for uri in o["images"]:
                head, b64 = uri.split(",", 1)
                ext = head.split("/")[1].split(";")[0]          # webp / png
                raw = base64.b64decode(b64)
                name = hashlib.sha1(raw).hexdigest()[:16] + "." + ext
                if not (folder / name).exists():
                    (folder / name).write_bytes(raw)
                keep.add(name)
                paths.append("img/" + name)
            o["images"] = paths
    for f in folder.iterdir():                                  # পুরোনো ছবি মুছে ফেলা
        if f.name not in keep:
            f.unlink()
    if os.environ.get("GITHUB_ACTIONS"):
        # GitHub Actions-এ চললে ছবিগুলো সরাসরি সাইটের ফোল্ডারেও রাখা,
        # যাতে deploy.yml পুরোনো হলেও ছবি সাইটে ওঠে
        site_img = ROOT / "_site" / "img"
        site_img.mkdir(parents=True, exist_ok=True)
        for name in keep:
            shutil.copy2(folder / name, site_img / name)
    return len(keep)


def build():
    import sys
    cats, libs = load()
    n_files = export_images(libs, inline="--inline" in sys.argv)
    data = json.dumps(dict(cats=cats, libs=libs, pyrt=PYRT), ensure_ascii=False).replace("</", "<\\/")
    n_full = sum(l["full"] for l in libs)
    n_ex = sum(len(l["ex"]) for l in libs)
    n_img = sum(1 for l in libs for e in l["ex"] if e["out"] and e["out"].get("images"))
    page = (TEMPLATE.replace("__TITLE__", SITE_TITLE)
                    .replace("__YEAR__", str(date.today().year))
                    .replace("__DATA__", data))
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    if os.environ.get("GITHUB_ACTIONS"):
        (ROOT / "_site").mkdir(exist_ok=True)
        (ROOT / "_site" / "index.html").write_text(page, encoding="utf-8")
    print(f"index.html তৈরি ✔  {len(libs)}টা লাইব্রেরি · {n_full}টা সম্পূর্ণ · "
          f"{n_ex}টা উদাহরণ · {n_img}টায় ছবি · {(ROOT / 'index.html').stat().st_size / 1e6:.1f} MB"
          + (f" · img/ ফোল্ডারে {n_files}টা ছবি" if n_files else " · ছবি HTML-এর ভেতরে"))


TEMPLATE = r"""<!doctype html>
<html lang="bn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · পাইথন লাইব্রেরির জীবন্ত সংগ্রহ</title>
<meta name="description" content="৬৪৫টা পাইথন ও জাভাস্ক্রিপ্ট লাইব্রেরি: কী কাজে লাগে, চালানো উদাহরণ, আউটপুট আর প্রজেক্ট।">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#f6f2ff;--line:rgba(124,58,237,.13);--line2:rgba(124,58,237,.22);--tx:#140E29;--tx2:#4C4369;--mut:#6b6288;--faint:#a49cc0;--ac:#7C3AED;--acbg:rgba(124,58,237,.09);--ac2:#0D9488;--warn:#E11D48;--r:22px;
--sh:0 1px 0 rgba(255,255,255,.9) inset,0 10px 40px -14px rgba(76,29,149,.20),0 2px 6px rgba(20,14,41,.04);--sh2:0 1px 0 rgba(255,255,255,.9) inset,0 30px 80px -24px rgba(76,29,149,.32),0 4px 14px rgba(20,14,41,.06);
--sans:"Plus Jakarta Sans","Hind Siliguri","Noto Sans Bengali",system-ui,-apple-system,sans-serif;--disp:"Space Grotesk","Hind Siliguri","Plus Jakarta Sans",system-ui,sans-serif;--mono:"JetBrains Mono","Hind Siliguri",ui-monospace,"SF Mono",Menlo,Consolas,monospace;
--prism:linear-gradient(135deg,rgba(2,132,199,.55),rgba(124,58,237,.55) 35%,rgba(225,29,72,.45) 65%,rgba(13,148,136,.55));
--gblur:saturate(1.6) blur(20px)}
*{box-sizing:border-box}html,body{height:100%}
body{margin:0;color:var(--tx);font:14.5px/1.6 var(--sans);-webkit-font-smoothing:antialiased;display:grid;grid-template-columns:284px 1fr;grid-template-rows:60px 1fr;overflow:hidden;
 background:radial-gradient(1200px 700px at 12% -10%,#e9ddff 0,transparent 60%),radial-gradient(900px 600px at 100% 0,#dff3ff 0,transparent 55%),linear-gradient(180deg,#FAF7FF,#EFE5FF);background-attachment:fixed;transition:grid-template-columns .3s cubic-bezier(.2,.8,.2,1)}
a{color:var(--ac);text-decoration:none}button{font:inherit;color:inherit}
code{font-family:var(--mono);font-size:.88em;background:rgba(124,58,237,.08);color:#4c1d95;padding:1px 5px;border-radius:5px}
#liq{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
#liq i{position:absolute;width:46vmax;height:46vmax;border-radius:42% 58% 63% 37%/41% 44% 56% 59%;filter:blur(74px);opacity:.42;animation:liquidMorph 26s ease-in-out infinite alternate}
#liq i:nth-child(1){left:-12vmax;top:-14vmax;background:radial-gradient(circle at 30% 30%,#c4b5fd,#7c3aed 70%)}
#liq i:nth-child(2){right:-14vmax;top:8vmax;background:radial-gradient(circle at 40% 40%,#7dd3fc,#0284c7 70%);animation-duration:31s;opacity:.30}
#liq i:nth-child(3){left:30vw;bottom:-22vmax;background:radial-gradient(circle,#99f6e4,#0d9488 70%);animation-duration:36s;opacity:.22}
#liq i:nth-child(4){right:18vw;bottom:-10vmax;width:30vmax;height:30vmax;background:radial-gradient(circle,#fda4af,#e11d48 70%);animation-duration:22s;opacity:.18}
@keyframes liquidMorph{0%{transform:translate(0,0) rotate(0) scale(1)}50%{transform:translate(6vw,4vh) rotate(120deg) scale(1.12)}100%{transform:translate(-4vw,8vh) rotate(240deg) scale(.94)}}
#reticle{position:fixed;inset:0;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(124,58,237,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,.055) 1px,transparent 1px);background-size:72px 72px;mask-image:radial-gradient(ellipse at 50% 30%,#000 30%,transparent 85%);-webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000 30%,transparent 85%)}
#top,#side,#main{position:relative;z-index:1}
/* top bar */
#top{grid-column:1/-1;display:flex;align-items:center;gap:14px;padding:0 18px;background:rgba(250,247,255,.62);backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);border-bottom:1px solid rgba(124,58,237,.12);z-index:20}
#logo{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--tx);white-space:nowrap}
#logo i{width:30px;height:30px;border-radius:11px;background:conic-gradient(from 210deg,#0284c7,#7c3aed,#e11d48,#d97706,#0d9488,#0284c7);display:grid;place-items:center;color:#fff;font:700 12px var(--mono);font-style:normal;box-shadow:0 6px 18px -6px rgba(124,58,237,.6),inset 0 0 0 2px rgba(255,255,255,.4)}
#logo span{font:700 19px var(--disp);letter-spacing:-.02em;background:linear-gradient(90deg,#140E29,#4C1D95 60%,#0284C7);-webkit-background-clip:text;background-clip:text;color:transparent}
#logo em{font-style:normal;border:1px solid var(--line2);background:rgba(255,255,255,.5);border-radius:99px;padding:1px 8px;font:10.5px var(--mono);text-transform:uppercase;letter-spacing:.08em;color:var(--mut)}
#sbox{position:relative;flex:1;max-width:560px;margin-left:auto}
#q{width:100%;height:38px;border:1px solid rgba(124,58,237,.2);border-radius:14px;background:rgba(255,255,255,.7);padding:0 44px 0 38px;font:inherit;outline:none;transition:border-color .15s,box-shadow .15s}
#q:focus{border-color:var(--ac);box-shadow:0 0 0 4px rgba(124,58,237,.14)}
#sbox:before{content:"";position:absolute;left:13px;top:12px;width:11px;height:11px;border:2px solid var(--faint);border-radius:50%}
#sbox:after{content:"/";position:absolute;right:10px;top:9px;font:12px var(--mono);color:var(--mut);border:1px solid var(--line2);border-radius:6px;padding:1px 7px;background:rgba(255,255,255,.7)}
#res{position:absolute;top:44px;left:0;right:0;background:rgba(255,255,255,.94);backdrop-filter:blur(18px);border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh2);max-height:440px;overflow:auto;display:none;padding:6px}
#res.on{display:block}
#res a{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:9px;color:var(--tx)}
#res a.sel,#res a:hover{background:var(--acbg)}
#res a small{color:var(--mut);margin-left:auto;font-size:12px;white-space:nowrap;max-width:40%;overflow:hidden;text-overflow:ellipsis}
#res mark{background:#fef08a;color:inherit;border-radius:3px;padding:0 1px}
.tbtn{height:36px;border:1px solid var(--line2);border-radius:99px;background:rgba(255,255,255,.6);padding:0 14px;cursor:pointer;white-space:nowrap;color:#4c1d95;font:600 12.5px var(--sans)}
.tbtn:hover{border-color:var(--ac);background:#fff}
#menu{display:none}
#sidet{width:36px;height:36px;border-radius:12px;border:1px solid rgba(124,58,237,.18);background:rgba(255,255,255,.6);display:grid;place-content:center;gap:4px;cursor:pointer;flex:none}
#sidet i{display:block;width:16px;height:2px;border-radius:2px;background:#4c1d95}
body.side-hidden{grid-template-columns:0 1fr}body.side-hidden #side{padding:0;border:0;overflow:hidden;opacity:0}
/* sidebar */
#side{background:rgba(255,255,255,.38);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-right:1px solid rgba(124,58,237,.1);overflow:auto;padding:14px 10px 40px;scrollbar-width:thin;transition:opacity .25s}
#side .navtop{margin-bottom:10px;padding-bottom:10px;border-bottom:1px dashed var(--line2)}
#side .navtop a{display:flex;gap:8px;align-items:center;padding:7px 10px;border-radius:9px;color:var(--tx);font-weight:500}
#side .navtop a:hover{background:rgba(124,58,237,.06)}#side .navtop a.on{background:#fff;box-shadow:0 0 0 1px var(--line);color:var(--ac)}
#side .navtop a span{margin-left:auto;color:var(--faint);font:12px var(--sans)}
#side .grp{margin:2px 0 4px}
#side .gh{display:flex;align-items:center;gap:8px;width:100%;border:0;background:none;padding:7px 8px;border-radius:8px;cursor:pointer;font-weight:600;font-size:12px;letter-spacing:.02em;color:var(--mut);text-align:left}
#side .gh:hover{background:rgba(124,58,237,.06);color:var(--tx)}
#side .gh i{width:8px;height:8px;border-radius:3px;flex:none}
#side .gh small{margin-left:auto;font:600 11.5px var(--sans);white-space:nowrap}
#side .grp.closed .gl{display:none}
#side .gl a{display:flex;align-items:center;gap:8px;padding:4px 8px 4px 24px;border-radius:8px;color:var(--tx2);font-size:13.5px}
#side .gl a:hover{background:rgba(124,58,237,.06)}
#side .gl a.soon{color:var(--faint)}
#side .gl a.on{background:#fff;color:var(--ac);font-weight:600;box-shadow:0 0 0 1px var(--line),0 1px 3px rgba(0,0,0,.04)}
#side .gl a span{margin-left:auto;font:12px var(--sans);color:var(--faint)}
#side .gl a b.dot{width:6px;height:6px;border-radius:50%;background:#0d9488;flex:none;margin-left:-14px;box-shadow:0 0 0 3px rgba(13,148,136,.15)}
/* main */
#main{overflow:auto;scroll-behavior:smooth;background:transparent}
.wrap{max-width:1380px;margin:0 auto;padding:26px 30px 90px}
h1,h2,h3,h4{font-family:var(--disp);letter-spacing:-.02em}
.crumb{font-size:12.5px;color:var(--mut);display:flex;gap:6px;align-items:center;margin-bottom:12px;flex-wrap:wrap}
.crumb a{color:var(--mut)}.crumb a:hover{color:var(--ac)}
.glass,.ex,.cat,.tile,.man .box,.note,.soonbig{position:relative;background:linear-gradient(155deg,rgba(255,255,255,.66),rgba(255,255,255,.36))!important;backdrop-filter:var(--gblur);-webkit-backdrop-filter:var(--gblur);border:1px solid rgba(255,255,255,.85)!important;border-radius:var(--r)!important;box-shadow:var(--sh)}
.ex:before,.cat:before,.tile:before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;background:var(--prism);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:.35;pointer-events:none;transition:opacity .3s;z-index:2}
.ex:after,.cat:after,.tile:after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:radial-gradient(420px circle at var(--mx,50%) var(--my,-20%),rgba(255,255,255,.55),transparent 45%);opacity:0;transition:opacity .3s;z-index:2;mix-blend-mode:soft-light}
.ex:hover:before,.cat:hover:before,.tile:hover:before{opacity:.9}.ex:hover:after,.cat:hover:after,.tile:hover:after{opacity:1}
.ex:hover,.cat:hover,.tile:hover{box-shadow:var(--sh2);transform:translateY(-2px)}
/* hero */
.hero{position:relative;min-height:560px;border-radius:30px;overflow:hidden;background:linear-gradient(160deg,rgba(255,255,255,.55),rgba(240,232,255,.35));border:1px solid rgba(255,255,255,.9);box-shadow:var(--sh2)}
.hero canvas{position:absolute;inset:0;width:100%;height:100%}
.hero:after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;background:linear-gradient(90deg,rgba(250,247,255,.92) 0,rgba(250,247,255,.7) 34%,rgba(250,247,255,0) 58%)}
.hero>div{position:relative;z-index:1;max-width:680px;padding:56px 54px;pointer-events:none}.hero>div *{pointer-events:auto}
.hero .crumb{font:600 12px var(--sans);letter-spacing:.02em;color:#7c3aed;display:inline-flex;gap:8px;align-items:center;padding:5px 12px;border-radius:99px;background:rgba(255,255,255,.6);border:1px solid rgba(124,58,237,.18)}
.hero .crumb:before{content:"";width:7px;height:7px;border-radius:50%;background:#0d9488;box-shadow:0 0 0 4px rgba(13,148,136,.18);animation:pulseDot 2s infinite}
@keyframes pulseDot{50%{box-shadow:0 0 0 8px rgba(13,148,136,0)}}
.hero h1{font-size:clamp(38px,5vw,68px);line-height:1.02;font-weight:700;margin:20px 0 18px;color:#140E29}
.hero h1 em{font-style:normal;background:linear-gradient(100deg,#0284c7,#7c3aed 40%,#e11d48 75%,#d97706);-webkit-background-clip:text;background-clip:text;color:transparent;background-size:200% 100%;animation:shine 8s linear infinite}
@keyframes shine{to{background-position:200% 0}}
.hero p{color:#4C4369;font-size:16px;max-width:560px;margin:0 0 20px}
.stats{display:flex;gap:10px;flex-wrap:wrap}
.stats div{background:rgba(255,255,255,.62);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.9);border-radius:16px;box-shadow:var(--sh);padding:9px 14px}
.stats b{display:block;font:700 24px/1.15 var(--disp);background:linear-gradient(135deg,#140E29,#7c3aed);-webkit-background-clip:text;background-clip:text;color:transparent}
.stats small{color:var(--mut);font-size:12px}
.note{margin-top:16px;font-size:13px;color:var(--tx2);border-radius:14px!important;padding:11px 15px;max-width:600px}
.sec{margin-top:42px}
.sec>h2{font:600 28px/1.2 var(--disp);margin:0 0 4px}
.sec>p.lead{color:var(--mut);margin:0 0 18px;max-width:820px}
/* categories */
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.cat{display:block;padding:16px 16px 14px;color:var(--tx);transition:transform .25s,box-shadow .35s;overflow:hidden}
.cat i{display:block;width:34px;height:6px;border-radius:9px;margin-bottom:12px}
.cat b{font:600 15.5px var(--disp);display:block}.cat p{margin:3px 0 10px;color:var(--mut);font-size:12.5px;line-height:1.45}
.cat small{font:12px var(--sans);color:var(--faint)}
.bar{height:5px;border-radius:9px;background:rgba(124,58,237,.1);margin:8px 0 6px;overflow:hidden}.bar i{display:block;height:100%;border-radius:9px;margin:0;width:0}
/* lib header */
.lh{display:flex;gap:22px;align-items:flex-start;flex-wrap:wrap;padding:24px 26px;border-radius:24px!important}
.ico{width:64px;height:64px;border-radius:18px;display:grid;place-items:center;color:#fff;font:700 22px var(--disp);flex:none;box-shadow:inset 0 0 0 4px rgba(255,255,255,.2),0 10px 24px -10px rgba(76,29,149,.5)}
.lh h1{font:700 36px/1.1 var(--disp);margin:0 0 6px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.lh p{margin:0;color:var(--tx2);font-size:15.5px;max-width:780px}
.lh .acts{margin-left:auto;display:flex;gap:8px;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.chips span{background:rgba(255,255,255,.65);border:1px solid var(--line);border-radius:99px;padding:3px 11px;font-size:12px;color:var(--mut)}.chips b{color:var(--tx);font-weight:600}
.badge{font:600 11px var(--sans);border-radius:99px;padding:2px 9px;color:#fff;background:linear-gradient(135deg,#0d9488,#0284c7)}
.badge.soon{background:rgba(124,58,237,.12);color:#6b6288}
.badge.js{background:linear-gradient(135deg,#d97706,#e11d48)}
.star{font-size:17px;line-height:1}.star.on{color:#d97706;border-color:#fcd34d;background:#fffbeb}
/* example cards */
.exs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,470px),1fr));gap:20px;margin-top:22px;align-items:start}
.ex{display:flex;flex-direction:column;overflow:hidden;transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.ex.wide{grid-column:1/-1}
.ex>header{display:flex;align-items:center;gap:10px;padding:11px 12px 10px 16px;border-bottom:1px solid rgba(124,58,237,.08);background:rgba(255,255,255,.45)}
.ex .no{font:600 13px var(--sans);color:var(--faint)}
.ex h4{margin:0;font-size:15px;font-weight:600;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ex .libs{font-size:11.5px;color:var(--mut);white-space:nowrap}
.tb{display:flex;gap:4px}
.tb button{width:30px;height:28px;border-radius:10px;cursor:pointer;color:var(--mut);font-size:12.5px;display:grid;place-items:center;background:rgba(255,255,255,.55);border:1px solid rgba(255,255,255,.9);box-shadow:0 1px 0 #fff inset,0 2px 6px -2px rgba(76,29,149,.18);transition:transform .2s,background .2s}
.tb button:hover{background:#fff;transform:translateY(-1px);color:var(--tx)}
.tb button.on{background:var(--acbg);color:var(--ac)}
.tb button.cpy{width:auto;padding:0 10px;font-weight:700;color:var(--ac);white-space:nowrap}
.stage{position:relative;background:#faf7ff;min-height:200px;display:grid;place-items:center;overflow:hidden}
.stage img{display:block;width:100%;height:auto;max-height:560px;object-fit:contain;background:#fff;cursor:zoom-in}
.stage .dots{position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:6px;background:rgba(20,14,41,.55);padding:5px 8px;border-radius:99px}
.stage .dots button{width:8px;height:8px;border-radius:50%;border:0;background:rgba(255,255,255,.5);cursor:pointer;padding:0}.stage .dots button.on{background:#fff}
.stage.live{display:block;background:#fff}.stage.live iframe{display:block;width:100%;height:430px;border:0;background:#fff}
.stage.live .boot{height:430px;display:grid;place-items:center;color:var(--mut);font-size:13px}
.livechip{font:700 10px var(--sans);letter-spacing:.08em;color:#fff;background:linear-gradient(135deg,#e11d48,#d97706);border-radius:99px;padding:2px 8px;white-space:nowrap}
.livechip:before{content:"● "}
.ex:fullscreen .stage.live iframe,.ex.pfs .stage.live iframe{height:calc(100vh - 150px)}
.livechip.py{background:linear-gradient(135deg,#0d9488,#0284c7)}.livechip.py:before{content:"▶ "}
.pyrun{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:9px 14px;border-top:1px solid rgba(124,58,237,.08);background:rgba(250,247,255,.6);font-size:12px;color:var(--mut)}
.pyrun button{font:600 12px var(--sans);border:1px solid #0d9488;background:#0d9488;color:#fff;border-radius:99px;padding:6px 14px;cursor:pointer}
.pyrun button:hover{filter:brightness(1.08)}.pyrun.on{display:none}
.term{width:100%;align-self:stretch;margin:0;background:#140e29;color:#e9d5ff;font:12.5px/1.6 var(--mono);padding:16px 18px 16px 18px;white-space:pre-wrap;word-break:break-word;max-height:420px;overflow:auto}
.term:before{content:"● ● ●  output";display:block;color:#6b6288;font-size:10.5px;letter-spacing:.12em;margin-bottom:8px}
.term.sub{max-height:200px;border-top:1px solid rgba(255,255,255,.08)}
.skip{padding:30px 24px;text-align:center;color:var(--tx2);font-size:13.5px;max-width:420px}
.skip b{display:block;font:700 17px var(--disp);color:var(--tx);margin:8px 0 4px}
.skip .big{font-size:30px}
.skip code{display:inline-block;margin-top:10px}
.files{display:flex;gap:6px;flex-wrap:wrap;padding:8px 14px;border-top:1px solid rgba(124,58,237,.08);background:rgba(250,247,255,.6);font-size:12px;color:var(--mut)}
.files span{font:11.5px var(--mono);background:#fff;border:1px solid var(--line);border-radius:8px;padding:1px 8px;color:#4c1d95}
.exd{padding:11px 16px 14px;font-size:13.5px;color:var(--tx2);background-color:rgba(255,255,255,.35)}
.exd p{margin:0}
.exd .hint{display:inline-flex;gap:6px;align-items:center;margin-top:7px;color:var(--ac);font-size:12px;font-weight:600}
.exd .hint:before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor;box-shadow:0 0 0 3px rgba(124,58,237,.15)}
pre.code{margin:0;border-top:1px solid var(--line);background:#140e29;color:#ede9fe;padding:14px 16px;font:12.5px/1.6 var(--mono);overflow:auto;max-height:420px;white-space:pre;position:relative}
pre.code .k{color:#c4b5fd}pre.code .s{color:#86efac}pre.code .n{color:#fcd34d}pre.code .c{color:#a8a29e;font-style:italic}pre.code .f{color:#7dd3fc}pre.code .b{color:#f9a8d4}
.cwrap{position:relative}.cwrap[hidden]{display:none}
button.copy{position:absolute;top:8px;right:10px;z-index:3;border:0;border-radius:99px;padding:5px 12px;background:#7c3aed;color:#fff;font:600 11.5px var(--sans);cursor:pointer}
.ex:fullscreen,.ex.pfs{position:fixed!important;inset:0;z-index:80;border-radius:0!important;background:radial-gradient(1200px 700px at 10% -10%,#e9ddff,transparent 60%),linear-gradient(180deg,#FAF7FF,#EFE5FF)!important;overflow:auto}
.ex:fullscreen .stage,.ex.pfs .stage{flex:1;background:transparent}.ex:fullscreen .stage img,.ex.pfs .stage img{max-height:calc(100vh - 140px);width:auto;max-width:100%;border-radius:16px;box-shadow:var(--sh2)}
/* field manual */
.man{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:14px;margin-top:14px}
.man .box{padding:16px 18px}
.man .box.code{grid-column:1/-1;padding:0;overflow:hidden}
.man .box.code header{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line)}
.man .box.code pre{max-height:none;border:0}
.man h5{margin:0 0 8px;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ac)}
.man ul{margin:0;padding-left:18px}.man li{margin:3px 0}.man ul.lim li::marker{color:#e11d48}
.man p{margin:0;color:var(--tx2)}
.btn{border:1px solid var(--line2);background:#fff;border-radius:99px;padding:5px 12px;cursor:pointer;font-size:12.5px;color:var(--tx2)}
.btn:hover{border-color:var(--ac);color:var(--ac)}
.pn{display:flex;justify-content:space-between;gap:12px;margin-top:34px}
.pn a{flex:1;padding:14px 18px;color:var(--tx);display:flex;flex-direction:column;border-radius:16px!important}
.pn a:hover{border-color:var(--ac)!important}.pn a small{color:var(--mut)}.pn a.r{text-align:right}
/* tiles */
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:16px;margin-top:20px}
.tile{overflow:hidden;color:var(--tx);display:flex;flex-direction:column;transition:transform .25s,box-shadow .35s}
.tile .pv{aspect-ratio:16/9;border-bottom:1px solid rgba(124,58,237,.08);background:#faf7ff;display:grid;place-items:center;overflow:hidden;position:relative}
.tile .pv img{width:100%;height:100%;object-fit:cover;object-position:top}
.tile .pv pre{margin:0;width:100%;height:100%;background:#140e29;color:#c4b5fd;font:10.5px/1.5 var(--mono);padding:12px 14px;overflow:hidden;white-space:pre}
.tile .pv .ph{font:700 44px var(--disp);color:#fff;opacity:.95;text-shadow:0 6px 20px rgba(20,14,41,.25)}
.tile .m{padding:12px 15px 14px}.tile b{font:600 15.5px var(--disp)}.tile p{margin:3px 0 0;color:var(--mut);font-size:13px}
.tile small{font:12px var(--sans);color:var(--faint);margin-top:8px;display:block}
.soonbig{margin-top:22px;padding:34px 30px;text-align:center}
.soonbig b{display:block;font:700 22px var(--disp);margin:6px 0}.soonbig p{color:var(--tx2);margin:0 auto;max-width:560px}
.ideas{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:8px;margin-top:14px;padding:0;list-style:none}
.ideas li{background:rgba(255,255,255,.7);border:1px solid var(--line);border-radius:12px;padding:9px 12px;font-size:13.5px}
.ideas li:before{content:"💡 "}
.tbl{border-collapse:separate;border-spacing:0;width:100%;font-size:13.5px;background:rgba(255,255,255,.7);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.tbl td,.tbl th{border-bottom:1px solid var(--line);padding:9px 14px;text-align:left;vertical-align:top}
.tbl th{background:#f5f0ff;color:var(--mut);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.tbl td a{font-weight:600}
.tfin{width:100%;max-width:440px;height:38px;border:1px solid var(--line2);border-radius:12px;padding:0 12px;font:inherit;margin-bottom:12px;outline:none;background:rgba(255,255,255,.8)}
.tfin:focus{border-color:var(--ac);box-shadow:0 0 0 4px rgba(124,58,237,.12)}
footer{color:var(--mut);font-size:12.5px;margin-top:50px;border-top:1px solid var(--line);padding-top:18px}
.kbd{font:11px var(--mono);border:1px solid var(--line2);border-bottom-width:2px;border-radius:5px;padding:0 5px;background:rgba(255,255,255,.7)}
#toast{position:fixed;left:50%;top:76px;transform:translate(-50%,-20px);opacity:0;pointer-events:none;z-index:90;padding:10px 18px;border-radius:99px;background:rgba(20,14,41,.86);color:#fff;font:600 13px var(--sans);transition:all .3s}
#toast.on{opacity:1;transform:translate(-50%,0)}
#main .rv{opacity:0;transform:translateY(16px);transition:opacity .6s,transform .7s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
#main .rv.in{opacity:1;transform:none}
@media (max-width:900px){body{grid-template-columns:1fr}#side{position:fixed;top:60px;left:0;bottom:0;width:290px;z-index:30;transform:translateX(-100%);transition:transform .2s;box-shadow:var(--sh2);background:rgba(250,247,255,.96)}body.sideopen #side{transform:none}#menu{display:block}#sidet{display:none}#logo em{display:none}#logo span{font-size:16px}.hero{min-height:0}.hero:after{background:linear-gradient(180deg,rgba(250,247,255,.92),rgba(250,247,255,.6) 60%,rgba(250,247,255,.25))}.hero>div{padding:30px 22px}.wrap{padding:16px 12px 80px}.lh{padding:18px}.lh h1{font-size:28px}.lh .acts{margin-left:0}#top{gap:8px;padding:0 10px}}
@media (prefers-reduced-motion:reduce){#liq i,.hero h1 em{animation:none!important}#main .rv{opacity:1;transform:none;transition:none}}
</style>
</head>
<body>
<div id="liq" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div id="reticle" aria-hidden="true"></div>
<header id="top"><button class="tbtn" id="menu" aria-label="মেনু">☰</button><button id="sidet" title="সাইডবার লুকাও/দেখাও"><i></i><i></i><i></i></button><a id="logo" href="#/"><i>Py</i><span>Library Atlas</span><em>বাংলা</em></a><div id="sbox"><input id="q" type="search" placeholder="লাইব্রেরি বা উদাহরণ খোঁজো…" autocomplete="off"><div id="res"></div></div></header>
<nav id="side"></nav>
<main id="main"></main>
<script>
const DATA=__DATA__;
const CATS=DATA.cats,LIBS=DATA.libs,CATMAP={},LIBMAP={};
CATS.forEach(c=>CATMAP[c.id]=c);LIBS.forEach(l=>LIBMAP[l.id]=l);
const FULL=LIBS.filter(l=>l.full);
const esc=s=>String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const bn=n=>String(n).replace(/\d/g,d=>'০১২৩৪৫৬৭৮৯'[d]);
const pad2=n=>bn(String(n).padStart(2,'0'));
let FAV=[];try{FAV=JSON.parse(localStorage.getItem('pyatlas_fav')||'[]');}catch(e){}
const saveFav=()=>{try{localStorage.setItem('pyatlas_fav',JSON.stringify(FAV));}catch(e){}};
function toast(m){let t=document.getElementById('toast');if(!t){t=document.createElement('div');t.id='toast';document.body.appendChild(t);}t.textContent=m;t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('on'),1600);}
function copy(txt,msg){try{navigator.clipboard.writeText(txt).then(()=>toast(msg||'কপি হয়েছে'),()=>toast('কপি করা গেল না'));}catch(e){toast('কপি করা গেল না');}}

/* ---------- Python syntax highlight ---------- */
const KW=new Set('False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield match case'.split(' '));
const BI=new Set('print len range open int float str list dict set tuple sum min max sorted enumerate zip map filter abs round isinstance type super input any all next iter bool'.split(' '));
const JSKW=new Set('const let var function return new this if else for of in while do break continue class extends import from export default async await try catch finally throw typeof instanceof null undefined true false switch case'.split(' '));
function hl(src,lang){const js=lang==='js',kw=js?JSKW:KW;let o='',i=0;const n=src.length;
 while(i<n){const ch=src[i];
  if((!js&&ch==='#')||(js&&ch==='/'&&src[i+1]==='/')){let j=src.indexOf('\n',i);if(j<0)j=n;o+='<span class="c">'+esc(src.slice(i,j))+'</span>';i=j;continue;}
  if(js&&ch==='`'){let j=i+1;while(j<n&&src[j]!=='`'){if(src[j]==='\\')j++;j++;}j=Math.min(n,j+1);o+='<span class="s">'+esc(src.slice(i,j))+'</span>';i=j;continue;}
  if(ch==='"'||ch==="'"){let q=!js&&src.startsWith(ch.repeat(3),i)?ch.repeat(3):ch,j=i+q.length;
   while(j<n&&!src.startsWith(q,j)){if(src[j]==='\\')j++;if(q.length===1&&src[j]==='\n')break;j++;}j=Math.min(n,j+q.length);
   let k=i;while(!js&&k>0&&/[rbfuRBFU]/.test(src[k-1]))k--;o=o.slice(0,o.length-(i-k));o+='<span class="s">'+esc(src.slice(k,j))+'</span>';i=j;continue;}
  if(/[0-9]/.test(ch)&&!/[\w]/.test(src[i-1]||'')){let j=i;while(j<n&&/[0-9._xXa-fA-FeE]/.test(src[j]))j++;o+='<span class="n">'+esc(src.slice(i,j))+'</span>';i=j;continue;}
  if(/[A-Za-z_]/.test(ch)){let j=i;while(j<n&&/\w/.test(src[j]))j++;const w=src.slice(i,j);
   if(kw.has(w))o+='<span class="k">'+w+'</span>';else if(src[j]==='(')o+='<span class="'+(!js&&BI.has(w)?'b':'f')+'">'+w+'</span>';else o+=esc(w);i=j;continue;}
  o+=esc(ch);i++;}
 return o;}

/* ---------- pieces ---------- */
function libIcon(L,size){const c=CATMAP[L.cat].col,ini=L.name.replace(/[^A-Za-z0-9]/g,'').slice(0,2);const s=size?';width:'+size+'px;height:'+size+'px;font-size:'+size*.36+'px;border-radius:'+size*.3+'px':'';return '<div class="ico" style="background:linear-gradient(135deg,'+c+',#1c1636)'+s+'">'+esc(ini.charAt(0).toUpperCase()+ini.slice(1))+'</div>';}
function firstImg(L){const has=e=>e.out&&e.out.images&&e.out.images.length;const pick=L.ex.slice(2).find(has)||L.ex.find(has);return pick?pick.out.images[0]:null;}
function firstText(L){for(const e of L.ex)if(e.out&&e.out.text)return e.out.text;return L.ex.length?L.ex[0].code:null;}
function liveDoc(lv){const css=(lv.css||[]).map(u=>'<link rel="stylesheet" href="'+u+'">').join('');
 const js=(lv.cdn||[]).map(u=>'<script src="'+u+'" onerror="window.__libfail=1;show(\'লাইব্রেরি লোড হয়নি – ইন্টারনেট সংযোগ লাগে\')"><\/script>').join('');
 return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+css+'<style>html,body{margin:0;height:100%;background:#fff;font-family:system-ui,-apple-system,sans-serif;overflow:hidden}#app{position:relative;width:100%;height:100%;box-sizing:border-box;padding:10px}#app>svg{display:block}button{font:600 12px system-ui;border:1px solid #c4b5fd;background:#f5f3ff;color:#4c1d95;border-radius:99px;padding:6px 14px;cursor:pointer;z-index:5}#err{position:absolute;inset:0;display:none;place-items:center;text-align:center;padding:20px;color:#6b6288;font-size:14px;background:#faf7ff}</style></head><body><div id="app"></div><div id="err"></div><script>function show(m){var e=document.getElementById("err");e.style.display="grid";e.textContent="⚠ "+m;}window.onerror=function(m){if(/ResizeObserver loop/.test(m))return true;show(m);};<\/script>'+js+'<script>window.addEventListener("load",function(){if(window.__libfail)return;try{'+lv.js.replace(/<\/script/gi,'<\\/script')+'\n}catch(e){show(e.message);}});<\/script></body></html>';}
function pyJS(X,auto){const R=DATA.pyrt,p=X.live.py,J=v=>JSON.stringify(v);const sub={__CODE__:J(X.code),__PIP__:J(p.pip||[]),__SQL__:J(p.sql||false),__PRE__:J(p.pre||''),__INDEX__:J(R.index),__AUTO__:auto?'true':'false',__RUNNER__:J(R.runner),__SQLPY__:J(p.sql?R.sqlpy:'')};
 return R.tpl.replace(/__(CODE|PIP|SQL|PRE|INDEX|AUTO|RUNNER|SQLPY)__/g,m=>sub[m]);}
function bootLive(st,X){if(st._on)return;st._on=true;const lv=X.live.py?{cdn:X.live.cdn,css:[],js:pyJS(X,true)}:X.live;const f=document.createElement('iframe');f.title=X.t;f.setAttribute('sandbox','allow-scripts');f.setAttribute('loading','lazy');f.srcdoc=liveDoc(lv);st.innerHTML='';st.appendChild(f);}
function runPy(el,X){const old=el.querySelector('.stage'),sub=el.querySelector('.term.sub');if(sub)sub.remove();
 const st=document.createElement('div');st.className='stage live';old.replaceWith(st);el.querySelector('.pyrun').classList.add('on');bootLive(st,X);}
const LIO='IntersectionObserver' in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){bootLive(e.target,e.target._X);LIO.unobserve(e.target);}}),{rootMargin:'200px'}):null;
function imgFail(im){if(!im.dataset.retry){im.dataset.retry=1;setTimeout(()=>{im.src=im.getAttribute('src').split('?')[0]+'?r='+Date.now();},600);return;}
 const box=document.createElement('div');box.className='skip';box.innerHTML='<div class="big">🖼️</div><b>ছবিটা লোড হয়নি</b>ফাইলটা সাইটে পাওয়া যায়নি ('+esc(im.getAttribute('src').split('?')[0])+')। GitHub-এ outputs.json আর build.py আপলোড হয়েছে কিনা দেখো।';im.replaceWith(box);}
function stageHTML(X){const o=X.out;
 if(X.live&&!X.live.py)return '<div class="stage live"><div class="boot">লাইভ ডেমো লোড হচ্ছে…</div></div>';
 if(o&&o.images&&o.images.length){return '<div class="stage">'+'<img loading="lazy" alt="'+esc(X.t)+'" src="'+o.images[0]+'" onerror="imgFail(this)">'+(o.images.length>1?'<div class="dots">'+o.images.map((_,k)=>'<button data-k="'+k+'"'+(k?'':' class="on"')+' aria-label="ছবি '+(k+1)+'"></button>').join('')+'</div>':'')+'</div>'+(o.text?'<pre class="term sub">'+esc(o.text)+'</pre>':'');}
 if(o&&o.text)return '<div class="stage"><pre class="term">'+esc(o.text)+'</pre></div>';
 const why=o&&o.reason||(X.lang==='js'?'এটা Node.js বা নিজের ওয়েবপেজে চালানোর কোড':'আউটপুট এখনো তৈরি হয়নি');
 return '<div class="stage"><div class="skip"><div class="big">▶</div><b>নিজের কম্পিউটারে চালাও</b>'+esc(why)+', তাই এখানে আগে থেকে চালানো যায়নি। নিচের <span class="kbd">&lt;/&gt;</span> বাটনে কোড দেখো।</div></div>';}
function mountEx(L,X,i,into,showLib){const el=document.createElement('article');el.className='ex rv';el.id='ex-'+L.id+'-'+(i+1);
 const o=X.out||{};
 el.innerHTML='<header><span class="no">'+pad2(i+1)+'</span><h4 title="'+esc(X.t)+'">'+esc(X.t)+'</h4>'+(X.live?(X.live.py?'<span class="livechip py">চালানো যায়</span>':'<span class="livechip">লাইভ</span>'):'')+(showLib?'<a class="libs" href="#/l/'+L.id+'">'+esc(L.name)+'</a>':'')+'<div class="tb">'+(X.live&&!X.live.py?'<button data-a="re" title="আবার চালাও">↻</button>':'')+'<button data-a="cp" class="cpy" title="এক ক্লিকে পুরো কোড কপি">⧉ কপি</button><button data-a="link" title="এই উদাহরণের লিংক কপি">🔗</button><button data-a="code" title="কোড দেখাও">&lt;/&gt;</button><button data-a="wide" title="চওড়া করো">⤢</button><button data-a="fs" title="ফুলস্ক্রিন">⛶</button></div></header>'
  +stageHTML(X)+(X.live&&X.live.py?'<div class="pyrun"><button data-py>▶ ব্রাউজারে চালাও · কোড বদলাও</button><span>Python সরাসরি তোমার ব্রাউজারে চলবে (প্রথমবার কয়েক সেকেন্ড)</span></div>':'')+(o.files&&o.files.length?'<div class="files">তৈরি হলো: '+o.files.map(f=>'<span>'+esc(f)+'</span>').join('')+'</div>':'')
  +'<div class="exd"><p>'+esc(X.d||'')+'</p>'+(X.hint?'<span class="hint">'+esc(X.hint)+'</span>':'')+'</div>'
  +'<div class="cwrap" hidden><button class="copy">কোড কপি</button><pre class="code">'+hl(X.code,X.lang)+'</pre></div>';
 const tb=el.querySelector('.tb');
 if(X.live&&!X.live.py){const st=el.querySelector('.stage');st._X=X;if(LIO)LIO.observe(st);else bootLive(st,X);}
 if(X.live&&X.live.py)el.querySelector('[data-py]').onclick=()=>runPy(el,X);
 tb.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const a=b.dataset.a;
  if(a==='code'){const w=el.querySelector('.cwrap');w.hidden=!w.hidden;b.classList.toggle('on',!w.hidden);}
  if(a==='wide'){el.classList.toggle('wide');b.classList.toggle('on');}
  if(a==='cp'){copy(X.code,'কোড কপি হয়েছে');b.textContent='✓ কপি';b.classList.add('on');setTimeout(()=>{b.textContent='⧉ কপি';b.classList.remove('on');},1400);}
  if(a==='link')copy(location.href.split('#')[0]+'#/l/'+L.id+'/'+(i+1),'লিংক কপি হয়েছে');
  if(a==='fs')fullscreen(el);
  if(a==='re'){const st=el.querySelector('.stage');st._on=false;bootLive(st,X);}});
 el.querySelector('.copy').onclick=()=>copy(X.code,'কোড কপি হয়েছে');
 const img=el.querySelector('.stage img');if(img)img.onclick=()=>fullscreen(el);
 el.querySelectorAll('.dots button').forEach(b=>b.onclick=ev=>{ev.stopPropagation();img.src=o.images[+b.dataset.k];el.querySelectorAll('.dots button').forEach(x=>x.classList.toggle('on',x===b));});
 into.appendChild(el);return el;}
function fullscreen(el){if(document.fullscreenElement){document.exitFullscreen();return;}
 if(el.requestFullscreen&&!/iPhone|iPad/.test(navigator.userAgent))el.requestFullscreen().catch(()=>pfs(el));else pfs(el);}
function pfs(el){const on=el.classList.toggle('pfs');document.body.style.overflow=on?'hidden':'';if(on){const k=e=>{if(e.key==='Escape'){el.classList.remove('pfs');document.removeEventListener('keydown',k);}};document.addEventListener('keydown',k);}}
function tile(L,into){const a=document.createElement('a');a.className='tile rv';a.href='#/l/'+L.id;
 const img=firstImg(L),txt=!img&&L.full?firstText(L):null,c=CATMAP[L.cat].col;
 const pv=img?'<img loading="lazy" alt="" src="'+img+'">':txt?'<pre>'+esc(txt.split('\n').slice(0,12).join('\n'))+'</pre>':'<div class="ph">'+esc(L.name.replace(/[^A-Za-z0-9]/g,'').slice(0,2))+'</div>';
 a.innerHTML='<div class="pv"'+(img||txt?'':' style="background:linear-gradient(135deg,'+c+'cc,#1c1636)"')+'>'+pv+'</div><div class="m"><b>'+esc(L.name)+'</b> '+(L.full?'<span class="badge">✓ সম্পূর্ণ</span>':'<span class="badge soon">শীঘ্রই</span>')+(L.kind==='javascript'?' <span class="badge js">JS</span>':'')+(L.ex.some(e=>e.live&&!e.live.py)?' <span class="livechip">লাইভ</span>':'')+'<p>'+esc(L.tag)+'</p><small>'+(L.full?bn(L.ex.length)+'টা উদাহরণ':bn(L.nIdeas)+'টা প্রজেক্ট আইডিয়া')+'</small></div>';
 into.appendChild(a);}

/* ---------- views ---------- */
const $main=()=>document.getElementById('main');
function setView(h){const m=$main();m.scrollTop=0;m.innerHTML='<div class="wrap">'+h+'</div>';reveal();return m.firstChild;}
function reveal(){const els=$main().querySelectorAll('.rv');if(!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return;}
 const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{root:$main(),rootMargin:'80px'});
 setTimeout(()=>$main().querySelectorAll('.rv').forEach(e=>io.observe(e)),0);}
function viewHome(){const nEx=LIBS.reduce((a,l)=>a+l.ex.length,0),nImg=LIBS.reduce((a,l)=>a+l.ex.filter(e=>e.out&&e.out.images&&e.out.images.length).length,0);
 const w=setView('<section class="hero"><canvas id="herocv"></canvas><div><div class="crumb">পাইথন লাইব্রেরি আর্কাইভ · বাংলা সংস্করণ</div><h1>সব লাইব্রেরি, <em>চোখের সামনে</em>।</h1><p>পাইথনের ৬৪৫টা লাইব্রেরির জীবন্ত সংগ্রহ। প্রতিটা সম্পূর্ণ লাইব্রেরিতে আছে চালানো উদাহরণ, তার আসল আউটপুট (চার্ট, ফাইল, টার্মিনাল), পুরো কোড, প্রজেক্ট আর একটা field manual।</p><div class="stats"><div><b>'+bn(LIBS.length)+'</b><small>লাইব্রেরি</small></div><div><b>'+bn(FULL.length)+'</b><small>সম্পূর্ণ</small></div><div><b>'+bn(nEx)+'</b><small>উদাহরণ</small></div><div><b>'+bn(nImg)+'</b><small>ছবিসহ আউটপুট</small></div><div><b>'+bn(CATS.length)+'</b><small>ক্যাটাগরি</small></div></div><div class="note"><b>উদাহরণ কীভাবে কাজ করে:</b> প্রতিটা কোড আগে থেকে আসলেই চালানো হয়েছে, কার্ডে তার সত্যিকারের আউটপুট দেখানো আছে। কার্ডের <span class="kbd">&lt;/&gt;</span> বাটনে কোড, <span class="kbd">⛶</span> দিয়ে বড় করে দেখা।</div></div></section>'
 +'<section class="sec"><h2>শোকেস</h2><p class="lead">পত্রিকা আর গবেষণাপত্রের মানের চার্ট – প্রতিটার পুরো পাইথন কোড আছে, <span class="kbd">&lt;/&gt;</span> চাপলেই দেখবে।</p><div class="exs" id="feat"></div></section>'
 +'<section class="sec"><h2>ক্যাটাগরি অনুযায়ী দেখো</h2><p class="lead">একটা ক্যাটাগরি বেছে নাও, অথবা <span class="kbd">/</span> চেপে সব লাইব্রেরি আর উদাহরণে খোঁজো।</p><div class="cats" id="cats"></div></section>'
 +'<section class="sec"><h2>সম্পূর্ণ লাইব্রেরি</h2><p class="lead">এগুলোতে উদাহরণ, আউটপুট আর প্রজেক্ট সব আছে।</p><div class="tiles" id="done"></div></section>'
 +'<footer>© __YEAR__ · Python দিয়ে বানানো 🐍 · তালিকা: Library Atlas · কিবোর্ড: <span class="kbd">/</span> খোঁজো · <span class="kbd">[</span> <span class="kbd">]</span> আগের / পরের লাইব্রেরি</footer>');
 const feat=w.querySelector('#feat');let k=0;
 const liveFeat=[['d3-js',0],['apache-echarts',1]];
 const showcase=[];FULL.forEach(L=>L.ex.forEach((X,i)=>{if(X.hint==='শোকেস'&&X.out&&X.out.images&&X.out.images.length)showcase.push([L,X,i]);}));
 const pickIdx=[0,4,8,10,2,13];pickIdx.forEach(j=>{const s=showcase[j];if(s)mountEx(s[0],s[1],s[2],feat,true);});
 liveFeat.forEach(([id,i])=>{const L=LIBMAP[id];if(L&&L.ex[i])mountEx(L,L.ex[i],i,feat,true);});
 const cats=w.querySelector('#cats');CATS.forEach(c=>{const ls=LIBS.filter(l=>l.cat===c.id),d=ls.filter(l=>l.full).length;
  cats.insertAdjacentHTML('beforeend','<a class="cat rv" href="#/c/'+c.id+'"><i style="background:'+c.col+'"></i><b>'+esc(c.name)+'</b><p>'+esc(c.blurb)+'</p><div class="bar"><i style="width:'+(100*d/ls.length)+'%;background:'+c.col+'"></i></div><small>'+bn(ls.length)+'টা লাইব্রেরি · '+bn(d)+'টা সম্পূর্ণ</small></a>');});
 const dn=w.querySelector('#done');FULL.forEach(L=>tile(L,dn));
 heroAnim();reveal();}
function viewCat(id){const c=CATMAP[id];if(!c)return viewHome();const ls=LIBS.filter(l=>l.cat===id),d=ls.filter(l=>l.full).length;
 const w=setView('<div class="crumb"><a href="#/">হোম</a> / '+esc(c.name)+'</div><div class="lh glass"><div class="ico" style="background:linear-gradient(135deg,'+c.col+',#1c1636)">'+esc(c.name.charAt(0))+'</div><div><h1>'+esc(c.name)+'</h1><p>'+esc(c.blurb)+'</p><div class="chips"><span><b>'+bn(ls.length)+'</b>টা লাইব্রেরি</span><span><b>'+bn(d)+'</b>টা সম্পূর্ণ</span><span><b>'+bn(ls.reduce((a,l)=>a+l.ex.length,0))+'</b>টা উদাহরণ</span></div></div></div><div class="tiles" id="tl"></div>');
 const tl=w.querySelector('#tl');ls.forEach(L=>tile(L,tl));reveal();}
function neighbours(L){const list=L.full?FULL:LIBS,i=list.indexOf(L);return[list[(i-1+list.length)%list.length],list[(i+1)%list.length]];}
function viewLib(id,exn){const L=LIBMAP[id];if(!L)return viewHome();const c=CATMAP[L.cat],[P,N]=neighbours(L),fav=FAV.includes(id),m=L.man;
 const chips='<div class="chips">'+(m&&m.level?'<span>লেভেল <b>'+esc(m.level)+'</b></span>':'')+'<span>ভাষা <b>'+(L.kind==='python'?'Python':'JavaScript')+'</b></span>'+(L.full?'<span><b>'+bn(L.ex.length)+'</b>টা উদাহরণ</span>':'')+(L.install?'<span><code>'+esc(L.install.split('\n')[0])+'</code></span>':'')+'</div>';
 let h='<div class="crumb"><a href="#/">হোম</a> / <a href="#/c/'+c.id+'">'+esc(c.name)+'</a> / '+esc(L.name)+'</div><div class="lh glass">'+libIcon(L)+'<div style="flex:1;min-width:240px"><h1>'+esc(L.name)+(L.full?' <span class="badge">✓ সম্পূর্ণ</span>':' <span class="badge soon">শীঘ্রই আসছে</span>')+'</h1><p>'+esc(L.full?L.about:L.tag)+'</p>'+chips+'</div><div class="acts"><button class="tbtn star'+(fav?' on':'')+'" id="fv" title="প্রিয়">'+(fav?'★':'☆')+'</button>'+(L.full?'<button class="tbtn" id="allcode">সব কোড দেখাও</button>':'')+'</div></div>';
 if(L.full){h+='<div class="exs" id="exs"></div>'
  +'<section class="sec"><h2>Field manual</h2><p class="lead">'+esc(L.name)+' কী কাজে লাগে, কী পারে, কোথায় থামে।</p><div class="man">'
  +'<div class="box"><h5>যা যা বানানো যায়</h5><ul>'+m.tasks.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>'
  +(m.caps.length?'<div class="box"><h5>ক্ষমতা</h5><ul>'+m.caps.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>':'')
  +'<div class="box">'+(m.limits.length?'<h5>সীমাবদ্ধতা</h5><ul class="lim">'+m.limits.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':'')+'<h5 style="margin-top:'+(m.limits.length?14:0)+'px">ইনস্টল</h5><p><code>'+esc(L.install).replace(/\n/g,'</code><br><code>')+'</code></p>'+(m.alt?'<h5 style="margin-top:14px">বিকল্প</h5><p>'+m.alt.split(',').map(linkLib).join(', ')+'</p>':'')+'</div>'
  +'<div class="box code"><header><h5 style="margin:0">শুরুর কোড</h5><button class="btn" id="cp">কপি</button></header><pre class="code">'+hl(L.ex[0].code,L.ex[0].lang)+'</pre></div></div></section>';}
 else{h+='<div class="soonbig"><div style="font-size:34px">⏳</div><b>এই লাইব্রেরির উদাহরণ শীঘ্রই আসছে</b><p>'+esc(L.tag)+' নিচে Atlas থেকে নেওয়া প্রজেক্টের আইডিয়াগুলো দেখো।</p></div>'
  +'<section class="sec"><h2>কী বানানো যায়</h2><p class="lead">'+bn(L.nIdeas)+'টা প্রজেক্ট আইডিয়া'+(L.nIdeas>L.ideas.length?' (প্রথম '+bn(L.ideas.length)+'টা)':'')+'।</p><ul class="ideas">'+L.ideas.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></section>';}
 h+='<div class="pn"><a class="glass" href="#/l/'+P.id+'"><small>← আগের</small><b>'+esc(P.name)+'</b></a><a class="glass r" href="#/l/'+N.id+'"><small>পরের →</small><b>'+esc(N.name)+'</b></a></div>';
 const w=setView(h);
 if(L.full){const exs=w.querySelector('#exs');L.ex.forEach((X,k)=>mountEx(L,X,k,exs));
  w.querySelector('#allcode').onclick=e=>{const ws=[...w.querySelectorAll('.ex .cwrap')],open=ws.some(x=>x.hidden);ws.forEach(x=>x.hidden=!open);w.querySelectorAll('.ex [data-a=code]').forEach(b=>b.classList.toggle('on',open));e.currentTarget.textContent=open?'সব কোড লুকাও':'সব কোড দেখাও';};
  w.querySelector('#cp').onclick=()=>copy(L.ex[0].code,'কোড কপি হয়েছে');}
 w.querySelector('#fv').onclick=e=>{const b=e.currentTarget,k=FAV.indexOf(id);if(k<0)FAV.push(id);else FAV.splice(k,1);saveFav();b.classList.toggle('on',k<0);b.textContent=k<0?'★':'☆';buildSide();};
 reveal();
 if(exn){const t=document.getElementById('ex-'+id+'-'+exn);if(t)setTimeout(()=>{t.classList.add('in');t.scrollIntoView({block:'center'});t.style.outline='3px solid var(--ac)';setTimeout(()=>t.style.outline='',1600);},80);}}
function linkLib(name){const n=name.trim().toLowerCase();const L=LIBS.find(l=>l.name.toLowerCase()===n);return L?'<a href="#/l/'+L.id+'">'+esc(name.trim())+'</a>':esc(name.trim());}
function viewFav(){const ls=LIBS.filter(l=>FAV.includes(l.id));const w=setView('<div class="crumb"><a href="#/">হোম</a> / প্রিয়</div><div class="lh glass"><div class="ico" style="background:#d97706">★</div><div><h1>প্রিয় লাইব্রেরি</h1><p>'+(ls.length?'যেগুলোতে তুমি ☆ দিয়েছ। এই ব্রাউজারে সেভ থাকে।':'এখনো কিছু নেই। যেকোনো লাইব্রেরির পেজে ☆ চাপলে এখানে আসবে।')+'</p></div></div><div class="tiles" id="tl"></div>');ls.forEach(L=>tile(L,w.querySelector('#tl')));reveal();}
function viewIndex(){let rows='';CATS.forEach(c=>LIBS.filter(l=>l.cat===c.id&&l.full).forEach(L=>{rows+='<tr><td><a href="#/l/'+L.id+'">'+esc(L.name)+'</a><br><small style="color:var(--mut)">'+esc(c.name)+'</small></td><td>'+L.ex.map((X,k)=>'<a href="#/l/'+L.id+'/'+(k+1)+'" style="font-weight:400">'+pad2(k+1)+' · '+esc(X.t)+'</a>').join('<br>')+'</td></tr>';}));
 const w=setView('<div class="crumb"><a href="#/">হোম</a> / সম্পূর্ণ সূচি</div><div class="lh glass"><div class="ico" style="background:#140e29">≡</div><div><h1>সম্পূর্ণ সূচি</h1><p>সব সম্পূর্ণ লাইব্রেরি আর তাদের প্রতিটা উদাহরণ। উদাহরণে চাপলে সরাসরি সেখানে যাবে।</p></div></div><section class="sec"><input class="tfin" id="ixq" placeholder="সূচিতে খোঁজো…"><table class="tbl" id="ix"><tr><th style="width:240px">লাইব্রেরি</th><th>উদাহরণ</th></tr>'+rows+'</table></section>');
 w.querySelector('#ixq').addEventListener('input',e=>{const q=e.target.value.toLowerCase();w.querySelectorAll('#ix tr').forEach((r,i)=>{if(i)r.style.display=!q||r.textContent.toLowerCase().includes(q)?'':'none';});});}

/* ---------- sidebar & search ---------- */
let CLOSED=null;try{CLOSED=JSON.parse(localStorage.getItem('pyatlas_closed')||'null');}catch(e){}
if(!CLOSED){CLOSED={};CATS.forEach((c,i)=>{if(!LIBS.some(l=>l.cat===c.id&&l.full))CLOSED[c.id]=true;});}
function buildSide(){const sd=document.getElementById('side');let h='<div class="navtop"><a href="#/" data-r="">⌂ হোম</a><a href="#/index" data-r="index">≡ সম্পূর্ণ সূচি <span>'+bn(FULL.length)+'</span></a><a href="#/fav" data-r="fav">★ প্রিয়'+(FAV.length?'<span>'+bn(FAV.length)+'</span>':'')+'</a></div>';
 CATS.forEach(c=>{const ls=LIBS.filter(l=>l.cat===c.id),d=ls.filter(l=>l.full).length;
  h+='<div class="grp'+(CLOSED[c.id]?' closed':'')+'" data-c="'+c.id+'"><button class="gh"><i style="background:'+c.col+'"></i>'+esc(c.name)+'<small>'+bn(d)+'/'+bn(ls.length)+'</small></button><div class="gl">'+ls.map(l=>'<a href="#/l/'+l.id+'" data-l="'+l.id+'"'+(l.full?'':' class="soon"')+'>'+(l.full?'<b class="dot"></b>':'')+esc(l.name)+'<span>'+(l.full?bn(l.ex.length):'·')+'</span></a>').join('')+'</div></div>';});
 sd.innerHTML=h;sd.querySelectorAll('.gh').forEach(b=>b.onclick=()=>{const g=b.parentNode;g.classList.toggle('closed');CLOSED[g.dataset.c]=g.classList.contains('closed');try{localStorage.setItem('pyatlas_closed',JSON.stringify(CLOSED));}catch(e){}});markSide();}
function markSide(){const p=location.hash.replace(/^#\/?/,'').split('/');document.querySelectorAll('#side a').forEach(a=>a.classList.toggle('on',(p[0]==='l'&&a.dataset.l===p[1])||(a.dataset.r!==undefined&&a.dataset.r===p[0]&&p[0]!=='l')));
 const on=document.querySelector('#side .gl a.on');if(on){const g=on.closest('.grp');g.classList.remove('closed');const sd=document.getElementById('side'),r=on.getBoundingClientRect(),sr=sd.getBoundingClientRect();if(r.top<sr.top+60||r.bottom>sr.bottom-20)sd.scrollTop+=r.top-sr.top-sr.height/2;}}
function fz(q,s){q=q.toLowerCase();const t=s.toLowerCase(),i0=t.indexOf(q);if(i0>=0)return{sc:100-i0-t.length*.1+(i0===0?30:0),ix:[...Array(q.length).keys()].map(k=>k+i0)};let i=0,sc=0,last=-2;const ix=[];for(let k=0;k<t.length&&i<q.length;k++){if(t[k]===q[i]){ix.push(k);sc+=k===last+1?3:1;last=k;i++;}}return i===q.length&&q.length>1?{sc:sc-t.length*.05,ix}:null;}
function mk(s,ix){let o='';for(let i=0;i<s.length;i++)o+=ix&&ix.includes(i)?'<mark>'+esc(s[i])+'</mark>':esc(s[i]);return o;}
let SIDX=null;function sindex(){if(SIDX)return SIDX;SIDX=[];LIBS.forEach(L=>{SIDX.push({k:'lib',L,txt:L.name,sub:CATMAP[L.cat].name,extra:L.tag+' '+L.ideas.join(' ')});L.ex.forEach((X,i)=>SIDX.push({k:'ex',L,i,txt:X.t,sub:L.name,extra:X.d||''}));});return SIDX;}
function search(q){const out=[];if(!q.trim())return out;for(const e of sindex()){const a=fz(q,e.txt);let sc=a?a.sc+(e.k==='lib'?40:0)+(e.L.full?15:0):-1;if(sc<0&&q.length>1&&(e.extra+' '+e.sub).toLowerCase().includes(q.toLowerCase()))sc=10+(e.L.full?8:0);if(sc>=0)out.push({e,sc,ix:a&&a.ix});}return out.sort((x,y)=>y.sc-x.sc).slice(0,16);}
function initSearch(){const q=document.getElementById('q'),res=document.getElementById('res');let sel=0;
 const draw=()=>{const cur=search(q.value);sel=0;res.innerHTML=cur.map((r,i)=>'<a href="#/l/'+r.e.L.id+(r.e.k==='ex'?'/'+(r.e.i+1):'')+'" class="'+(i===sel?'sel':'')+'">'+(r.e.k==='lib'?libIcon(r.e.L,26):'<span style="width:26px;text-align:center;color:var(--faint);font:12px var(--mono)">'+pad2(r.e.i+1)+'</span>')+'<span>'+(r.e.k==='lib'?'<b>'+mk(r.e.txt,r.ix)+'</b>'+(r.e.L.full?' ✓':''):mk(r.e.txt,r.ix))+'</span><small>'+esc(r.e.sub)+'</small></a>').join('')||(q.value.trim()?'<div style="padding:12px;color:var(--mut)">কিছু পাওয়া যায়নি। "chart", "pdf", "excel" এর মতো শব্দ দিয়ে খোঁজো।</div>':'');res.classList.toggle('on',!!q.value.trim());};
 q.addEventListener('input',draw);q.addEventListener('focus',()=>{if(q.value.trim())draw();});
 q.addEventListener('keydown',e=>{const as=res.querySelectorAll('a');if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();sel=Math.max(0,Math.min(as.length-1,sel+(e.key==='ArrowDown'?1:-1)));as.forEach((a,i)=>a.classList.toggle('sel',i===sel));if(as[sel])as[sel].scrollIntoView({block:'nearest'});}if(e.key==='Enter'&&as[sel]){location.hash=as[sel].getAttribute('href');q.blur();res.classList.remove('on');}if(e.key==='Escape'){q.value='';res.classList.remove('on');q.blur();}});
 document.addEventListener('click',e=>{if(!e.target.closest('#sbox'))res.classList.remove('on');});res.addEventListener('click',()=>{res.classList.remove('on');q.value='';});
 document.addEventListener('keydown',e=>{const tg=e.target.tagName;if(tg==='INPUT'||tg==='TEXTAREA'||e.target.isContentEditable)return;if(e.key==='/'){e.preventDefault();q.focus();}
  const p=location.hash.split('/');if(p[1]==='l'&&(e.key==='['||e.key===']')){const L=LIBMAP[p[2]];if(L){const [P,N]=neighbours(L);location.hash='#/l/'+(e.key===']'?N:P).id;}}});}
function route(){const p=location.hash.replace(/^#\/?/,'').split('/');document.body.classList.remove('sideopen');stopHero();
 if(p[0]==='l')viewLib(p[1],p[2]);else if(p[0]==='c')viewCat(p[1]);else if(p[0]==='fav')viewFav();else if(p[0]==='index')viewIndex();else viewHome();markSide();}

/* ---------- hero animation ---------- */
let HERO=null;function stopHero(){if(HERO){cancelAnimationFrame(HERO);HERO=null;}}
function heroAnim(){const cv=document.getElementById('herocv');if(!cv)return;const box=cv.parentNode,d=Math.min(2,window.devicePixelRatio||1);let w=box.clientWidth,h=box.clientHeight;cv.width=w*d;cv.height=h*d;const ctx=cv.getContext('2d');ctx.setTransform(d,0,0,d,0,0);
 let seed=42;const r=()=>(seed=(seed*16807)%2147483647)/2147483647;const P=[];
 for(let i=0;i<90;i++)P.push({x:w*.4+r()*w*.6,y:r()*h,vx:(r()-.5)*16,vy:(r()-.5)*16,c:CATS[i%CATS.length].col,s:2+r()*3.5});
 let mx=-999,my=-999;box.addEventListener('pointermove',e=>{const b=cv.getBoundingClientRect();mx=e.clientX-b.left;my=e.clientY-b.top;});box.addEventListener('pointerleave',()=>{mx=my=-999;});
 const still=matchMedia('(prefers-reduced-motion: reduce)').matches;let last=0;
 const frame=ts=>{const dt=Math.min(.05,(ts-last)/1000||.016);last=ts;ctx.clearRect(0,0,w,h);
  for(const p of P){if(!still){p.x+=p.vx*dt;p.y+=p.vy*dt;}if(p.x<w*.25||p.x>w)p.vx*=-1;if(p.y<0||p.y>h)p.vy*=-1;const dx=p.x-mx,dy=p.y-my,dd=Math.hypot(dx,dy);if(dd<120&&dd>1){p.x+=dx/dd*(120-dd)*.04;p.y+=dy/dd*(120-dd)*.04;}}
  ctx.lineWidth=1;for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++){const a=P[i],b=P[j],dd=Math.hypot(a.x-b.x,a.y-b.y);if(dd<95){ctx.strokeStyle='rgba(124,58,237,'+(1-dd/95)*.25+')';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}
  for(const p of P){ctx.fillStyle=p.c;ctx.globalAlpha=.85;ctx.beginPath();ctx.arc(p.x,p.y,p.s,0,Math.PI*2);ctx.fill();}ctx.globalAlpha=1;
  if(!document.hidden&&!still)HERO=requestAnimationFrame(frame);};
 HERO=requestAnimationFrame(frame);}

/* ---------- boot ---------- */
buildSide();initSearch();route();window.addEventListener('hashchange',route);
document.getElementById('menu').onclick=()=>document.body.classList.toggle('sideopen');
document.getElementById('sidet').onclick=()=>document.body.classList.toggle('side-hidden');
document.addEventListener('pointermove',e=>{const c=e.target.closest&&e.target.closest('.ex,.cat,.tile');if(!c)return;const b=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-b.left)+'px');c.style.setProperty('--my',(e.clientY-b.top)+'px');},{passive:true});
</script>
</body>
</html>
"""


def split_outputs(limit_mb=9):
    """outputs.json → outputs/part-01.json, part-02.json … (প্রতিটা ≤ limit_mb), যাতে ব্রাউজার দিয়ে GitHub-এ আপলোড করা যায়।"""
    data = json.loads((ROOT / "outputs.json").read_text(encoding="utf-8"))
    folder = ROOT / "outputs"
    folder.mkdir(exist_ok=True)
    for old in folder.glob("part-*.json"):
        old.unlink()
    parts, cur, size = [], {}, 0
    for k, v in data.items():
        n = len(json.dumps({k: v}, ensure_ascii=False).encode("utf-8"))
        if cur and size + n > limit_mb * 1024 * 1024:
            parts.append(cur); cur, size = {}, 0
        cur[k] = v; size += n
    if cur:
        parts.append(cur)
    for i, part in enumerate(parts, 1):
        f = folder / f"part-{i:02d}.json"
        f.write_text(json.dumps(part, ensure_ascii=False), encoding="utf-8")
        print(f"{f.name}: {len(part)}টা আউটপুট, {f.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    import sys
    if "--split" in sys.argv:
        split_outputs()
    else:
        build()
