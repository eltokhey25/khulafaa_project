# دليل نشر المشروع على PythonAnywhere

## المتطلبات
- حساب على PythonAnywhere (مجاني أو مدفوع)
- Python 3.12 أو 3.13 (Django 6.0 يتطلب على الأقل Python 3.12)
- تأكد أن System Image هو "innit" من صفحة Account

---

## الخطوات

### 1. رفع المشروع (Upload the Project)

**الطريقة الأولى – عبر Git (الأفضل):**
```bash
# في Bash console على PythonAnywhere
git clone https://github.com/YOUR_USERNAME/khulafaa_project.git
```

**الطريقة الثانية – رفع يدوي:**
- اذهب إلى Files → Upload a file
- ارفع ملف ZIP للمشروع ثم فكّه:
  ```bash
  unzip khulafaa_project.zip
  ```

---

### 2. إنشاء البيئة الافتراضية (Virtual Environment)

```bash
# في Bash console
mkvirtualenv --python=/usr/bin/python3.12 khulafaa-env

# تفعيل البيئة
workon khulafaa-env

# تثبيت المتطلبات
pip install -r ~/khulafaa_project/requirements.txt
```

---

### 3. إعداد ملف WSGI

- اذهب إلى **Web** tab في PythonAnywhere
- انقر **Add a new web app** → Manual configuration → Python 3.12
- في قسم **Code**، اضبط:
  - **Source code:** `/home/YOUR_USERNAME/khulafaa_project`
  - **Working directory:** `/home/YOUR_USERNAME/khulafaa_project`
- في قسم **Virtualenv:** أدخل `/home/YOUR_USERNAME/.virtualenvs/khulafaa-env`
- انقر على رابط ملف **WSGI configuration file** وضع محتوى الملف `pythonanywhere_wsgi.py` (انظر الخطوة 4)

---

### 4. ملف WSGI (pythonanywhere_wsgi.py)

انسخ هذا المحتوى في ملف WSGI الموجود في PythonAnywhere (يبدأ اسمه بـ `/var/www/...`):

```python
import os
import sys

path = '/home/YOUR_USERNAME/khulafaa_project'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'results.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_SECRET_KEY'] = 'PASTE_YOUR_SECRET_KEY_HERE'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> ⚠️ استبدل `YOUR_USERNAME` باسم المستخدم الخاص بك على PythonAnywhere
> ⚠️ استبدل `PASTE_YOUR_SECRET_KEY_HERE` بمفتاح سري قوي (انظر الخطوة 5)

---

### 5. توليد Secret Key جديد

```bash
workon khulafaa-env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

انسخ الناتج وضعه في ملف WSGI في خانة `DJANGO_SECRET_KEY`.

---

### 6. إعداد قاعدة البيانات والملفات الساكنة

```bash
workon khulafaa-env
cd ~/khulafaa_project

# تطبيق migrations
python manage.py migrate

# جمع الملفات الساكنة
python manage.py collectstatic --noinput

# إنشاء مستخدم مدير (اختياري)
python manage.py createsuperuser
```

---

### 7. إعداد Static Files في PythonAnywhere

في صفحة **Web** tab، أضف في قسم **Static files**:
| URL          | Directory                                      |
|--------------|------------------------------------------------|
| `/static/`   | `/home/YOUR_USERNAME/khulafaa_project/staticfiles` |

---

### 8. تشغيل الموقع

- انقر زر **Reload** في صفحة Web
- افتح الرابط: `https://YOUR_USERNAME.pythonanywhere.com`

---

## استيراد بيانات موجودة (اختياري)

إذا كنت تريد ترحيل البيانات من قاعدة البيانات المحلية:

```bash
# على جهازك المحلي – تصدير البيانات
python manage.py dumpdata core --indent 2 > data_backup.json

# ارفع data_backup.json إلى PythonAnywhere ثم:
workon khulafaa-env
cd ~/khulafaa_project
python manage.py loaddata data_backup.json
```

---

## ملاحظات مهمة
- **لا ترفع ملف `.env` أو `db.sqlite3`** إلى Git (موجودان في `.gitignore`)
- **لا ترفع `venv/`** إلى PythonAnywhere – استخدم البيئة الافتراضية المنشأة هناك
- على الحسابات المجانية: لا يوجد HTTPS مخصص، لكن `YOUR_USERNAME.pythonanywhere.com` يأتي مع HTTPS تلقائياً
