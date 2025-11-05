# گزارش امکان‌سنجی فنی، اقتصادی و امنیتی
## پیاده‌سازی مدل تحلیل متن فارسی لوکال با قابلیت RAG

**تاریخ تهیه:** آبان ۱۴۰۴
**مشاور فنی:** سیستم تحلیل هوش مصنوعی
**نسخه:** 1.0

---

## 🎯 خلاصه اجرایی (Executive Summary)

این گزارش امکان‌سنجی جامع برای طراحی و پیاده‌سازی یک سیستم تحلیل متن فارسی مبتنی بر هوش مصنوعی ارائه شده است که می‌تواند به‌صورت آفلاین یا نیمه‌آنلاین عمل کند. سیستم پیشنهادی قابلیت‌های خلاصه‌سازی، طبقه‌بندی و استخراج دانش را با معماری RAG پشتیبانی می‌کند.

**توصیه نهایی:** معماری هیبریدی (Hybrid Local-Cloud) با تمرکز بر اجرای لوکال و استفاده انتخابی از ابر برای Fine-tuning.

---

## 📋 فهرست مطالب

1. [مقدمه](#مقدمه)
2. [تحلیل فنی](#تحلیل-فنی)
3. [تحلیل اقتصادی](#تحلیل-اقتصادی)
4. [تحلیل ریسک‌ها](#تحلیل-ریسک‌ها)
5. [معماری پیشنهادی](#معماری-پیشنهادی)
6. [نتیجه‌گیری و توصیه‌ها](#نتیجه‌گیری-و-توصیه‌ها)

---

## 1️⃣ مقدمه

### 1.1 چالش‌های پردازش زبان فارسی

زبان فارسی با ویژگی‌های خاص خود (راست‌چین، نویسه عربی-فارسی، غنای صرفی و نحوی) نیازمند رویکردهای تخصصی در NLP است. چالش‌های اصلی عبارتند از:

- **کمبود مجموعه داده‌های باکیفیت**: دیتاست‌های عمومی فارسی نسبت به انگلیسی محدودتر هستند
- **مدل‌های pre-trained محدود**: تعداد مدل‌های آموزش‌دیده فارسی کمتر از زبان‌های غربی است
- **محدودیت‌های زیرساختی**: دسترسی محدود به GPU‌های پرقدرت و سرویس‌های ابری در ایران
- **نیازهای امنیتی و حریم خصوصی**: حساسیت داده‌ها در برخی کاربردها (بانکی، دولتی، پزشکی)

### 1.2 اهداف پروژه

1. **خلاصه‌سازی (Summarization)**: تولید خلاصه‌های coherent و meaningful از اسناد طولانی فارسی
2. **طبقه‌بندی (Classification)**: دسته‌بندی خودکار اسناد به categories مختلف (خبری، اداری، فنی و ...)
3. **استخراج دانش (Knowledge Extraction)**: شناسایی entity‌ها، روابط و concepts کلیدی
4. **یکپارچگی با RAG**: قابلیت جستجو و بازیابی اطلاعات با تولید پاسخ

### 1.3 محدودیت‌های عملیاتی

- **دسترسی به اینترنت**: نیاز به عملکرد در محیط‌های آفلاین یا با اینترنت محدود
- **محدودیت منابع**: احتمال عدم دسترسی به GPU‌های سطح بالا (A100, H100)
- **بودجه محدود**: نیاز به بهینه‌سازی هزینه‌ها در شرایط اقتصادی فعلی ایران

---

## 2️⃣ تحلیل فنی

### 2.1 نیازمندی‌های سخت‌افزاری

#### الف) سناریو اجرای لوکال - سطح مبتدی (Entry Level)

**مناسب برای:** Proof of Concept، آزمایش اولیه، مدل‌های کوچک

| مشخصات | حداقل | توصیه شده |
|--------|------|-----------|
| **GPU** | NVIDIA RTX 3060 (12GB VRAM) | RTX 4070 Ti (12GB) یا RTX 3090 (24GB) |
| **RAM** | 16 GB DDR4 | 32 GB DDR4/DDR5 |
| **Storage** | 256 GB SSD | 512 GB NVMe SSD |
| **CPU** | Intel i5-12400 / AMD Ryzen 5 5600 | Intel i7-13700 / AMD Ryzen 7 7700X |

**قابلیت‌ها:**
- اجرای مدل‌های تا 7B پارامتر (مثل `ParsBERT`, `mT5-small`)
- Batch size محدود (2-4)
- سرعت استنتاج: متوسط (2-5 ثانیه برای متن متوسط)

**هزینه تخمینی:**
- GPU: $400-600 (RTX 3060 در بازار ایران)
- سیستم کامل: $800-1,200

---

#### ب) سناریو اجرای لوکال - سطح حرفه‌ای (Professional)

**مناسب برای:** Production deployment، مدل‌های متوسط تا بزرگ

| مشخصات | حداقل | توصیه شده |
|--------|------|-----------|
| **GPU** | NVIDIA RTX 4090 (24GB) | NVIDIA A5000 (24GB) یا دو RTX 4090 |
| **RAM** | 64 GB DDR5 | 128 GB DDR5 |
| **Storage** | 1 TB NVMe SSD | 2 TB NVMe SSD (Gen4) |
| **CPU** | AMD Ryzen 9 7950X | AMD Threadripper PRO |

**قابلیت‌ها:**
- اجرای مدل‌های تا 13B-20B پارامتر
- Fine-tuning مدل‌های کوچک تا متوسط
- پشتیبانی از چند کاربر همزمان (Multi-user serving)
- Batch processing کارآمد

**هزینه تخمینی:**
- GPU: $1,800-2,500 (RTX 4090 در ایران)
- سیستم کامل: $3,500-5,000

---

#### ج) سناریو اجرای لوکال - سطح سازمانی (Enterprise)

**مناسب برای:** سازمان‌ها، شرکت‌ها، نیاز به High Availability

| مشخصات | حداقل | توصیه شده |
|--------|------|-----------|
| **GPU** | 2x NVIDIA A6000 (48GB each) | 4x NVIDIA A100 (40GB/80GB) |
| **RAM** | 256 GB DDR5 ECC | 512 GB DDR5 ECC |
| **Storage** | 4 TB NVMe RAID | 8 TB NVMe RAID + NAS |
| **CPU** | AMD EPYC 7443P | AMD EPYC 9654 |

**قابلیت‌ها:**
- اجرای مدل‌های تا 70B پارامتر (با quantization)
- Fine-tuning مدل‌های بزرگ
- High throughput serving
- Redundancy و High Availability

**هزینه تخمینی:**
- سیستم کامل: $15,000-40,000
- ⚠️ **نکته مهم**: GPU‌های datacenter در ایران با تحریم‌ها و هزینه‌های بالا همراه است

---

### 2.2 معماری‌های پیشنهادی برای RAG

#### 🔷 معماری ۱: RAG ساده لوکال (Simple Local RAG)

```
┌─────────────────────────────────────────────────────┐
│  User Query                                          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Embedding Model (Local)                             │
│  • sentence-transformers/paraphrase-multilingual    │
│  • HooshvareLab/bert-fa-base-uncased-farstail       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Vector Store (Local)                                │
│  • FAISS / Chroma / Qdrant (embedded)               │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Document Retriever                                  │
│  • Top-K similarity search                          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  LLM (Local)                                         │
│  • Ollama + Llama3 fine-tuned for Persian           │
│  • GPT-J Persian / mT5-large                        │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Response Generation                                 │
└─────────────────────────────────────────────────────┘
```

**مزایا:**
- کاملاً آفلاین
- حریم خصوصی کامل
- No vendor lock-in

**معایب:**
- نیاز به GPU قوی
- کیفیت پایین‌تر از مدل‌های ابری بزرگ
- نیاز به maintenance و updates دستی

---

#### 🔷 معماری ۲: RAG هیبریدی (Hybrid RAG)

```
┌─────────────────────────────────────────────────────┐
│  User Query                                          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  Router / Decision Layer                             │
│  • Sensitive data → Local                           │
│  • General data → Cloud (if available)              │
└────┬────────────────────────────────────────────┬───┘
     │                                            │
     │ Local Path                    Cloud Path  │
     ▼                                            ▼
┌──────────────────────┐            ┌──────────────────────┐
│  Local Embedding     │            │  Cloud API           │
│  + Vector Store      │            │  (Ferdowsi Cloud)    │
│  + Local LLM         │            │  + OpenAI API        │
└──────────────────────┘            └──────────────────────┘
     │                                            │
     └────────────┬───────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────┐
│  Response Merger & Validator                         │
└─────────────────────────────────────────────────────┘
```

**مزایا:**
- بهترین trade-off بین کیفیت و امنیت
- انعطاف‌پذیری بالا
- Fallback به لوکال در قطعی اینترنت

**معایب:**
- پیچیدگی معماری بیشتر
- نیاز به logic routing هوشمند

---

### 2.3 مدل‌های پیشنهادی برای زبان فارسی

#### 🏆 بهترین مدل‌های Embedding فارسی

| مدل | پارامترها | VRAM | کیفیت | منبع |
|-----|-----------|------|--------|------|
| **HooshvareLab/bert-fa-base-uncased** | 118M | ~2GB | ⭐⭐⭐⭐ | HuggingFace |
| **sentence-transformers/paraphrase-multilingual** | 278M | ~4GB | ⭐⭐⭐⭐⭐ | HuggingFace |
| **m3hrdadfi/bert-zwnj-wnli-mean-tokens** | 118M | ~2GB | ⭐⭐⭐ | HuggingFace |
| **xlm-roberta-base** (multilingual) | 270M | ~4GB | ⭐⭐⭐⭐ | HuggingFace |

**توصیه:** `sentence-transformers/paraphrase-multilingual` برای کیفیت بالا یا `HooshvareLab/bert-fa-base-uncased` برای کارایی بهتر

---

#### 🏆 بهترین مدل‌های LLM برای تولید متن فارسی

| مدل | پارامترها | VRAM (FP16) | کیفیت فارسی | روش اجرا |
|-----|-----------|-------------|-------------|----------|
| **Llama-3-8B-Instruct** (Fine-tuned Persian) | 8B | ~18GB | ⭐⭐⭐⭐⭐ | Ollama/vLLM |
| **aya-101** (Multilingual by Cohere) | 13B | ~28GB | ⭐⭐⭐⭐ | HuggingFace |
| **mT5-large** (Persian fine-tuned) | 1.2B | ~6GB | ⭐⭐⭐ | HuggingFace |
| **Qwen2.5** (14B) | 14B | ~30GB | ⭐⭐⭐⭐⭐ | Ollama |
| **PersianLlama** (Community model) | 7B | ~16GB | ⭐⭐⭐⭐ | HuggingFace |

**توصیه:**
- **بودجه محدود:** `mT5-large` یا `Llama-3-8B` با quantization (4-bit)
- **کیفیت بالا:** `Qwen2.5-14B` یا `Llama-3-8B` fine-tuned

---

#### 🔧 Quantization برای کاهش نیاز به VRAM

| روش | کاهش VRAM | کاهش کیفیت | ابزار |
|-----|-----------|------------|-------|
| **FP16** | Baseline | 0% | PyTorch |
| **INT8** | ~50% | ~2-3% | bitsandbytes |
| **4-bit (GPTQ)** | ~75% | ~5-7% | AutoGPTQ |
| **4-bit (GGUF)** | ~75% | ~5-7% | llama.cpp/Ollama |

**مثال:** Llama-3-8B با 4-bit quantization تنها ~5GB VRAM نیاز دارد (قابل اجرا روی RTX 3060)

---

### 2.4 ابزارها و فریم‌ورک‌های پیشنهادی

#### 🛠️ Stack پیشنهادی برای پیاده‌سازی

```python
# Core ML Framework
import torch
from transformers import AutoModel, AutoTokenizer, pipeline

# LLM Serving
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Vector Store
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Document Processing
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader

# Monitoring
from prometheus_client import start_http_server, Counter, Histogram
```

#### 📦 مقایسه فریم‌ورک‌های LLM Serving

| فریم‌ورک | مزایا | معایب | مناسب برای |
|----------|-------|-------|-----------|
| **Ollama** | نصب آسان، پشتیبانی از GGUF، مدیریت مدل‌ها | کمتر قابل customize | Development & Small Production |
| **vLLM** | سرعت بالا، PagedAttention، throughput عالی | پیچیدگی بالاتر | Production با traffic بالا |
| **llama.cpp** | سبک، پشتیبانی از CPU، quantization عالی | API محدود | Edge devices & Low-resource |
| **HuggingFace TGI** | یکپارچگی عالی با HF، streaming | نیاز به Docker، resource-heavy | Enterprise |
| **LangChain** | RAG out-of-the-box، orchestration | Overhead بالا | Rapid prototyping |

**توصیه:** ترکیب `Ollama` برای LLM serving + `LangChain` برای RAG orchestration

---

### 2.5 نیازمندی‌های شبکه و اینترنت

#### سناریو ۱: کاملاً آفلاین

**نیازمندی‌ها:**
- دانلود و ذخیره تمام مدل‌ها (20-100 GB فضا)
- پیکربندی اولیه با دسترسی موقت به اینترنت
- بروزرسانی‌های دوره‌ای (ماهیانه) از طریق USB/Network محلی

**محدودیت‌ها:**
- عدم دسترسی به مدل‌های جدید به‌صورت real-time
- نیاز به fine-tuning لوکال برای بهبود

---

#### سناریو ۲: نیمه‌آنلاین (Semi-Online)

**نیازمندی‌ها:**
- اتصال اینترنت با پهنای باند ~5-10 Mbps برای sync
- Fallback به مدل لوکال در قطعی اینترنت
- Cache کردن نتایج برای کاهش درخواست‌های ابری

**مزایا:**
- دسترسی به مدل‌های بهتر (در صورت نیاز)
- بروزرسانی خودکار

---

## 3️⃣ تحلیل اقتصادی

### 3.1 هزینه‌های اولیه راه‌اندازی (CAPEX)

#### سناریو A: اجرای کاملاً لوکال (Entry Level)

| ردیف | آیتم | هزینه (تومان) | هزینه (دلار) |
|------|------|--------------|-------------|
| 1 | GPU (RTX 3060 12GB) | 25,000,000 | ~$500 |
| 2 | CPU + Motherboard + RAM (32GB) | 20,000,000 | ~$400 |
| 3 | SSD 512GB NVMe | 4,000,000 | ~$80 |
| 4 | Power Supply + Case + Cooling | 8,000,000 | ~$160 |
| 5 | نصب و راه‌اندازی | 3,000,000 | ~$60 |
| **جمع** | | **60,000,000** | **~$1,200** |

---

#### سناریو B: اجرای لوکال (Professional)

| ردیف | آیتم | هزینه (تومان) | هزینه (دلار) |
|------|------|--------------|-------------|
| 1 | GPU (RTX 4090 24GB) | 110,000,000 | ~$2,200 |
| 2 | CPU (Ryzen 9 7950X) + Motherboard | 35,000,000 | ~$700 |
| 3 | RAM (64GB DDR5) | 15,000,000 | ~$300 |
| 4 | SSD 2TB NVMe Gen4 | 12,000,000 | ~$240 |
| 5 | Power Supply (1000W) + Case + Cooling | 15,000,000 | ~$300 |
| 6 | نصب و راه‌اندازی | 5,000,000 | ~$100 |
| **جمع** | | **192,000,000** | **~$3,840** |

---

#### سناریو C: اجرای ابری (Cloud GPU)

**ابر فردوسی (تخمین هزینه‌ها براساس اطلاعات عمومی):**

| GPU Type | VRAM | قیمت/ساعت (تومان) | قیمت ماهانه (720h) |
|----------|------|------------------|-------------------|
| T4 | 16GB | ~50,000 | ~36,000,000 |
| V100 | 16GB | ~120,000 | ~86,400,000 |
| A100 | 40GB | ~250,000 | ~180,000,000 |

**⚠️ نکته:** این قیمت‌ها تخمینی هستند و باید از ارائه‌دهنده خدمات استعلام شود.

---

#### سناریو D: اجرای ابری بین‌المللی (Google Cloud Platform)

| GPU Type | VRAM | قیمت/ساعت (USD) | قیمت ماهانه (720h) |
|----------|------|----------------|-------------------|
| NVIDIA T4 | 16GB | $0.35 | ~$252 |
| NVIDIA V100 | 16GB | $2.48 | ~$1,786 |
| NVIDIA A100 (40GB) | 40GB | $3.67 | ~$2,642 |
| NVIDIA L4 | 24GB | $0.80 | ~$576 |

**⚠️ محدودیت‌ها:**
- نیاز به VPN برای دسترسی (هزینه اضافی ~$10-20/ماه)
- ریسک قطع سرویس به دلیل تحریم‌ها
- هزینه انتقال داده (Egress): $0.12/GB

---

### 3.2 هزینه‌های عملیاتی (OPEX)

#### مقایسه هزینه‌های ماهانه (720 ساعت/ماه)

| سناریو | هزینه سخت‌افزار | برق (300W @ $0.05/kWh) | نگهداری | جمع ماهانه |
|--------|----------------|----------------------|---------|-----------|
| **Local Entry** | استهلاک 5-ساله: $20/ماه | ~$11 | $10 | **~$41** |
| **Local Pro** | استهلاک 5-ساله: $64/ماه | ~$22 | $20 | **~$106** |
| **Ferdowsi Cloud (T4)** | - | - | - | **~$720** (36M تومان) |
| **GCP (T4)** | - | - | VPN ~$15 | **~$267** |

**نتیجه‌گیری:** لوکال پس از 3-6 ماه break-even می‌شود.

---

### 3.3 هزینه‌های توسعه و Fine-tuning

| فعالیت | ساعات کاری | هزینه نیروی انسانی | هزینه محاسباتی | جمع |
|---------|----------|-------------------|----------------|-----|
| **جمع‌آوری و Preprocessing داده** | 80h | $2,400 | - | $2,400 |
| **Fine-tuning مدل اولیه** | 40h کاری + 100h GPU | $1,200 | $350 (GCP) | $1,550 |
| **ارزیابی و بهینه‌سازی** | 60h | $1,800 | $200 | $2,000 |
| **یکپارچه‌سازی با RAG** | 80h | $2,400 | - | $2,400 |
| **تست و Debug** | 60h | $1,800 | - | $1,800 |
| **مستندات و Deployment** | 40h | $1,200 | - | $1,200 |
| **جمع** | **360h** | **$10,800** | **$550** | **~$11,350** |

**⚠️ نکته:** هزینه نیروی انسانی با نرخ $30/ساعت (متوسط برای ML Engineer در ایران) محاسبه شده.

---

### 3.4 تحلیل ROI (Return on Investment)

#### فرض: استفاده پروژه به مدت 2 سال

| سناریو | CAPEX | OPEX (24 ماه) | جمع | Break-even |
|--------|-------|--------------|-----|-----------|
| **Local Entry** | $1,200 | $984 | **$2,184** | بلافاصله |
| **Local Pro** | $3,840 | $2,544 | **$6,384** | بلافاصله |
| **Ferdowsi Cloud** | $0 | $17,280 | **$17,280** | - |
| **GCP** | $0 | $6,408 | **$6,408** | - |

**نتیجه:**
- Local Pro از ماه 7 شروع به صرفه‌جویی می‌کند
- در 2 سال: صرفه‌جویی ~$11,000 نسبت به Ferdowsi Cloud
- GCP اگر VPN و تحریم مشکل نباشند، گزینه مقرون‌به‌صرفه برای short-term است

---

### 3.5 هزینه‌های پنهان (Hidden Costs)

| آیتم | Local | Cloud |
|------|-------|-------|
| **مدیریت سخت‌افزار** | نیاز به DevOps (20h/ماه) | خیر |
| **بروزرسانی‌ها** | دستی (10h/ماه) | خودکار |
| **Downtime** | ریسک خرابی سخت‌افزار | SLA 99.9% |
| **Security & Compliance** | مسئولیت خودتان | مسئولیت مشترک |
| **Scaling** | نیاز به خرید سخت‌افزار جدید | On-demand |

---

## 4️⃣ تحلیل ریسک‌ها

### 4.1 ریسک‌های امنیتی

#### 🔴 ریسک‌های اجرای لوکال

| ریسک | احتمال | شدت | راهکار کاهش |
|------|--------|-----|-------------|
| **دسترسی فیزیکی غیرمجاز** | متوسط | بالا | رمزگذاری دیسک (LUKS/BitLocker) + امنیت فیزیکی |
| **حملات داخلی** | کم | بالا | Role-based access control + Audit logs |
| **از دست رفتن داده (Hardware failure)** | متوسط | بحرانی | RAID + Backup خودکار روزانه |
| **نفوذ به شبکه محلی** | کم | متوسط | Firewall + Network segmentation + IDS |
| **عدم پچ امنیتی به‌موقع** | بالا | متوسط | Automated update pipeline + Vulnerability scanning |

**جمع‌بندی:** ریسک کلی **متوسط** با امکان کاهش به **کم** با اقدامات مناسب.

---

#### 🔴 ریسک‌های اجرای ابری

| ریسک | احتمال | شدت | راهکار کاهش |
|------|--------|-----|-------------|
| **نقض حریم خصوصی (Data breach)** | کم | بحرانی | Encryption at rest/transit + Private VPC |
| **قطع سرویس (ابر فردوسی)** | کم | متوسط | Multi-cloud یا hybrid architecture |
| **تحریم‌ها (GCP, AWS)** | بالا | بحرانی | استفاده از ابر داخلی یا fallback لوکال |
| **افزایش ناگهانی هزینه** | متوسط | متوسط | Budget alerts + Cost optimization |
| **Vendor lock-in** | بالا | متوسط | استفاده از استانداردهای باز (ONNX, HuggingFace) |
| **قطع اینترنت** | متوسط (در ایران) | بالا | Fallback به سیستم لوکال |

**جمع‌بندی:** ریسک کلی **متوسط تا بالا** به‌خصوص در شرایط ایران.

---

### 4.2 ریسک‌های حریم خصوصی (Privacy)

#### مقایسه سطوح حریم خصوصی

| معیار | Local | Ferdowsi Cloud | GCP/OpenAI |
|-------|-------|---------------|-----------|
| **کنترل کامل داده** | ✅ بله | ⚠️ محدود | ❌ خیر |
| **Data residency** | ✅ کاملاً محلی | ✅ ایران | ❌ خارج از کشور |
| **Third-party access** | ❌ خیر | ⚠️ احتمالاً | ✅ بله (OpenAI Terms) |
| **مناسب برای داده حساس** | ✅ بله | ⚠️ بسته به SLA | ❌ خیر |
| **GDPR/Compliance** | ✅ کنترل کامل | ⚠️ بستگی دارد | ⚠️ پیچیده |

**توصیه:** برای داده‌های حساس (پزشکی، مالی، دولتی) حتماً از **Local deployment** استفاده شود.

---

### 4.3 ریسک‌های فنی

| ریسک | توضیح | راهکار |
|------|-------|--------|
| **Model Drift** | کاهش دقت مدل در طول زمان | Continuous evaluation + Periodic retraining |
| **Hallucination** | تولید محتوای نادرست توسط LLM | RAG + Fact-checking layer + Temperature tuning |
| **Prompt Injection** | حملات از طریق prompt مخرب | Input sanitization + Prompt filtering |
| **Resource Exhaustion** | مصرف بیش از حد منابع | Rate limiting + Resource quotas + Monitoring |
| **Dependency Vulnerabilities** | آسیب‌پذیری در کتابخانه‌ها | Automated dependency scanning (Dependabot) |

---

### 4.4 ریسک‌های عملیاتی

| ریسک | احتمال | تأثیر | راهکار |
|------|--------|-------|--------|
| **عدم تخصص تیم** | متوسط | بالا | آموزش + مشاوره خارجی |
| **تغییر سریع تکنولوژی** | بالا | متوسط | معماری modular + استفاده از استانداردها |
| **کمبود پشتیبانی** | متوسط | متوسط | جامعه open-source + قراردادهای پشتیبانی |
| **مقیاس‌پذیری محدود** | کم | متوسط | معماری cloud-ready از ابتدا |

---

### 4.5 ریسک‌های قانونی و Compliance

**در ایران:**
- قانون حمایت از داده‌های شخصی (در حال تصویب)
- الزامات سازمان‌های نظارتی (بانک مرکزی، وزارت بهداشت و ...)

**توصیه‌ها:**
- مشورت با مشاور حقوقی برای compliance
- مستندسازی کامل جریان داده
- پیاده‌سازی data anonymization

---

## 5️⃣ معماری پیشنهادی

### 5.1 معماری هیبریدی (توصیه نهایی)

```
┌───────────────────────────────────────────────────────────────┐
│                         API Gateway                            │
│                     (Rate Limiting, Auth)                      │
└────────────┬──────────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────────┐
│                      Request Router                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Decision Logic:                                          │  │
│  │ • Sensitive data (بانکی، پزشکی) → Local                │  │
│  │ • Non-sensitive + Complex → Cloud (if available)         │  │
│  │ • Fallback: Always Local                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────┬───────────────────────────────────────────────────────┬───┘
     │                                                       │
     │ Local Path (Primary)                    Cloud Path   │
     ▼                                          (Fallback)   ▼
┌─────────────────────────────┐          ┌──────────────────────┐
│   LOCAL STACK               │          │   CLOUD STACK        │
│                             │          │                      │
│ ┌─────────────────────────┐ │          │ ┌──────────────────┐ │
│ │ Embedding Model         │ │          │ │ Ferdowsi Cloud   │ │
│ │ • paraphrase-multi      │ │          │ │ GPU Instance     │ │
│ │ • HooshvareLab BERT     │ │          │ │ (T4/V100)        │ │
│ └─────────────────────────┘ │          │ └──────────────────┘ │
│                             │          │                      │
│ ┌─────────────────────────┐ │          │ ┌──────────────────┐ │
│ │ Vector Store            │ │          │ │ OpenAI API       │ │
│ │ • FAISS (in-memory)     │ │          │ │ (for experiments)│ │
│ │ • Qdrant (persistent)   │ │          │ └──────────────────┘ │
│ └─────────────────────────┘ │          │                      │
│                             │          │                      │
│ ┌─────────────────────────┐ │          └──────────────────────┘
│ │ LLM Serving             │ │
│ │ • Ollama + Llama3-8B    │ │
│ │ • 4-bit Quantized       │ │
│ │ • vLLM (production)     │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Document Processing     │ │
│ │ • Hazm (Persian NLP)    │ │
│ │ • ParsBERT              │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────────┐
│                    Monitoring & Logging                         │
│  • Prometheus + Grafana                                         │
│  • ELK Stack (optional)                                         │
│  • Custom metrics (latency, accuracy, cost)                     │
└────────────────────────────────────────────────────────────────┘
```

---

### 5.2 مشخصات سخت‌افزار پیشنهادی برای معماری هیبریدی

```
┌─────────────────────────────────────────────────────────────┐
│  LOCAL SERVER (Primary Workload)                            │
├─────────────────────────────────────────────────────────────┤
│  GPU: NVIDIA RTX 4070 Ti (12GB) یا RTX 4090 (24GB)         │
│  CPU: AMD Ryzen 9 7900X (12-core)                           │
│  RAM: 64 GB DDR5                                             │
│  Storage: 1TB NVMe SSD + 4TB HDD (backup)                   │
│  OS: Ubuntu 22.04 LTS Server                                │
│  Cost: ~$2,500-3,500                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CLOUD BACKUP (Burst & Fine-tuning)                         │
├─────────────────────────────────────────────────────────────┤
│  Provider: Ferdowsi Cloud یا RunPod                         │
│  GPU: T4 (16GB) on-demand                                   │
│  Usage: ~20-40 hours/month                                  │
│  Cost: ~$200-400/month                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### 5.3 نقشه راه پیاده‌سازی (Implementation Roadmap)

#### فاز ۱: Proof of Concept (هفته‌های 1-4)

```
Week 1-2:
├── نصب زیرساخت اولیه
│   ├── راه‌اندازی Ubuntu + CUDA drivers
│   ├── نصب Docker + Docker Compose
│   └── پیکربندی Ollama
│
├── انتخاب و تست مدل‌های اولیه
│   ├── دانلود Llama-3-8B-Instruct
│   ├── تست با prompt‌های فارسی
│   └── Benchmark سرعت و کیفیت
│
Week 3-4:
├── پیاده‌سازی RAG ساده
│   ├── جمع‌آوری مجموعه داده تست (1000 document)
│   ├── تست embedding models فارسی
│   ├── راه‌اندازی FAISS vector store
│   └── اتصال به LLM با LangChain
│
└── ارزیابی اولیه
    ├── تست دقت (Accuracy)
    ├── اندازه‌گیری latency
    └── تصمیم GO/NO-GO
```

**خروجی:** یک demo کار که می‌تواند به 10 سوال فارسی پاسخ دهد

---

#### فاز ۲: MVP Development (هفته‌های 5-12)

```
Week 5-7:
├── توسعه Pipeline اصلی
│   ├── Document preprocessing (Hazm, cleantext)
│   ├── Chunking strategy (recursive vs semantic)
│   ├── Metadata extraction
│   └── بهینه‌سازی embedding
│
├── Fine-tuning مدل LLM
│   ├── جمع‌آوری داده آموزشی (5000+ samples)
│   ├── LoRA fine-tuning روی Llama-3-8B
│   └── Evaluation و Comparison
│
Week 8-10:
├── توسعه API و Backend
│   ├── FastAPI backend
│   ├── Authentication & Authorization
│   ├── Rate limiting
│   └── Caching layer (Redis)
│
├── Monitoring & Logging
│   ├── Prometheus metrics
│   ├── Grafana dashboards
│   └── Error tracking (Sentry)
│
Week 11-12:
├── تست و Optimization
│   ├── Load testing (Locust)
│   ├── Memory optimization
│   ├── Quantization experiments
│   └── Documentation
│
└── MVP Release
    └── Deployment در محیط staging
```

**خروجی:** یک سیستم قابل استفاده برای 10-50 کاربر همزمان

---

#### فاز ۳: Production Hardening (هفته‌های 13-20)

```
Week 13-16:
├── Security Hardening
│   ├── Penetration testing
│   ├── SSL/TLS configuration
│   ├── Input validation و sanitization
│   └── Secrets management (HashiCorp Vault)
│
├── Scalability Improvements
│   ├── Multi-GPU support (optional)
│   ├── Load balancing
│   ├── Horizontal scaling design
│   └── Database optimization
│
Week 17-20:
├── Advanced Features
│   ├── Multi-document summarization
│   ├── Advanced classification (multi-label)
│   ├── Named Entity Recognition
│   └── Relation extraction
│
├── UI/UX Development
│   ├── Web interface (React/Vue)
│   ├── Admin dashboard
│   └── Usage analytics
│
└── Production Deployment
    ├── Blue-green deployment
    ├── Monitoring alerts
    └── Backup & DR procedures
```

**خروجی:** سیستم production-ready با SLA 99%+

---

### 5.4 Stack تکنولوژی کامل

```yaml
# Infrastructure
OS: Ubuntu 22.04 LTS Server
Containerization: Docker + Docker Compose
Orchestration: Docker Swarm (simple) یا K3s (advanced)

# ML Stack
LLM Serving: Ollama (dev) + vLLM (production)
LLM Model: Llama-3-8B-Instruct (4-bit GGUF)
Embedding: sentence-transformers/paraphrase-multilingual
Vector Store: FAISS (development) + Qdrant (production)
Framework: LangChain / LlamaIndex

# Backend
API: FastAPI + Uvicorn
Authentication: JWT (PyJWT)
Caching: Redis
Database: PostgreSQL (metadata) + Qdrant (vectors)
Task Queue: Celery + RabbitMQ (for async processing)

# Frontend (Optional)
Web: React + TypeScript
UI Library: shadcn/ui یا MUI
State: Zustand یا Redux Toolkit

# Monitoring
Metrics: Prometheus
Visualization: Grafana
Logging: Loki یا ELK Stack
Tracing: Jaeger (optional)
Error Tracking: Sentry

# DevOps
CI/CD: GitLab CI یا GitHub Actions
IaC: Ansible
Backup: Restic + B2/S3-compatible storage

# Persian NLP Tools
Tokenization: Hazm
Normalization: cleantext, parsivar
Sentiment: HooshvareLab models
```

---

## 6️⃣ نتیجه‌گیری و توصیه‌ها

### 6.1 جدول مقایسه نهایی

| معیار | لوکال Entry | لوکال Pro | هیبریدی | Ferdowsi Cloud | GCP |
|-------|------------|----------|---------|---------------|-----|
| **هزینه اولیه** | $1,200 | $3,840 | $2,500 | $0 | $0 |
| **هزینه ماهانه** | $41 | $106 | $106 + $200 | $720 | $267 |
| **هزینه 2-ساله** | $2,184 | $6,384 | $9,844 | $17,280 | $6,408 |
| **کیفیت خروجی** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **حریم خصوصی** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **سرعت پاسخ** | متوسط (3-5s) | سریع (1-2s) | سریع (1-3s) | سریع | سریع |
| **Throughput** | کم (2-5 req/s) | متوسط (10-20) | بالا (20-50) | بالا | بالا |
| **مقیاس‌پذیری** | محدود | محدود | بالا | بالا | بالا |
| **Maintenance** | سنگین | سنگین | متوسط | سبک | سبک |
| **ریسک تحریم** | - | - | کم | کم | بالا |
| **Offline Capability** | ✅ کامل | ✅ کامل | ⚠️ Fallback | ❌ | ❌ |
| **مناسب برای ایران** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

### 6.2 توصیه نهایی بر اساس Use Case

#### 🎯 سناریو 1: استارتاپ / پروژه تحقیقاتی

**توصیه:** **لوکال Entry Level**

**دلایل:**
- سرمایه اولیه کم
- انعطاف‌پذیری بالا برای آزمایش
- استقلال کامل
- مناسب برای 1-3 محقق

**Stack:**
```
GPU: RTX 3060 12GB
Model: Llama-3-8B (4-bit)
Storage: 512GB SSD
Budget: $1,200 initial + $41/month
```

---

#### 🎯 سناریو 2: شرکت کوچک تا متوسط

**توصیه:** **معماری هیبریدی**

**دلایل:**
- بهترین trade-off بین کیفیت و هزینه
- قابلیت scale کردن
- Fallback در قطعی اینترنت
- مناسب برای 50-200 کاربر

**Stack:**
```
Local: RTX 4070 Ti + Llama-3-8B
Cloud: Ferdowsi T4 (burst)
Budget: $2,500 initial + $300/month
```

---

#### 🎯 سناریو 3: سازمان بزرگ / بانک / بیمارستان

**توصیه:** **لوکال Professional با Redundancy**

**دلایل:**
- حریم خصوصی بحرانی
- الزامات compliance
- نیاز به High Availability
- کنترل کامل

**Stack:**
```
GPU: 2x RTX 4090 (HA)
Model: Llama-3-8B + Fine-tuned models
Storage: RAID + Daily backups
Budget: $8,000 initial + $200/month
```

---

### 6.3 Checklist پیاده‌سازی

#### قبل از شروع پروژه:

- [ ] تعریف دقیق use case و KPI‌های موفقیت
- [ ] تأمین بودجه (CAPEX + OPEX برای حداقل 6 ماه)
- [ ] تشکیل تیم (حداقل: 1 ML Engineer + 1 DevOps)
- [ ] انتخاب معماری نهایی
- [ ] تهیه داده آموزشی اولیه (حداقل 1000 sample)

#### فاز Setup:

- [ ] خرید و راه‌اندازی سخت‌افزار
- [ ] نصب OS و driver‌های GPU
- [ ] پیکربندی Docker و environment
- [ ] دانلود و تست مدل‌های اولیه
- [ ] راه‌اندازی monitoring اولیه

#### فاز Development:

- [ ] پیاده‌سازی RAG pipeline
- [ ] Fine-tuning مدل (در صورت نیاز)
- [ ] توسعه API
- [ ] تست‌های امنیتی
- [ ] مستندسازی

#### فاز Production:

- [ ] Load testing
- [ ] Backup و Disaster Recovery
- [ ] Security hardening
- [ ] User training
- [ ] Go-live planning

---

### 6.4 KPI‌های پیشنهادی برای ارزیابی موفقیت

| KPI | هدف | نحوه اندازه‌گیری |
|-----|-----|------------------|
| **Accuracy** | >85% | Human evaluation روی 100 sample |
| **Response Time** | <3s (p95) | Prometheus metrics |
| **Availability** | >99% | Uptime monitoring |
| **Cost per Query** | <$0.01 | Total cost / Total queries |
| **User Satisfaction** | >4/5 | Survey |

---

### 6.5 ریسک‌های باقی‌مانده و Mitigation

| ریسک | Mitigation |
|------|-----------|
| **تغییر سریع تکنولوژی** | معماری modular + budget برای upgrade سالانه |
| **عدم تخصص تیم** | آموزش مستمر + مشارکت با دانشگاه‌ها |
| **محدودیت‌های قانونی** | مشاوره حقوقی + compliance از ابتدا |
| **Competition** | تمرکز بر quality و customization |

---

## 📚 منابع و مطالعه بیشتر

### مدل‌های فارسی

- [HooshvareLab - Persian NLP Models](https://github.com/hooshvare/parsbert)
- [ParsiNLU - Persian Language Understanding](https://github.com/persiannlp/parsinlu)
- [Persian Wikipedia Corpus](https://github.com/Text-Mining/Persian-Wikipedia-Corpus)

### ابزارها و فریم‌ورک‌ها

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama](https://ollama.ai/)
- [vLLM](https://github.com/vllm-project/vllm)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Qdrant](https://qdrant.tech/)

### مقالات و Papers

- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
- "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021)
- "ParsBERT: Transformer-based Model for Persian Language Understanding" (Farahani et al., 2020)

---

## 📞 تماس و پشتیبانی

این گزارش توسط سیستم تحلیل هوش مصنوعی تهیه شده است. برای پیاده‌سازی واقعی:

1. **مشاوره تخصصی**: مشورت با ML Engineer باتجربه در NLP فارسی
2. **Proof of Concept**: شروع با پروژه pilot کوچک (4-8 هفته)
3. **مشارکت دانشگاهی**: همکاری با دانشگاه‌های صنعتی شریف، تهران، امیرکبیر
4. **جامعه فارسی NLP**: عضویت در گروه‌های Telegram و GitHub

---

## 🔄 نسخه‌های آتی

این گزارش یک سند زنده است و در صورت نیاز به‌روزرسانی خواهد شد:

- **v1.1 (بهمن ۱۴۰۴):** بروزرسانی قیمت‌ها + مدل‌های جدید
- **v2.0 (فروردین ۱۴۰۵):** نتایج پیاده‌سازی واقعی + Benchmark‌ها

---

**تاریخ انتشار:** آبان ۱۴۰۴
**وضعیت:** نسخه نهایی v1.0
**مجوز:** این گزارش برای استفاده شخصی و تحقیقاتی آزاد است

---

## ✅ چک‌لیست تصمیم نهایی

برای تصمیم‌گیری نهایی، این سوالات را پاسخ دهید:

1. آیا داده‌های شما حساس هستند (بانکی، پزشکی، دولتی)? → **بله: لوکال / خیر: هیبریدی**
2. آیا بودجه اولیه >$3000 دارید? → **بله: Local Pro / خیر: Entry**
3. آیا دسترسی پایدار به اینترنت دارید? → **بله: هیبریدی / خیر: لوکال**
4. آیا نیاز به scale سریع دارید? → **بله: هیبریدی یا Cloud / خیر: لوکال**
5. آیا تیم DevOps/MLOps دارید? → **بله: لوکال / خیر: Cloud یا مشاوره**

---

**جمع‌بندی نهایی:**

برای **اکثر سازمان‌های ایرانی** که نیاز به پردازش متن فارسی دارند، **معماری هیبریدی با تمرکز بر اجرای لوکال** بهترین انتخاب است. این رویکرد تعادل مناسبی بین کیفیت، هزینه، امنیت و قابلیت اطمینان ایجاد می‌کند.

**شروع پیشنهادی:**
1. خرید یک RTX 4070 Ti ($2,000)
2. نصب Ollama + Llama-3-8B
3. ساخت POC با 100 document
4. ارزیابی و تصمیم برای scale

---

**موفق باشید! 🚀**
