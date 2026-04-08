# Shram Setu 🌉 (The Bridge to Fair Pay)

**Empowering unorganized labor through digital transparency and secure wage verification.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-1.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

**Shram Setu** is a dedicated web platform designed to eliminate wage exploitation in the unorganized sector. By digitizing work records and automating wage calculations, it ensures that every worker is paid fairly and transparently.

> [!NOTE]
> This project has evolved from a desktop utility into a full-scale **Web Application**, featuring **Mobile-First Design**, **Multi-Language Support**, and **Secure Authentication**.

---

## ✨ Core Features

### 🛡️ Non-Deniable Digital Logs
- Securely records Worker ID, Date, and Hours worked.
- Persistent digital trail that prevents "verbal agreement" disputes.

### 🧮 Intelligent Wage Engine (OOP Based)
- Automated calculations based on worker skill levels.
- **Unskilled:** 1.5x Overtime for hours exceeding 8.
- **Skilled:** 2.0x Overtime for hours exceeding 8.

### 🌍 Accessibility & Multi-Language
- **Bilingual Interface:** Toggle between **English** and **Hindi** for better accessibility.
- **Responsive UI:** Seamless experience on Mobile, Tablet, and Desktop.

### 🔐 Enterprise-Grade Security
- **JWT Authentication:** Stateless, secure token-based logins.
- **Google OAuth:** Integrated login for Administrators and Supervisors.
- **Role-Based Access (RBAC):** Strict separation of Admin, Supervisor, and Worker functionalities.

### 📸 Proof of Work
- Mandatory photo uploads for overtime (>8 hours) to ensure verification.
- GPS location tracking for on-site verification.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python (Flask), JWT, OAuth2 |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Bootstrap 5, Jinja2 |
| **Database** | PostgreSQL (Supabase) |
| **Utilities** | Pandas (Reports), Fast2SMS (OTP), Canvas-Confetti (UX) |

---

## 📂 Project Structure

```text
WageVerificationSystem/
├── static/              # Assets (Images, Uploads, CSS)
├── templates/           # HTML Layouts & Views
├── app.py               # Core Flask Application & Routes
├── database.py          # Schema Definition & Seed Data
├── logic.py             # Business Logic & OOP Models
├── translations.py      # i18n support (EN/HI)
└── .env.example         # Environment template
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Purjeet979/ShramSetu-The-Bridge-to-Fair-Pay.git
cd ShramSetu-The-Bridge-to-Fair-Pay
```

### 2. Environment Configuration
Create a `.env` file in the root directory and add the following:
```env
# Database (PostgreSQL/Supabase)
DATABASE_URL=your_postgresql_connection_string

# App Secrets
APP_SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key

# Integrations
GOOGLE_CLIENT_ID=your_google_id
GOOGLE_CLIENT_SECRET=your_google_secret
FAST2SMS_API_KEY=your_sms_key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Ensure you have `flask`, `flask-jwt-extended`, `authlib`, `psycopg2-binary`, `requests`, and `pandas` installed.)*

### 4. Initialize Database
```bash
python database.py
```

### 5. Run the Application
```bash
python app.py
```

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---



*Built with ❤️ for the hardworking hands of India.*
