#!/usr/bin/env python3
"""Fetch korea.kr MOIS RSS; save the 10 newest items to news.json."""
import datetime as dt
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

URL = 'https://www.korea.kr/rss/dept_mois.xml'
req = urllib.request.Request(URL, headers={'User-Agent':'Mozilla/5.0 (compatible; IntegrityNewsBot/1.0)'})
with urllib.request.urlopen(req, timeout=35) as response:
    xml = response.read()
root = ET.fromstring(xml)
items = []
for entry in root.findall('.//item'):
    title = (entry.findtext('title') or '').strip()
    link = (entry.findtext('link') or '').strip()
    date = (entry.findtext('pubDate') or '').strip()
    if title and link.startswith(('https://www.korea.kr/', 'http://www.korea.kr/', 'https://korea.kr/')):
        items.append({'title': title, 'link': link.replace('http://','https://',1), 'date': date})
    if len(items) >= 10:
        break
if len(items) < 5:
    raise RuntimeError(f'RSS items fewer than 5 ({len(items)}); retaining existing news.json')
out = {'updated_at': dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).isoformat(timespec='minutes'), 'source':URL, 'items':items}
pathlib.Path(__file__).with_name('news.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Updated {len(items)} press releases')
