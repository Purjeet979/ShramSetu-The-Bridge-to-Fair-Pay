import mysql.connector

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "Purjeet@342",
    'database': "daily_wage_db"
}


def get_connection():

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Connection Error: {err}")
        return None


def setup_tables():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # 1. New Users Table (Hierarchy: Admin, Supervisor, Worker handle karne ke liye)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            identifier VARCHAR(100) UNIQUE NOT NULL, -- Email (Admin/Sup) ya Phone (Worker)
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

        # 3. Work Entries Table (Updated with Approval Logic and Remarks)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_entries (
            entry_id INT AUTO_INCREMENT PRIMARY KEY,
            worker_id INT,
            work_date DATE NOT NULL,
            hours_worked DECIMAL(4, 1) NOT NULL,
            wage_calculated DECIMAL(10, 2),
            status ENUM('Pending', 'Paid') DEFAULT 'Pending',
            approval_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
            admin_remark TEXT, -- Admin rejection ka reason yahan likhega
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
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

        print("✅ SUCCESS: All tables (Users, Workers, Entries, Payments) are updated and ready!")
        conn.close()

if __name__ == "__main__":
    setup_tables()