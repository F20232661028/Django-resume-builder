# 🚀 ProResume Builder

![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-4.4.1-purple?logo=bootstrap)

## ✨ Features

- 📝 **Modern Resume Builder**: Create, edit, and print beautiful resumes.
- 👤 **User Authentication**: Email/password & Google OAuth login (with email confirmation).
- 📚 **Extensive Data Collection**: Experience, Education, Skills, Certifications, Projects, and more.
- 🏆 **Certifications & Projects**: Add unlimited certifications and projects with details.
- 🛠️ **Dynamic Formsets**: Add/remove multiple entries for all sections with real-time validation.
- 🔍 **Skill Autocomplete**: Smart suggestions for skills (Select2).
- 🌗 **Dark/Light Mode**: Toggle theme instantly from the navbar.
- 📤 **Export & Share**: Save resume to Google Drive, email as PDF, or print.
- 🔔 **Toasts & Guidance**: Real-time feedback, tooltips, and section instructions.
- 🛡️ **Robust Validation**: Logical, user-friendly validation for all fields.

---

## 🛠️ Quick Start (Windows)

1. **Clone the repository**
2. **Open a terminal in the project root**
3. **Run:**
   ```
   start_project.bat
   ```
   - This will set up a virtual environment, install dependencies, run migrations, collect static files, prompt for a superuser, and start the server.

## 🛠️ Quick Start (PowerShell)

1. **Clone the repository**
2. **Open PowerShell in the project root**
3. **Run:**
   ```
   .\start_project.ps1
   ```

---

## ⚙️ Manual Setup

1. **Create and activate a virtual environment**
2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Run migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Collect static files**
   ```
   python manage.py collectstatic
   ```
5. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```
6. **Start the server**
   ```
   python manage.py runserver
   ```

---

## 🌟 Usage
- Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the app.
- Log in or sign up (Google or email).
- Create a resume with as much detail as you want.
- Add multiple experiences, educations, skills, certifications, and projects.
- Save, print, email, or upload your resume to Google Drive.

---

## 🧩 Tech Stack
- **Django** (backend, ORM, admin)
- **Django Allauth** (authentication, social login)
- **Bootstrap 4** (responsive UI)
- **jQuery & Select2** (dynamic forms, autocomplete)
- **Flatpickr** (date pickers)
- **Google API** (Drive integration)

---

## 📝 License
MIT
