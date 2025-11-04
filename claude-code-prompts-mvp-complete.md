# 📋 لیست کامل پرامپت‌های Claude Code برای MVP
# سیستم پیش‌بینی هوشمند مصرف

**نسخه:** 1.0
**تاریخ:** 2025-11-04
**مدت زمان:** 21 روز کاری (3 هفته)

---

## 📖 راهنمای استفاده

### چگونه از این فایل استفاده کنیم؟

1. **Copy-Paste مستقیم**: هر پرامپت را کپی کنید و به Claude Code بدهید
2. **منتظر بمانید**: بعد از هر پرامپت، صبر کنید تا Claude کار را تمام کند
3. **تست کنید**: طبق چک‌لیست تست، عملکرد را بررسی کنید
4. **OK بدهید**: اگر OK بود بگویید "عالی! ادامه بده" - اگر نه، خطا را copy کنید
5. **بروید به پرامپت بعدی**: مرحله به مرحله پیش بروید

### نکات مهم:
```
⚠️ هرگز بیش از یک پرامپت همزمان ندهید
⚠️ حتماً هر مرحله را تست کنید
⚠️ اگر خطا گرفتید، متن خطا را به Claude نشان دهید
✅ کدها را در Git commit کنید
✅ پرامپت‌ها را به ترتیب اجرا کنید
```

---

## 🚀 پرامپت اولیه (قبل از شروع)

### پرامپت 0: آماده‌سازی محیط

```
سلام Claude! می‌خواهم یک MVP برای "سیستم پیش‌بینی هوشمند مصرف" بسازم.

قبل از شروع، لطفاً چک کن که آیا این ابزارها نصب هستند:
1. Python 3.10+
2. Node.js 18+
3. Git

دستورات چک را به من بده تا اجرا کنم و نتیجه را بهت نشان دهم.
```

**چک‌لیست:**
```bash
# شما این دستورات را اجرا کنید
python --version    # باید Python 3.10+ باشد
node --version      # باید Node 18+ باشد
npm --version       # باید نصب باشد
git --version       # باید نصب باشد
```

---

# 🔵 هفته اول: Backend Development

## Day 1: ساختار پروژه و Setup

### پرامپت 1.1: ایجاد ساختار پروژه

```
بیایید شروع کنیم! Day 1 را آغاز می‌کنیم.

لطفاً این کارها را انجام بده:

1. ساختار کامل فولدرها برای پروژه MVP را بساز:
   - فولدر backend (Python/FastAPI)
   - فولدر frontend (React)
   - فولدر sample-data

2. ساختار دقیق باید مطابق این باشد:

consumption-predictor-mvp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── ml/
│   │   ├── core/
│   │   └── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── (فعلاً خالی)
├── sample-data/
├── docker-compose.yml
├── .gitignore
└── README.md

لطفاً:
- تمام فولدرها و فایل‌های __init__.py را بساز
- .gitignore مناسب Python و Node.js
- README.md اولیه با توضیح پروژه

بعد از ساخت، لیست فایل‌های ساخته‌شده را نشانم بده.
```

**چک‌لیست:**
```bash
# بعد از اینکه Claude فایل‌ها را ساخت، این را چک کنید:
ls -la
cd backend && ls -la app/
tree backend  # اگر tree نصب است

# باید ساختار فولدرها درست باشد
```

---

### پرامپت 1.2: Requirements.txt اولیه

```
خوب! حالا برای backend، فایل requirements.txt را بساز.

شامل این پکیج‌ها:

**Core:**
- fastapi
- uvicorn[standard]
- python-dotenv
- pydantic
- python-multipart

**Database:**
- sqlalchemy
- alembic

**ML & Data:**
- prophet
- pandas
- numpy
- scikit-learn

**Utils:**
- python-jose[cryptography]  # برای JWT
- passlib[bcrypt]  # برای password hashing
- python-dateutil

**Reports:**
- reportlab
- openpyxl

**Testing:**
- pytest
- httpx

لطفاً نسخه‌های مناسب را مشخص کن (compatible versions).
```

**چک‌لیست:**
```bash
# تست نصب
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا: venv\Scripts\activate  # Windows

pip install -r requirements.txt

# باید همه بدون خطا نصب شوند
```

---

### پرامپت 1.3: Config و Environment Variables

```
حالا فایل‌های config را بساز:

1. backend/app/config.py:
   - کلاس Settings با pydantic
   - خواندن از environment variables
   - تنظیمات database
   - تنظیمات JWT (secret key, algorithm, expire)
   - تنظیمات CORS

2. backend/.env.example:
   - نمونه environment variables
   - DATABASE_URL
   - SECRET_KEY
   - ALGORITHM
   - ACCESS_TOKEN_EXPIRE_MINUTES

لطفاً کد clean و documented بنویس.
```

**چک‌لیست:**
```bash
# کپی کردن .env
cp backend/.env.example backend/.env

# ویرایش .env و پر کردن مقادیر
nano backend/.env  # یا هر editor دیگری
```

---

### پرامپت 1.4: Main.py و FastAPI Setup

```
خیلی خوب! حالا فایل main.py را بساز:

1. ایجاد FastAPI app
2. تنظیم CORS (allow all origins برای development)
3. Health check endpoint: GET /health
4. Root endpoint: GET /
5. شامل metadata (title, description, version)

کد باید اجرا شود و Swagger UI در /docs قابل دسترس باشد.

بعد از ساخت، دستور اجرا را بهم بده.
```

**چک‌لیست:**
```bash
# اجرای backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# باز کنید: http://localhost:8000
# باز کنید: http://localhost:8000/docs  ← باید Swagger UI را ببینید
# تست کنید: GET /health ← باید {"status": "healthy"} برگرداند
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 1: Initial project setup and FastAPI basic structure"
```

---

## Day 2: Database Models

### پرامپت 2.1: Database Setup

```
Day 2 را شروع می‌کنیم!

لطفاً فایل backend/app/database.py را بساز:

1. SQLAlchemy engine setup
2. SessionLocal
3. Base برای models
4. Dependency: get_db() برای FastAPI

از SQLite استفاده کن برای development:
- DATABASE_URL = "sqlite:///./consumption.db"

کد باید شامل:
- Connection pooling
- Error handling
- توضیحات کامل
```

**چک‌لیست:**
```python
# می‌توانید این کد را تست کنید:
from app.database import engine, Base

# باید بدون خطا import شود
print("Database setup OK!")
```

---

### پرامپت 2.2: Models - User

```
حالا اولین model را بسازیم.

در backend/app/models/user.py:

کلاس User با این فیلدها:
- id (Integer, primary key)
- email (String, unique, index)
- username (String, unique, nullable=True)
- hashed_password (String)
- full_name (String, nullable=True)
- is_active (Boolean, default=True)
- is_superuser (Boolean, default=False)
- created_at (DateTime, default=now)
- updated_at (DateTime, onupdate=now)

از SQLAlchemy ORM استفاده کن.
توضیحات و type hints کامل.
```

---

### پرامپت 2.3: Models - Consumption

```
مدل اصلی ما: Consumption

در backend/app/models/consumption.py:

کلاس Consumption:
- id (Integer, primary key)
- user_id (Integer, ForeignKey to User, nullable=True)
- timestamp (DateTime, index=True)
- value (Float) - مقدار مصرف
- unit (String, default="kWh") - واحد (kWh, m3, GB, ...)
- location (String, nullable=True) - مکان یا شناسه دستگاه
- category (String, nullable=True) - دسته‌بندی (electricity, water, gas)
- notes (Text, nullable=True)
- created_at (DateTime)

شامل:
- Relationship به User
- Index روی timestamp و user_id
- repr method برای debugging
```

---

### پرامپت 2.4: Models - Alert

```
مدل هشدارها: Alert

در backend/app/models/alert.py:

کلاس Alert:
- id (Integer, primary key)
- user_id (Integer, ForeignKey, nullable=True)
- alert_type (String) - "threshold", "spike", "trend", "forecast"
- severity (String) - "low", "medium", "high", "critical"
- message (Text)
- details (JSON, nullable=True) - اطلاعات اضافی
- is_read (Boolean, default=False)
- is_resolved (Boolean, default=False)
- triggered_at (DateTime, index=True)
- resolved_at (DateTime, nullable=True)

شامل relationship به User.
```

---

### پرامپت 2.5: Models - __init__.py و Create Tables

```
حالا:

1. backend/app/models/__init__.py را بساز و همه models را import کن

2. اسکریپت کوچکی بساز: backend/create_tables.py که:
   - تمام جداول را بسازد
   - یک user پیش‌فرض بسازد (admin/admin)

3. دستورات اجرا را بهم بده

کد باید idempotent باشد (چند بار اجرا شود مشکلی نباشد).
```

**چک‌لیست:**
```bash
# ساخت جداول
cd backend
python create_tables.py

# باید فایل consumption.db ساخته شود
ls -la consumption.db

# چک جدول‌ها
sqlite3 consumption.db ".tables"
# باید: users, consumptions, alerts
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 2: Database models (User, Consumption, Alert)"
```

---

## Day 3: Pydantic Schemas

### پرامپت 3.1: Schemas - Consumption

```
Day 3: Pydantic Schemas

در backend/app/schemas/consumption.py:

ایجاد این schema ها:

1. ConsumptionBase (BaseModel):
   - timestamp: datetime
   - value: float
   - unit: str = "kWh"
   - location: Optional[str]
   - category: Optional[str]
   - notes: Optional[str]

2. ConsumptionCreate (ConsumptionBase):
   - برای ساخت consumption جدید
   - validators برای value (باید مثبت باشد)

3. ConsumptionUpdate (BaseModel):
   - همه فیلدها Optional
   - برای update

4. ConsumptionResponse (ConsumptionBase):
   - id: int
   - created_at: datetime
   - Config: orm_mode = True

شامل validators و examples برای Swagger.
```

---

### پرامپت 3.2: Schemas - Alert

```
در backend/app/schemas/alert.py:

کلاس‌های Schema:

1. AlertBase:
   - alert_type, severity, message, details

2. AlertCreate (AlertBase):
   - برای ساخت alert

3. AlertResponse (AlertBase):
   - id, triggered_at, is_read, is_resolved
   - orm_mode

4. AlertUpdate:
   - is_read, is_resolved (optional)

validators برای alert_type و severity (enum validation).
```

---

### پرامپت 3.3: Schemas - Prediction

```
در backend/app/schemas/prediction.py:

برای API پیش‌بینی:

1. PredictionRequest:
   - days_ahead: int (default=7, min=1, max=30)
   - include_confidence: bool = True
   - category: Optional[str]

2. PredictionPoint:
   - timestamp: datetime
   - predicted_value: float
   - lower_bound: Optional[float]
   - upper_bound: Optional[float]

3. PredictionResponse:
   - predictions: List[PredictionPoint]
   - model_used: str
   - accuracy_metrics: dict
   - generated_at: datetime

4. __init__.py که همه را import کند
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 3: Pydantic schemas for API validation"
```

---

## Day 4-5: API Endpoints

### پرامپت 4.1: API Router Setup

```
Day 4: شروع API Endpoints

در backend/app/api/__init__.py:

ایجاد APIRouter اصلی که شامل:
- prefix="/api/v1"
- tags

و زیر-روترها:
- consumption
- prediction
- alert

در main.py، این router را include کن.
```

---

### پرامپت 4.2: Consumption API - Create

```
در backend/app/api/consumption.py:

ایجاد این endpoints:

1. POST /api/v1/consumption
   - دریافت ConsumptionCreate
   - ذخیره در دیتابیس
   - برگرداندن ConsumptionResponse
   - status_code=201

شامل:
- Dependency injection برای db
- Error handling (try/except)
- مستندات Swagger کامل
```

**چک‌لیست:**
```bash
# تست با curl یا Swagger
curl -X POST http://localhost:8000/api/v1/consumption \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-11-04T10:00:00",
    "value": 125.5,
    "unit": "kWh",
    "category": "electricity"
  }'

# باید 201 و داده ذخیره شده برگردد
```

---

### پرامپت 4.3: Consumption API - Read

```
ادامه consumption.py:

2. GET /api/v1/consumption
   - Query params: skip, limit, category, start_date, end_date
   - برگرداندن List[ConsumptionResponse]
   - Pagination
   - فیلتر بر اساس تاریخ و category

3. GET /api/v1/consumption/{id}
   - دریافت یک consumption با id
   - HTTPException 404 اگر نبود

4. DELETE /api/v1/consumption/{id}
   - حذف consumption
   - 204 No Content
```

**چک‌لیست:**
```bash
# تست GET
curl http://localhost:8000/api/v1/consumption

# باید لیست داده‌ها برگردد

# تست فیلتر
curl "http://localhost:8000/api/v1/consumption?category=electricity&limit=10"
```

---

### پرامپت 4.4: File Upload - CSV

```
در consumption.py:

5. POST /api/v1/consumption/upload
   - دریافت CSV file
   - خواندن و parse کردن CSV
   - ذخیره bulk در دیتابیس
   - برگرداندن تعداد رکوردهای ثبت‌شده

فرمت CSV مورد انتظار:
```csv
timestamp,value,unit,category
2025-11-01T10:00:00,120.5,kWh,electricity
2025-11-01T11:00:00,115.2,kWh,electricity
```

شامل:
- Validation هر row
- Error handling برای فرمت نادرست
- نمایش خطاهای هر سطر
```

**چک‌لیست:**
```bash
# ساخت sample CSV
cat > sample.csv << EOF
timestamp,value,unit,category
2025-11-04T10:00:00,120.5,kWh,electricity
2025-11-04T11:00:00,115.2,kWh,electricity
2025-11-04T12:00:00,130.8,kWh,electricity
EOF

# آپلود
curl -X POST http://localhost:8000/api/v1/consumption/upload \
  -F "file=@sample.csv"

# باید تعداد رکوردها برگردد
```

---

### پرامپت 4.5: Statistics API

```
endpoint جدید در consumption.py:

6. GET /api/v1/consumption/stats
   - Query: start_date, end_date, category
   - محاسبه آمار:
     * total: مجموع مصرف
     * average: میانگین
     * min: حداقل
     * max: حداکثر
     * count: تعداد رکوردها
   - برگرداندن JSON

مفید برای نمایش KPI cards در frontend.
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 4-5: Consumption API endpoints (CRUD + Upload + Stats)"
```

---

## Day 6-7: ML Engine - Prediction

### پرامپت 6.1: Feature Engineering

```
Day 6: Machine Learning شروع می‌شود!

در backend/app/ml/features.py:

تابع prepare_features(df: pd.DataFrame) -> pd.DataFrame:

از داده‌های consumption، این ویژگی‌ها را بساز:

1. Time features:
   - hour
   - day_of_week
   - day_of_month
   - month
   - is_weekend

2. Lag features:
   - lag_1h (مصرف 1 ساعت قبل)
   - lag_1d (1 روز قبل)
   - lag_7d (1 هفته قبل)

3. Rolling features:
   - rolling_mean_24h
   - rolling_std_24h
   - rolling_mean_7d

کد باید robust باشد:
- handle کردن missing values
- handle کردن insufficient data

شامل docstring و type hints.
```

---

### پرامپت 6.2: Prophet Predictor - Part 1

```
در backend/app/ml/predictor.py:

کلاس ConsumptionPredictor:

متد __init__:
- ذخیره model (Prophet)
- تنظیمات (daily_seasonality, weekly_seasonality)

متد prepare_data(consumptions: List) -> pd.DataFrame:
- تبدیل consumption objects به DataFrame
- ستون‌های ds (timestamp) و y (value)
- مرتب‌سازی بر اساس زمان
- حذف duplicates

کد clean با error handling.
```

---

### پرامپت 6.3: Prophet Predictor - Part 2

```
ادامه ConsumptionPredictor:

متد train(df: pd.DataFrame):
- ساخت Prophet model
- تنظیم seasonality
- fit کردن مدل
- ذخیره مدل در self.model

متد predict(days_ahead: int = 7) -> pd.DataFrame:
- ساخت future dataframe
- پیش‌بینی با model
- برگرداندن df شامل:
  * ds (timestamp)
  * yhat (predicted)
  * yhat_lower (lower bound)
  * yhat_upper (upper bound)

handle کردن حالتی که model train نشده باشد.
```

---

### پرامپت 6.4: Prophet Predictor - Evaluation

```
ادامه ConsumptionPredictor:

متد evaluate(y_true: np.array, y_pred: np.array) -> dict:

محاسبه این متریک‌ها:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score

برگرداندن dict با همه metrics.

از scikit-learn استفاده کن.
```

---

### پرامپت 6.5: Prediction API

```
در backend/app/api/prediction.py:

POST /api/v1/predict
- دریافت PredictionRequest
- خواندن داده‌های consumption از دیتابیس
- چک حداقل داده (باید 14 روز داشته باشیم)
- ساخت ConsumptionPredictor
- train کردن
- پیش‌بینی
- برگرداندن PredictionResponse

شامل:
- Error handling (insufficient data)
- محاسبه accuracy metrics
- نمایش model info

در main.py این router را include کن.
```

**چک‌لیست:**
```bash
# اول داده بگذارید (از CSV upload)
# سپس پیش‌بینی بگیرید:

curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "days_ahead": 7,
    "include_confidence": true
  }'

# باید پیش‌بینی 7 روز آینده برگردد
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 6-7: ML Engine with Prophet - Feature Engineering & Prediction API"
```

---

✅ **Milestone 1 Complete: Backend کار می‌کند!** 🎉

---

# 🟢 هفته دوم: Frontend Development

## Day 8: React Setup

### پرامپت 8.1: Create React App

```
Day 8: شروع Frontend!

لطفاً:

1. در فولدر frontend، یک React app بساز:
   - استفاده از Vite (سریع‌تر از Create React App)
   - دستور: npm create vite@latest . -- --template react

2. بعد از ساخت:
   - npm install
   - اضافه کردن این dependencies:
     * @mui/material @emotion/react @emotion/styled
     * @mui/x-charts
     * recharts
     * axios
     * react-router-dom
     * @reduxjs/toolkit react-redux
     * date-fns-jalali

3. package.json نهایی را بهم نشان بده

دستور نصب را step by step بگو.
```

**چک‌لیست:**
```bash
cd frontend
npm install

# اجرا
npm run dev

# باید در http://localhost:5173 اجرا شود
```

---

### پرامپت 8.2: Project Structure

```
در frontend، این ساختار را بساز:

frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   ├── Charts/
│   │   ├── DataEntry/
│   │   ├── Alerts/
│   │   └── Reports/
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── DataPage.jsx
│   │   ├── PredictionPage.jsx
│   │   └── AlertsPage.jsx
│   ├── services/
│   │   └── api.js
│   ├── store/
│   │   └── store.js
│   ├── theme/
│   │   └── theme.js
│   ├── utils/
│   │   └── helpers.js
│   ├── App.jsx
│   └── main.jsx

همه فولدرها و فایل‌های placeholder را بساز.
```

---

### پرامپت 8.3: Material-UI Theme (RTL)

```
در frontend/src/theme/theme.js:

ایجاد Material-UI theme با:

1. RTL support برای فارسی
2. رنگ‌های اصلی:
   - primary: آبی (#1976d2)
   - secondary: سبز (#4caf50)
   - error: قرمز
   - warning: نارنجی
   - success: سبز

3. Typography با فونت فارسی:
   - Vazir یا IRANSans (از Google Fonts یا local)

4. Custom styles برای components

theme را export کن.
```

---

### پرامپت 8.4: API Service

```
در frontend/src/services/api.js:

ساخت axios instance و توابع API:

1. Setup:
   - baseURL: http://localhost:8000/api/v1
   - headers
   - interceptors (error handling)

2. توابع:
   - getConsumptions(params)
   - createConsumption(data)
   - uploadConsumptionCSV(file)
   - getStats(params)
   - getPrediction(days_ahead)
   - getAlerts()

هر تابع async/await با try/catch.

export کردن همه.
```

---

### پرامپت 8.5: App Layout و Routing

```
1. در App.jsx:
   - React Router setup
   - ThemeProvider با theme
   - RTL direction
   - Layout اصلی (Header, Sidebar, Content)

2. Routes:
   - / → HomePage
   - /data → DataPage
   - /prediction → PredictionPage
   - /alerts → AlertsPage

3. Header component:
   - عنوان برنامه
   - منو ناوبری
   - فارسی

4. Sidebar (optional):
   - لینک‌های صفحات

کد باید اجرا شود و routing کار کند.
```

**چک‌لیست:**
```bash
npm run dev

# باید app اجرا شود
# لینک‌های مختلف را تست کنید
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 8: React setup with Material-UI, routing, and API service"
```

---

## Day 9-10: Data Entry Components

### پرامپت 9.1: Manual Entry Form

```
Day 9: Data Entry Components

در frontend/src/components/DataEntry/ManualEntryForm.jsx:

فرم ورود دستی داده با Material-UI:

فیلدها:
- تاریخ و زمان (DateTimePicker)
- مقدار مصرف (TextField - number)
- واحد (Select: kWh, m³, GB)
- دسته‌بندی (Select: برق, آب, گاز)
- توضیحات (TextField - multiline)

دکمه‌ها:
- ثبت (submit)
- پاک کردن (reset)

شامل:
- Form validation با Formik یا react-hook-form
- نمایش error messages
- نمایش loading state
- نمایش success message بعد از submit
- ارسال به API با axios

UI تمیز و user-friendly.
```

**چک‌لیست:**
```
1. فرم نمایش داده می‌شود ✓
2. validation کار می‌کند ✓
3. submit داده را ارسال می‌کند ✓
4. پیام موفقیت نمایش داده می‌شود ✓
```

---

### پرامپت 9.2: CSV File Upload

```
در frontend/src/components/DataEntry/FileUpload.jsx:

Component آپلود فایل CSV:

1. Drag & drop zone
2. یا دکمه انتخاب فایل
3. نمایش فایل انتخاب‌شده (نام، حجم)
4. دکمه آپلود
5. Progress bar حین آپلود
6. نمایش نتیجه:
   - تعداد رکوردهای موفق
   - خطاها (اگر بود)

استفاده از Material-UI components.

شامل:
- File type validation (.csv فقط)
- File size check (مثلاً حداکثر 5MB)
- Error handling
- API call با FormData

نمونه فایل CSV را نمایش بده.
```

---

### پرامپت 9.3: Data Table

```
در frontend/src/components/DataEntry/DataTable.jsx:

جدول نمایش داده‌های ثبت‌شده:

از Material-UI DataGrid یا Table:
- ستون‌ها: تاریخ، مقدار، واحد، دسته‌بندی
- Pagination
- Sorting
- Search/Filter
- دکمه حذف برای هر ردیف

شامل:
- دریافت داده از API
- Loading state (skeleton)
- Empty state (وقتی داده نیست)
- Refresh button
- تبدیل تاریخ میلادی به شمسی
```

---

### پرامپت 9.4: Data Page Integration

```
در frontend/src/pages/DataPage.jsx:

صفحه کامل ورود داده شامل:

Layout:
- بالا: Tabs یا Buttons (ورود دستی / آپلود فایل)
- وسط: ManualEntryForm یا FileUpload (بر اساس انتخاب)
- پایین: DataTable

ویژگی‌ها:
- Switch بین دو حالت
- بعد از submit موفق، جدول refresh شود
- نمایش آمار سریع (کل رکوردها، آخرین ثبت)

UI responsive و زیبا.
```

**چک‌لیست:**
```
1. می‌توانید داده دستی ثبت کنید ✓
2. می‌توانید CSV آپلود کنید ✓
3. جدول داده‌ها نمایش داده می‌شود ✓
4. می‌توانید داده حذف کنید ✓
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 9-10: Data entry components (manual form, CSV upload, data table)"
```

---

## Day 11-12: Dashboard و Charts

### پرامپت 11.1: KPI Cards

```
Day 11: Dashboard Components

در frontend/src/components/Dashboard/KPICard.jsx:

یک component برای نمایش KPI:

Props:
- title (عنوان، مثلاً "میانگین مصرف")
- value (مقدار)
- unit (واحد)
- icon (optional)
- trend (optional: up/down/stable)
- color (primary/secondary/success/warning)

طراحی:
- Card با Material-UI
- نمایش بزرگ value
- نمایش کوچک trend (با فلش)
- آیکون در گوشه

زیبا و responsive.
```

---

### پرامپت 11.2: Time Series Chart

```
در frontend/src/components/Charts/TimeSeriesChart.jsx:

نمودار خطی با Recharts:

Props:
- data: آرایه {timestamp, actual, predicted}
- showPrediction: boolean

نمایش:
- خط آبی: مصرف واقعی
- خط سبز دش‌دار: پیش‌بینی
- ناحیه سایه: confidence interval
- محور X: تاریخ (فارسی)
- محور Y: مقدار مصرف

شامل:
- Tooltip فارسی
- Legend
- Grid
- Responsive
```

---

### پرامپت 11.3: Comparison Chart

```
در frontend/src/components/Charts/ComparisonChart.jsx:

نمودار میله‌ای مقایسه:

نمایش:
- مقایسه مصرف روزانه
- واقعی vs پیش‌بینی
- Grouped bar chart

استفاده از Recharts BarChart.

Props:
- data: آرایه {date, actual, predicted}

ویژگی‌ها:
- رنگ‌های متفاوت برای actual و predicted
- Tooltip
- Legend
- واحد در محور Y
```

---

### پرامپت 11.4: Stats Summary

```
در frontend/src/components/Dashboard/StatsSummary.jsx:

یک component برای نمایش آمار کلی:

شامل 4 KPI Card:
1. مجموع مصرف (Total)
2. میانگین روزانه (Average)
3. حداکثر (Max)
4. حداقل (Min)

دریافت داده از API endpoint /stats.

Grid layout با Material-UI Grid.
Responsive (4 ستون desktop، 2 ستون tablet، 1 ستون mobile).
```

---

### پرامپت 11.5: Dashboard Page

```
در frontend/src/pages/HomePage.jsx:

صفحه Dashboard کامل:

Layout (از بالا به پایین):
1. StatsSummary (4 KPI cards)
2. دو دکمه:
   - "دریافت پیش‌بینی" → می‌رود به /prediction
   - "ثبت داده جدید" → می‌رود به /data
3. TimeSeriesChart (نمایش داده‌های اخیر)
4. ComparisonChart (مقایسه 7 روز اخیر)

شامل:
- دریافت داده از API
- Loading states
- Error handling
- Refresh button
- فیلتر تاریخ (optional)

UI جذاب و کاربردی.
```

**چک‌لیست:**
```
1. KPI cards نمایش داده می‌شوند ✓
2. نمودارها داده را صحیح نشان می‌دهند ✓
3. نمودارها responsive هستند ✓
4. می‌توانید به صفحات دیگر بروید ✓
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 11-12: Dashboard with KPI cards and interactive charts"
```

---

## Day 13: Prediction Page

### پرامپت 13.1: Prediction Form

```
Day 13: صفحه پیش‌بینی

در frontend/src/components/Prediction/PredictionForm.jsx:

فرم ساده:

فیلدها:
- تعداد روزهای پیش‌بینی (Slider: 7-30 روز)
- نمایش confidence interval (Switch)
- دسته‌بندی (Select - optional)

دکمه:
- "دریافت پیش‌بینی"

بعد از کلیک:
- Loading state
- ارسال درخواست به API
- نمایش نتیجه

Material-UI components.
```

---

### پرامپت 13.2: Prediction Results

```
در frontend/src/components/Prediction/PredictionResults.jsx:

نمایش نتایج پیش‌بینی:

شامل:
1. نمودار TimeSeriesChart با پیش‌بینی
2. جدول داده‌های پیش‌بینی شده:
   - تاریخ
   - مقدار پیش‌بینی
   - حد پایین
   - حد بالا
3. Metrics box:
   - Model used
   - Accuracy (MAPE)
   - Generated at

4. دکمه‌های:
   - Export PDF
   - Export CSV

UI تمیز.
```

---

### پرامپت 13.3: Prediction Page Integration

```
در frontend/src/pages/PredictionPage.jsx:

صفحه کامل پیش‌بینی:

Layout:
- بالا: PredictionForm
- وسط: PredictionResults (اگر پیش‌بینی گرفته شده)
- پایین: راهنما (چگونه از پیش‌بینی استفاده کنیم)

شامل:
- مدیریت state
- Error handling (مثلاً داده کافی نیست)
- نمایش پیام‌های راهنما

Material-UI Paper/Card برای sections.
```

**چک‌لیست:**
```
1. فرم نمایش داده می‌شود ✓
2. می‌توانید پیش‌بینی دریافت کنید ✓
3. نتایج به درستی نمایش داده می‌شود ✓
4. خطاها handle می‌شوند ✓
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 13: Prediction page with form and results visualization"
```

---

## Day 14: Alerts Page

### پرامپت 14.1: Alert List

```
Day 14: صفحه هشدارها

در frontend/src/components/Alerts/AlertList.jsx:

لیست هشدارها:

از Material-UI List/Card:

برای هر alert:
- آیکون (بر اساس severity)
- عنوان (alert_type)
- پیام (message)
- زمان (triggered_at - فارسی)
- وضعیت (خوانده شده / حل شده)
- دکمه‌های:
  * علامت‌گذاری به عنوان خوانده‌شده
  * علامت‌گذاری به عنوان حل‌شده
  * حذف

رنگ‌بندی بر اساس severity:
- critical: قرمز
- high: نارنجی
- medium: زرد
- low: آبی

Pagination و Filter (by severity, by status).
```

---

### پرامپت 14.2: Alert Settings

```
در frontend/src/components/Alerts/AlertSettings.jsx:

تنظیمات هشدار:

فرم ساده:

فیلدها:
- سقف مصرف (threshold) - number
- درصد هشدار (مثلاً 80% از سقف)
- فعال/غیرفعال کردن هشدارها

دکمه ذخیره.

از Material-UI Switch و TextField.

(نکته: این فقط UI است، backend برای این در فاز بعدی)
```

---

### پرامپت 14.3: Alerts Page

```
در frontend/src/pages/AlertsPage.jsx:

صفحه کامل هشدارها:

Layout:
- بالا: آمار (تعداد هشدارهای جدید، حل نشده)
- وسط: AlertSettings (collapsible)
- پایین: AlertList

شامل:
- دریافت alerts از API (فعلاً mock data بده)
- Filter و sort
- Refresh button

UI منظم و کاربردی.
```

**چک‌لیست:**
```
1. لیست alerts نمایش داده می‌شود ✓
2. رنگ‌ها بر اساس severity درست است ✓
3. می‌توانید alert را mark as read کنید ✓
4. تنظیمات قابل ویرایش است ✓
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 14: Alerts page with list and settings"
```

---

✅ **Milestone 2 Complete: Frontend کار می‌کند!** 🎉

---

# 🟡 هفته سوم: Integration & Finalization

## Day 15-16: Alert Engine Backend

### پرامپت 15.1: Alert Logic

```
Day 15: Alert Engine

در backend/app/core/alerts.py:

کلاس AlertEngine:

متد check_threshold(consumption_data, threshold):
- چک می‌کند آیا مصرف > threshold
- اگر بله، Alert می‌سازد

متد check_spike(consumption_data):
- چک می‌کند آیا افزایش ناگهانی داشتیم
- مقایسه با میانگین
- اگر > 1.5x میانگین، Alert

متد check_trend(consumption_data, days=7):
- چک می‌کند روند افزایشی
- linear regression ساده
- اگر slope > threshold، Alert

متد generate_alerts(consumption_data, config):
- اجرای تمام چک‌ها
- ذخیره alerts در دیتابیس
- برگرداندن لیست alerts

استفاده از pandas و numpy.
```

---

### پرامپت 15.2: Alert API

```
در backend/app/api/alert.py:

endpoints:

1. GET /api/v1/alerts
   - Query: is_read, is_resolved, severity
   - برگرداندن لیست alerts
   - Pagination

2. GET /api/v1/alerts/{id}
   - دریافت یک alert

3. PUT /api/v1/alerts/{id}
   - آپدیت alert (mark as read/resolved)

4. DELETE /api/v1/alerts/{id}
   - حذف alert

5. POST /api/v1/alerts/check
   - اجرای دستی alert checks
   - برگرداندن alerts جدید

در main.py include کن.
```

---

### پرامپت 15.3: Scheduled Alert Checking (Simple)

```
برای MVP، یک endpoint ساده:

POST /api/v1/alerts/check-now
- دریافت داده‌های اخیر
- اجرای AlertEngine
- ذخیره alerts
- برگرداندن تعداد alerts جدید

(نکته: در production، این با Celery Beat scheduled می‌شود)

frontend می‌تواند دکمه "چک کردن هشدارها" داشته باشد.
```

---

### پرامپت 15.4: Frontend-Backend Integration

```
در frontend/src/services/api.js:

اضافه کردن توابع alert:

- getAlerts(params)
- updateAlert(id, data)
- deleteAlert(id)
- checkAlerts()

در AlertList.jsx:
- استفاده از API واقعی به جای mock
- دکمه‌ها به API متصل شوند

تست کامل end-to-end:
1. داده بگذارید
2. check alerts بزنید
3. alerts نمایش داده شوند
```

**چک‌لیست:**
```bash
# Backend test
curl -X POST http://localhost:8000/api/v1/alerts/check-now

# باید alerts ساخته شود

# Frontend test
# دکمه "چک کردن هشدارها" را بزنید
# باید alerts در لیست نمایش داده شود
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 15-16: Alert engine backend and frontend integration"
```

---

## Day 17-18: Report Generation

### پرامپت 17.1: PDF Report Generator

```
Day 17: گزارش‌گیری

در backend/app/core/reports.py:

کلاس ReportGenerator:

متد generate_pdf(data: dict, output_path: str):

گزارش PDF شامل:
1. سرصفحه (عنوان، تاریخ)
2. خلاصه آمار (KPIs)
3. جدول داده‌ها
4. نمودارها (با matplotlib یا plotly)
5. توصیه‌ها

استفاده از reportlab.

داده ورودی:
{
  "stats": {...},
  "consumptions": [...],
  "predictions": [...],
  "alerts": [...]
}

کد modular و documented.
```

---

### پرامپت 17.2: Excel Report Generator

```
در همان reports.py:

متد generate_excel(data: dict, output_path: str):

Excel با چند شیت:
1. "خلاصه" - KPIs
2. "داده‌های مصرف" - جدول consumptions
3. "پیش‌بینی" - جدول predictions
4. "هشدارها" - جدول alerts

استفاده از openpyxl یا pandas.to_excel().

شامل:
- فرمت‌دهی (header bold، colors)
- عرض ستون‌ها auto-adjust
- فریز کردن header row
```

---

### پرامپت 17.3: Report API

```
در backend/app/api/report.py:

endpoints:

1. GET /api/v1/reports/pdf
   - Query: start_date, end_date
   - تولید PDF
   - برگرداندن فایل (FileResponse)

2. GET /api/v1/reports/excel
   - Query: start_date, end_date
   - تولید Excel
   - برگرداندن فایل

3. GET /api/v1/reports/data
   - برگرداندن JSON خام برای custom reports

شامل:
- دریافت داده از دیتابیس
- فراخوانی ReportGenerator
- ذخیره موقت فایل
- ارسال به client
- حذف فایل موقت

در main.py include کن.
```

---

### پرامپت 17.4: Report UI Components

```
در frontend:

1. src/components/Reports/ReportViewer.jsx:
   - انتخاب بازه تاریخ
   - انتخاب فرمت (PDF/Excel)
   - دکمه دانلود
   - نمایش preview (optional)

2. src/pages/ReportsPage.jsx:
   - ReportViewer
   - لیست گزارش‌های قبلی (optional)

شامل:
- ارسال درخواست به API
- دانلود فایل
- نمایش loading و success message
```

**چک‌لیست:**
```bash
# تست PDF
curl "http://localhost:8000/api/v1/reports/pdf?start_date=2025-11-01&end_date=2025-11-04" \
  --output report.pdf

# باید فایل PDF دانلود شود و قابل باز شدن باشد

# تست از UI
# بروید به صفحه Reports
# بازه تاریخ انتخاب کنید
# دکمه Download PDF بزنید
# فایل باید دانلود شود
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 17-18: Report generation (PDF and Excel) with API and UI"
```

---

## Day 19: Docker Setup

### پرامپت 19.1: Backend Dockerfile

```
Day 19: Dockerization

در backend/Dockerfile:

Multi-stage build:

Stage 1: builder
- FROM python:3.10-slim
- WORKDIR /app
- COPY requirements.txt
- RUN pip install --no-cache-dir -r requirements.txt

Stage 2: runner
- COPY --from=builder
- COPY app/ app/
- EXPOSE 8000
- CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

شامل:
- .dockerignore (venv, __pycache__, *.pyc, .env)
- استفاده از slim image (کوچک‌تر)
- health check
```

---

### پرامپت 19.2: Frontend Dockerfile

```
در frontend/Dockerfile:

Multi-stage build:

Stage 1: builder
- FROM node:18-alpine as builder
- WORKDIR /app
- COPY package*.json
- RUN npm ci
- COPY . .
- RUN npm run build

Stage 2: nginx
- FROM nginx:alpine
- COPY --from=builder /app/dist /usr/share/nginx/html
- COPY nginx.conf /etc/nginx/conf.d/default.conf
- EXPOSE 80

nginx.conf:
- serve static files
- proxy /api requests به backend
```

---

### پرامپت 19.3: Docker Compose

```
در ریشه پروژه، docker-compose.yml:

services:

1. backend:
   - build: ./backend
   - ports: 8000:8000
   - environment: env_file
   - volumes: ./backend:/app (development)
   - depends_on: db

2. frontend:
   - build: ./frontend
   - ports: 3000:80
   - depends_on: backend

3. db (optional - PostgreSQL):
   - image: postgres:15
   - ports: 5432:5432
   - environment: POSTGRES_PASSWORD, POSTGRES_DB
   - volumes: pgdata

volumes:
- pgdata

networks:
- app-network

development override: docker-compose.dev.yml
```

---

### پرامپت 19.4: Docker Test

```
دستورات setup و test:

1. ساخت images:
   docker-compose build

2. اجرا:
   docker-compose up

3. چک health:
   curl http://localhost:8000/health
   curl http://localhost:3000

4. README-DOCKER.md:
   - توضیح نصب Docker
   - دستورات اجرا
   - troubleshooting

لطفاً این فایل README را بساز.
```

**چک‌لیست:**
```bash
# Build
docker-compose build

# Run
docker-compose up

# باید هر دو سرویس بدون خطا اجرا شوند

# تست
curl http://localhost:8000/health  # backend
curl http://localhost:3000         # frontend

# Stop
docker-compose down
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 19: Docker setup with multi-stage builds and docker-compose"
```

---

## Day 20-21: Testing & Bug Fixing

### پرامپت 20.1: Backend Unit Tests

```
Day 20-21: Testing و رفع باگ

در backend/app/tests/:

1. test_api_consumption.py:
   - تست CRUD endpoints
   - تست upload CSV
   - تست stats endpoint

2. test_ml_predictor.py:
   - تست ConsumptionPredictor
   - تست با داده sample
   - تست accuracy

3. test_alert_engine.py:
   - تست alert logic
   - تست threshold checks

استفاده از pytest و httpx.

pytest.fixtures برای db و test data.

تمام تست‌ها باید pass شوند.
```

**چک‌لیست:**
```bash
cd backend
pytest -v

# تمام تست‌ها باید pass شوند
# Coverage > 70%
```

---

### پرامپت 20.2: Frontend Component Tests (Optional)

```
در frontend/src/__tests__/:

تست‌های ساده برای components:

1. KPICard.test.jsx
2. TimeSeriesChart.test.jsx
3. ManualEntryForm.test.jsx

استفاده از React Testing Library.

(اختیاری برای MVP - اگر وقت کم است skip کنید)
```

---

### پرامپت 20.3: End-to-End Test Plan

```
لطفاً یک چک‌لیست کامل E2E تست بساز:

TEST-PLAN.md شامل:

1. Backend API Tests:
   - [ ] Health check
   - [ ] Create consumption
   - [ ] Get consumptions
   - [ ] Upload CSV
   - [ ] Get stats
   - [ ] Get prediction
   - [ ] Get alerts

2. Frontend Tests:
   - [ ] همه صفحات لود می‌شوند
   - [ ] Forms کار می‌کنند
   - [ ] Charts نمایش داده می‌شوند
   - [ ] Navigation کار می‌کند

3. Integration Tests:
   - [ ] داده ثبت → نمایش در جدول
   - [ ] پیش‌بینی → نمایش در نمودار
   - [ ] Alert ساخت → نمایش در لیست

4. Docker Tests:
   - [ ] Build موفق
   - [ ] Run بدون خطا
   - [ ] Services communicate

با دستورات دقیق برای هر تست.
```

---

### پرامپت 20.4: Bug Fixing Session

```
لطفاً کل سیستم را یک بار review کن:

1. چک کن:
   - همه endpoints کار می‌کنند؟
   - همه error ها handle می‌شوند؟
   - کد documented است؟
   - UI/UX مشکلی ندارد؟

2. رفع مشکلات رایج:
   - CORS errors
   - Date/time timezone issues
   - فارسی/انگلیسی inconsistency
   - Responsive design issues

3. بهینه‌سازی:
   - Loading states همه جا هست؟
   - Error messages واضح هستند؟
   - Code duplication کم شود

لیست مشکلات و راه حل‌ها را به من بده.
```

---

### پرامپت 20.5: Documentation Final

```
لطفاً مستندات نهایی را کامل کن:

1. README.md:
   - توضیح پروژه
   - Features
   - نصب و راه‌اندازی
   - استفاده
   - Screenshots (placeholder)

2. SETUP-GUIDE.md:
   - راهنمای نصب قدم‌به‌قدم
   - پیش‌نیازها
   - نصب dependencies
   - راه‌اندازی database
   - اجرای backend
   - اجرای frontend

3. API-DOCS.md:
   - لیست تمام endpoints
   - Request/Response examples
   - Error codes

4. USER-GUIDE.md:
   - راهنمای کاربری
   - چگونه داده ثبت کنیم
   - چگونه پیش‌بینی بگیریم
   - چگونه هشدارها را مدیریت کنیم

همه فارسی و واضح.
```

✅ **Commit Point:**
```bash
git add .
git commit -m "Day 20-21: Testing, bug fixes, and complete documentation"
```

---

✅ **Milestone 3 Complete: MVP کامل و آماده نمایش!** 🎉🎉🎉

---

# 🔧 پرامپت‌های کمکی (در صورت نیاز)

## پرامپت‌های رفع اشکال

### اگر Backend اجرا نشد:

```
من این خطا را می‌گیرم:
[COPY-PASTE ERROR MESSAGE]

لطفاً:
1. خطا را تحلیل کن
2. علت را توضیح بده
3. راه حل step-by-step بده
4. اگر نیاز به تغییر کد است، کد جدید را نشان بده
```

---

### اگر Frontend build نشد:

```
npm run build یا npm run dev این خطا را می‌دهد:
[COPY-PASTE ERROR]

لطفاً مشکل را پیدا کن و رفع کن.
```

---

### اگر API call کار نمی‌کند:

```
من از frontend تلاش می‌کنم API را صدا بزنم ولی این خطا می‌آید:
[COPY-PASTE ERROR FROM BROWSER CONSOLE]

Backend console می‌گوید:
[COPY-PASTE BACKEND ERROR IF ANY]

لطفاً دیباگ کن.
```

---

### اگر CORS Error:

```
من CORS error می‌گیرم:

"Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy"

لطفاً CORS را در FastAPI درست پیکربندی کن.
```

---

### اگر Database Error:

```
خطای دیتابیس:
[COPY-PASTE ERROR]

لطفاً:
1. چک کن models درست هستند
2. چک کن migrations اجرا شده
3. راه حل بده
```

---

## پرامپت‌های بهینه‌سازی

### بهبود Performance:

```
Backend response time کند است (> 3 seconds).

لطفاً:
1. کد را profile کن
2. bottleneck ها را پیدا کن
3. بهینه‌سازی پیشنهاد بده (caching, indexing, query optimization)
```

---

### بهبود UI/UX:

```
UI خیلی ساده است و حرفه‌ای به نظر نمی‌رسد.

لطفاً:
1. پیشنهاد بهبود UI/UX بده
2. رنگ‌ها و spacing را بهتر کن
3. animation و transition اضافه کن (subtle)
4. loading states را بهتر کن
```

---

### اضافه کردن Validation:

```
می‌خواهم validation بیشتری در forms داشته باشم:

- مقدار مصرف باید > 0 باشد
- تاریخ نباید آینده باشد
- فایل CSV باید فرمت درست داشته باشد

لطفاً validation های لازم را اضافه کن (frontend و backend).
```

---

## پرامپت‌های Feature اضافی (بعد از MVP)

### اضافه کردن Authentication:

```
می‌خواهم login/register اضافه کنم.

لطفاً:
1. Backend: JWT authentication با FastAPI
2. Frontend: login form و protected routes
3. توکن را در localStorage ذخیره کن
4. interceptor برای اضافه کردن token به requests

قدم به قدم پیاده‌سازی کن.
```

---

### اضافه کردن Multiple Models:

```
می‌خواهم علاوه بر Prophet، مدل ARIMA هم داشته باشم.

لطفاً:
1. کلاس ARIMAPredictor بساز
2. در prediction API، امکان انتخاب model بده
3. Ensemble model (میانگین دو مدل)
4. مقایسه accuracy دو مدل

پیاده‌سازی کن.
```

---

### اضافه کردن Email Alerts:

```
می‌خواهم وقتی alert جدید ساخته شد، ایمیل ارسال شود.

لطفاً:
1. از python-dotenv و smtplib استفاده کن
2. تابع send_email_alert() بساز
3. در AlertEngine بعد از ساخت alert، ایمیل بفرست
4. فقط برای severity > medium

کد کامل بده.
```

---

## پرامپت‌های Testing اضافی

### Load Testing:

```
می‌خواهم ببینم backend تا چه تعداد request همزمان را می‌تواند handle کند.

لطفاً:
1. با locust یا ab (Apache Bench) یک load test بساز
2. تست scenarios:
   - 100 concurrent users
   - 1000 requests/sec
3. دستورات اجرا و تحلیل نتایج
```

---

### Security Testing:

```
می‌خواهم امنیت API را بررسی کنم.

لطفاً checklist امنیتی بده:
- SQL injection
- XSS
- CSRF
- Input validation
- Rate limiting
- ...

و راهکارهای پیاده‌سازی.
```

---

# 📝 چک‌لیست نهایی MVP

بعد از اتمام تمام پرامپت‌ها، این چک‌لیست را مرور کنید:

## Backend Checklist:

```
✅ ساختار پروژه ساخته شده
✅ Database models (User, Consumption, Alert)
✅ Pydantic schemas
✅ API endpoints:
   ✅ Consumption CRUD
   ✅ Upload CSV
   ✅ Stats
   ✅ Prediction
   ✅ Alerts
   ✅ Reports
✅ ML engine (Prophet)
✅ Alert engine
✅ Report generator (PDF, Excel)
✅ Tests (pytest)
✅ Docker setup
✅ Documentation
```

## Frontend Checklist:

```
✅ React setup با Material-UI
✅ RTL و فارسی
✅ Routing
✅ API service
✅ Components:
   ✅ KPI Cards
   ✅ TimeSeriesChart
   ✅ ComparisonChart
   ✅ ManualEntryForm
   ✅ FileUpload
   ✅ DataTable
   ✅ AlertList
   ✅ PredictionForm
   ✅ ReportViewer
✅ Pages:
   ✅ HomePage (Dashboard)
   ✅ DataPage
   ✅ PredictionPage
   ✅ AlertsPage
   ✅ ReportsPage
✅ State management
✅ Error handling
✅ Loading states
✅ Docker setup
```

## Integration Checklist:

```
✅ Frontend ↔ Backend connected
✅ داده می‌تواند ثبت شود (manual + CSV)
✅ پیش‌بینی کار می‌کند
✅ نمودارها صحیح نمایش می‌دهند
✅ Alerts generate می‌شوند
✅ گزارش download می‌شود (PDF, Excel)
✅ Docker compose کل سیستم را اجرا می‌کند
✅ مستندات کامل است
```

---

# 🎉 تبریک! MVP کامل شد!

اگر تمام چک‌لیست‌ها تیک خوردند، **MVP شما آماده نمایش است!** 🚀

---

# 📞 اگر به کمک نیاز داشتید:

```
فقط بگویید:
"Claude، در مرحله X گیر کردم. این خطا را می‌گیرم: [ERROR]"

یا:

"Claude، می‌خواهم feature Y را اضافه کنم. راهنمایی کن."

من همیشه کمکتان می‌کنم! 🤝
```

---

**موفق باشید!** 💪

*این فایل شامل تمام پرامپت‌های لازم برای ساخت MVP از صفر تا صد است.*
*فقط copy-paste کنید و مرحله به مرحله پیش بروید.*
*در پایان، یک سیستم کامل خواهید داشت!*

---

**نسخه:** 1.0
**تاریخ:** 2025-11-04
**تهیه‌کننده:** Claude Code
**مدت زمان:** 21 روز کاری (3 هفته)
**زبان:** فارسی
