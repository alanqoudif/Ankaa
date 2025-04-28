# مكتبات مشروع Ankaa

فيما يلي قائمة بالمكتبات الرئيسية المستخدمة في مشروع Ankaa والتي تحتاج إلى تثبيتها:

## المكتبات الأساسية

1. **langchain** و **langchain-community** - إطار عمل لبناء تطبيقات الذكاء الاصطناعي
2. **chromadb** - قاعدة بيانات للتضمينات النصية (embeddings)
3. **pymupdf** (يستورد كـ `fitz`) - لمعالجة ملفات PDF
4. **streamlit** - لبناء واجهة المستخدم التفاعلية
5. **sentence-transformers** - لإنشاء تضمينات نصية
6. **llama-cpp-python** - لتشغيل نماذج LLM محليًا
7. **pydantic** - للتحقق من صحة البيانات
8. **python-dotenv** - لإدارة متغيرات البيئة
9. **tqdm** - لعرض شريط التقدم
10. **numpy** - للعمليات الحسابية
11. **faiss-cpu** - للبحث السريع في التضمينات النصية
12. **transformers** - لاستخدام نماذج التعلم العميق
13. **torch** - إطار عمل للتعلم العميق
14. **accelerate** - لتسريع نماذج التعلم العميق

## مكتبات معالجة الصوت

1. **vosk** - للتعرف على الكلام
2. **sounddevice** و **soundfile** - للتعامل مع الصوت
3. **pyttsx3** و **gtts** - لتحويل النص إلى كلام

## مكتبات إنشاء المستندات والصور

1. **weasyprint** - لإنشاء ملفات PDF من HTML
2. **pillow** - لمعالجة الصور
3. **reportlab** - لإنشاء ملفات PDF
4. **pdfkit** - لتحويل HTML إلى PDF

## مكتبات خارجية

1. **openai** - للتكامل مع واجهة برمجة تطبيقات OpenAI

## كيفية التثبيت

يمكن تثبيت جميع هذه المكتبات باستخدام ملف `requirements.txt` الموجود في المشروع عن طريق:

```bash
pip install -r requirements.txt
```

أو باستخدام ملفات التشغيل السريع التي قمنا بإنشائها:
- على Linux/macOS: `./run_app.sh`
- على Windows: `run_app.bat`

## ملاحظات مهمة

1. **PyMuPDF (fitz)**: قد تواجه مشاكل في تثبيت هذه المكتبة على بعض الأنظمة. إذا واجهت مشكلة، جرب:
   ```bash
   pip install pymupdf==1.23.7
   ```

2. **llama-cpp-python**: قد تحتاج إلى مترجم C++ مثبت على نظامك لتثبيت هذه المكتبة.

3. **torch**: إذا كنت تريد دعم GPU، تأكد من تثبيت الإصدار المناسب لبطاقة GPU الخاصة بك.

4. **weasyprint**: قد تحتاج إلى تثبيت بعض المكتبات الإضافية على مستوى النظام، خاصة على Linux.

5. **vosk**: تحتاج إلى تنزيل نموذج لغة منفصل لاستخدام هذه المكتبة للتعرف على الكلام.

# Libraries for Ankaa Project

Here is a list of the main libraries used in the Ankaa project that need to be installed:

## Core Libraries

1. **langchain** and **langchain-community** - Framework for building AI applications
2. **chromadb** - Vector database for text embeddings
3. **pymupdf** (imported as `fitz`) - For PDF document processing
4. **streamlit** - For building interactive user interfaces
5. **sentence-transformers** - For creating text embeddings
6. **llama-cpp-python** - For running LLM models locally
7. **pydantic** - For data validation
8. **python-dotenv** - For managing environment variables
9. **tqdm** - For progress bars
10. **numpy** - For numerical operations
11. **faiss-cpu** - For fast search in text embeddings
12. **transformers** - For using deep learning models
13. **torch** - Deep learning framework
14. **accelerate** - For accelerating deep learning models

## Voice Processing Libraries

1. **vosk** - For speech recognition
2. **sounddevice** and **soundfile** - For audio handling
3. **pyttsx3** and **gtts** - For text-to-speech conversion

## Document and Image Generation Libraries

1. **weasyprint** - For creating PDF files from HTML
2. **pillow** - For image processing
3. **reportlab** - For creating PDF files
4. **pdfkit** - For converting HTML to PDF

## External Libraries

1. **openai** - For integration with OpenAI API

## How to Install

You can install all these libraries using the `requirements.txt` file in the project:

```bash
pip install -r requirements.txt
```

Or by using the quick start scripts we created:
- On Linux/macOS: `./run_app.sh`
- On Windows: `run_app.bat`

## Important Notes

1. **PyMuPDF (fitz)**: You may encounter issues installing this library on some systems. If you have a problem, try:
   ```bash
   pip install pymupdf==1.23.7
   ```

2. **llama-cpp-python**: You may need a C++ compiler installed on your system to install this library.

3. **torch**: If you want GPU support, make sure to install the appropriate version for your GPU.

4. **weasyprint**: You may need to install some additional system-level libraries, especially on Linux.

5. **vosk**: You need to download a separate language model to use this library for speech recognition.
