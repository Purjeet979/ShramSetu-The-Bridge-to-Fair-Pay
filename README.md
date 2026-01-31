# Daily Wage Worker Fair Payment Verification System

**A Desktop-based Wage Protection System to prevent exploitation and ensure transparent payments.**

## 📌 Project Overview
This project addresses the critical issue of wage exploitation in the unorganized sector (construction, factories). By replacing verbal agreements with a **digital, non-deniable record system**, it ensures daily wage workers receive the exact amount they are owed.

Unlike standard payroll apps, this system focuses on **verification and proof**. It records daily hours, automatically applies wage rules (OOP logic), and generates a **digital payment receipt** that acts as proof of work.

## 🚀 Key Features

### 1. 🛡️ Non-Deniable Work Entry
- Records Worker ID, Date, and Hours Worked.
- Once entered, data cannot be manipulated without Admin logs.
- Eliminates "I didn't ask you to work today" excuses.

### 2. 🧮 Auto-Wage Calculation (OOP Based)
- **Base Logic:** `Hours × Hourly Rate`
- **Overtime Logic:** Automatically applies 1.5x rate for hours > 8.
- Removes manual calculation errors or intentional underpayment.

### 3. 🧾 Instant Payment Receipt
- Generates a text/PDF receipt upon payment.
- Includes Date, Amount, Mode (Cash/UPI), and Transaction ID.
- Provides workers with physical/digital proof of income.

### 4. 📊 Compliance Dashboard
- Tracks pending payments.
- Visualizes "Fairness Score" (Paid vs. Pending wages).

## 🛠️ Technology Stack
- **Language:** Python 3.10+
- **GUI Framework:** Tkinter / CustomTkinter (for Modern UI)
- **Database:** MySQL (Relational Data Management)
- **Database Connector:** `mysql-connector-python`
- **Reporting:** Python File Handling / ReportLab

## ⚙️ Installation & Setup

### Prerequisites
1. Python installed (v3.x)
2. MySQL Server installed (e.g., XAMPP or MySQL Workbench)
3. PyCharm IDE (Recommended)

### Step 1: Install Dependencies
Open your terminal in PyCharm and run:
```bash
pip install mysql-connector-python customtkinter matplotlib
