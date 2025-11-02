# 🔍 راهنمای سریع Web Scraping و Social Media

این پوشه شامل ابزارها و اسکریپت‌های مختلف برای جمع‌آوری اطلاعات از منابع مختلف است.

---

## 📁 فایل‌ها

### 🎯 Workflows آماده (توصیه می‌شود)

1. **`Water_Authority_Khorasan_Search.json`** ⭐ بهترین گزینه
   - Workflow n8n آماده استفاده
   - استفاده از ScrapingDog API
   - تشخیص خودکار اخبار جدید
   - ارسال به تلگرام
   - [راهنمای راه‌اندازی](SETUP_WATER_AUTHORITY.md)

### 🐍 اسکریپت‌های Python

2. **`telegram_scraper.py`** ⭐ برای کانال‌های تلگرام
   - نظارت بر کانال‌های تلگرام
   - جستجوی کلمات کلیدی
   - نیاز به Telegram API

3. **`scrape_water_news_rss.py`**
   - خواندن RSS feeds سایت‌های خبری
   - در محیط‌های محدود شده کار نمی‌کند

4. **`scrape_water_news.py`**
   - Scraping مستقیم از Google/DuckDuckGo
   - در محیط‌های محدود شده کار نمی‌کند

### 📚 مستندات

5. **`SOCIAL_MEDIA_SCRAPING_GUIDE.md`** 📖
   - راهنمای جامع scraping شبکه‌های اجتماعی
   - کتابخانه‌ها و ابزارها
   - نمونه کدها
   - ملاحظات قانونی

6. **`SETUP_WATER_AUTHORITY.md`**
   - راهنمای راه‌اندازی workflow اصلی
   - تنظیمات Telegram Bot
   - عیب‌یابی

---

## 🚀 شروع سریع

### گزینه 1: استفاده از n8n Workflow (ساده‌ترین)

```bash
# 1. فایل را در n8n import کنید
Water_Authority_Khorasan_Search.json

# 2. Telegram Bot را تنظیم کنید
# (طبق راهنمای SETUP_WATER_AUTHORITY.md)

# 3. Workflow را Active کنید
```

### گزینه 2: استفاده از Telegram Scraper

```bash
# 1. نصب پکیج‌ها
pip install -r requirements.txt

# 2. دریافت API credentials از my.telegram.org
# 3. تنظیم environment variables
export TELEGRAM_API_ID='your_api_id'
export TELEGRAM_API_HASH='your_api_hash'

# 4. اجرا
python3 telegram_scraper.py
```

خروجی:
```json
{
  "success": true,
  "total_results": 15,
  "results": [
    {
      "channel": "@khorasannews",
      "text": "قطعی آب در مناطق شرقی مشهد...",
      "date": "2025-11-02T10:30:00",
      "link": "https://t.me/khorasannews/12345"
    }
  ]
}
```

---

## 📊 مقایسه روش‌ها

| روش | مزایا | معایب | توصیه |
|-----|-------|-------|-------|
| **n8n + ScrapingDog** | ✅ آماده<br>✅ بدون محدودیت<br>✅ یکپارچه | ❌ نیاز به API key | ⭐⭐⭐⭐⭐ |
| **Telegram API** | ✅ رایگان<br>✅ قدرتمند<br>✅ کانال‌های زیاد | ❌ نیاز به setup | ⭐⭐⭐⭐⭐ |
| **RSS Scraping** | ✅ ساده | ❌ محدود<br>❌ 403 errors | ⭐⭐ |
| **Direct Scraping** | ✅ کنترل کامل | ❌ Anti-bot<br>❌ پیچیده | ⭐ |

---

## 🎯 پیشنهاد برای "آب منطقه‌ای خراسان رضوی"

### استراتژی ترکیبی:

```
1. n8n Workflow (ScrapingDog API)
   └─> سایت‌های خبری عمومی

2. Telegram Scraper
   └─> کانال‌های خبری مرتبط

3. ترکیب نتایج
   └─> ارسال به Telegram Bot شخصی
```

---

## 📦 نصب وابستگی‌ها

### همه پکیج‌ها:
```bash
pip install -r requirements.txt
```

### فقط برای Telegram:
```bash
pip install telethon
# یا
pip install pyrogram
```

### فقط برای Web Scraping:
```bash
pip install requests beautifulsoup4 lxml
```

---

## 🔐 دریافت API Credentials

### Telegram:
1. برو به https://my.telegram.org
2. وارد شو با شماره تلگرام
3. API Development Tools
4. Create New Application
5. کپی کن: `api_id` و `api_hash`

### ScrapingDog:
1. ثبت‌نام در https://scrapingdog.com
2. Free plan را انتخاب کن
3. API key را از Dashboard کپی کن

### YouTube:
1. برو به https://console.cloud.google.com
2. پروژه جدید بساز
3. YouTube Data API v3 را فعال کن
4. Credentials ایجاد کن

---

## 🛠️ نمونه کد ترکیبی

```python
#!/usr/bin/env python3
"""
جمع‌آوری اخبار از Telegram + Web
"""

import asyncio
import requests
from telethon import TelegramClient

async def main():
    # 1. Telegram
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start()

    telegram_news = []
    async for msg in client.iter_messages('@khorasannews', limit=50):
        if 'آب' in msg.text:
            telegram_news.append({
                'source': 'Telegram',
                'text': msg.text,
                'date': msg.date
            })

    # 2. ScrapingDog API
    response = requests.get(
        'https://api.scrapingdog.com/search',
        params={
            'api_key': 'YOUR_KEY',
            'query': 'آب خراسان'
        }
    )
    web_news = response.json().get('results', [])

    # 3. ترکیب
    all_news = telegram_news + web_news
    print(f"Total: {len(all_news)} news items")

asyncio.run(main())
```

---

## ⚠️ ملاحظات مهم

### قانونی:
- ✅ استفاده از API های رسمی
- ✅ خواندن محتوای عمومی
- ❌ نقض Terms of Service
- ❌ جمع‌آوری اطلاعات خصوصی

### فنی:
- رعایت Rate Limits
- استفاده از User-Agent مناسب
- مدیریت خطاها
- Cache کردن نتایج

### امنیتی:
- API keys را در environment variables ذخیره کنید
- از `.gitignore` برای session files استفاده کنید
- رمزهای عبور را هرگز در کد ننویسید

---

## 📞 منابع و کمک

- [Telethon Documentation](https://docs.telethon.dev)
- [ScrapingDog API Docs](https://docs.scrapingdog.com)
- [n8n Documentation](https://docs.n8n.io)
- [راهنمای جامع](SOCIAL_MEDIA_SCRAPING_GUIDE.md)

---

**نسخه:** 1.0
**تاریخ:** نوامبر 2025
