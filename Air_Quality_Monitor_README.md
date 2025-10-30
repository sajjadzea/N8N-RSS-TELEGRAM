# راهنمای استفاده از Workflow کیفیت هوا

این workflow به صورت خودکار هر ساعت داده‌های کیفیت هوا (AQI) را از سایت سازمان محیط زیست دریافت کرده و خلاصه‌ای از وضعیت را به کانال تلگرام ارسال می‌کند.

## 📋 فهرست مطالب
- [معماری Workflow](#معماری-workflow)
- [پیش‌نیازها](#پیشنیازها)
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [توضیح Node‌ها](#توضیح-nodeها)
- [نمونه خروجی](#نمونه-خروجی)
- [عیب‌یابی](#عیبیابی)

## 🏗️ معماری Workflow

```
Cron Trigger (هر ساعت)
    ├──> Get Stations (HTTP Request)
    │         │
    │         ├──> Merge Stations & AQI (Function)
    │                     │
    └──> Get AQI (HTTP Request)──┘
                                  │
                                  ├──> Duplicate Prevention (Function)
                                           │
                                           ├──> Should Send? (IF)
                                                    │
                                                    └──> Send to Telegram
```

## 📦 پیش‌نیازها

### 1. متغیرهای محیطی (Environment Variables)

در n8n خود باید متغیرهای زیر را تنظیم کنید:

```bash
AQMS_BEARER=your_bearer_token_here
TELEGRAM_CHAT_ID=@your_channel_or_chat_id
```

#### نحوه دریافت AQMS_BEARER:

1. به سایت https://aqms.doe.ir بروید
2. DevTools مرورگر را باز کنید (F12)
3. به تب Network بروید
4. یک درخواست API را انجام دهید
5. در Headers درخواست، مقدار `Authorization: Bearer ...` را کپی کنید

### 2. Telegram Bot Credentials

در n8n:
1. به Settings → Credentials بروید
2. یک credential جدید از نوع "Telegram API" ایجاد کنید
3. Access Token ربات تلگرام خود را وارد کنید (از @BotFather دریافت می‌شود)

## 🚀 نصب و راه‌اندازی

### گام 1: Import کردن Workflow

1. فایل `Air_Quality_Monitor.json` را باز کنید
2. در n8n به قسمت Workflows بروید
3. روی "Import from File" کلیک کنید
4. فایل JSON را انتخاب کنید

### گام 2: تنظیم Credentials

1. روی node "Send to Telegram" کلیک کنید
2. Telegram Bot credential خود را انتخاب کنید

### گام 3: تنظیم Environment Variables

**روش 1: استفاده از فایل .env.example موجود**

1. فایل `.env.example` را کپی کنید و نام آن را به `.env` تغییر دهید
2. توکن Bearer قبلاً در فایل قرار داده شده است
3. فقط مقدار `TELEGRAM_CHAT_ID` را با شناسه کانال/چت خود جایگزین کنید

**روش 2: تنظیم مستقیم در n8n**

در n8n به مسیر زیر بروید:
- Settings → Environments → Add Variable

متغیرهای مورد نیاز:

```env
AQMS_BEARER=PD-jvbkAgKdeLFivtcSyxsJxt3WG94u59PMTNWccp9EXI7yO5Zg6ET8I2p0gACOpDbI6jdFVkl2pVZPwhuxZFWTo5W67YK9liE9sAcJWqzK30TmD-XMYKUUgUiXgA1PrytYyTsuTUF72NmZ7RorFLueMJNGrywYuUhAv0XRbLIcFQH123JCvahFzU29HF9SGVu-fAVx68mVzQlwdcfjSfM6CFaLuWdBg6VK5bWKUV837jv7nTESLate0huP7_HVdQ3F8kwR_0_TNdmocePsfb4KaNLl9zgzfoyoE5aSK6JDGJvVZ3Zb6_jEQ5mdVlQbj
TELEGRAM_CHAT_ID=@your_channel
```

**⚠️ نکته امنیتی**: این توکن برای استفاده شخصی شما است. آن را با دیگران به اشتراک نگذارید.

### گام 4: فعال‌سازی Workflow

1. روی دکمه "Active" در بالای workflow کلیک کنید
2. Workflow هر ساعت به صورت خودکار اجرا خواهد شد

### گام 5: تست دستی

برای تست، روی node "Every Hour" کلیک راست کرده و "Execute Node" را انتخاب کنید.

## 🔧 توضیح Node‌ها

### 1. Every Hour (Cron Trigger)
- **نوع**: Schedule Trigger
- **تنظیمات**: هر ساعت، در دقیقه 0
- **خروجی**: یک trigger برای شروع workflow

### 2. Get Stations (HTTP Request)
- **URL**: `https://aqms.doe.ir/Service/api/v2/Station/GetStationsByStateId/?StateId=8`
- **Method**: GET
- **Headers**:
  - `Accept: application/json`
  - `Authorization: Bearer {{$env.AQMS_BEARER}}`
- **خروجی**: لیست ایستگاه‌های سنجش کیفیت هوا در خراسان رضوی

### 3. Get AQI (HTTP Request)
- **URL**: `https://aqms.doe.ir/Service/api/v2/AQI/Get/?StateId=8`
- **Method**: GET
- **Headers**: همانند Get Stations
- **خروجی**: داده‌های AQI فعلی برای هر ایستگاه

### 4. Merge Stations & AQI (Function)
این node:
- داده‌های دو API را با هم ترکیب می‌کند
- اعداد فارسی را به انگلیسی تبدیل می‌کند (normalize)
- ایستگاه‌ها را بر اساس AQI مرتب می‌کند
- پیام نهایی را با فرمت Markdown می‌سازد

**خروجی**:
```json
{
  "merged": [...],  // آرایه کامل ایستگاه‌ها
  "summary": {
    "updated_at": "2025-10-30T12:00:00.000Z",
    "total_stations": 24,
    "top5": [...]
  },
  "message": "متن پیام Markdown"
}
```

### 5. Duplicate Prevention (Function)
- از Workflow Static Data استفاده می‌کند
- زمان آخرین ارسال را ذخیره می‌کند
- اگر داده جدید باشد، `send: true` برمی‌گرداند
- از ارسال تکراری جلوگیری می‌کند

### 6. Should Send? (IF)
- بررسی می‌کند که آیا `send === true`
- اگر true باشد، به node تلگرام می‌رود
- اگر false باشد، workflow متوقف می‌شود

### 7. Send to Telegram
- پیام را به کانال/چت مشخص شده ارسال می‌کند
- از فرمت Markdown استفاده می‌کند
- پیش‌نمایش لینک غیرفعال است

## 📱 نمونه خروجی

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

## 🔍 عیب‌یابی

### خطا: "Bearer token is invalid"
**راه حل**: توکن منقضی شده است. یک توکن جدید از DevTools دریافت کنید.

### خطا: "Could not reach URL"
**راه حل**:
- اتصال اینترنت را بررسی کنید
- VPN یا پروکسی را فعال کنید (اگر لازم است)

### خطا: "Chat not found"
**راه حل**:
- TELEGRAM_CHAT_ID را بررسی کنید
- مطمئن شوید ربات به کانال اضافه شده است
- اگر از عدد استفاده می‌کنید، علامت `-` را فراموش نکنید (مثلاً `-1001234567890`)

### پیام ارسال نمی‌شود
**راه حل**:
- Workflow Static Data را پاک کنید (Settings → Reset Static Data)
- Node "Duplicate Prevention" را موقتاً حذف کنید
- مستقیماً از "Merge Stations & AQI" به "Should Send?" وصل کنید

### اعداد فارسی به درستی نمایش داده نمی‌شوند
**راه حل**: تابع `persianNumber` در node "Merge Stations & AQI" اعداد انگلیسی را به فارسی تبدیل می‌کند. کد را بررسی کنید.

## 🎛️ سفارشی‌سازی

### تغییر تعداد ایستگاه‌های نمایش داده شده
در node "Merge Stations & AQI":
```javascript
const top5 = sorted.slice(0, 5);  // تغییر 5 به تعداد دلخواه
```

### تغییر فرمت پیام
در همان node، قسمت `let message = ...` را ویرایش کنید.

### تغییر زمان اجرا
در node "Every Hour":
- برای اجرا هر 30 دقیقه: Minutes interval = 30
- برای اجرا روزانه: Hours interval = 24

### افزودن فیلتر آستانه
برای ارسال فقط زمانی که AQI بالاتر از 150 است:
```javascript
// در node "Merge Stations & AQI"
const hasHighAQI = top5.some(s => s.aqi_now > 150);
return [{ json: { merged, summary, message, shouldAlert: hasHighAQI } }];
```

سپس در node "Should Send?" شرط را تغییر دهید:
```
$json.send === true AND $json.shouldAlert === true
```

## 📊 ذخیره داده‌های تاریخی

اگر می‌خواهید داده‌ها را ذخیره کنید:

1. یک node "Google Sheets" یا "Database" اضافه کنید
2. بعد از "Merge Stations & AQI" وصل کنید
3. فیلد `merged` را در آن ذخیره کنید

## 📝 یادداشت‌ها

- **StateId=8**: خراسان رضوی. برای استان‌های دیگر این پارامتر را تغییر دهید
- **Rate Limiting**: با اجرای هر ساعت، مشکلی با rate limit نخواهید داشت
- **توکن**: به طور معمول توکن‌های Bearer بعد از چند ساعت منقضی می‌شوند
- **Timezone**: زمان نمایشی با locale سرور شما مطابقت دارد

## 🔐 امنیت

- ⚠️ توکن‌ها را هرگز در کد هاردکد نکنید
- ✅ از Environment Variables استفاده کنید
- ✅ دسترسی به workflow را محدود کنید
- ✅ توکن را به صورت دوره‌ای تغییر دهید

## 📞 پشتیبانی

اگر مشکلی داشتید:
1. لاگ‌های execution را بررسی کنید (کلیک روی هر node و مشاهده Output)
2. Console logs را در node‌های Function بررسی کنید
3. از قابلیت "Execute Node" برای تست تک‌تک node‌ها استفاده کنید

---

**نسخه**: 1.0
**تاریخ**: ۱۴۰۴/۰۷/۳۰
**سازنده**: Claude Code
