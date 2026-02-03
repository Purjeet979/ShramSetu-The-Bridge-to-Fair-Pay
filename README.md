# Shram Setu (The Bridge to Fair Pay) 🌉

**A Web-based Wage Protection System to prevent exploitation and ensure transparent payments for daily wage workers.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Database](https://img.shields.io/badge/Database-MySQL-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📌 Project Overview
**Shram Setu** addresses the critical issue of wage exploitation in the unorganized sector (construction, factories). By replacing verbal agreements with a **digital, non-deniable record system**, it ensures daily wage workers receive the exact amount they are owed.

Moved from a desktop-only application to a **Web Application**, this system is now accessible via any device (Mobile/Laptop), focusing on **verification, proof, and accessibility**.

## 🚀 Key Features

### 1. 🛡️ Non-Deniable Work Entry
- Records Worker ID, Date, and Hours Worked securely in a MySQL database.
- Once entered, data serves as a digital log that cannot be easily manipulated.
- Eliminates "I didn't ask you to work today" excuses.

### 2. 🧮 Auto-Wage Calculation (OOP Based)
- **Base Logic:** `Hours × Hourly Rate`
- **Overtime Logic:** - **Unskilled:** 1.5x rate for hours > 8.
  - **Skilled:** 2.0x rate for hours > 8.
- Removes manual calculation errors or intentional underpayment.

### 3. 🌐 Web-Based Accessibility
- Built with **Flask** and **Bootstrap 5**.
- Responsive UI: Works on smartphones and desktops.
- Simple dashboard for quick navigation.

### 4. 📊 Compliance & Transparency
- Tracks pending payments in real-time.
- Visual "Status" indicators (Pending/Paid) for every work entry.

## 🛠️ Technology Stack
- **Backend:** Python 3.10+, Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5 (Jinja2 Templates)
- **Database:** MySQL
- **Database Connector:** `mysql-connector-python`

## 📂 Project Structure
```text
ShramSetu-Web/
├── templates/           # HTML Files (Frontend)
│   ├── base.html        # Master Layout
│   ├── index.html       # Dashboard
│   ├── add_worker.html  # Registration Form
│   ├── record_work.html # Daily Entry Form
│   └── payments.html    # Pending Wages Table
├── app.py               # Main Flask Application
├── database.py          # Database Connection & Setup
├── logic.py             # OOP Business Logic (Calculations)
└── README.md            # Project Documentation
```
## ⚙️ Installation & Setup

### Prerequisites
* Python installed (v3.x)
* MySQL Server installed (running on localhost)
* Git installed

### Step 1: Clone the Repository
```bash
git clone [https://github.com/Purjeet979/ShramSetu-The-Bridge-to-Fair-Pay.git](https://github.com/Purjeet979/ShramSetu-The-Bridge-to-Fair-Pay.git)
cd ShramSetu-The-Bridge-to-Fair-Pay
```
### Step 2: Install Dependencies
* Create a virtual environment (optional but recommended) and install required libraries:
```bash
pip install flask mysql-connector-python
```
### Step 3: Configure Database
* Open database.py. Update the DB_CONFIG dictionary with your MySQL credentials:
```bash
DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "YOUR_MYSQL_PASSWORD",  # <--- Update this!
    'database': "daily_wage_db"
}
```
### Step 4: Run the Application
```bash
python app.py
```
