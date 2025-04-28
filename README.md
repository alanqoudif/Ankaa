# 🏛️ Sultanate Legal AI Assistant 🤖⚖️

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/LangChain-Enabled-green" alt="LangChain">
  <img src="https://img.shields.io/badge/Streamlit-UI-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenRouter-Integrated-purple" alt="OpenRouter">
  <img src="https://img.shields.io/badge/Vosk-Voice_Recognition-orange" alt="Vosk">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</div>

<h1 align="center">Sultanate Legal AI Assistant</h1>

<p align="center">An advanced system for intelligent search, legal analysis, and report generation based on Omani laws, with support for both Arabic and English languages, voice interaction, and legal document generation.</p>

<p align="center">
  <img src="https://github.com/alanqoudif/Ankaa/raw/master/docs/images/demo.gif" alt="Demo" width="700">
</p>

## 📋 Table of Contents

- [🔍 Overview](#overview)
- [🔎 Features](#features)
  - [Level 1: Intelligent Search Bot](#level-1-intelligent-search-bot)
  - [Level 2: Legal Article Extraction](#level-2-legal-article-extraction)
  - [Level 3: Law Comparison and Voice Interaction](#level-3-law-comparison-and-voice-interaction)
  - [Level 4: Legal Document Generation](#level-4-legal-document-generation)
  - [Level 5: Intelligent Reports and Case Analysis](#level-5-intelligent-reports-and-case-analysis)
- [🌟 New Features](#new-features)
  - [OpenRouter Integration](#openrouter-integration)
  - [Voice Recognition Improvements](#voice-recognition-improvements)
  - [UI Enhancements](#ui-enhancements)
- [💻 System Requirements](#system-requirements)
- [⚙️ Installation and Setup](#installation-and-setup)
- [🚀 Usage](#usage)
- [💡 Examples](#examples)

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

## System Requirements

<table>
  <tr>
    <th>Requirement</th>
    <th>Details</th>
  </tr>
  <tr>
    <td>Programming Language</td>
    <td>Python 3.10 or newer</td>
  </tr>
  <tr>
    <td>Memory</td>
    <td>8GB minimum (16GB recommended)</td>
  </tr>
  <tr>
    <td>Storage</td>
    <td>10GB minimum</td>
  </tr>
  <tr>
    <td>Operating System</td>
    <td>Windows 10/11, macOS 12+, or Linux</td>
  </tr>
  <tr>
    <td>Optional</td>
    <td>GPU for accelerating language models</td>
  </tr>
</table>

## Installation and Setup

### Step 1: Clone the Repository

```bash
# Clone the repository from GitHub
git clone https://github.com/alanqoudif/Ankaa.git

# Navigate to the project directory
cd Ankaa
```

### Step 2: Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Requirements

```bash
# Install required libraries
pip install -r requirements.txt
```

### Step 4: Set Up Environment File

```bash
# Create .env file
touch .env
```

Add the following environment variables to the `.env` file:

```
# Example .env file
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Specify default model
DEFAULT_MODEL=openai/gpt-4-turbo

# Optional: Voice settings
VOICE_MODEL_PATH=./models/vosk-model-small-ar
TEXT_TO_SPEECH_ENGINE=pyttsx3  # Options: pyttsx3, gtts
```

You can get an OpenRouter API key by signing up at [OpenRouter.ai](https://openrouter.ai/).

### Step 5: Run the Application

```bash
# Run the application
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
What are the requirements for obtaining Omani citizenship?
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0369a1;">
<h3>📑 Extract Specific Legal Articles</h3>

```
Show me Article 150 of the Omani Penal Code
```

```
Show me Article 25 of the Omani Labor Law
```

```
What is Article 10 of the Commercial Companies Law?
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0fff4; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #166534;">
<h3>🔄 Compare Laws</h3>

```
Compare the Labor Law and Civil Service Law regarding vacations
```

```
Compare the regulations for commercial 
companies between different Omani laws
```
</div>

<div style="flex: 1; min-width: 300px; background-color: #fff7ed; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #c2410c;">
<h3>🎤 Voice Interaction</h3>

<p>• Click the <strong>"Voice Input"</strong> button and ask your question verbally</p>

<p>• Click the <strong>"Read Aloud"</strong> button to hear the answer</p>
</div>

<div style="flex: 1; min-width: 300px; background-color: #faf5ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #7e22ce;">
<h3>📝 Create Legal Documents</h3>

<p>Use the "Generate Documents" section to create:</p>

<ul>
  <li>Employment contracts</li>
  <li>Lease agreements</li>
  <li>Service contracts</li>
  <li>Legal authorizations</li>
</ul>
</div>

<div style="flex: 1; min-width: 300px; background-color: #f0f9ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0284c7;">
<h3>📊 Scenario Analysis and Report Generation</h3>

```
A citizen invested money abroad without declaring it to Omani authorities. What are the legal implications? I need a PDF report.
```

```
A company terminated an employee without prior notice. What are the employee's rights according to Omani law?
```
</div>

</div>
</div>

## New Features

### OpenRouter Integration
- Added support for OpenRouter API to access powerful language models
- Automatic model selection and fallback mechanisms
- Improved response quality for legal queries

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
