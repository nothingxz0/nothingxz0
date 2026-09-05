#!/usr/bin/env python3
"""GitHub stats card.

Drawn here rather than pulled from a widget service: the popular ones
(github-readme-stats, github-profile-trophy, github-readme-activity-graph)
are all returning 5xx/402, and each would drag in its own visual style.
"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

USER = sys.argv[1] if len(sys.argv) > 1 else "nothingxz0"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/stats.svg"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API, GQL = "https://api.github.com", "https://api.github.com/graphql"
u = "g"

SHORT = {"Jupyter Notebook": "Jupyter", "Go Template": "Go tmpl"}


def get(url):
    r = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-readme",
        "Accept": "application/vnd.github+json"})
    return json.loads(urllib.request.urlopen(r, timeout=45).read().decode())


user = get(f"{API}/users/{USER}")

contrib = 0
try:
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar'
         '{totalContributions}}}}' % USER)
    r = urllib.request.Request(GQL, data=json.dumps({"query": q}).encode(), headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-readme",
        "Content-Type": "application/json"})
    contrib = (json.loads(urllib.request.urlopen(r, timeout=45).read().decode())
               ["data"]["user"]["contributionsCollection"]["contributionCalendar"]
               ["totalContributions"])
except Exception as e:
    print("contrib lookup failed:", e, file=sys.stderr)

langs, stars, repos, page = {}, 0, [], 1
while True:
    b = get(f"{API}/users/{USER}/repos?per_page=100&page={page}&type=owner")
    if not b:
        break
    repos += b
    page += 1
own = [r for r in repos if not r.get("fork")]
for r in own:
    stars += r.get("stargazers_count", 0)
    try:
        for k, v in get(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    except Exception:
        pass

total = sum(langs.values()) or 1
top = [(SHORT.get(k, k), v) for k, v in sorted(langs.items(), key=lambda kv: -kv[1])[:5]]
rows = [(k, v / total * 100) for k, v in top]
rest = total - sum(v for _, v in top)
if rest > 0:
    rows.append(("Other", rest / total * 100))

BAR_Y, BAR_H = 112, 6
LEG = BAR_Y + BAR_H + 28
per = 3
H = int(LEG + ((len(rows) + per - 1) // per) * 21 + 10)

figs = [(str(len(own)), "REPOS"), (str(contrib), "COMMITS / YR"),
        (str(user.get("followers", 0)), "FOLLOWERS"), (str(stars), "STARS")]

p = [head(H, f"GitHub statistics for {USER}"),
     f"<title>{USER} — {len(own)} repos, {contrib} contributions in the last year</title>",
     plate_defs(H, u), f'<g clip-path="url(#clip{u})">', plate(H, u), eyes(u),
     eyebrow(62, 32.5, "GITHUB"),
     eyebrow(W - PAD, 32.5, f"@{USER.upper()}", anchor="end", fill=GHOST)]

col = (W - PAD * 2) / 4
for i, (val, lab) in enumerate(figs):
    x = PAD + col * i
    p.append(f'<text x="{x:.1f}" y="88" font-family="{MONO}" font-size="34" '
             f'font-weight="500" letter-spacing="-0.34" fill="{BONE}">{val}</text>')
    p.append(f'<text x="{x:.1f}" y="103" font-family="{MONO}" font-size="9" '
             f'font-weight="500" letter-spacing="1.1" fill="{DIM}">{lab}</text>')

bar_w = W - PAD * 2
x = PAD
p.append(f'<rect x="{PAD}" y="{BAR_Y}" width="{bar_w}" height="{BAR_H}" rx="1" fill="{TRACK}"/>')
for i, (n, pc) in enumerate(rows):
    w = bar_w * pc / 100
    # rank-1 in crimson: the card's second and last crimson element, unglowed
    fill = f'{CRIM}" fill-opacity="0.88' if i == 0 else RAMP[(i - 1) % len(RAMP)]
    p.append(f'<rect x="{x:.2f}" y="{BAR_Y}" width="{max(w,1):.2f}" height="{BAR_H}" rx="1" '
             f'fill="{fill}"/>')
    x += w

for i, (n, pc) in enumerate(rows):
    cx = PAD + (i % per) * (bar_w / per)
    cy = LEG + (i // per) * 21
    sw = CRIM if i == 0 else RAMP[(i - 1) % len(RAMP)]
    p.append(f'<rect x="{cx:.1f}" y="{cy-7.5:.1f}" width="6" height="6" rx="1" fill="{sw}"/>')
    p.append(f'<text x="{cx+15:.1f}" y="{cy:.1f}" font-family="{MONO}" font-size="10.5" '
             f'fill="{MUTED}">{n} <tspan fill="{GHOST}">{pc:.1f}%</tspan></text>')

p += ["</g>", border(H), "</svg>"]
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT}: {len(own)} repos, {contrib} contributions, {stars} stars, top={rows[0][0]}")
