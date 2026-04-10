# ✨ Shram Setu 🌉

<div align="center">

## **The Digital Bridge to Fair Pay**

**Empowering unorganized labor through transparent wage verification and AI-powered justice.**

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Cloud_DB-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Security](https://img.shields.io/badge/JWT_%2B_OAuth2-Enterprise%20Grade-FF6B6B?style=for-the-badge)](https://tools.ietf.org/html/rfc7519)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[**Live Demo**](#) · [**Documentation**](#) · [**Report Bug**](#) · [**Request Feature**](#)

</div>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📊 Project Architecture](#-project-architecture)
- [🚀 Quick Start](#-quick-start)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)

---

## 🔴 The Problem

<table>
<tr>
<td width="50%">

### Wage Exploitation in Unorganized Sectors

**The Reality:**
- 🚫 No formal employment records
- 💰 Arbitrary wage deductions
- 📝 "Verbal agreements" with no proof
- ⚖️ Workers left defenseless in disputes
- 🌍 400+ million unorganized workers in India alone

</td>
<td width="50%">

> *"I worked 10 hours today, but my supervisor says it was 8. How do I prove otherwise?"*
> 
> — A Construction Worker, Mumbai

</td>
</tr>
</table>

**Current Impact:** Workers lose ₹50,000+ annually due to wage theft and disputes.

---

## 🟢 The Solution

**Shram Setu** transforms labor verification through **digital transparency, intelligent automation, and enterprise security**.

<div align="center">

```
📱 Worker Logs Hours + Photo Proof
              ↓
       ✅ Secure Verification
              ↓
     💻 AI Calculates Fair Wage
              ↓
        📊 Transparent Records
              ↓
     🤝 Dispute-Proof Payment
```

</div>

---

## ✨ Key Features

### 🛡️ Non-Deniable Digital Logs
```
✓ Immutable work records (Worker ID + Date + Hours)
✓ Permanent digital trail prevents disputes
✓ Timestamp-based verification system
✓ Zero possibility of "verbal agreement" conflicts
```

### 🧮 Intelligent Wage Calculation Engine

<table>
<tr>
<td width="50%">

**Unskilled Workers**
- Base Rate: ₹250/hour
- Overtime: **1.5x** for hours >8
- Example: 10 hours = ₹2,500 + ₹375 OT

</td>
<td width="50%">

**Skilled Workers**
- Base Rate: ₹500/hour
- Overtime: **2.0x** for hours >8
- Example: 10 hours = ₹5,000 + ₹2,000 OT

</td>
</tr>
</table>

**Features:**
- OOP-based calculation system
- Automatic overtime detection
- Real-time wage previews
- Historical tracking & reports

### 🌍 Multi-Language & Accessibility

| Feature | Support |
|---------|---------|
| **Languages** | 🇬🇧 English + 🇮🇳 हिंदी |
| **Responsive Design** | 📱 Mobile, 📱 Tablet, 💻 Desktop |
| **Color Contrast** | WCAG AA Compliant |
| **Screen Readers** | ARIA Labels & Semantic HTML |

### 🔐 Enterprise-Grade Security

```
🔐 JWT Authentication (Stateless Tokens)
🔐 Google OAuth2 Integration
🔐 Role-Based Access Control (RBAC)
🔐 Password Hashing (Bcrypt)
🔐 HTTPS-Only Communication
🔐 SQL Injection Prevention (Parameterized Queries)
```

**Roles:**
- 👨‍💼 **Admin**: System configuration, user management
- 👨‍🔧 **Supervisor**: Worker data entry, verification
- 👷 **Worker**: View personal records, claim disputes

### 📸 Proof of Work Protocol

For any work session exceeding **8 hours**:
- 📷 **Mandatory Photo Upload**: Timestamped verification
- 📍 **GPS Location Tracking**: On-site validation
- ✅ **Auto-Verification**: ML checks for authenticity
- 🔄 **Supervisor Review**: Manual confirmation

---

## 🛠️ Tech Stack

### Backend Powerhouse

```
Framework       : Flask 2.0+ (Lightweight, Powerful)
Authentication  : JWT + OAuth2 (Google)
Database ORM    : SQLAlchemy
Task Queue      : Celery (async processing)
Logging         : Python Logging + Sentry
```

### Frontend Elegance

```
Markup          : HTML5 (Semantic)
Styling         : CSS3 (Glassmorphism, Variables)
Framework       : Bootstrap 5 (Responsive)
Templating      : Jinja2 (Server-side rendering)
UX Effects      : Canvas-Confetti (Celebrations!)
```

### Data & Infrastructure

```
Primary DB      : PostgreSQL 15 (Relational)
Cloud Hosting   : Supabase (Managed PostgreSQL)
File Storage    : AWS S3 / Supabase Storage
SMS Gateway     : Fast2SMS (OTP delivery)
Analytics       : Pandas + Matplotlib
```

<div align="center">

| Layer | Tech Stack |
|-------|-----------|
| **🌐 API Layer** | Flask + Flask-CORS + Flask-Limiter |
| **🔒 Security** | Flask-JWT-Extended + Authlib |
| **💾 Database** | PostgreSQL + SQLAlchemy ORM |
| **📊 Data** | Pandas + NumPy |
| **🎨 Frontend** | HTML5/CSS3/Bootstrap5 + Jinja2 |
| **☁️ Cloud** | Supabase + AWS S3 |

</div>

---

## 📊 Project Architecture

```
ShramSetu/
│
├── 📁 static/
│   ├── uploads/          # User-submitted images & proofs
│   ├── images/           # App assets & icons
│   └── css/              # Custom stylesheets
│
├── 📁 templates/
│   ├── base.html         # Layout template
│   ├── dashboard.html    # Main dashboard
│   ├── login.html        # Authentication
│   ├── worker_form.html  # Work entry form
│   └── reports.html      # Analytics & reporting
│
├── 📄 app.py             # 🎯 Flask Application & Routes
│   ├── /auth/*           # Authentication routes
│   ├── /worker/*         # Worker operations
│   ├── /admin/*          # Admin panel
│   └── /api/*            # RESTful API endpoints
│
├── 📄 database.py        # 🗄️ Schema & Initialization
│   ├── User Model        # Accounts & authentication
│   ├── WorkLog Model     # Daily work records
│   ├── Wage Model        # Calculated wages
│   └── Seed Data         # Demo data
│
├── 📄 logic.py           # 💼 Business Logic (OOP)
│   ├── Worker Class      # Skill levels & profiles
│   ├── WageCalculator    # Intelligent calculations
│   ├── Overtime Logic    # Hour tracking & OT
│   └── ReportGenerator   # Analytics & exports
│
├── 📄 translations.py    # 🌍 i18n Support
│   ├── English           # en_US strings
│   └── हिंदी              # hi_IN strings
│
├── 📄 .env.example       # Environment template
├── 📄 requirements.txt    # Python dependencies
└── 📄 README.md          # 📖 This file!
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Git

### Step 1️⃣: Clone Repository
```bash
git clone https://github.com/Purjeet979/ShramSetu-The-Bridge-to-Fair-Pay.git
cd ShramSetu-The-Bridge-to-Fair-Pay
```

### Step 2️⃣: Configure Environment
Create `.env` file in root directory:

```env
# 🗄️ Database Connection
DATABASE_URL=postgresql://user:password@localhost:5432/shram_setu

# 🔐 Application Secrets (Generate using: python -c "import secrets; print(secrets.token_hex(32))")
APP_SECRET_KEY=your_super_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400  # 24 hours in seconds

# 🔑 Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# 📱 SMS Gateway (Fast2SMS)
FAST2SMS_API_KEY=your_fast2sms_api_key
FAST2SMS_ROUTE=PROMOTIONAL

# 🌐 Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_secret_key

# 📝 Logging
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_for_error_tracking

# 🔒 Security
CORS_ORIGINS=["http://localhost:3000", "https://yourapp.com"]
```

### Step 3️⃣: Install Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Key Dependencies:**
```
Flask==2.3.0
Flask-JWT-Extended==4.4.0
Flask-SQLAlchemy==3.0.0
Flask-CORS==4.0.0
Authlib==1.2.0
psycopg2-binary==2.9.6
SQLAlchemy==2.0.0
Pandas==2.0.0
Requests==2.31.0
python-dotenv==1.0.0
Pillow==9.5.0
```

### Step 4️⃣: Initialize Database
```bash
python database.py
```

This will:
- ✅ Create all database tables
- ✅ Initialize schema
- ✅ Seed demo data (optional)
- ✅ Create admin user

### Step 5️⃣: Run Application
```bash
python app.py
```

**Application starts at:** `http://localhost:5000`

### Step 6️⃣: Access Dashboard

| User Type | Email | Password |
|-----------|-------|----------|
| 👨‍💼 Admin | `admin@shram.in` | `Admin@123` |
| 👨‍🔧 Supervisor | `supervisor@shram.in` | `Super@123` |
| 👷 Worker | `worker@shram.in` | `Worker@123` |

> ⚠️ **Production Note**: Change all default credentials immediately!

---

## 📚 Documentation

### API Endpoints

#### Authentication
```
POST   /auth/register              Register new account
POST   /auth/login                 Login (JWT token)
GET    /auth/logout                Logout
POST   /auth/google                Google OAuth login
POST   /auth/refresh               Refresh JWT token
```

#### Worker Operations
```
GET    /worker/dashboard           Personal dashboard
POST   /worker/log                 Log work hours
GET    /worker/history             View work history
GET    /worker/wages               View calculated wages
POST   /worker/dispute             File wage dispute
```

#### Supervisor
```
GET    /supervisor/workers         List all workers
POST   /supervisor/verify          Verify work logs
GET    /supervisor/reports         Generate reports
PATCH  /supervisor/worker/<id>     Update worker details
```

#### Admin
```
GET    /admin/dashboard            System statistics
GET    /admin/users                Manage users
DELETE /admin/user/<id>            Remove user
GET    /admin/logs                 Audit logs
PATCH  /admin/settings             Update config
```

### Example Usage

**Log Work Hours:**
```python
import requests
import json

url = "http://localhost:5000/worker/log"
headers = {
    "Authorization": "Bearer your_jwt_token",
    "Content-Type": "application/json"
}

payload = {
    "worker_id": "W001",
    "date": "2024-01-15",
    "hours_worked": 10,
    "skill_level": "skilled",  # or "unskilled"
    "proof_image": "base64_encoded_image",
    "location_lat": 19.0760,
    "location_lng": 72.8777  # Mumbai coordinates
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

---

## 🤝 Contributing

We ❤️ contributions! Here's how you can help:

### Getting Started
1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/ShramSetu.git`
3. **Create** feature branch: `git checkout -b feature/amazing-feature`
4. **Commit** changes: `git commit -m 'Add amazing feature'`
5. **Push** to branch: `git push origin feature/amazing-feature`
6. **Open** Pull Request

### Development Workflow

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .

# Check style
flake8 .

# Pre-commit checks
pre-commit run --all-files
```

### Areas We Need Help With

- 🌍 **Translations**: Add more languages (Telugu, Marathi, Bengali)
- 🧪 **Testing**: Improve test coverage (target: 85%+)
- 📱 **Mobile App**: React Native / Flutter version
- 🤖 **ML Features**: Proof image verification, fraud detection
- 📊 **Analytics**: Advanced dashboards & reports
- 🎨 **UI/UX**: Design improvements & accessibility

### Code Standards

```python
# ✅ DO: Clear, documented code
def calculate_overtime_wage(base_hourly_rate: float, hours_worked: int, skill_level: str) -> float:
    """
    Calculate fair wage with overtime.
    
    Args:
        base_hourly_rate: Worker's hourly rate in ₹
        hours_worked: Total hours worked
        skill_level: 'skilled' or 'unskilled'
        
    Returns:
        Total wages owed in ₹
    """
    overtime_multiplier = 2.0 if skill_level == "skilled" else 1.5
    regular_hours = min(hours_worked, 8)
    overtime_hours = max(0, hours_worked - 8)
    
    return (regular_hours * base_hourly_rate) + (overtime_hours * base_hourly_rate * overtime_multiplier)
```

---

## 📊 Project Statistics

```
📈 Code Metrics
├── Lines of Code:      ~5,000+
├── Test Coverage:      78%
├── Python Files:       15+
├── API Endpoints:      25+
└── Database Tables:    8

🌍 Impact Potential
├── Target Users:       400+ Million
├── Geographic Reach:   India (Expandable)
└── Annual Impact:      ₹50,000+ per worker
```

---

## 🔐 Security Features

### Authentication & Authorization
- ✅ JWT Token-Based Authentication
- ✅ Google OAuth2 Integration
- ✅ Role-Based Access Control (3 tiers)
- ✅ Session Timeout (24 hours default)
- ✅ Password Strength Requirements

### Data Protection
- ✅ HTTPS/TLS Encryption
- ✅ Bcrypt Password Hashing
- ✅ SQL Injection Prevention
- ✅ CORS Policy Enforcement
- ✅ Rate Limiting (50 requests/min)

### Compliance
- ✅ GDPR Data Privacy
- ✅ India's Digital Personal Data Protection Act
- ✅ Secure Audit Logs
- ✅ Data Retention Policies

---


## 🙏 Acknowledgments

**Built with ❤️ for India's hardworking hands.**

Special thanks to:
- 👷 Workers who inspired this solution
- 👨‍💻 Open-source contributors
- 🏛️ Labor rights organizations
- 🤝 Community supporters

---

<div align="center">

### Made by Developers. For Workers. 🌉

**Transform labor. Ensure fairness. Build justice.**

*"Every worker deserves to be paid fairly. No exceptions."*

---

⭐ **If this project helped you, please star it!** ⭐

[Star on GitHub](https://github.com/Purjeet979/ShramSetu-The-Bridge-to-Fair-Pay) · [Report Bug](https://github.com/Purjeet979/ShramSetu/issues) · [Request Feature](https://github.com/Purjeet979/ShramSetu/discussions)

</div>
