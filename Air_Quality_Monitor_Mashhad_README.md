# راهنمای Workflow کیفیت هوا مشهد (Payesh)

این workflow به صورت خودکار هر ساعت داده‌های کیفیت هوای شهر مشهد را از API سامانه پایش شهری دریافت کرده و خلاصه‌ای از وضعیت را به کانال تلگرام ارسال می‌کند.

## 🏗️ معماری Workflow

```
Cron Trigger (هر ساعت)
    │
    ├──> Get Dashboard (Payesh) [HTTP Request]
              │
              ├──> Build Telegram Message [Function]
                        │
                        ├──> Deduplicate / Send Control [Function]
                                  │
                                  ├──> Should Send? [IF]
                                           │
                                           └──> Send to Telegram
```

## 📦 پیش‌نیازها

### 1. متغیرهای محیطی

فقط یک متغیر محیطی نیاز است:

```bash
TELEGRAM_CHAT_ID=@your_channel_or_chat_id
```

### 2. Telegram Bot Credentials

در n8n:
1. به Settings → Credentials بروید
2. یک credential جدید از نوع "Telegram API" ایجاد کنید
3. Access Token ربات تلگرام خود را وارد کنید (از @BotFather دریافت می‌شود)

## 🚀 نصب و راه‌اندازی

### گام 1: Import کردن Workflow

1. فایل `Air_Quality_Monitor_Mashhad.json` را در n8n import کنید
2. به قسمت Workflows → Import from File بروید
3. فایل را انتخاب کنید

### گام 2: تنظیم Telegram Credentials

1. روی node "Send to Telegram" کلیک کنید
2. Telegram Bot credential خود را انتخاب کنید

### گام 3: تنظیم Chat ID

**روش 1: استفاده از Environment Variable**

در n8n:
```
TELEGRAM_CHAT_ID=@your_channel
```

**روش 2: Hardcode در workflow** (اگر می‌خواهید)

شناسه کانال/چت خود را مستقیماً در node "Send to Telegram" وارد کنید.

### گام 4: فعال‌سازی

1. دکمه "Active" را روشن کنید
2. Workflow هر ساعت اجرا می‌شود

### گام 5: تست

روی node "Every Hour" کلیک راست کرده و "Execute Node" را انتخاب کنید.

## 🔧 توضیح Node‌ها

### 1. Every Hour (Cron Trigger)
- **نوع**: Schedule Trigger
- **تنظیمات**: اجرای خودکار هر ساعت
- **خروجی**: یک trigger برای شروع workflow

### 2. Get Dashboard (Payesh)
- **URL**: `https://payesh.mashhad.ir/api/Dashboard/Citizen`
- **Method**: GET
- **Authentication**: None (API عمومی است)
- **Headers**:
  - `Accept: application/json`
  - `User-Agent: n8n-payesh-fetcher/1.0`
- **خروجی**: داده‌های کامل Dashboard شامل:
  - `aqi`: شاخص کل شهر
  - `stationsAQI`: آرایه ایستگاه‌ها با AQI هر کدام
  - `airQualityMeasurementDateTime`: زمان اندازه‌گیری
  - `past24HourChanges`: تغییرات 24 ساعت گذشته

### 3. Build Telegram Message (Function)

این node:
- داده‌های API را پردازش می‌کند
- اعداد را به فارسی تبدیل می‌کند
- ایستگاه‌ها را بر اساس AQI مرتب می‌کند (بدترین اول)
- پیام Markdown را می‌سازد

**ورودی**:
```json
{
  "data": {
    "aqi": 120,
    "airQualityMeasurementDateTime": "2025-10-30T09:00:00",
    "stationsAQI": [
      {
        "label": "چمن",
        "value": {
          "aqi": 145,
          "influetialParameter": "PM2.5",
          "dateTime": "..."
        }
      }
    ]
  }
}
```

**خروجی**:
```json
{
  "send": true,
  "message": "متن پیام Markdown",
  "meta": {
    "cityAqi": 120,
    "measuredAt": "2025-10-30T09:00:00"
  }
}
```

### 4. Deduplicate / Send Control (Function)

- از Workflow Static Data استفاده می‌کند
- زمان اندازه‌گیری (`measuredAt`) را با آخرین ارسال مقایسه می‌کند
- اگر داده جدید باشد، `send: true` برمی‌گرداند
- از ارسال تکراری همان داده جلوگیری می‌کند

### 5. Should Send? (IF)

- بررسی می‌کند که آیا `send === true`
- اگر true باشد، به Telegram ارسال می‌شود
- اگر false باشد، workflow متوقف می‌شود

### 6. Send to Telegram

- پیام را به کانال/چت ارسال می‌کند
- از فرمت Markdown استفاده می‌کند
- پیش‌نمایش لینک غیرفعال است

## 📱 نمونه خروجی

```
*شاخص کیفیت هوا — خلاصه (مشهد)*
زمان اندازه‌گیری: ۱۴۰۴/۰۷/۳۰ ۰۹:۰۰
شاخص کل شهر: *۱۲۰*

*پنج ایستگاه با بدترین وضعیت:*
1. *چمن* — شاخص: *۱۴۵* — آلاینده: PM2.5
2. *وکیل‌آباد* — شاخص: *۱۳۸* — آلاینده: PM10
3. *کوهسنگی* — شاخص: *۱۲۵*
4. *سجاد* — شاخص: *۱۱۸*
5. *رسالت* — شاخص: *۱۱۰*

شاخص اخیر: ۱۲۲

_پیام خودکار — هر ساعت به‌روزرسانی می‌شود._
```

## 🔍 عیب‌یابی

### خطا: "Could not reach URL"
**راه حل**:
- اتصال اینترنت را بررسی کنید
- ممکن است سایت payesh.mashhad.ir موقتاً در دسترس نباشد
- VPN را امتحان کنید (اگر لازم است)

### خطا: "Cannot read property 'stationsAQI'"
**راه حل**:
- ساختار API تغییر کرده است
- کد Function را بررسی کنید
- خروجی HTTP Request را چک کنید

### پیام ارسال نمی‌شود
**راه حل**:
- Workflow Static Data را پاک کنید
- Node "Deduplicate" را موقتاً حذف کنید
- مستقیماً "Build Telegram Message" را به "Should Send?" وصل کنید

### اعداد فارسی نمایش داده نمی‌شوند
**راه حل**: تابع `toFaDigits` در code را بررسی کنید.

## 🎛️ سفارشی‌سازی

### تغییر تعداد ایستگاه‌های نمایش داده شده

در node "Build Telegram Message":
```javascript
const top5 = mapped.slice(0, 5);  // تغییر 5 به تعداد دلخواه
```

### تغییر فرمت پیام

در همان node، قسمت `let msg = ...` را ویرایش کنید.

### افزودن اطلاعات بیشتر

API اطلاعات زیادی برمی‌گرداند:
- `past24HourChanges`: تغییرات 24 ساعت
- `pollutionSourcePercentage`: درصد منابع آلودگی
- `todayWeather`: اطلاعات آب و هوا

می‌توانید این‌ها را در کد Function اضافه کنید.

### تغییر زمان اجرا

در node "Every Hour":
- هر 30 دقیقه: `Minutes interval = 30`
- هر 2 ساعت: `Hours interval = 2`
- روزانه: `Hours interval = 24`

## 🆚 تفاوت با Workflow AQMS (خراسان رضوی)

| ویژگی | Mashhad Payesh | AQMS Khorasan |
|-------|---------------|---------------|
| منبع داده | payesh.mashhad.ir | aqms.doe.ir |
| پوشش | فقط مشهد | استان خراسان رضوی |
| احراز هویت | بدون نیاز | نیاز به Bearer Token |
| تعداد Request | 1 | 2 (Stations + AQI) |
| ساختار داده | Dashboard API | دو API جداگانه |

## 📊 ذخیره داده‌های تاریخی

برای ذخیره:

1. یک node "Google Sheets" یا "Database" اضافه کنید
2. بعد از "Build Telegram Message" وصل کنید
3. فیلدهای `cityAqi`, `measuredAt` و `top5` را ذخیره کنید

## 📝 یادداشت‌ها

- **API عمومی**: این API بدون نیاز به authentication قابل دسترسی است
- **Rate Limiting**: با اجرای هر ساعت مشکلی ایجاد نمی‌شود
- **Timezone**: زمان به صورت خودکار به فارسی تبدیل می‌شود
- **Duplicate Prevention**: از ارسال مجدد همان داده جلوگیری می‌کند

## 🔐 امنیت

- ✅ API عمومی است و نیاز به توکن ندارد
- ✅ از Environment Variables برای TELEGRAM_CHAT_ID استفاده کنید
- ✅ دسترسی به workflow را محدود کنید

## 🔄 اطلاعات API

**Endpoint**: `https://payesh.mashhad.ir/api/Dashboard/Citizen`

**نمونه Response**:
```json
{
  "data": {
    "aqi": 120,
    "instantAqi": 120,
    "airQualityMeasurementDateTime": "2025-10-30T09:00:00",
    "stationsAQI": [
      {
        "label": "ایستگاه چمن",
        "value": {
          "stationId": 1,
          "aqi": 145,
          "influetialParameter": "PM2.5",
          "dateTime": "2025-10-30T09:00:00"
        }
      }
    ],
    "past24HourChanges": {
      "cityAQI_Changes": [100, 105, 110, ...]
    }
  }
}
```

## 📞 پشتیبانی

اگر مشکلی داشتید:
1. لاگ‌های execution را بررسی کنید
2. خروجی HTTP Request را چک کنید
3. از "Execute Node" برای تست استفاده کنید

---

**نسخه**: 1.0
**تاریخ**: ۱۴۰۴/۰۷/۳۰
**سازنده**: Claude Code
**منبع داده**: [پایش شهری مشهد](https://payesh.mashhad.ir)
