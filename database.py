import mysql.connector

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "Purjeet@342",
    'database': "daily_wage_db"
}


def get_connection():
    """Connects to the specific database and returns the connection object."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Connection Error: {err}")
        return None


def setup_tables():
    """Creates the necessary tables if they don't exist."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # 1. Create Workers Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            worker_type ENUM('Unskilled', 'Skilled') NOT NULL,
            wage_rate DECIMAL(10, 2) NOT NULL,
            phone VARCHAR(15)
        )
        """)

        # 2. Create Work Entries Table (The "No Denial" Record)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_entries (
            entry_id INT AUTO_INCREMENT PRIMARY KEY,
            worker_id INT,
            work_date DATE NOT NULL,
            hours_worked DECIMAL(4, 1) NOT NULL,
            wage_calculated DECIMAL(10, 2),
            status ENUM('Pending', 'Paid') DEFAULT 'Pending',
            FOREIGN KEY (worker_id) REFERENCES workers(worker_id)
        )
        """)

        # 3. Create Payments Table (The "Proof")
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

        print("✅ SUCCESS: All tables (Workers, Entries, Payments) are ready!")
        conn.close()


if __name__ == "__main__":
    setup_tables()