# 🔍 راهنمای جامع Scraping شبکه‌های اجتماعی

## 📊 مقایسه شبکه‌های اجتماعی

| شبکه | API رسمی | Scraping امکان‌پذیر؟ | سختی | توصیه |
|------|---------|---------------------|------|-------|
| **Telegram** | ✅ رایگان و عالی | ✅ خیلی آسان | ⭐ | **API رسمی** |
| **Twitter/X** | 💰 پولی شده | ⚠️ سخت | ⭐⭐⭐⭐ | API یا ابزارهای third-party |
| **Instagram** | 💰 محدود | ⚠️ خیلی سخت | ⭐⭐⭐⭐⭐ | Unofficial APIs |
| **LinkedIn** | 💰 بسیار محدود | ❌ تقریباً غیرممکن | ⭐⭐⭐⭐⭐ | توصیه نمی‌شود |
| **Facebook** | 💰 محدود | ⚠️ سخت | ⭐⭐⭐⭐ | Graph API |
| **YouTube** | ✅ رایگان | ✅ آسان | ⭐⭐ | **API رسمی** |
| **Reddit** | ✅ رایگان | ✅ آسان | ⭐⭐ | **API رسمی** |
| **Pinterest** | 💰 محدود | ⚠️ متوسط | ⭐⭐⭐ | API یا scraping |

---

## 1️⃣ Telegram (بهترین گزینه برای ایران) 🚀

### ✅ مزایا:
- **API رایگان و قدرتمند**
- بدون محدودیت rate limit شدید
- پشتیبانی از Python, Node.js و...
- می‌توانید از کانال‌ها، گروه‌ها و user ها پیام بخوانید

### کتابخانه‌ها:

#### Python - Telethon
```python
pip install telethon
```

```python
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

client = TelegramClient('session', api_id, api_hash)

async def scrape_channel(channel_username):
    await client.start()

    # دریافت پیام‌های کانال
    messages = await client.get_messages(channel_username, limit=100)

    for message in messages:
        if message.text:
            print(f"Date: {message.date}")
            print(f"Text: {message.text}")
            print("-" * 50)

# اجرا
with client:
    client.loop.run_until_complete(scrape_channel('@channel_username'))
```

#### Python - Pyrogram (ساده‌تر)
```python
pip install pyrogram
```

```python
from pyrogram import Client

app = Client("my_account", api_id='API_ID', api_hash='API_HASH')

async def main():
    async with app:
        # دریافت پیام‌های کانال
        async for message in app.get_chat_history("@channel_username", limit=100):
            print(message.text)

app.run(main())
```

### نمونه: نظارت بر کانال‌های خبری آب خراسان

```python
#!/usr/bin/env python3
import asyncio
from telethon import TelegramClient
from datetime import datetime
import json

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# لیست کانال‌های مرتبط
channels = [
    '@abfa_khorasan',
    '@khorasan_news',
    '@mashhad_news',
]

client = TelegramClient('water_monitor', api_id, api_hash)

async def search_in_channels(keywords):
    await client.start()

    results = []

    for channel in channels:
        try:
            async for message in client.iter_messages(channel, limit=50):
                if message.text:
                    # جستجو برای کلمات کلیدی
                    if any(keyword in message.text for keyword in keywords):
                        results.append({
                            'channel': channel,
                            'date': message.date.isoformat(),
                            'text': message.text,
                            'link': f"https://t.me/{channel.replace('@', '')}/{message.id}"
                        })
        except Exception as e:
            print(f"Error in {channel}: {e}")

    return results

keywords = ['آب منطقه‌ای', 'خراسان رضوی', 'قطعی آب']

with client:
    results = client.loop.run_until_complete(search_in_channels(keywords))
    print(json.dumps(results, ensure_ascii=False, indent=2))
```

---

## 2️⃣ Twitter/X (سخت شده)

### مشکلات:
- API رایگان حذف شد
- حساب Developer نیاز به پرداخت ($100+/ماه)
- Rate limiting شدید

### راه‌حل‌ها:

#### گزینه 1: API رسمی (پولی)
```python
pip install tweepy
```

#### گزینه 2: Nitter (Scraping غیررسمی)
Nitter یک frontend آزاد برای Twitter است:

```python
import requests
from bs4 import BeautifulSoup

def scrape_twitter_via_nitter(username):
    url = f"https://nitter.net/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    tweets = []
    for tweet in soup.find_all('div', class_='tweet-content'):
        tweets.append(tweet.get_text(strip=True))

    return tweets
```

#### گزینه 3: snscrape (بهترین برای scraping)
```bash
pip install snscrape
```

```python
import snscrape.modules.twitter as sntwitter

# جستجو در توییتر
query = "آب منطقه‌ای خراسان"
tweets = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 100:  # محدودیت تعداد
        break

    tweets.append({
        'date': tweet.date,
        'text': tweet.rawContent,
        'user': tweet.user.username,
        'url': tweet.url
    })
```

---

## 3️⃣ Instagram (خیلی سخت)

### مشکلات:
- Anti-bot بسیار قوی
- نیاز به login
- Rate limiting شدید
- خطر ban شدن اکانت

### راه‌حل‌ها:

#### Instaloader
```bash
pip install instaloader
```

```python
import instaloader

L = instaloader.Instaloader()

# Login (اختیاری اما توصیه می‌شود)
L.login('your_username', 'your_password')

# دانلود پست‌های یک پروفایل
profile = instaloader.Profile.from_username(L.context, 'target_username')

for post in profile.get_posts():
    if 'آب خراسان' in post.caption:
        print(f"Caption: {post.caption}")
        print(f"Likes: {post.likes}")
        print(f"URL: {post.url}")
```

⚠️ **هشدار**: استفاده زیاد می‌تواند به ban شدن منجر شود!

---

## 4️⃣ YouTube (API عالی دارد)

### YouTube Data API (رایگان)
```bash
pip install google-api-python-client
```

```python
from googleapiclient.discovery import build

api_key = 'YOUR_YOUTUBE_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

# جستجو در YouTube
request = youtube.search().list(
    part='snippet',
    q='آب منطقه‌ای خراسان رضوی',
    type='video',
    maxResults=50
)

response = request.execute()

for item in response['items']:
    print(f"Title: {item['snippet']['title']}")
    print(f"URL: https://youtube.com/watch?v={item['id']['videoId']}")
```

---

## 5️⃣ Reddit (API رایگان)

### PRAW (Python Reddit API Wrapper)
```bash
pip install praw
```

```python
import praw

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='my_scraper'
)

# جستجو در subreddit
for submission in reddit.subreddit('all').search('Khorasan water', limit=100):
    print(f"Title: {submission.title}")
    print(f"URL: {submission.url}")
    print(f"Score: {submission.score}")
```

---

## 6️⃣ LinkedIn (تقریباً غیرممکن)

⛔ **توصیه نمی‌شود:**
- Anti-bot بسیار پیشرفته
- نیاز به login واقعی
- خطر ban دائمی
- نقض Terms of Service

---

## 🎯 بهترین راه‌حل برای "آب منطقه‌ای خراسان رضوی"

### پیشنهاد ترکیبی:

```python
#!/usr/bin/env python3
"""
جمع‌آوری اخبار از چند منبع
"""

import asyncio
from telethon import TelegramClient
import json
from datetime import datetime

class MultiSourceScraper:
    def __init__(self):
        self.results = []

    async def scrape_telegram(self, channels, keywords):
        """اسکرپ کانال‌های تلگرام"""
        api_id = 'YOUR_API_ID'
        api_hash = 'YOUR_API_HASH'

        client = TelegramClient('session', api_id, api_hash)
        await client.start()

        for channel in channels:
            try:
                async for msg in client.iter_messages(channel, limit=100):
                    if msg.text and any(kw in msg.text for kw in keywords):
                        self.results.append({
                            'source': 'Telegram',
                            'channel': channel,
                            'text': msg.text,
                            'date': msg.date.isoformat(),
                            'url': f"https://t.me/{channel.replace('@', '')}/{msg.id}"
                        })
            except:
                pass

        await client.disconnect()

    def scrape_youtube(self, query):
        """جستجو در YouTube"""
        # کد YouTube API
        pass

    def scrape_reddit(self, query):
        """جستجو در Reddit"""
        # کد Reddit API
        pass

    async def run(self):
        keywords = ['آب منطقه‌ای', 'خراسان رضوی']
        telegram_channels = ['@abfa_news', '@khorasan_news']

        # اجرای موازی
        await asyncio.gather(
            self.scrape_telegram(telegram_channels, keywords),
            # سایر منابع...
        )

        return self.results

# اجرا
scraper = MultiSourceScraper()
results = asyncio.run(scraper.run())
print(json.dumps(results, ensure_ascii=False, indent=2))
```

---

## 🔐 ملاحظات قانونی و اخلاقی

### ✅ مجاز:
- استفاده از API های رسمی
- خواندن محتوای عمومی
- رعایت Terms of Service
- رعایت Rate Limits

### ❌ غیرمجاز:
- نقض Terms of Service
- دور زدن محدودیت‌های امنیتی
- جمع‌آوری اطلاعات خصوصی
- استفاده تجاری بدون مجوز

---

## 📦 پکیج‌های توصیه شده

```bash
# Telegram (بهترین برای ایران)
pip install telethon pyrogram

# Twitter
pip install snscrape tweepy

# Instagram (استفاده محتاطانه)
pip install instaloader

# YouTube
pip install google-api-python-client

# Reddit
pip install praw

# ابزارهای عمومی
pip install beautifulsoup4 lxml requests
```

---

## 🎯 نتیجه‌گیری برای پروژه شما

برای "آب منطقه‌ای خراسان رضوی":

1. **اولویت 1: Telegram** ⭐⭐⭐⭐⭐
   - API رایگان و قدرتمند
   - کانال‌های خبری زیاد
   - بدون محدودیت

2. **اولویت 2: ScrapingDog API** ⭐⭐⭐⭐
   - برای سایت‌های خبری
   - همان workflow که ساختیم

3. **اولویت 3: Twitter/X** ⭐⭐⭐
   - اگر API key دارید
   - یا از snscrape

4. **اولویت 4: YouTube** ⭐⭐
   - برای ویدیوهای خبری

---

**آیا می‌خواهید یک workflow ترکیبی بسازم که از Telegram + ScrapingDog استفاده کند؟**
