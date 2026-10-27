#!/usr/bin/env python3
"""Collect recent Google News RSS headlines about Korean integrity policy."""
import datetime as dt
import email.utils
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

query = '행정안전부 청렴 OR 공직자 부패 OR 공직윤리'
url = 'https://news.google.com/rss/search?' + urlencode({'q':query,'hl':'ko','gl':'KR','ceid':'KR:ko'})
request = Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; NewsRSSReader/1.0)'})
with urlopen(request,timeout=30) as response:
    root = ET.fromstring(response.read())
items=[]
for entry in root.findall('./channel/item'):
    title=(entry.findtext('title') or '').strip()
    link=(entry.findtext('link') or '').strip()
    date=(entry.findtext('pubDate') or '').strip()
    source=(entry.findtext('source') or '').strip()
    if not title or not link.startswith('https://news.google.com/'):
        continue
    try: timestamp=email.utils.parsedate_to_datetime(date).isoformat()
    except (ValueError,TypeError): timestamp=''
    items.append({'title':title,'link':link,'date':date,'source':source,'sort_date':timestamp})
items.sort(key=lambda x:x['sort_date'],reverse=True)
items=items[:10]
if len(items)<5:
    raise RuntimeError(f'Only {len(items)} items returned; news.json left unchanged')
for item in items: item.pop('sort_date',None)
output={'updated_at':dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).isoformat(timespec='minutes'),'source':url,'items':items}
Path(__file__).with_name('news.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'[OK] Google News RSS: {len(items)} items -> news.json')
