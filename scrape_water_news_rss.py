#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
جمع‌آوری اخبار آب منطقه‌ای خراسان رضوی از RSS feeds
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime
import re
from xml.etree import ElementTree as ET

class RSSNewsSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        }

        # لیست RSS feeds سایت‌های خبری ایرانی
        self.rss_feeds = [
            {
                'name': 'ایرنا',
                'url': 'https://www.irna.ir/rss',
                'category': 'general'
            },
            {
                'name': 'ایسنا',
                'url': 'https://www.isna.ir/rss',
                'category': 'general'
            },
            {
                'name': 'مهر',
                'url': 'https://www.mehrnews.com/rss',
                'category': 'general'
            },
            {
                'name': 'تسنیم',
                'url': 'https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%DB%8C%D8%B1%D8%A7%D9%86',
                'category': 'iran'
            },
            {
                'name': 'فارس',
                'url': 'https://www.farsnews.ir/rss',
                'category': 'general'
            },
            {
                'name': 'ایلنا',
                'url': 'https://www.ilna.ir/rss',
                'category': 'general'
            },
        ]

    def fetch_rss(self, feed_url, timeout=20):
        """دریافت و پارس کردن RSS feed"""
        try:
            response = requests.get(feed_url, headers=self.headers, timeout=timeout)
            response.raise_for_status()

            # پارس XML
            root = ET.fromstring(response.content)

            items = []

            # پیدا کردن تمام item ها در RSS
            for item in root.findall('.//item'):
                try:
                    title = item.find('title')
                    link = item.find('link')
                    description = item.find('description')
                    pubDate = item.find('pubDate')

                    item_data = {
                        'title': title.text if title is not None else '',
                        'url': link.text if link is not None else '',
                        'description': description.text if description is not None else '',
                        'pubDate': pubDate.text if pubDate is not None else '',
                    }

                    items.append(item_data)
                except Exception as e:
                    print(f"Error parsing item: {e}", file=sys.stderr)
                    continue

            return items

        except Exception as e:
            print(f"Error fetching RSS from {feed_url}: {e}", file=sys.stderr)
            return []

    def search_in_text(self, text, keywords):
        """جستجو برای کلمات کلیدی در متن"""
        if not text:
            return False

        text_lower = text.lower()

        for keyword in keywords:
            if keyword.lower() in text_lower:
                return True

        return False

    def search_news(self, keywords):
        """جستجو در تمام RSS feeds برای کلمات کلیدی"""
        all_results = []

        # تبدیل کلمات کلیدی به لیست
        if isinstance(keywords, str):
            keyword_list = [kw.strip() for kw in keywords.split()]
        else:
            keyword_list = keywords

        print(f"Searching for keywords: {keyword_list}", file=sys.stderr)

        for feed in self.rss_feeds:
            print(f"Fetching {feed['name']}...", file=sys.stderr)

            items = self.fetch_rss(feed['url'])
            print(f"Found {len(items)} items from {feed['name']}", file=sys.stderr)

            # فیلتر کردن اخبار مرتبط
            for item in items:
                # جستجو در عنوان و توضیحات
                title_match = self.search_in_text(item['title'], keyword_list)
                desc_match = self.search_in_text(item['description'], keyword_list)

                if title_match or desc_match:
                    # پاک‌سازی HTML از توضیحات
                    clean_description = item['description']
                    try:
                        soup = BeautifulSoup(clean_description, 'lxml')
                        clean_description = soup.get_text(strip=True)
                    except:
                        pass

                    # محدود کردن طول توضیحات
                    if len(clean_description) > 300:
                        clean_description = clean_description[:300] + '...'

                    # استخراج دامنه
                    domain = ''
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(item['url']).netloc.replace('www.', '')
                    except:
                        domain = feed['name']

                    result = {
                        'title': item['title'],
                        'url': item['url'],
                        'snippet': clean_description,
                        'domain': domain,
                        'source': feed['name'],
                        'pubDate': item['pubDate'],
                        'timestamp': datetime.now().isoformat(),
                        'matched_in': 'title' if title_match else 'description'
                    }

                    all_results.append(result)

        print(f"Total matching results: {len(all_results)}", file=sys.stderr)

        return all_results

    def search_with_multiple_queries(self, query):
        """جستجو با کلمات کلیدی متعدد"""

        # کلمات کلیدی اصلی
        main_keywords = query.split()

        # کلمات کلیدی جایگزین و مرتبط
        related_keywords = [
            'آب منطقه‌ای',
            'آب منطقه ای',
            'خراسان رضوی',
            'خراسان',
            'آبفا',
            'شرکت آب',
            'منابع آب',
        ]

        all_keywords = list(set(main_keywords + related_keywords))

        results = self.search_news(all_keywords)

        # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
        results.sort(key=lambda x: x.get('pubDate', ''), reverse=True)

        return results

def main():
    query = "آب منطقه‌ای خراسان رضوی"

    # دریافت query از command line
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])

    searcher = RSSNewsSearcher()
    results = searcher.search_with_multiple_queries(query)

    # حذف نتایج تکراری بر اساس URL
    seen_urls = set()
    unique_results = []
    for result in results:
        if result['url'] not in seen_urls:
            seen_urls.add(result['url'])
            unique_results.append(result)

    # خروجی JSON
    output = {
        'success': True,
        'query': query,
        'count': len(unique_results),
        'results': unique_results,
        'timestamp': datetime.now().isoformat()
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
