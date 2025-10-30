# N8N-RSS-TELEGRAM

مجموعه‌ای از Workflowهای n8n برای اتوماسیون اخبار و پایش کیفیت هوا با ارسال خودکار به تلگرام.

## 📦 Workflowهای موجود

این repository شامل سه workflow اصلی است:

### 1. 📰 RSS to Telegram
Workflow برای دریافت خودکار اخبار از RSS feedها و ارسال به تلگرام با قابلیت‌های:
- استخراج خودکار تصاویر و متن
- خلاصه‌سازی خبر با هوش مصنوعی (Gemini)
- فرمت‌بندی زیبا با HTML
- پشتیبانی از Binary Data

**فایل**: `My workflow 4(7).json`

---

### 2. 🌫️ Air Quality Monitor - Khorasan Razavi
Workflow برای پایش کیفیت هوای استان خراسان رضوی از API سازمان محیط زیست.

**منبع داده**: [AQMS - سازمان محیط زیست](https://aqms.doe.ir)

**ویژگی‌ها**:
- ✅ دریافت داده از دو API (Stations + AQI)
- ✅ ترکیب و نرمال‌سازی داده‌ها
- ✅ نمایش 5 ایستگاه با بدترین شاخص
- ✅ تبدیل خودکار اعداد به فارسی
- ✅ جلوگیری از ارسال تکراری
- ✅ اجرای خودکار هر ساعت

**فایل‌ها**:
- Workflow: `Air_Quality_Monitor.json`
- راهنما: `Air_Quality_Monitor_README.md`
- شروع سریع: `QUICK_START.md`

**احراز هویت**: نیاز به Bearer Token دارد (قبلاً در workflow embed شده)

**نمونه خروجی**:
```
*شاخص کیفیت هوا — خلاصه (خراسان رضوی)*
زمان بروزرسانی: ۱۴۰۴/۰۷/۳۰ ۰۹:۰۰
تعداد ایستگاه‌ها: ۲۴

*پنج ایستگاه با بدترین وضعیت (AQI):*
1. *مشهد - رسالت* — شاخص: *۱۸۴* — آلاینده‌ی غالب: PM10
...
```

---

### 3. 🏙️ Air Quality Monitor - Mashhad (Payesh)
Workflow برای پایش کیفیت هوای شهر مشهد از API پایش شهری.

**منبع داده**: [پایش شهری مشهد](https://payesh.mashhad.ir)

**ویژگی‌ها**:
- ✅ دریافت داده از یک API واحد (Dashboard)
- ✅ شاخص کل شهر + جزئیات ایستگاه‌ها
- ✅ نمایش 5 ایستگاه با بدترین وضعیت
- ✅ تبدیل خودکار اعداد به فارسی
- ✅ جلوگیری از ارسال تکراری
- ✅ اجرای خودکار هر ساعت

**فایل‌ها**:
- Workflow: `Air_Quality_Monitor_Mashhad.json`
- راهنما: `Air_Quality_Monitor_Mashhad_README.md`

**احراز هویت**: بدون نیاز به توکن (API عمومی)

**نمونه خروجی**:
```
*شاخص کیفیت هوا — خلاصه (مشهد)*
زمان اندازه‌گیری: ۱۴۰۴/۰۷/۳۰ ۰۹:۰۰
شاخص کل شهر: *۱۲۰*

*پنج ایستگاه با بدترین وضعیت:*
1. *چمن* — شاخص: *۱۴۵* — آلاینده: PM2.5
...
```

---

## 🚀 شروع سریع

### پیش‌نیازها

1. **n8n نصب شده** (Self-hosted یا Cloud)
2. **Telegram Bot** (از [@BotFather](https://t.me/BotFather) دریافت کنید)
3. **شناسه کانال/چت تلگرام**

### نصب گام به گام

#### گام 1: Clone کردن Repository

```bash
git clone https://github.com/sajjadzea/N8N-RSS-TELEGRAM.git
cd N8N-RSS-TELEGRAM
```

#### گام 2: Import Workflow در n8n

1. در n8n به **Workflows** بروید
2. روی **Import from File** کلیک کنید
3. یکی از فایل‌های JSON را انتخاب کنید:
   - `Air_Quality_Monitor.json` (برای خراسان رضوی)
   - `Air_Quality_Monitor_Mashhad.json` (برای مشهد)
   - `My workflow 4(7).json` (برای RSS)

#### گام 3: تنظیم Telegram Bot Credentials

1. در n8n به **Settings → Credentials** بروید
2. روی **New** کلیک کنید
3. نوع: **Telegram API**
4. Access Token ربات خود را وارد کنید
5. ذخیره کنید

#### گام 4: تنظیم Environment Variables

در n8n (Settings → Variables):

```bash
# فقط برای Air Quality Workflows
TELEGRAM_CHAT_ID=@your_channel

# اگر از RSS workflow استفاده می‌کنید
TELEGRAM_BOT_TOKEN=your_bot_token
```

**نکته**: برای workflow خراسان رضوی، Bearer Token قبلاً در فایل embed شده و نیازی به تنظیم `AQMS_BEARER` ندارید.

#### گام 5: فعال‌سازی

1. روی workflow مورد نظر کلیک کنید
2. دکمه **Active** را روشن کنید
3. برای تست، روی node اول کلیک راست کرده و **Execute Node** را انتخاب کنید

---

## 📚 مستندات

هر workflow مستندات کامل خود را دارد:

| Workflow | فایل مستندات | راهنمای سریع |
|----------|-------------|--------------|
| Air Quality - Khorasan | `Air_Quality_Monitor_README.md` | `QUICK_START.md` |
| Air Quality - Mashhad | `Air_Quality_Monitor_Mashhad_README.md` | - |
| RSS to Telegram | - | - |

---

## 🔧 تنظیمات پیشرفته

### تغییر زمان اجرا

در هر workflow، node "Every Hour" را ویرایش کنید:

- **هر 30 دقیقه**: `Minutes interval = 30`
- **هر 2 ساعت**: `Hours interval = 2`
- **روزانه در ساعت 8 صبح**: Cron expression = `0 8 * * *`

### Hardcode کردن Chat ID

اگر نمی‌خواهید از Environment Variable استفاده کنید:

1. روی node "Send to Telegram" کلیک کنید
2. در فیلد Chat ID، به جای `={{ $env.TELEGRAM_CHAT_ID }}`
3. مستقیماً شناسه کانال را وارد کنید: `@your_channel` یا `-1001234567890`

### ذخیره داده‌های تاریخی

برای ذخیره سابقه AQI:

1. یک node "Google Sheets" یا "PostgreSQL" اضافه کنید
2. بعد از Function node وصل کنید
3. داده‌های مورد نظر را ذخیره کنید

---

## 🆚 مقایسه Workflowهای کیفیت هوا

| ویژگی | Khorasan (AQMS) | Mashhad (Payesh) |
|-------|-----------------|------------------|
| **پوشش** | استان خراسان رضوی | فقط شهر مشهد |
| **منبع** | aqms.doe.ir | payesh.mashhad.ir |
| **احراز هویت** | Bearer Token (embedded) | بدون نیاز |
| **تعداد Request** | 2 (Stations + AQI) | 1 (Dashboard) |
| **اطلاعات اضافه** | Metadata ایستگاه‌ها | تغییرات 24 ساعت |
| **پیچیدگی** | متوسط | ساده |

**توصیه**:
- اگر فقط مشهد می‌خواهید → از **Payesh** استفاده کنید (ساده‌تر)
- اگر کل استان می‌خواهید → از **AQMS** استفاده کنید

---

## 🔐 امنیت

### نکات امنیتی مهم:

- ✅ **توکن‌ها را در Environment Variables ذخیره کنید**
- ✅ **فایل `.env` را به `.gitignore` اضافه کنید**
- ✅ **در repository عمومی توکن قرار ندهید**
- ✅ **دسترسی به n8n را محدود کنید**
- ⚠️ **توکن‌های Bearer معمولاً منقضی می‌شوند** - راهنمای به‌روزرسانی در مستندات موجود است

---

## 🐛 عیب‌یابی رایج

### خطا: "Bearer token is invalid"
- **علت**: توکن AQMS منقضی شده
- **راه حل**: توکن جدید از [راهنما](./Air_Quality_Monitor_README.md#%D8%A8%D9%87%D8%B1%D9%88%D8%B2%D8%B1%D8%B3%D8%A7%D9%86%DB%8C-%D8%AA%D9%88%DA%A9%D9%86) دریافت کنید

### خطا: "Chat not found"
- **علت**: TELEGRAM_CHAT_ID اشتباه یا ربات به کانال اضافه نشده
- **راه حل**:
  1. ربات را به کانال اضافه کنید
  2. Chat ID را بررسی کنید
  3. برای کانال‌های خصوصی از عدد منفی استفاده کنید

### خطا: "Could not reach URL"
- **علت**: مشکل شبکه یا API در دسترس نیست
- **راه حل**:
  1. اتصال اینترنت را بررسی کنید
  2. VPN را امتحان کنید
  3. بعداً دوباره تلاش کنید

### پیام ارسال نمی‌شود
- **علت**: Duplicate Prevention node
- **راه حل**:
  1. Workflow Static Data را Reset کنید
  2. یا node "Duplicate Prevention" را موقتاً حذف کنید

---

## 🤝 مشارکت

برای گزارش مشکلات یا پیشنهادات:

1. یک Issue در GitHub ایجاد کنید
2. یا یک Pull Request ارسال کنید

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

---

## 🙏 تشکر

- **n8n** - پلتفرم اتوماسیون workflow
- **سازمان محیط زیست** - API کیفیت هوای ملی
- **شهرداری مشهد** - API پایش شهری
- **Telegram** - پلتفرم پیام‌رسانی

---

## 📞 پشتیبانی

اگر سوالی دارید:

1. مستندات مربوطه را مطالعه کنید
2. بخش عیب‌یابی را چک کنید
3. در GitHub Issue ایجاد کنید

---

**آخرین به‌روزرسانی**: ۱۴۰۴/۰۷/۳۰
**نسخه**: 2.0
**نگهدارنده**: [@sajjadzea](https://github.com/sajjadzea)
