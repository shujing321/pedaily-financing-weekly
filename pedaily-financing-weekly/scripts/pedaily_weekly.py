#!/usr/bin/env python3
"""抓取投资界融资周报列表页的候选事件。

该脚本只抓取公开列表页，不绕过反爬；单篇字段核验和赛道判断由 Agent
打开 article_url 后完成。输出 JSON，便于后续写入 Excel。
"""
from __future__ import annotations

import argparse
import html
import json
import re
import ssl
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

BASE = 'https://www.pedaily.cn/weeklyinvest/'


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; pedaily-financing-weekly/1.0)'})
    try:
        import certifi  # type: ignore
        context = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        context = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=context) as r:
        return r.read().decode('utf-8', errors='replace')


def mondays(start: date, end: date):
    current = start - timedelta(days=start.weekday())
    while current <= end:
        yield current
        current += timedelta(days=7)


def parse_page(page_url: str, text: str, default_week: date):
    text = html.unescape(text)
    # 事件新闻链接格式为 news.pedaily.cn/数字/数字.shtml 或 /first/数字.shtml。
    pattern = re.compile(r'<a[^>]+href=["\']([^"\']*news\.pedaily\.cn/[^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
    rows = []
    for match in pattern.finditer(text):
        link, title_html = match.groups()
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        title = re.sub(r'\s+', ' ', title)
        if not title or not re.search(r'融资|投资|轮融资|天使|种子|Pre-A|A轮|B轮|C轮|战略', title, re.I):
            continue
        link = urllib.parse.urljoin(page_url, link)
        before = re.sub(r'<[^>]+>', ' ', text[max(0, match.start()-1200):match.start()])
        date_match = re.findall(r'(\d{1,2})-(\d{1,2})', before)
        disclosure = ''
        if date_match:
            month, day = map(int, date_match[-1])
            try:
                disclosure = date(default_week.year, month, day).isoformat()
            except ValueError:
                pass
        rows.append({'week_page': page_url, 'disclosure_date': disclosure, 'title': title, 'article_url': link})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', required=True, help='YYYY-MM-DD')
    ap.add_argument('--end', required=True, help='YYYY-MM-DD')
    ap.add_argument('--output', default='pedaily_candidates.json')
    args = ap.parse_args()
    start = datetime.strptime(args.start, '%Y-%m-%d').date()
    end = datetime.strptime(args.end, '%Y-%m-%d').date()
    all_rows = []
    errors = []
    for monday in mondays(start, end):
        url = BASE + monday.strftime('%Y%m%d') + '/'
        try:
            all_rows.extend(parse_page(url, fetch(url), monday))
        except Exception as exc:
            errors.append({'url': url, 'error': str(exc)})
    deduped = {}
    for row in all_rows:
        deduped[row['article_url']] = row
    result = {'query': {'start': args.start, 'end': args.end}, 'events': list(deduped.values()), 'errors': errors}
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"候选事件 {len(result['events'])} 条，已写入 {args.output}")
    if errors:
        print(f"失败页面 {len(errors)} 个")


if __name__ == '__main__':
    main()
