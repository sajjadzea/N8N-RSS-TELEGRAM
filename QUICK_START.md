# راهنمای سریع - Air Quality Monitor

این راهنما را برای راه‌اندازی سریع Workflow در n8n دنبال کنید.

## ✅ چک‌لیست راه‌اندازی (5 دقیقه)

### مرحله 1: Import کردن Workflow
1. در n8n روی **Workflows** کلیک کنید
2. روی **Import from File** کلیک کنید
3. فایل `Air_Quality_Monitor.json` را انتخاب کنید
4. روی **Import** کلیک کنید

### مرحله 2: تنظیم Telegram Bot
1. در Telegram به ربات [@BotFather](https://t.me/BotFather) پیام دهید
2. دستور `/newbot` را ارسال کنید (اگر قبلاً ربات ندارید)
3. یا از ربات موجود خود استفاده کنید
4. Access Token را کپی کنید (مثال: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### مرحله 3: اضافه کردن Credentials در n8n
1. در n8n به **Settings → Credentials** بروید
2. روی **New** کلیک کنید
3. نوع: **Telegram API** را انتخاب کنید
4. نام: `Telegram Bot` (یا هر نام دلخواه)
5. Access Token را وارد کنید
6. روی **Create** کلیک کنید

### مرحله 4: تنظیم Environment Variables
1. در n8n به **Settings → Variables** (یا Environments) بروید
2. دو متغیر زیر را اضافه کنید:

```
Name: AQMS_BEARER
Value: PD-jvbkAgKdeLFivtcSyxsJxt3WG94u59PMTNWccp9EXI7yO5Zg6ET8I2p0gACOpDbI6jdFVkl2pVZPwhuxZFWTo5W67YK9liE9sAcJWqzK30TmD-XMYKUUgUiXgA1PrytYyTsuTUF72NmZ7RorFLueMJNGrywYuUhAv0XRbLIcFQH123JCvahFzU29HF9SGVu-fAVx68mVzQlwdcfjSfM6CFaLuWdBg6VK5bWKUV837jv7nTESLate0huP7_HVdQ3F8kwR_0_TNdmocePsfb4KaNLl9zgzfoyoE5aSK6JDGJvVZ3Zb6_jEQ5mdVlQbj
```

```
Name: TELEGRAM_CHAT_ID
Value: @your_channel_or_chat_id
```

**نکته**: برای دریافت Chat ID:
- برای کانال: نام کاربری کانال با @ (مثال: `@my_channel`)
- برای چت خصوصی: از ربات [@userinfobot](https://t.me/userinfobot) استفاده کنید

### مرحله 5: اتصال Telegram Credential به Node
1. در Workflow روی node **"Send to Telegram"** کلیک کنید
2. در قسمت **Credential to connect with** روی آیکون ⚙️ کلیک کنید
3. Credential **"Telegram Bot"** که ساختید را انتخاب کنید

### مرحله 6: تست و فعال‌سازی
1. روی node **"Every Hour"** کلیک راست کنید
2. **Execute Node** را انتخاب کنید
3. اگر خطایی نداشت، workflow اجرا می‌شود
4. پیام را در کانال تلگرام خود چک کنید
5. روی دکمه **Active** در بالای صفحه کلیک کنید تا workflow هر ساعت اجرا شود

---

## 📌 نکات مهم

### شناسه استان‌ها (StateId)
برای تغییر استان، در nodeهای "Get Stations" و "Get AQI" پارامتر `StateId` را تغییر دهید:

- خراسان رضوی: `StateId=8`
- تهران: `StateId=1`
- اصفهان: `StateId=3`
- استان‌های دیگر: از [API documentation](https://aqms.doe.ir) چک کنید

### اگر خطا دریافت کردید:

**خطا: "Bearer token is invalid"**
→ توکن منقضی شده. یک توکن جدید از سایت aqms.doe.ir دریافت کنید.

**خطا: "Chat not found"**
→ ربات به کانال اضافه نشده یا Chat ID اشتباه است.

**خطا: "Could not reach URL"**
→ اتصال اینترنت را چک کنید. ممکن است نیاز به VPN باشد.

**خطا: "Unauthorized"**
→ Telegram Bot Token اشتباه است.

### تغییر زمان اجرا

در node "Every Hour":
- هر 30 دقیقه: `Minutes interval = 30`
- هر 2 ساعت: `Hours interval = 2`
- روزانه در ساعت 8 صبح: `Cron Expression = 0 8 * * *`

---

## 📱 نمونه خروجی

بعد از اجرای موفق، این پیام در تلگرام ارسال می‌شود:

```
*شاخص کیفیت هوا — خلاصه (خراسان رضوی)*
زمان بروزرسانی: ۱۴۰۴/۰۷/۳۰ ۰۹:۰۰
تعداد ایستگاه‌ها: ۲۴

*پنج ایستگاه با بدترین وضعیت (AQI):*
1. *مشهد - رسالت* — شاخص: *۱۸۴* — آلاینده‌ی غالب: PM10
2. *مشهد - سجاد* — شاخص: *۱۶۷* — آلاینده‌ی غالب: PM2.5
3. *مشهد - کوهسنگی* — شاخص: *۱۵۲*
4. *مشهد - وکیل‌آباد* — شاخص: *۱۴۵*
5. *نیشابور* — شاخص: *۱۲۳*

_پیام خودکار — هر ساعت به‌روزرسانی می‌شود._
```

---

## 🔄 به‌روزرسانی توکن

وقتی توکن منقضی شد:

1. به [https://aqms.doe.ir](https://aqms.doe.ir) بروید
2. DevTools (F12) → Network را باز کنید
3. یک درخواست API را مشاهده کنید
4. از Headers مقدار `Authorization: Bearer ...` را کپی کنید
5. در n8n Settings → Variables مقدار `AQMS_BEARER` را به‌روزرسانی کنید

---

## 📖 مستندات کامل

برای جزئیات بیشتر، فایل [Air_Quality_Monitor_README.md](./Air_Quality_Monitor_README.md) را مطالعه کنید.

---

**✨ موفق باشید!**
