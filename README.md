# 🏛️ Sultanate Legal AI Assistant 🤖⚖️

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/LangChain-Enabled-green" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-UI-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenRouter-Integrated-purple" alt="OpenRouter">
  <img src="https://img.shields.io/badge/Vosk-Voice_Recognition-orange" alt="Vosk">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</div>

<div dir="rtl">
<h2>مساعد ذكاء اصطناعي قانوني متكامل لسلطنة عمان</h2>
<p>نظام متطور يتيح البحث الذكي والتحليل القانوني وإنشاء التقارير استناداً إلى القوانين العمانية، مع دعم اللغتين العربية والإنجليزية، والتفاعل الصوتي، وإنشاء المستندات القانونية.</p>
</div>

<p align="center">
  <img src="https://github.com/alanqoudif/Ankaa/raw/master/docs/images/demo.gif" alt="Demo" width="700">
</p>

<div align="center">
  <h3>🌐 <a href="#english-readme">English</a> | <a href="#arabic-readme">العربية</a> 🌐</h3>
</div>

<h2 id="english-readme">📋 Table of Contents (English)</h2>

- [🔍 Overview](#overview)
- [🔎 Features](#features)
- [🌟 New Features](#new-features)
- [💻 System Requirements](#system-requirements)
- [⚙️ Installation and Setup](#installation-and-setup)
- [🚀 Usage](#usage)
- [💡 Examples](#examples)

<h2 id="arabic-readme">📋 جدول المحتويات (العربية)</h2>

- [🔍 نظرة عامة](#نظرة-عامة)
- [🔎 المستوى الأول - بوت البحث الذكي](#المستوى-الأول---بوت-البحث-الذكي)
- [📑 المستوى الثاني - استخراج المواد القانونية](#المستوى-الثاني---استخراج-المواد-القانونية)
- [🔄 المستوى الثالث - مقارنة القوانين والتفاعل الصوتي](#المستوى-الثالث---مقارنة-القوانين-والتفاعل-الصوتي)
- [📝 المستوى الرابع - إنشاء المستندات القانونية](#المستوى-الرابع---إنشاء-المستندات-القانونية)
- [📊 المستوى الخامس - التقارير الذكية ودراسة الحالات](#المستوى-الخامس---التقارير-الذكية-ودراسة-الحالات)
- [🌟 الميزات الجديدة](#الميزات-الجديدة)
- [💻 متطلبات النظام](#متطلبات-النظام)
- [⚙️ التثبيت والإعداد](#التثبيت-والإعداد)
- [🗂️ هيكل المشروع](#هيكل-المشروع)
- [🚀 استخدام النظام](#استخدام-النظام)
- [💡 أمثلة على الاستخدام](#أمثلة-على-الاستخدام)

## Overview

The Sultanate Legal AI Assistant is a comprehensive legal assistant designed for Omani laws. It combines advanced AI technologies to provide accurate answers, legal document analysis, voice interaction, and document generation capabilities. The system supports both Arabic and English languages, making it accessible to a wider audience.

## Features

- **Intelligent Search**: Search and answer questions based on Omani legal documents
- **Legal Document Analysis**: Extract and analyze specific articles and sections from legal texts
- **Law Comparison**: Compare different laws and identify similarities and differences
- **Voice Interaction**: Interact with the system using voice commands and queries
- **Document Generation**: Create legal documents based on user requirements
- **Multi-language Support**: Full support for both Arabic and English

## New Features

### OpenRouter Integration
- Added support for OpenRouter API to access powerful language models
- Automatic model selection and fallback mechanisms
- Enhanced response quality for legal queries

### Voice Recognition Improvements
- Integrated Vosk for offline voice recognition
- Added automatic model downloading
- Enhanced voice processing capabilities
- Improved error handling and user feedback

### UI Enhancements
- Reorganized interface for better user experience
- Clear sections for different functionalities
- Improved visual feedback and styling
- Better organization of system components

## نظرة عامة

تم تطوير هذا المشروع على خمس مراحل متتالية، كل مرحلة تضيف مجموعة من الميزات والوظائف المتقدمة. يعتمد النظام على تقنيات الذكاء الاصطناعي والتعلم الآلي لمعالجة وتحليل القوانين العمانية وتقديم إجابات دقيقة للمستخدمين.

## المستوى الأول - بوت البحث الذكي

### الوصف
في هذا المستوى، تم تطوير شات بوت ذكي قادر على البحث والإجابة على أسئلة المستخدمين استناداً فقط إلى الوثائق القانونية العمانية (باللغتين العربية والإنجليزية).

### الميزات المنفذة
- تحليل ومعالجة مستندات PDF القانونية
- إنشاء تضمينات متجهية (Vector Embeddings) للبحث الفعال
- واجهة محادثة حديثة باستخدام Streamlit
- استخدام نماذج لغوية محلية لمعالجة الأسئلة والإجابات
- دعم اللغتين العربية والإنجليزية

### التقنيات المستخدمة
- Python 3.10+
- LangChain لإدارة المستندات
- ChromaDB لتخزين التضمينات المتجهية
- PyMuPDF لتحليل ملفات PDF
- Streamlit لواجهة المستخدم
- نماذج LLM محلية للاستدلال

## المستوى الثاني - استخراج المواد القانونية

### الوصف
في هذا المستوى، تم تحسين النظام ليكون قادراً على استخراج مواد قانونية محددة من القوانين العمانية وتقديم ملخصات لها.

### الميزات المنفذة
- استخراج مواد قانونية محددة بناءً على رقم المادة
- تلخيص المواد القانونية
- تحسين دقة البحث والاسترجاع
- تحسين واجهة المستخدم لعرض المواد القانونية

### التقنيات المستخدمة
- تقنيات معالجة اللغة الطبيعية المتقدمة
- خوارزميات استخراج النصوص
- تقنيات التلخيص الآلي

## المستوى الثالث - مقارنة القوانين والتفاعل الصوتي

### الوصف
في هذا المستوى، تم إضافة وظائف مقارنة القوانين والتفاعل الصوتي مع النظام.

### الميزات المنفذة
- مقارنة القوانين من مستندات قانونية مختلفة
- التفاعل الصوتي عبر الميكروفون (تحويل الصوت إلى نص)
- قراءة الإجابات بصوت عالٍ (تحويل النص إلى صوت)

### التقنيات المستخدمة
- Vosk (للتعرف على الصوت بدون إنترنت) أو Whisper API (عبر الإنترنت)
- pyttsx3 (للقراءة بدون إنترنت) أو gTTS (عبر الإنترنت)
- LangChain و LLM لمقارنة المستندات القانونية

## المستوى الرابع - إنشاء المستندات القانونية

### الوصف
في هذا المستوى، تم تطوير وظائف إنشاء المستندات القانونية بناءً على متطلبات المستخدم.

### الميزات المنفذة
- إنشاء عقود قانونية (عقود عمل، عقود إيجار، عقود خدمات)
- إنشاء تفويضات قانونية
- تصدير المستندات بصيغة PDF
- إنشاء صور للمستندات
- حزم المستندات في ملفات ZIP

### التقنيات المستخدمة
- WeasyPrint أو ReportLab لإنشاء ملفات PDF
- PIL لإنشاء صور المستندات
- نماذج قوالب HTML لتصميم المستندات

## المستوى الخامس - التقارير الذكية ودراسة الحالات

### الوصف
في هذا المستوى النهائي، تم تطوير وظائف متقدمة لتحليل السيناريوهات القانونية المعقدة وإنشاء تقارير PDF شاملة.

### الميزات المنفذة
- استقبال سيناريوهات قانونية واقعية من المستخدم
- تحليل السيناريوهات بشكل قانوني استناداً إلى القوانين العمانية
- تحديد القوانين والمواد ذات الصلة
- تحليل الآثار القانونية المترتبة
- إنشاء تقارير PDF شاملة تتضمن التحليل والنتائج

### التقنيات المستخدمة
- LangChain و LlamaIndex لإدارة المستندات
- FAISS أو ChromaDB للبحث الدلالي
- WeasyPrint أو ReportLab لإنشاء تقارير PDF
- تقنيات تحليل النصوص المتقدمة

## 💻 متطلبات النظام

<div dir="rtl">
<table>
  <tr>
    <th>المتطلب</th>
    <th>التفاصيل</th>
  </tr>
  <tr>
    <td>لغة البرمجة</td>
    <td>Python 3.10 أو أحدث</td>
  </tr>
  <tr>
    <td>الذاكرة</td>
    <td>8GB على الأقل (16GB موصى به)</td>
  </tr>
  <tr>
    <td>مساحة التخزين</td>
    <td>10GB على الأقل</td>
  </tr>
  <tr>
    <td>نظام التشغيل</td>
    <td>Windows 10/11، macOS 12+، أو Linux</td>
  </tr>
  <tr>
    <td>اختياري</td>
    <td>وحدة معالجة رسومات (GPU) لتسريع النماذج اللغوية</td>
  </tr>
</table>
</div>

## ⚙️ التثبيت والإعداد

### 📌 الخطوة 1: استنساخ المستودع

```bash
# استنساخ المستودع من GitHub
git clone https://github.com/alanqoudif/Ankaa.git

# الدخول إلى مجلد المشروع
cd Ankaa
```

### 🔍 الخطوة 2: إنشاء بيئة افتراضية (موصى به)

<details>
<summary>لنظام macOS/Linux</summary>

```bash
# إنشاء البيئة الافتراضية
python -m venv .venv

# تفعيل البيئة الافتراضية
source .venv/bin/activate
```
</details>

<details>
<summary>لنظام Windows</summary>

```bash
# إنشاء البيئة الافتراضية
python -m venv .venv

# تفعيل البيئة الافتراضية
.venv\Scripts\activate
```
</details>

### 📚 الخطوة 3: تثبيت المتطلبات

```bash
# تثبيت جميع المكتبات المطلوبة
pip install -r requirements.txt
```

### 🤖 الخطوة 4: إعداد نموذج اللغة

<details>
<summary>الخيار 1: استخدام Ollama (موصى به)</summary>

```bash
# تثبيت Ollama من الموقع الرسمي
# https://ollama.com/download

# تشغيل خدمة Ollama
ollama serve

# في نافذة طرفية جديدة، قم بتنزيل نموذج مناسب يدعم اللغة العربية مثل:
ollama pull mistral:latest
# أو
ollama pull qwen:latest
# أو
ollama pull llama3
```
</details>

<details>
<summary>الخيار 2: استخدام نموذج محلي</summary>

```bash
# إنشاء مجلد النماذج إذا لم يكن موجوداً
mkdir -p models

# تنزيل نموذج مناسب من Hugging Face
# مثال: تنزيل نموذج GGUF من موقع Hugging Face
# يمكنك استخدام أي نموذج يدعم اللغة العربية مثل Mistral، Qwen، Llama، إلخ

# مثال لتنزيل نموذج Mistral 7B
wget -P models/ https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```
</details>

### 🚀 الخطوة 5: تشغيل التطبيق

```bash
# تشغيل واجهة Streamlit
streamlit run src/app.py
```

بعد تشغيل الأمر، سيفتح المتصفح تلقائياً على الرابط `http://localhost:8501`

## هيكل المشروع

```
.
├── README.md
├── requirements.txt
├── src
│   ├── app.py                     # نقطة الدخول الرئيسية للتطبيق
│   ├── data/                      # مجلد للوثائق القانونية
│   ├── document_loader.py         # وظائف تحميل وتحليل المستندات
│   ├── document_structure.py      # تعريف هيكل المستندات
│   ├── embeddings.py              # إنشاء التضمينات المتجهية
│   ├── llm_chain.py               # سلسلة LLM للأسئلة والأجوبة
│   ├── models/                    # مجلد لنماذج اللغة والتضمين
│   ├── retriever.py               # استرجاع المستندات ذات الصلة
│   ├── setup.py                   # إعداد المشروع
│   ├── ui/                        # مكونات واجهة المستخدم
│   │   ├── components.py          # مكونات واجهة المستخدم الأساسية
│   │   ├── document_components.py # مكونات إنشاء المستندات
│   │   └── voice_components.py    # مكونات التفاعل الصوتي
│   └── utils/                     # وظائف مساعدة
│       ├── arabic_utils.py        # معالجة اللغة العربية
│       ├── case_analysis_utils.py # تحليل القضايا القانونية
│       ├── comparison_utils.py    # مقارنة القوانين
│       ├── document_generation_utils.py # إنشاء المستندات
│       ├── document_utils.py      # معالجة المستندات
│       ├── image_generation_utils.py # إنشاء صور المستندات
│       ├── model_utils.py         # إدارة النماذج
│       ├── ollama_utils.py        # التكامل مع Ollama
│       └── voice_utils.py         # معالجة الصوت
└── chroma_db/                     # قاعدة بيانات ChromaDB
```

## 🚀 استخدام النظام

<div dir="rtl">
<h3>📝 دليل البدء السريع</h3>

<table>
  <tr>
    <th>الخطوة</th>
    <th>الوصف</th>
  </tr>
  <tr>
    <td><strong>1. تحضير المستندات</strong></td>
    <td>ضع المستندات القانونية العمانية (بصيغة PDF) في مجلد <code>src/data/</code></td>
  </tr>
  <tr>
    <td><strong>2. تشغيل التطبيق</strong></td>
    <td>شغّل التطبيق باستخدام الأمر <code>streamlit run src/app.py</code></td>
  </tr>
  <tr>
    <td><strong>3. إعداد النظام</strong></td>
    <td>انقر على زر <strong>"إعداد الكل"</strong> لتحميل المستندات وإنشاء التضمينات وتهيئة النظام دفعة واحدة</td>
  </tr>
  <tr>
    <td><strong>4. استخدام النظام</strong></td>
    <td>استخدم واجهة المحادثة لطرح الأسئلة واستخدام الميزات المختلفة</td>
  </tr>
</table>

<h3>💬 ميزات النظام وكيفية استخدامها</h3>

<details>
<summary>🔍 <strong>البحث عن المعلومات القانونية</strong></summary>
<p>اكتب سؤالك في مربع المحادثة باللغة العربية أو الإنجليزية مثل:</p>
<ul>
  <li>"ما هي عقوبة السرقة وفقاً للقوانين العمانية؟"</li>
  <li>"What are the requirements for establishing a company in Oman?"</li>
</ul>
</details>

<details>
<summary>📝 <strong>استخراج مواد قانونية محددة</strong></summary>
<p>اطلب مادة قانونية محددة بذكر رقمها والقانون الذي تنتمي إليه:</p>
<ul>
  <li>"أعطني المادة 150 من قانون الجزاء العماني"</li>
  <li>"Show me Article 25 of the Omani Labor Law"</li>
</ul>
</details>

<details>
<summary>🔄 <strong>مقارنة القوانين</strong></summary>
<p>استخدم كلمة "قارن" أو "compare" في سؤالك لمقارنة القوانين أو المواد:</p>
<ul>
  <li>"قارن بين قانون العمل وقانون الخدمة المدنية فيما يتعلق بالإجازات"</li>
  <li>"Compare the regulations for commercial companies between different Omani laws"</li>
</ul>
</details>

<details>
<summary>🎤 <strong>التفاعل الصوتي</strong></summary>
<p>استخدم الأزرار المخصصة للتفاعل الصوتي:</p>
<ul>
  <li>انقر على زر <strong>"إدخال صوتي"</strong> لطرح سؤالك بالصوت</li>
  <li>انقر على زر <strong>"قراءة بصوت عالٍ"</strong> لسماع الإجابة</li>
</ul>
</details>

<details>
<summary>📄 <strong>إنشاء المستندات القانونية</strong></summary>
<p>استخدم قسم "إنشاء المستندات" لإنشاء مستندات قانونية مثل:</p>
<ul>
  <li>عقود العمل</li>
  <li>عقود الإيجار</li>
  <li>عقود الخدمات</li>
  <li>التفويضات القانونية</li>
</ul>
</details>

<details>
<summary>📊 <strong>تحليل السيناريوهات القانونية وإنشاء التقارير</strong></summary>
<p>قدم سيناريو قانوني واقعي واطلب تحليله وإنشاء تقرير PDF مثل:</p>
<ul>
  <li>"مواطن استثمر أموالاً في الخارج بدون أن يصرح بها للسلطات العمانية، ما هي الآثار القانونية؟"</li>
  <li>"شركة قامت بتسريح موظف دون إشعار مسبق، ما هي حقوق الموظف وفقاً للقانون العماني؟ أريد تقرير PDF"</li>
</ul>
</details>
</div>

## 💡 أمثلة على الاستخدام

<div dir="rtl">
<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">

<div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #1E3A8A;">
<h3>🔎 البحث عن المعلومات القانونية</h3>

```
ما هي عقوبة السرقة وفقًا للقوانين العمانية؟
```

```
What are the requirements for establishing 
a company in Oman?
```

```
ما هي شروط الحصول على الجنسية العمانية؟
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0369a1;">
<h3>📑 استخراج مواد قانونية محددة</h3>

```
أعطني المادة 150 من قانون الجزاء العماني
```

```
Show me Article 25 of the Omani Labor Law
```

```
ما هي المادة 10 من قانون الشركات التجارية؟
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0fff4; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #166534;">
<h3>🔄 مقارنة القوانين</h3>

```
قارن بين قانون العمل وقانون الخدمة المدنية فيما يتعلق بالإجازات
```

```
Compare the regulations for commercial 
companies between different Omani laws
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #fff7ed; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #c2410c;">
<h3>🎤 التفاعل الصوتي</h3>

<p>• انقر على زر <strong>"إدخال صوتي"</strong> واطرح سؤالك شفهياً</p>

<p>• انقر على زر <strong>"قراءة بصوت عالٍ"</strong> لسماع الإجابة</p>
</div>

<div style="flex: 1; min-width: 300px; background-color: #faf5ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #7e22ce;">
<h3>📝 إنشاء المستندات القانونية</h3>

<p>استخدم قسم "إنشاء المستندات" لإنشاء:</p>

<ul>
  <li>عقود العمل</li>
  <li>عقود الإيجار</li>
  <li>عقود الخدمات</li>
  <li>التفويضات القانونية</li>
</ul>
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0f9ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0284c7;">
<h3>📊 تحليل السيناريوهات وإنشاء التقارير</h3>

```
مواطن استثمر أموالاً في الخارج بدون أن يصرح بها للسلطات العمانية، ما هي الآثار القانونية؟ أريد تقرير PDF
```

```
شركة قامت بتسريح موظف دون إشعار مسبق، ما هي حقوق الموظف وفقاً للقانون العماني؟
```
</div>

</div>
</div>

## الميزات الجديدة

### تكامل OpenRouter
- إضافة دعم لواجهة برمجة تطبيقات OpenRouter للوصول إلى نماذج لغوية قوية
- اختيار تلقائي للنموذج وآليات الرجوع الاحتياطي
- تحسين جودة الردود للاستفسارات القانونية

### تحسينات التعرف على الصوت
- دمج Vosk للتعرف على الصوت دون اتصال بالإنترنت
- إضافة تنزيل تلقائي للنموذج
- تعزيز قدرات معالجة الصوت
- تحسين معالجة الأخطاء والتغذية الراجعة للمستخدم

### تحسينات واجهة المستخدم
- إعادة تنظيم الواجهة لتحسين تجربة المستخدم
- أقسام واضحة للوظائف المختلفة
- تحسين التغذية الراجعة المرئية والتصميم
- تنظيم أفضل لمكونات النظام
