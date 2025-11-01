# 🚀 Workflow استخراج چالش‌های نوآوری NAN - خراسان رضوی

این workflow برای استخراج خودکار چالش‌های نوآوری مربوط به استان خراسان رضوی از سایت [nan.ac](https://nan.ac/challenges) طراحی شده است.

## 🎯 قابلیت‌ها

- ✅ استخراج خودکار چالش‌ها از سایت NAN
- ✅ فیلتر کردن چالش‌های خراسان رضوی
- ✅ تشخیص هوشمند تغییرات (چالش‌های جدید و به‌روزرسانی‌ها)
- ✅ ارسال خودکار به تلگرام
- ✅ اجرای دوره‌ای هر 12 ساعت

## ⚙️ نحوه راه‌اندازی

### مرحله 1️⃣: بررسی ساختار سایت

قبل از استفاده، **حتماً** باید ساختار سایت رو بررسی کنی و کد پارسر رو تنظیم کنی:

#### روش بررسی:

1. **باز کردن Developer Tools:**
   - سایت [https://nan.ac/challenges](https://nan.ac/challenges) رو باز کن
   - کلید `F12` رو بزن (یا کلیک راست → Inspect)

2. **بررسی Network Requests:**
   - به تب **Network** برو
   - صفحه رو Refresh کن (`Ctrl+R`)
   - دنبال درخواست‌های API بگرد:
     - چیزی شبیه `/api/challenges`
     - یا `challenges.json`
     - یا `data.json`

3. **اگر API پیدا کردی:**
   ```
   ✅ بهترین حالت!
   - URL رو یادداشت کن
   - Response رو ببین (JSON یا HTML؟)
   - ساختار داده‌ها رو بررسی کن
   ```

4. **اگر API نبود، بررسی HTML:**
   - به تب **Elements** برو
   - دنبال کارت‌ها یا لیست چالش‌ها بگرد
   - ببین چالش‌های خراسان رضوی چه `class` یا `id` دارن
   - ساختار HTML رو یادداشت کن

#### مثال ساختار‌های ممکن:

**حالت 1: داده در JSON داخل صفحه**
```html
<script>
  var challenges = [
    {
      "title": "چالش نمونه",
      "province": "خراسان رضوی",
      "deadline": "1403/09/01"
    }
  ];
</script>
```

**حالت 2: کارت‌های HTML**
```html
<div class="challenge-card" data-province="خراسان رضوی">
  <h3>عنوان چالش</h3>
  <p>توضیحات...</p>
  <span class="deadline">1403/09/01</span>
</div>
```

**حالت 3: API جداگانه**
```
GET https://nan.ac/api/challenges
Response: [{"id": 1, "title": "...", "province": "..."}]
```

### مرحله 2️⃣: تنظیم Workflow

بعد از بررسی ساختار:

1. **Import کردن Workflow:**
   - فایل `NAN_Challenges_Scraper_Khorasan.json` رو باز کن
   - محتوا رو کپی کن
   - در n8n: Workflows → Import

2. **تنظیم HTTP Request Node:**

   **اگر سایت API داره:**
   - Node "Fetch NAN Challenges Page" رو باز کن
   - URL رو به آدرس API تغییر بده
   - `responseFormat` رو روی `json` بذار (اگه JSON برمی‌گردونه)

   **اگه API نداره:**
   - همون URL فعلی رو نگه دار
   - ولی ممکنه نیاز باشه Headers بیشتری اضافه کنی

3. **تنظیم Parser Code:**

   Node "Parse & Filter Khorasan Challenges" رو باز کن و کد رو با ساختار واقعی سایت تنظیم کن:

   **نمونه برای JSON API:**
   ```javascript
   const data = $input.item.json;
   const allChallenges = data.challenges || data.data || [];

   const challenges = allChallenges
     .filter(c => {
       const province = c.province || c.استان || '';
       return province.includes('خراسان رضوی') ||
              province.includes('مشهد');
     })
     .map(c => ({
       title: c.title || c.عنوان || '',
       description: c.description || c.توضیحات || '',
       province: c.province || 'خراسان رضوی',
       deadline: c.deadline || c.مهلت || '',
       link: c.link || `https://nan.ac/challenges/${c.id}`,
       organization: c.organization || c.سازمان || ''
     }));

   return [{ json: { success: true, challenges, count: challenges.length }}];
   ```

   **نمونه برای HTML Parsing:**
   ```javascript
   const html = $input.item.json;
   const htmlContent = typeof html === 'string' ? html : html.data || '';

   const challenges = [];

   // مثال: استخراج از div های challenge-card
   const regex = /<div class="challenge-card"[^>]*data-province="خراسان رضوی"[^>]*>(.*?)<\\/div>/gis;
   const matches = htmlContent.match(regex) || [];

   matches.forEach(card => {
     const titleMatch = card.match(/<h3[^>]*>(.*?)<\\/h3>/i);
     const descMatch = card.match(/<p class="description">(.*?)<\\/p>/i);

     if (titleMatch) {
       challenges.push({
         title: titleMatch[1].replace(/<[^>]+>/g, '').trim(),
         description: descMatch ? descMatch[1].replace(/<[^>]+>/g, '').trim() : '',
         province: 'خراسان رضوی',
         // ... بقیه فیلدها
       });
     }
   });

   return [{ json: { success: true, challenges, count: challenges.length }}];
   ```

4. **تنظیم Telegram:**
   - Node "Send to Telegram" رو باز کن
   - Chat ID کانال رو وارد کن (با `-` در ابتدا)
   - Credential تلگرام رو انتخاب کن

### مرحله 3️⃣: تست و Debug

1. **اجرای دستی:**
   - روی node "Every 12 Hours" کلیک راست کن
   - "Execute Node" رو بزن

2. **بررسی خروجی Parser:**
   - روی node "Parse & Filter Khorasan Challenges" کلیک کن
   - خروجی رو ببین:
     - اگه `challenges` خالی بود → کد پارسر اشتباهه
     - اگه `rawHtmlLength` بزرگ بود → HTML دریافت شده، باید parse بشه
     - اگه داده داشت → عالیه! ✅

3. **Debug کردن:**

   **اگه داده استخراج نشد:**
   - در Code node این رو اضافه کن برای دیدن محتوا:
   ```javascript
   // در ابتدای کد اضافه کن
   console.log('HTML Length:', htmlContent.length);
   console.log('First 500 chars:', htmlContent.substring(0, 500));
   ```
   - Execution Log رو چک کن

   **اگه 403 گرفتی:**
   - Headers بیشتر اضافه کن
   - یا از روش API استفاده کن

### مرحله 4️⃣: فعال‌سازی

- روی "Active" کلیک کن
- هر 12 ساعت به طور خودکار اجرا می‌شه

## 🎨 فرمت پیام‌ها

### پیام خلاصه:
```
🔔 چالش‌های نوآوری — خراسان رضوی

🆕 چالش‌های جدید: ۳
🔄 چالش‌های به‌روزرسانی شده: ۱

📅 زمان بررسی: ۱۴۰۳/۰۸/۱۰
```

### پیام چالش جدید:
```
🆕 چالش نوآوری جدید

📌 عنوان:
[عنوان چالش]

🏢 سازمان:
[نام سازمان]

🏷 دسته‌بندی:
[دسته]

📝 توضیحات:
[شرح چالش]

⏰ مهلت:
[تاریخ]

📍 استان: خراسان رضوی

🔗 مشاهده جزئیات
```

## 🔧 سفارشی‌سازی

### تغییر استان

برای استخراج چالش‌های استان دیگر:

1. در node "Parse & Filter Khorasan Challenges":
   ```javascript
   // خط زیر رو پیدا کن:
   if (province.includes('خراسان رضوی') || ...)

   // تغییر بده به:
   if (province.includes('تهران') || ...)
   ```

2. در node "Format Telegram Messages":
   ```javascript
   // خط زیر رو پیدا کن:
   msg += `*📍 استان:* خراسان رضوی\\n\\n`;

   // تغییر بده به استان مورد نظر
   ```

3. نام workflow رو عوض کن

### افزودن فیلترهای بیشتر

می‌تونی بر اساس دسته‌بندی یا سازمان هم فیلتر کنی:

```javascript
const challenges = allChallenges
  .filter(c => {
    const province = c.province || '';
    const category = c.category || '';

    return (province.includes('خراسان رضوی')) &&
           (category.includes('فناوری اطلاعات'));
  });
```

## ⚠️ نکات مهم

1. **ساختار سایت ممکنه تغییر کنه**
   - هر از گاهی workflow رو چک کن
   - اگه داده نیومد، ساختار سایت رو دوباره بررسی کن

2. **محدودیت Rate Limiting**
   - اگه درخواست‌های زیاد زدی و ban شدی، فاصله زمانی رو زیاد کن
   - از 12 ساعت به 24 ساعت تغییر بده

3. **داده‌های ذخیره شده**
   - برای reset: workflow رو غیرفعال و دوباره فعال کن

## 🐛 عیب‌یابی

### داده استخراج نمی‌شه
1. ✅ Developer Tools رو باز کن و ساختار سایت رو ببین
2. ✅ کد parser رو با ساختار واقعی تطبیق بده
3. ✅ اگه سایت از JavaScript استفاده می‌کنه، ممکنه نیاز به Puppeteer باشه

### خطای 403
1. ✅ Headers بیشتری اضافه کن
2. ✅ از API استفاده کن (اگه داره)
3. ✅ User-Agent رو تغییر بده

### هیچ چالشی برای خراسان رضوی نیست
1. ✅ مطمئن شو سایت واقعاً چالش داره
2. ✅ فیلتر province رو چک کن
3. ✅ ببین سایت چه نامی برای استان استفاده می‌کنه

## 📚 منابع

- [مستندات n8n](https://docs.n8n.io)
- [HTML Parsing با Regex](https://regex101.com)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 🤝 کمک

اگه مشکلی داشتی:
1. Execution log رو چک کن
2. خروجی هر node رو ببین
3. ساختار واقعی سایت رو با کد مقایسه کن

---

**نکته مهم:** این workflow یه template کلی هست. **حتماً** باید کد parser رو با ساختار واقعی سایت تنظیم کنی! 🔧
