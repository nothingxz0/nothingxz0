#!/usr/bin/env python3
"""Render a GitHub stats card in the same visual language as the 42 badge.

Third-party stat widgets each bring their own look, and half of them are dead
(github-readme-stats and github-profile-trophy are both returning 5xx/402 as of
now). Drawing it here keeps one consistent style and one less thing to rot.
"""
import json
import os
import sys
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "nothingxz0"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/stats.svg"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

sys.path.insert(0, os.path.dirname(__file__))
from theme import *
SHADES = RAMP

API = "https://api.github.com"
GQL = "https://api.github.com/graphql"


def get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-readme",
        "Accept": "application/vnd.github+json"})
    return json.loads(urllib.request.urlopen(req, timeout=45).read().decode())


def gql(query):
    body = json.dumps({"query": query}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-readme",
        "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=45).read().decode())


user = get(f"{API}/users/{USER}")

# total contributions across the last year, public only
contrib = 0
try:
    q = '{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions}}}}' % USER
    contrib = gql(q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
except Exception as e:
    print("contrib lookup failed:", e, file=sys.stderr)

# public repos owned by the user -> stars + language bytes
langs, stars, repos = {}, 0, []
page = 1
while True:
    batch = get(f"{API}/users/{USER}/repos?per_page=100&page={page}&type=owner")
    if not batch:
        break
    repos += batch
    page += 1
for r in repos:
    if r.get("fork"):
        continue
    stars += r.get("stargazers_count", 0)
    try:
        for k, v in get(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    except Exception:
        pass

total = sum(langs.values()) or 1
SHORT = {"Jupyter Notebook": "Jupyter", "Go Template": "Go tmpl"}
top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
top = [(SHORT.get(k, k), v) for k, v in top]
shown = sum(v for _, v in top)
rows = [(k, v / total * 100) for k, v in top]
if total - shown > 0:
    rows.append(("Other", (total - shown) / total * 100))

PAD, u = 34, "g"
BAR_Y, BAR_H = 104, 7
LEG_TOP = BAR_Y + BAR_H + 26
per_line = 3
lines = (len(rows) + per_line - 1) // per_line
H = LEG_TOP + lines * 20 + 6

figs = [(str(len([r for r in repos if not r.get('fork')])), "REPOS"),
        (str(contrib), "COMMITS / YR"),
        (str(user.get("followers", 0)), "FOLLOWERS"),
        (str(stars), "STARS")]

parts = [open_svg(H, f"GitHub statistics for {USER}"),
         f"<title>{USER} — {figs[0][0]} repos, {contrib} contributions in the last year</title>",
         defs(uid=u), clip(H, u), f'<g clip-path="url(#card{u})">', frame(H, u),
         orb(80, 10, 180, u, dur=13, delay=2), orb(700, H, 190, u, dur=16, delay=6),
         f'<g font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{DIM}">'
         f'<text x="{PAD}" y="36">GITHUB</text>'
         f'<text x="{W-PAD}" y="36" text-anchor="end">@{USER}</text></g>']

col = (W - PAD * 2) / 4
for i, (val, label) in enumerate(figs):
    x = PAD + col * i
    parts.append(f'<text x="{x:.1f}" y="80" font-family="{SANS}" font-size="30" font-weight="600" '
                 f'letter-spacing="-1" fill="{WHITE}" filter="url(#glow{u})">{val}</text>')
    parts.append(f'<text x="{x:.1f}" y="95" font-family="{MONO}" font-size="8.5" '
                 f'letter-spacing="1.6" fill="{DIM}">{label}</text>')

x = PAD
bar_w = W - PAD * 2
for i, (name, pct) in enumerate(rows):
    w = bar_w * pct / 100
    r_ = 'rx="3.5"' if (i == 0 or i == len(rows) - 1) else ''
    parts.append(f'<rect x="{x:.2f}" y="{BAR_Y}" width="{max(w,1):.2f}" height="{BAR_H}" {r_} '
                 f'fill="{SHADES[i % len(SHADES)]}"/>')
    x += w

for i, (name, pct) in enumerate(rows):
    cx = PAD + (i % per_line) * (bar_w / per_line)
    cy = LEG_TOP + (i // per_line) * 20
    parts.append(f'<rect x="{cx:.1f}" y="{cy-8:.1f}" width="7" height="7" rx="2" '
                 f'fill="{SHADES[i % len(SHADES)]}"/>')
    parts.append(f'<text x="{cx+15:.1f}" y="{cy:.1f}" font-family="{MONO}" font-size="10.5" '
                 f'fill="{MUTED}">{name} <tspan fill="{DIM}">{pct:.1f}%</tspan></text>')

parts += ["</g>", "</svg>"]
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(parts) + "\n")
print(f"wrote {OUT}: {figs[0][0]} repos, {contrib} contributions, {stars} stars, top={rows[0][0]}")
