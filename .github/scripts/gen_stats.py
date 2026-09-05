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

BG, LINE, FG, MUTED = "#0d1117", "#21262d", "#e6edf3", "#7d8590"
SHADES = ["#e6edf3", "#b6c2cf", "#8b98a5", "#6a7681", "#4d5760", "#363d45"]

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

W, PAD = 460, 24
BAR_Y, BAR_H = 86, 8
LEG_TOP = BAR_Y + BAR_H + 22
per_line = 3
lines = (len(rows) + per_line - 1) // per_line
H = LEG_TOP + lines * 18 + 8

figs = [(str(len([r for r in repos if not r.get('fork')])), "REPOS"),
        (str(contrib), "COMMITS/YR"),
        (str(user.get("followers", 0)), "FOLLOWERS"),
        (str(stars), "STARS")]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub statistics for {USER}">',
    f'<title>{USER} — {figs[0][0]} repos, {contrib} contributions in the last year</title>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="{BG}" stroke="{LINE}"/>',
    '<g font-family="ui-monospace,SFMono-Regular,\'JetBrains Mono\',Menlo,monospace">',
    f'<text x="{PAD}" y="30" font-size="11" letter-spacing="2.4" fill="{MUTED}">GITHUB</text>',
    f'<text x="{W-PAD}" y="30" font-size="11" letter-spacing="1.2" fill="{MUTED}" text-anchor="end">@{USER}</text>',
]

col = (W - PAD * 2) / 4
for i, (val, label) in enumerate(figs):
    x = PAD + col * i
    parts.append(f'<text x="{x:.1f}" y="62" font-size="20" fill="{FG}">{val}</text>')
    parts.append(f'<text x="{x:.1f}" y="76" font-size="8.5" letter-spacing="1.1" fill="{MUTED}">{label}</text>')

# stacked language bar
x = PAD
bar_w = W - PAD * 2
for i, (name, pct) in enumerate(rows):
    w = bar_w * pct / 100
    r_ = 'rx="4"' if (i == 0 or i == len(rows) - 1) else ''
    parts.append(f'<rect x="{x:.2f}" y="{BAR_Y}" width="{max(w,1):.2f}" height="{BAR_H}" {r_} fill="{SHADES[i % len(SHADES)]}"/>')
    x += w

for i, (name, pct) in enumerate(rows):
    cx = PAD + (i % per_line) * (bar_w / per_line)
    cy = LEG_TOP + (i // per_line) * 18
    parts.append(f'<circle cx="{cx+3:.1f}" cy="{cy-3.5:.1f}" r="3.5" fill="{SHADES[i % len(SHADES)]}"/>')
    parts.append(f'<text x="{cx+13:.1f}" y="{cy:.1f}" font-size="10.5" fill="{MUTED}">{name} {pct:.1f}%</text>')

parts += ['</g>', '</svg>']

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(parts) + "\n")
print(f"wrote {OUT}: {figs[0][0]} repos, {contrib} contributions, {stars} stars, top={rows[0][0]}")
