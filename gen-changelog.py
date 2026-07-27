#!/usr/bin/env python3
"""
Generate public changelog.xml (RSS 2.0 + Atom 1.0) for SJ88 Mission Control.

Fetches recent commits from GitHub API (across all lnwsj public repos),
generates both RSS 2.0 and Atom 1.0 feeds, writes to /var/www/git88.sj88ai.com/changelog.xml.

Run: python3 gen-changelog.py [--days=30] [--limit=100] [--out=path]
"""
import json
import urllib.request
import urllib.error
import argparse
import os
import datetime
import sys
from xml.sax.saxutils import escape as xml_escape

API_BASE = 'https://api.github.com'
USERNAME = 'lnwsj'
HOST = 'https://git88.sj88ai.com'
DAYS_BACK = 30  # default window
MAX_COMMITS = 100  # max commits in feed


def fetch(url, token=None):
    """Fetch JSON from GitHub API."""
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'sj88-changelog-gen'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read().decode('utf-8')
            return json.loads(data), dict(resp.headers)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise RuntimeError(f'GitHub API rate-limited (403). รอ 1 ชม. หรือใส่ GITHUB_TOKEN env var') from e
        raise


def get_recent_commits(token=None):
    """Fetch recent commits across all lnwsj public repos (since 30 days)."""
    print('📋 Step 1: Fetching repos...')
    repos, _ = fetch(f'{API_BASE}/users/{USERNAME}/repos?per_page=100&sort=pushed', token)
    print(f'   Found {len(repos)} repos')

    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS_BACK)
    active_repos = [r for r in repos if datetime.datetime.fromisoformat(r['pushed_at'].replace('Z', '+00:00')) >= cutoff]
    print(f'   Active in last {DAYS_BACK} days: {len(active_repos)} repos')

    all_commits = []
    for i, r in enumerate(active_repos):
        try:
            url = f'{API_BASE}/repos/{r["full_name"]}/commits?per_page=10&since={cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")}'
            commits, _ = fetch(url, token)
            for c in commits:
                if not c.get('commit', {}).get('author', {}).get('date'):
                    continue
                all_commits.append({
                    'repo': r['name'],
                    'repo_full': r['full_name'],
                    'sha': c['sha'],
                    'message': c['commit']['message'],
                    'author': c['commit']['author']['name'],
                    'email': c['commit']['author'].get('email', ''),
                    'date': c['commit']['author']['date'],
                    'url': c['html_url']
                })
        except Exception as e:
            print(f'   ⚠ {r["name"]}: {e}', file=sys.stderr)
        if (i + 1) % 10 == 0:
            print(f'   Progress: {i+1}/{len(active_repos)} repos...')

    # Sort by date desc
    all_commits.sort(key=lambda c: c['date'], reverse=True)
    return all_commits[:MAX_COMMITS], len(active_repos)


def build_xml(commits, repo_count):
    """Build combined RSS 2.0 + Atom 1.0 feed."""
    now = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    build_date = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Use latest commit for channel lastBuildDate
    if commits:
        latest = commits[0]
        latest_date = datetime.datetime.fromisoformat(latest['date'].replace('Z', '+00:00'))
        last_build = latest_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        last_build = now_str

    items_xml = []
    atom_entries = []
    for c in commits:
        date_obj = datetime.datetime.fromisoformat(c['date'].replace('Z', '+00:00'))
        rfc822 = date_obj.strftime('%a, %d %b %Y %H:%M:%S GMT')
        iso_date = c['date']
        # First line of message
        msg_first = c['message'].split('\n')[0][:200]
        msg_full = c['message'][:500]

        # GUID: use sha (stable) — pad with repo
        guid = f"{c['repo']}@{c['sha']}"

        # RSS item
        items_xml.append(f"""    <item>
      <title>{xml_escape(msg_first)}</title>
      <link>{xml_escape(c['url'])}</link>
      <guid isPermaLink="false">{xml_escape(guid)}</guid>
      <pubDate>{rfc822}</pubDate>
      <author>{xml_escape(c['email'])} ({xml_escape(c['author'])})</author>
      <category>github</category>
      <category>{xml_escape(c['repo'])}</category>
      <description><![CDATA[📦 {xml_escape(c['repo'])} · {xml_escape(msg_full)}]]></description>
    </item>""")

        # Atom entry
        atom_entries.append(f"""  <entry>
    <id>tag:{USERNAME}.github.io,2026:{guid}</id>
    <title>{xml_escape(msg_first)}</title>
    <link rel="alternate" type="text/html" href="{xml_escape(c['url'])}"/>
    <updated>{iso_date}</updated>
    <published>{iso_date}</published>
    <author><name>{xml_escape(c['author'])}</name></author>
    <category term="{xml_escape(c['repo'])}" label="{xml_escape(c['repo'])}"/>
    <category term="github" label="GitHub"/>
    <summary type="html"><![CDATA[📦 <b>{xml_escape(c['repo'])}</b> · {xml_escape(msg_full)}]]></summary>
  </entry>""")

    # Combined feed: <rss> wrapper with <atom:link> inside
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  Generated: {now.isoformat()}
  Source: {HOST}
  Commits: {len(commits)} (last {DAYS_BACK} days, {repo_count} active repos)
-->
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>SJ88 Mission Control — Commits Feed</title>
    <link>{HOST}/changelog.xml</link>
    <atom:link href="{HOST}/changelog.xml" rel="self" type="application/rss+xml"/>
    <description>🚀 Real-time GitHub commits from {USERNAME}'s {repo_count} active repos · Auto-generated from GitHub API</description>
    <language>en-us</language>
    <managingEditor>{USERNAME}@users.noreply.github.com ({USERNAME})</managingEditor>
    <webMaster>bot@{HOST} (Mavis)</webMaster>
    <lastBuildDate>{last_build}</lastBuildDate>
    <pubDate>{last_build}</pubDate>
    <ttl>30</ttl>
    <generator>Mavis changelog.py v1.0</generator>
{chr(10).join(items_xml)}
  </channel>
</rss>
<!--
  ═══════════════════════════════════════════════════════════
  ATOM 1.0 FEED (alternative format)
  ═══════════════════════════════════════════════════════════
-->
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>SJ88 Mission Control — Commits Feed (Atom)</title>
  <subtitle>🚀 Real-time GitHub commits from {USERNAME}</subtitle>
  <link href="{HOST}/changelog.xml" rel="self"/>
  <link href="{HOST}/"/>
  <id>tag:{USERNAME}.github.io,2026:sj88-changelog</id>
  <updated>{build_date}</updated>
  <author><name>Mavis</name><email>bot@{HOST}</email></author>
  <rights>MIT</rights>
  <generator uri="https://github.com/lnwsj/sj88-mission-control" version="v19.2">Mavis changelog.py</generator>
{chr(10).join(atom_entries)}
</feed>"""
    return xml


def main():
    global DAYS_BACK, MAX_COMMITS
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=DAYS_BACK, help='Days back to look')
    parser.add_argument('--limit', type=int, default=MAX_COMMITS, help='Max commits')
    parser.add_argument('--out', default='/workspace/lnwsj-mission-control/changelog.xml', help='Output path')
    args = parser.parse_args()

    DAYS_BACK = args.days
    MAX_COMMITS = args.limit

    token = os.environ.get('GITHUB_TOKEN')

    print(f'🚀 SJ88 Changelog Generator')
    print(f'   Window: {DAYS_BACK} days')
    print(f'   Limit: {MAX_COMMITS} commits')
    print(f'   Token: {"✓" if token else "✗ (60 req/hr limit)"}')
    print()

    commits, repo_count = get_recent_commits(token)
    print(f'\n📊 Got {len(commits)} commits from {repo_count} repos')

    xml = build_xml(commits, repo_count)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(xml)

    size = os.path.getsize(args.out)
    print(f'\n✅ Wrote {args.out} ({size} bytes, {len(xml)} chars)')


if __name__ == '__main__':
    main()
