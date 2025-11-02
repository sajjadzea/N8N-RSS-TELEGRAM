#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت نظارت بر کانال‌های تلگرام برای اخبار آب منطقه‌ای خراسان رضوی
نیاز به API ID و API Hash از my.telegram.org
"""

import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel
from telethon.errors import ChannelPrivateError, UsernameInvalidError
import json
from datetime import datetime, timedelta
import sys
import os

class TelegramNewsMonitor:
    def __init__(self, api_id, api_hash, session_name='water_monitor'):
        """
        مقداردهی اولیه

        برای دریافت API ID و API Hash:
        1. به https://my.telegram.org وارد شوید
        2. API Development Tools را انتخاب کنید
        3. یک اپلیکیشن جدید ایجاد کنید
        4. API ID و API Hash را کپی کنید
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(session_name, api_id, api_hash)

        # کانال‌های خبری مرتبط با آب و خراسان
        self.channels = [
            '@khabareabkhorasan',  # کانال اخبار آب خراسان (مثال)
            '@abfakhorasan',       # آبفای خراسان (مثال)
            '@khorasannews',       # اخبار خراسان
            '@mashhadnews',        # اخبار مشهد
            '@irnanewskhorasan',   # ایرنا خراسان
            '@isnanewskhorasan',   # ایسنا خراسان
        ]

        # کلمات کلیدی برای جستجو
        self.keywords = [
            'آب منطقه‌ای',
            'آب منطقه ای',
            'شرکت آب',
            'آبفا',
            'منابع آب',
            'خراسان رضوی',
            'قطعی آب',
            'کمبود آب',
            'تیرماه آب',
            'فشار آب',
        ]

    async def start(self):
        """اتصال به تلگرام"""
        await self.client.start()
        print("✅ Connected to Telegram", file=sys.stderr)

    async def get_channel_info(self, channel):
        """دریافت اطلاعات کانال"""
        try:
            entity = await self.client.get_entity(channel)
            if isinstance(entity, Channel):
                return {
                    'id': entity.id,
                    'title': entity.title,
                    'username': entity.username,
                    'participants': entity.participants_count if hasattr(entity, 'participants_count') else None
                }
        except (ChannelPrivateError, UsernameInvalidError, ValueError) as e:
            print(f"⚠️ Cannot access {channel}: {e}", file=sys.stderr)
            return None

    async def search_messages(self, channel, limit=100, hours_back=24):
        """
        جستجو در پیام‌های یک کانال

        Args:
            channel: نام کاربری کانال (مثلاً @channelname)
            limit: حداکثر تعداد پیام برای بررسی
            hours_back: تعداد ساعت گذشته برای بررسی
        """
        results = []

        try:
            # محاسبه زمان شروع
            since_date = datetime.now() - timedelta(hours=hours_back)

            print(f"🔍 Searching {channel}...", file=sys.stderr)

            message_count = 0
            async for message in self.client.iter_messages(channel, limit=limit):
                message_count += 1

                # بررسی تاریخ
                if message.date < since_date:
                    break

                # بررسی وجود متن
                if not message.text:
                    continue

                # جستجو برای کلمات کلیدی
                text_lower = message.text.lower()
                matched_keywords = [kw for kw in self.keywords if kw.lower() in text_lower]

                if matched_keywords:
                    # استخراج لینک پیام
                    if hasattr(message.peer_id, 'channel_id'):
                        username = channel.replace('@', '')
                        msg_link = f"https://t.me/{username}/{message.id}"
                    else:
                        msg_link = None

                    results.append({
                        'channel': channel,
                        'message_id': message.id,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'link': msg_link,
                        'views': message.views if hasattr(message, 'views') else None,
                        'matched_keywords': matched_keywords
                    })

            print(f"   Found {len(results)} matching messages from {message_count} total", file=sys.stderr)

        except (ChannelPrivateError, UsernameInvalidError) as e:
            print(f"   ❌ Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}", file=sys.stderr)

        return results

    async def monitor_all_channels(self, limit=100, hours_back=24):
        """نظارت بر تمام کانال‌ها"""
        all_results = []

        for channel in self.channels:
            results = await self.search_messages(channel, limit, hours_back)
            all_results.extend(results)

        # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
        all_results.sort(key=lambda x: x['date'], reverse=True)

        return all_results

    async def monitor_with_custom_channels(self, channels, limit=100, hours_back=24):
        """نظارت با لیست کانال‌های سفارشی"""
        all_results = []

        for channel in channels:
            if not channel.startswith('@'):
                channel = '@' + channel

            results = await self.search_messages(channel, limit, hours_back)
            all_results.extend(results)

        all_results.sort(key=lambda x: x['date'], reverse=True)
        return all_results

    async def close(self):
        """بستن اتصال"""
        await self.client.disconnect()


async def main():
    """تابع اصلی"""

    # دریافت API credentials از environment variables یا آرگومان‌ها
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')

    if not api_id or not api_hash:
        print("❌ Error: TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables required", file=sys.stderr)
        print("", file=sys.stderr)
        print("How to get API credentials:", file=sys.stderr)
        print("1. Go to https://my.telegram.org", file=sys.stderr)
        print("2. Log in with your phone number", file=sys.stderr)
        print("3. Go to 'API Development Tools'", file=sys.stderr)
        print("4. Create a new application", file=sys.stderr)
        print("5. Copy your api_id and api_hash", file=sys.stderr)
        print("", file=sys.stderr)
        print("Usage:", file=sys.stderr)
        print("  export TELEGRAM_API_ID='your_api_id'", file=sys.stderr)
        print("  export TELEGRAM_API_HASH='your_api_hash'", file=sys.stderr)
        print("  python3 telegram_scraper.py", file=sys.stderr)
        sys.exit(1)

    # ایجاد monitor
    monitor = TelegramNewsMonitor(api_id, api_hash)

    try:
        # اتصال
        await monitor.start()

        # نظارت بر کانال‌ها (آخرین 24 ساعت)
        print("🔍 Monitoring channels for the last 24 hours...", file=sys.stderr)
        results = await monitor.monitor_all_channels(limit=50, hours_back=24)

        # خروجی JSON
        output = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'total_results': len(results),
            'channels_monitored': monitor.channels,
            'keywords': monitor.keywords,
            'results': results
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        output = {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    finally:
        await monitor.close()


if __name__ == '__main__':
    # اجرای async main
    asyncio.run(main())
