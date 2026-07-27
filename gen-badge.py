#!/usr/bin/env python3
"""
Generate static SVG badge for SJ88 Mission Control.

Shows: "🚀 60 repos · 215 commits · 🟢 Live"

Endpoint: https://git88.sj88ai.com/badge.svg
Used in: README of every lnwsj repo (insert via <img src>)

Run: python3 gen-badge.py [--out=path]
"""
import json
import urllib.request
import urllib.error
import argparse
import os
import sys
import datetime
import hashlib

API_BASE = 'https://api.github.com'
USERNAME = 'lnwsj'
HOST = 'https://git88.sj88ai.com'


def fetch_repos_count(token=None):
    """Get total repos + recent commits count."""
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'sj88-badge-gen'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'

    # Total repos
    req = urllib.request.Request(f'{API_BASE}/users/{USERNAME}/repos?per_page=100', headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        repos = json.loads(resp.read().decode('utf-8'))

    total_repos = len(repos)
    # Public + not fork
    public_repos = len([r for r in repos if not r.get('fork')])

    # Active in 30 days
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    active = len([r for r in repos if datetime.datetime.fromisoformat(r['pushed_at'].replace('Z', '+00:00')) >= cutoff])

    # Live count (have homepage URL or 'live' in topics)
    live = len([r for r in repos if r.get('homepage')])

    return {
        'total': total_repos,
        'public': public_repos,
        'active_30d': active,
        'live': live,
        'fetched_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


def make_svg_left(repos):
    """Left half: gradient pink + label."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20" role="img" aria-label="SJ88 Mission Control">
  <title>SJ88 Mission Control</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="120" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="63" height="20" fill="#555"/>
    <rect x="63" width="57" height="20" fill="#ec4899"/>
    <rect width="120" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text aria-hidden="true" x="325" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="530">SJ88</text>
    <text x="325" y="140" transform="scale(.1)" fill="#fff" textLength="530">SJ88</text>
    <text aria-hidden="true" x="905" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="470">🚀 {repos} repos</text>
    <text x="905" y="140" transform="scale(.1)" fill="#fff" textLength="470">🚀 {repos} repos</text>
  </g>
</svg>'''


def make_svg_status(repos, active, live):
    """Right half: status + counts."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="280" height="20" role="img" aria-label="Status">
  <title>Status: {repos} repos · {active} active · {live} live</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="280" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="100" height="20" fill="#10b981"/>
    <rect x="100" width="180" height="20" fill="#6366f1"/>
    <rect width="280" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text aria-hidden="true" x="500" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="900">🟢 LIVE</text>
    <text x="500" y="140" transform="scale(.1)" fill="#fff" textLength="900">🟢 LIVE</text>
    <text aria-hidden="true" x="1900" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="1700">{active} active · {live} live</text>
    <text x="1900" y="140" transform="scale(.1)" fill="#fff" textLength="1700">{active} active · {live} live</text>
  </g>
</svg>'''


def make_full_badge(repos, active, live):
    """Full badge: 'SJ88 Mission Control | 🟢 LIVE | 60 repos · 50 active · 30 live'"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="450" height="28" role="img" aria-label="SJ88 Mission Control badge">
  <title>SJ88 Mission Control — {repos} repos · {active} active · {live} live</title>
  <defs>
    <linearGradient id="g1" x2="0" y2="100%">
      <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
      <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
  </defs>
  <clipPath id="r"><rect width="450" height="28" rx="4" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="180" height="28" fill="#1e1b4b"/>
    <rect x="180" width="90" height="28" fill="#ec4899"/>
    <rect x="270" width="180" height="28" fill="#6366f1"/>
    <rect width="450" height="28" fill="url(#g1)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text aria-hidden="true" x="900" y="190" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="1700">🚀 SJ88 Mission</text>
    <text x="900" y="180" transform="scale(.1)" fill="#fff" textLength="1700">🚀 SJ88 Mission</text>
    <text aria-hidden="true" x="2250" y="190" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="800">CONTROL</text>
    <text x="2250" y="180" transform="scale(.1)" fill="#fff" textLength="800">CONTROL</text>
    <text aria-hidden="true" x="3600" y="190" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="1700">{repos} repos · {active} active · {live} live</text>
    <text x="3600" y="180" transform="scale(.1)" fill="#fff" textLength="1700">{repos} repos · {active} active · {live} live</text>
  </g>
</svg>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='/workspace/lnwsj-mission-control/badge.svg', help='Output path')
    args = parser.parse_args()

    print('🏷️ SJ88 Badge Generator')
    token = os.environ.get('GITHUB_TOKEN')
    print(f'   Token: {"✓" if token else "✗"}')

    data = fetch_repos_count(token)
    print(f'   Total repos: {data["total"]}')
    print(f'   Public: {data["public"]}')
    print(f'   Active 30d: {data["active_30d"]}')
    print(f'   Live: {data["live"]}')

    svg = make_full_badge(data['public'], data['active_30d'], data['live'])
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(svg)

    size = os.path.getsize(args.out)
    print(f'\n✅ Wrote {args.out} ({size} bytes)')


if __name__ == '__main__':
    main()
