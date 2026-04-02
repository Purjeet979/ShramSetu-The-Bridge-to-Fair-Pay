import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'database': os.getenv("DB_NAME", "daily_wage_db")
}


def get_connection(include_db=True):
    """
    Establishes a connection to MySQL.
    If include_db is True, it connects to the specific database 'daily_wage_db'.
    If include_db is False, it connects to the MySQL server only (used for DB creation).
    """
    try:
        config = DB_CONFIG.copy()
        if not include_db:
            config.pop('database', None)

        conn = mysql.connector.connect(**config)

        # Automatically create database if it doesn't exist
        if not include_db:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.close()

        return conn
    except mysql.connector.Error as err:
        print(f"❌ Connection Error: {err}")
        print("💡 TIP: Check your MySQL credentials in DB_CONFIG inside database.py")
        return None


def setup_tables():
    # Step 1: Create Database if it doesn't exist
    conn = get_connection(include_db=False)
    if conn:
        conn.close()

    # Step 2: Create Tables
    conn = get_connection(include_db=True)
    if conn:
        cursor = conn.cursor()

        # 1. Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            identifier VARCHAR(100) UNIQUE NOT NULL, 
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'Supervisor', 'Worker') NOT NULL
        )
        """)

        # 2. Workers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            worker_type ENUM('Unskilled', 'Skilled') NOT NULL,
            wage_rate DECIMAL(10, 2) NOT NULL,
            phone VARCHAR(15) UNIQUE
        )
        """)

        # 3. Work Entries Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_entries (
            entry_id INT AUTO_INCREMENT PRIMARY KEY,
            worker_id INT,
            supervisor_id INT,
            work_date DATE NOT NULL,
            hours_worked DECIMAL(4, 1) NOT NULL,
            wage_calculated DECIMAL(10, 2),
            work_type VARCHAR(100),
            gps_location VARCHAR(100),
            photo_path VARCHAR(255),
            status ENUM('Pending', 'Paid') DEFAULT 'Pending',
            approval_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
            admin_remark TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id),
            FOREIGN KEY (supervisor_id) REFERENCES users(user_id)
        )
        """)

        # 4. Payments Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY,
            worker_id INT,
            amount_paid DECIMAL(10, 2) NOT NULL,
            payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            payment_mode VARCHAR(50),
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
        )
        """)

        # 5. Seed Default Admin User
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            print("👤 Seeding default admin user...")
            cursor.execute("""
                INSERT INTO users (name, identifier, password_hash, role) 
                VALUES ('System Admin', 'admin@example.com', 'admin_secure_123', 'Admin')
            """)
            conn.commit()
            print("✅ Default Admin Created: admin@example.com / admin123")

        print("✅ SUCCESS: All tables are updated and ready!")
        conn.close()

if __name__ == "__main__":
    setup_tables()