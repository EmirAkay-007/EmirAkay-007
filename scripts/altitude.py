#!/usr/bin/env python3
"""Draw the last year of GitHub contributions as a climb profile (SVG).

Every contribution adds one unit of altitude, so the line only ever climbs:
flat stretches are quiet weeks, steep steps are busy days.

Usage on GitHub Actions (see .github/workflows/altitude.yml):
    GH_TOKEN=... GH_LOGIN=EmirAkay-007 python3 scripts/altitude.py
Local test with a saved API response:
    python3 scripts/altitude.py --input calendar.json --output dist/altitude.svg
"""
import argparse
import datetime as dt
import json
import os
import urllib.request
from xml.sax.saxutils import escape

QUERY = """query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

COLORS = dict(black="#000000", navy9="#050D1F", navy7="#0B1F4B", line="#16306B",
              signal="#7FB2FF", paper="#E8EEFA", soft="#A9BEE6", muted="#6E8CC8", amber="#F2B544")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch(login, token):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": "bearer " + token, "Content-Type": "application/json", "User-Agent": "altitude-profile"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if data.get("errors"):
        raise SystemExit("GitHub API error: %s" % data["errors"])
    return data


def days_from(data):
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [(dt.date.fromisoformat(d["date"]), int(d["contributionCount"]))
            for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort()
    return days


def nice_ceiling(v):
    """Round up to an even number of grid units, so the middle line is a round value."""
    unit = 10 if v < 200 else 50 if v < 1000 else 100 if v < 5000 else 500
    return max(2 * unit, -(-int(v) // (2 * unit)) * 2 * unit)


def render(days, today=None):
    c = COLORS
    today = today or dt.date.today()
    W, H = 1760, 460
    x0, x1, y_top, y_base = 96, 1640, 150, 370
    n = len(days)
    total = sum(k for _, k in days)
    top = nice_ceiling(total)

    def X(i):
        return x0 + (x1 - x0) * i / max(n - 1, 1)

    def Y(v):
        return y_base - (y_base - y_top) * v / top

    cum, pts = 0, []
    for i, (_, k) in enumerate(days):
        cum += k
        pts.append((X(i), Y(cum)))
    line = "M" + "L".join("%.1f %.1f" % p for p in pts)
    area = line + "L%.1f %.1f L%.1f %.1f Z" % (pts[-1][0], y_base, pts[0][0], y_base)

    o = []
    a = o.append
    first, last = days[0][0], days[-1][0]
    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-labelledby="t d">' % (W, H, W // 2, H // 2))
    a('<title id="t">Climb profile: %d contributions in the last 12 months</title>' % total)
    a('<desc id="d">Cumulative GitHub contributions from %s to %s, drawn as an altitude line that climbs by one unit per contribution.</desc>'
      % (first.strftime("%d %b %Y"), last.strftime("%d %b %Y")))
    a('<defs><clipPath id="card"><rect width="%d" height="%d" rx="28"/></clipPath>' % (W, H))
    a('<radialGradient id="glow" cx="0.1" cy="0.1" r="0.9"><stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
      % (c["navy7"], c["navy9"], c["black"]))
    a('<linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0.38"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs>'
      % (c["signal"], c["signal"]))
    a('<g clip-path="url(#card)"><rect width="%d" height="%d" fill="%s"/><rect width="%d" height="%d" fill="url(#glow)" opacity="0.9"/></g>' % (W, H, c["black"], W, H))
    a('<rect x="1" y="1" width="%d" height="%d" rx="27" fill="none" stroke="%s" stroke-width="2"/>' % (W - 2, H - 2, c["line"]))

    a('<text x="48" y="74" font-family="%s" font-size="40" fill="%s">Climb profile</text>' % (SERIF, c["paper"]))
    a('<text x="48" y="110" font-family="%s" font-size="22" fill="%s">Cumulative contributions over the last 12 months</text>' % (SANS, c["soft"]))

    # altitude grid: three levels, recessive
    for v in (0, top // 2, top):
        y = Y(v)
        a('<path d="M%d %.1fH%d" stroke="%s" stroke-width="1.5" opacity="%s"/>' % (x0, y, x1, c["line"], "1" if v == 0 else "0.7"))
        a('<text x="%d" y="%.1f" text-anchor="end" font-family="%s" font-size="19" fill="%s">%d</text>' % (x0 - 16, y + 6, MONO, c["muted"], v))

    # month marks along the baseline
    for i, (d, _) in enumerate(days):
        if d.day == 1 and X(i) < x1 - 40:
            label = MONTHS[d.month - 1] + (" %d" % d.year if d.month == 1 else "")
            a('<path d="M%.1f %dv8" stroke="%s" stroke-width="1.5"/>' % (X(i), y_base, c["line"]))
            a('<text x="%.1f" y="%d" font-family="%s" font-size="19" fill="%s">%s</text>' % (X(i) + 6, y_base + 34, MONO, c["muted"], label))

    a('<path d="%s" fill="url(#fill)"/>' % area)
    a('<path d="%s" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>' % (line, c["signal"]))

    # steepest single day, labelled once
    best = max(range(n), key=lambda i: days[i][1])
    if days[best][1] > 0 and X(best) < x1 - 260:
        bx, by = pts[best]
        d = days[best][0]
        a('<circle cx="%.1f" cy="%.1f" r="6" fill="%s" stroke="%s" stroke-width="3"/>' % (bx, by, c["black"], c["signal"]))
        left = bx > x0 + 420          # label on the left of the point unless it would run off the card
        a('<text x="%.1f" y="%.1f" text-anchor="%s" font-family="%s" font-size="20" fill="%s">steepest day: +%d on %d %s</text>'
          % (bx - 16 if left else bx + 16, by - 12, "end" if left else "start", SANS, c["soft"], days[best][1], d.day, MONTHS[d.month - 1]))

    # aircraft at the current altitude
    ex, ey = pts[-1]
    plane = "M16 0L4 5L1 16L-3 16L-2 5L-10 4L-13 9L-16 9L-15 0L-16 -9L-13 -9L-10 -4L-2 -5L-3 -16L1 -16L4 -5Z"
    a('<g transform="translate(%.1f %.1f) rotate(-14) scale(1.25)"><path d="%s" fill="%s"/></g>' % (ex + 34, ey - 8, plane, c["amber"]))
    a('<text x="%.1f" y="%.1f" text-anchor="end" font-family="%s" font-size="30" fill="%s">%d<tspan font-family="%s" font-size="21" fill="%s"> contributions</tspan></text>'
      % (ex - 6, ey - 26, MONO, c["paper"], total, SANS, c["soft"]))

    a('<text x="%d" y="%d" text-anchor="end" font-family="%s" font-size="17" fill="%s">updated %d %s %d</text>'
      % (W - 48, H - 30, MONO, c["muted"], today.day, MONTHS[today.month - 1], today.year))
    a("</svg>")
    return "\n".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="saved GraphQL response (for local testing)")
    ap.add_argument("--output", default="dist/altitude.svg")
    args = ap.parse_args()
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = fetch(os.environ["GH_LOGIN"], os.environ["GH_TOKEN"])
    svg = render(days_from(data))
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote %s (%d bytes)" % (args.output, len(svg.encode("utf-8"))))


if __name__ == "__main__":
    main()
