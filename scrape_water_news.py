#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت جستجو و استخراج اخبار آب منطقه‌ای خراسان رضوی
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from urllib.parse import quote_plus, urljoin
from datetime import datetime
import re

class NewsSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.results = []

    def search_duckduckgo(self, query, max_results=20):
        """جستجو در DuckDuckGo"""
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # استخراج نتایج جستجو
            results = []
            for result in soup.find_all('div', class_='result')[:max_results]:
                try:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')

                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                        # استخراج دامنه
                        domain = ''
                        try:
                            from urllib.parse import urlparse
                            domain = urlparse(url).netloc
                        except:
                            pass

                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'domain': domain,
                            'source': 'DuckDuckGo',
                            'timestamp': datetime.now().isoformat()
                        })
                except Exception as e:
                    print(f"Error parsing result: {e}", file=sys.stderr)
                    continue

            return results

        except Exception as e:
            print(f"DuckDuckGo search error: {e}", file=sys.stderr)
            return []

    def search_google(self, query, max_results=20):
        """جستجو در Google (ساده - ممکن است blocked شود)"""
        try:
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"

            response = requests.get(search_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            results = []
            # Google search results structure
            for g in soup.find_all('div', class_='g')[:max_results]:
                try:
                    # عنوان
                    title_elem = g.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else ''

                    # لینک
                    link_elem = g.find('a')
                    url = link_elem.get('href', '') if link_elem else ''

                    # توضیحات
                    snippet_elem = g.find('div', class_=['VwiC3b', 'yXK7lf'])
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                    if title and url:
                        # استخراج دامنه
                        domain = ''
                        try:
                            from urllib.parse import urlparse
                            domain = urlparse(url).netloc
                        except:
                            pass

                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'domain': domain,
                            'source': 'Google',
                            'timestamp': datetime.now().isoformat()
                        })
                except Exception as e:
                    print(f"Error parsing Google result: {e}", file=sys.stderr)
                    continue

            return results

        except Exception as e:
            print(f"Google search error: {e}", file=sys.stderr)
            return []

    def search_iranian_news_sites(self, query):
        """جستجو در سایت‌های خبری ایرانی"""
        results = []

        # لیست سایت‌های خبری ایرانی
        sites = [
            {'name': 'IRNA', 'url': 'https://www.irna.ir', 'search': '/search?query='},
            {'name': 'ISNA', 'url': 'https://www.isna.ir', 'search': '/search?q='},
            {'name': 'Mehr', 'url': 'https://www.mehrnews.com', 'search': '/search?q='},
            {'name': 'Tasnim', 'url': 'https://www.tasnimnews.com', 'search': '/search?q='},
        ]

        for site in sites:
            try:
                search_url = f"{site['url']}{site['search']}{quote_plus(query)}"
                print(f"Searching {site['name']}...", file=sys.stderr)

                response = requests.get(search_url, headers=self.headers, timeout=20)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'lxml')

                # پیدا کردن لینک‌های خبری (این باید بر اساس ساختار هر سایت تنظیم شود)
                news_items = soup.find_all('a', href=True)

                for item in news_items[:5]:  # فقط 5 نتیجه اول از هر سایت
                    try:
                        url = item.get('href', '')
                        if not url.startswith('http'):
                            url = urljoin(site['url'], url)

                        title = item.get_text(strip=True)

                        # فیلتر کردن نتایج نامرتبط
                        if len(title) > 20 and query.split()[0] in title:
                            results.append({
                                'title': title,
                                'url': url,
                                'snippet': '',
                                'domain': site['url'].replace('https://', '').replace('www.', ''),
                                'source': site['name'],
                                'timestamp': datetime.now().isoformat()
                            })
                    except:
                        continue

            except Exception as e:
                print(f"Error searching {site['name']}: {e}", file=sys.stderr)
                continue

        return results

    def search_all(self, query, max_results=50):
        """جستجو در تمام منابع"""
        all_results = []

        # 1. جستجو در DuckDuckGo (اولویت اول)
        print("Searching DuckDuckGo...", file=sys.stderr)
        ddg_results = self.search_duckduckgo(query, max_results)
        all_results.extend(ddg_results)
        print(f"Found {len(ddg_results)} results from DuckDuckGo", file=sys.stderr)

        # 2. اگر نتایج کم بود، Google را امتحان کن
        if len(all_results) < 10:
            print("Searching Google...", file=sys.stderr)
            google_results = self.search_google(query, max_results)
            all_results.extend(google_results)
            print(f"Found {len(google_results)} results from Google", file=sys.stderr)

        # حذف نتایج تکراری بر اساس URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)

        return unique_results

def main():
    query = "آب منطقه‌ای خراسان رضوی"

    # دریافت query از command line اگر وجود داشت
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])

    searcher = NewsSearcher()
    results = searcher.search_all(query)

    # خروجی JSON
    output = {
        'success': True,
        'query': query,
        'count': len(results),
        'results': results,
        'timestamp': datetime.now().isoformat()
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
