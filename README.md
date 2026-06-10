# 🏫 School ERP System — Complete Setup Guide

Full-featured School Management System built with **Django 4.2** + SQLite.  
Manages Students, Teachers, Attendance, Fees, Exams, Library, Payroll, Transport, Hostel, and more.

---

## 📋 Modules Included

| Module | Features |
|---|---|
| 🎓 **Students** | Admission, Profile, Documents, Promotion, TC/ID Card PDF |
| 👨‍🏫 **Teachers** | Profile, Subjects, Qualifications |
| 📅 **Attendance** | Daily marking, Reports |
| 💰 **Fees** | Collection, Pending/Overdue, PDF Receipt |
| 📝 **Exams** | Schedule, Result Entry, Grade Reports |
| 📚 **Library** | Book Catalog, Issue/Return |
| 💵 **Payroll** | Salary Structure, Monthly Pay, Salary Slip PDF |
| 📢 **Communication** | Notice Board, Internal Messaging, Events |
| 🚌 **Transport** | Routes, Bus Assignment |
| 🏠 **Hostel** | Rooms, Allocation |
| 📊 **Analytics** | Charts — Attendance, Fees, Grades, Gender |
| 📄 **Reports** | PDF Reports for Students, Attendance, Fees |
| ⚙️ **Core** | School Profile, Academic Years, Settings |

---

## ⚡ VS Code Setup (Step by Step)

### Step 1 — Prerequisites Install karo

```
Python 3.10+ install karo from python.org
VS Code install karo from code.visualstudio.com
```

### Step 2 — Project Extract karo

```
ZIP file extract karo kisi folder mein, jaise:
C:\Projects\school_erp\
```

### Step 3 — VS Code mein open karo

```
VS Code open karo
File → Open Folder → school_erp folder select karo
```

### Step 4 — VS Code Extensions Install karo

VS Code mein Ctrl+Shift+X dabaao aur ye install karo:
- **Python** (Microsoft)
- **Django** (Baptiste Darthenay)
- **SQLite Viewer** (Florian Klampfer)
- **Pylance** (Microsoft)

### Step 5 — Virtual Environment banao

VS Code mein Terminal kholo (Ctrl+`) aur run karo:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Agar error aaye:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Step 6 — Dependencies install karo

```powershell
pip install -r requirements.txt
pip install reportlab
```

### Step 7 — Database setup karo

```powershell
python manage.py migrate
```

### Step 8 — Admin user banao

```powershell
python manage.py createsuperuser
```
Username, email, password enter karo.

### Step 9 — Server start karo

```powershell
python manage.py runserver
```

Browser mein kholo: **http://127.0.0.1:8000**

---

## 🔐 Login Details

- URL: http://127.0.0.1:8000/login/
- Username: jo tune createsuperuser mein set kiya
- Admin Panel: http://127.0.0.1:8000/admin/

---

## 📁 Folder Structure

```
school_erp/
├── manage.py
├── requirements.txt
├── school_erp/          ← Main Django settings
│   ├── settings.py
│   └── urls.py
├── core/                ← Login, Dashboard, School Profile
├── student_mgmt/        ← Students, Classes, Promotion
├── teacher_mgmt/        ← Teachers
├── attendance_mgmt/     ← Attendance
├── fees_mgmt/           ← Fee Management
├── exam_mgmt/           ← Examinations
├── library/             ← Library
├── payroll_mgmt/        ← Payroll
├── communication_mgmt/  ← Notices, Messages, Events
├── transport_mgmt/      ← Transport
├── hostel_mgmt/         ← Hostel
├── reports_mgmt/        ← Reports + PDF Generation
├── analytics_mgmt/      ← Charts & Analytics
└── templates/           ← All HTML templates
```

---

## 🆕 New Features Added

- ✅ **Student Promotion** — `/students/promote/`
- ✅ **Transfer Certificate PDF** — Student detail page → TC button
- ✅ **ID Card PDF** — Student detail page → ID Card button
- ✅ **Fee Receipt PDF** — Fee detail page → Download PDF button
- ✅ **Send Message** — Communication → Compose button
- ✅ **Events & Calendar** — Communication → Events
- ✅ **Notice Delete** — Notice board mein remove button

---

## ⚠️ Common Issues & Fix

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'reportlab'` | `pip install reportlab` |
| `EADDRINUSE` / Port already in use | Run: `python manage.py runserver 8001` |
| Static files not loading | `python manage.py collectstatic` |
| Migration errors | `python manage.py migrate --run-syncdb` |
| PowerShell `&&` error | Commands alag alag run karo |

