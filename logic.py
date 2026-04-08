import database
import psycopg2
from psycopg2 import extras
import os
import requests
import random
import pandas as pd
import math
from database import get_connection
from datetime import datetime, timedelta

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two GPS coordinates using the Haversine formula.
    Returns distance in meters.
    """
    R = 6371000  # Radius of the Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class User:
    def __init__(self, name, identifier, role):
        self.name = name
        self.identifier = identifier  # Email ya Phone
        self.role = role


class Admin(User):
    def __init__(self, name, identifier):
        super().__init__(name, identifier, 'Admin')


    def update_entry_status(self, entry_id, status, remark):
        conn = database.get_connection()
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE work_entries SET approval_status = %s, admin_remark = %s WHERE entry_id = %s"
            cursor.execute(sql, (status, remark, entry_id))
            conn.commit()
            cursor.close()
            database.release_connection(conn)
            return True
        return False


class Supervisor(User):
    def __init__(self, name, identifier):
        super().__init__(name, identifier, 'Supervisor')

# --- BASE CLASS ---
class Worker:
    def __init__(self, name, worker_type, hourly_rate):
        self.name = name
        self.worker_type = worker_type
        self._hourly_rate = hourly_rate

    def calculate_wage(self, hours_worked):
        return hours_worked * self._hourly_rate

    def save_to_db(self, phone=""):
        conn = database.get_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO workers (name, worker_type, wage_rate, phone) VALUES (%s, %s, %s, %s)"
            val = (self.name, self.worker_type, self._hourly_rate, phone)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            database.release_connection(conn)
            print(f"Worker {self.name} saved successfully.")

# --- CHILD CLASSES (OOP) ---
class UnskilledWorker(Worker):
    def __init__(self, name, hourly_rate):
        super().__init__(name, "Unskilled", hourly_rate)

    def calculate_wage(self, hours_worked):
        # 1.5x Overtime Logic
        if hours_worked > 8:
            return (8 * self._hourly_rate) + ((hours_worked - 8) * (self._hourly_rate * 1.5))
        return hours_worked * self._hourly_rate

class SkilledWorker(Worker):
    def __init__(self, name, hourly_rate):
        super().__init__(name, "Skilled", hourly_rate)

    def calculate_wage(self, hours_worked):
        # 2.0x Overtime Logic
        if hours_worked > 8:
            return (8 * self._hourly_rate) + ((hours_worked - 8) * (self._hourly_rate * 2.0))
        return hours_worked * self._hourly_rate

# --- HELPER FUNCTIONS ---
def add_work_entry(worker_id, hours_worked, supervisor_id, work_date=None, work_type=None, gps_location=None, photo_path=None):
    conn = database.get_connection()
    if not conn: return False

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM workers WHERE worker_id = %s", (worker_id,))
    data = cursor.fetchone()

    if data:
        # Create Object based on Type
        if data['worker_type'] == "Skilled":
            worker = SkilledWorker(data['name'], float(data['wage_rate']))
        else:
            worker = UnskilledWorker(data['name'], float(data['wage_rate']))

        wage = worker.calculate_wage(float(hours_worked))
        
        if not work_date:
            work_date = datetime.now().date()

        # Save Entry
        # AUTO-APPROVE if hours <= 8. Admin only approves OT (> 8h).
        approval_status = 'Approved' if float(hours_worked) <= 8 else 'Pending'

        sql = """
            INSERT INTO work_entries 
            (worker_id, supervisor_id, work_date, hours_worked, wage_calculated, work_type, gps_location, photo_path, status, approval_status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s)
        """
        cursor.execute(sql, (worker_id, supervisor_id, work_date, hours_worked, wage, work_type, gps_location, photo_path, approval_status))
        conn.commit()
        cursor.close()
        database.release_connection(conn)
        return True
    return False

def get_all_approved_wages():
    conn = database.get_connection()
    result = []
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = """
                    SELECT w.name, e.entry_id, e.work_date, e.wage_calculated, w.worker_type, e.status
                    FROM work_entries e 
                    JOIN workers w ON e.worker_id = w.worker_id 
                    WHERE e.approval_status = 'Approved'
                    ORDER BY e.work_date DESC
                """
        cursor.execute(sql)
        result = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        database.release_connection(conn)
    return result

def get_dashboard_stats():
    conn = database.get_connection()
    stats = {"total_workers": 0, "pending_wages": 0, "hours_today": 0}
    if conn:
        cursor = conn.cursor()
        # Total Workers
        cursor.execute("SELECT COUNT(*) FROM workers")
        stats["total_workers"] = cursor.fetchone()[0]
        # Total Pending Wages
        cursor.execute("SELECT SUM(wage_calculated) FROM work_entries WHERE status = 'Pending'")
        stats["pending_wages"] = cursor.fetchone()[0] or 0
        # Hours Logged Today
        cursor.execute("SELECT SUM(hours_worked) FROM work_entries WHERE work_date = CURRENT_DATE")
        stats["hours_today"] = cursor.fetchone()[0] or 0
        cursor.close()
        database.release_connection(conn)
    return stats

def get_chart_data():
    conn = database.get_connection()
    data = {"labels": [], "data_points": []}
    if conn:
        cursor = conn.cursor()
        # Pichle 30 dinon ka data fetch karne ke liye INTERVAL badal diya
        cursor.execute("""
            SELECT work_date, SUM(hours_worked) 
            FROM work_entries 
            WHERE work_date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY work_date ORDER BY work_date ASC
        """)
        rows = cursor.fetchall()
        for row in rows:
            data["labels"].append(row[0].strftime("%b %d"))
            data["data_points"].append(float(row[1]))
        cursor.close()
        database.release_connection(conn)
    return data

def get_composition_data():
    conn = database.get_connection()
    data = {"labels": ["Skilled", "Unskilled"], "counts": [0, 0]}
    if conn:
        cursor = conn.cursor()
        # Fetch sum of wages grouped by worker type
        cursor.execute("""
            SELECT w.worker_type, SUM(e.wage_calculated) 
            FROM work_entries e 
            JOIN workers w ON e.worker_id = w.worker_id 
            GROUP BY w.worker_type
        """)
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == "Skilled":
                data["counts"][0] = float(row[1])
            elif row[0] == "Unskilled":
                data["counts"][1] = float(row[1])
        cursor.close()
        database.release_connection(conn)
    return data


def get_worker_stats(identifier):
    """
    Fetches stats specifically for the logged-in worker using their phone number (identifier).
    """
    conn = database.get_connection()
    stats = {"total_pending": 0, "total_paid": 0}
    entries = []

    if conn:
        # 1. Fetch Stats (Using Tuple Cursor for simple SUMs)
        cursor = conn.cursor()

        # Get Worker ID from Phone
        cursor.execute("SELECT worker_id FROM workers WHERE phone = %s", (identifier,))
        worker_row = cursor.fetchone()

        if worker_row:
            worker_id = worker_row[0]

            # Calculate Total Pending
            cursor.execute("SELECT SUM(wage_calculated) FROM work_entries WHERE worker_id = %s AND status = 'Pending'",
                           (worker_id,))
            stats["total_pending"] = cursor.fetchone()[0] or 0

            # Calculate Total Paid
            cursor.execute("SELECT SUM(wage_calculated) FROM work_entries WHERE worker_id = %s AND status = 'Paid'",
                           (worker_id,))
            stats["total_paid"] = cursor.fetchone()[0] or 0

            cursor.close()

            # 2. Fetch Recent Entries
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("""
                SELECT e.*, u.name as supervisor_name 
                FROM work_entries e 
                LEFT JOIN users u ON e.supervisor_id = u.user_id
                WHERE e.worker_id = %s 
                ORDER BY e.work_date DESC LIMIT 10
            """, (worker_id,))
            entries = [dict(row) for row in cursor.fetchall()]
            cursor.close()

        database.release_connection(conn)

    return stats, entries

def add_supervisor_to_db(name, username, password):
    conn = database.get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Note: Abhi hum plain password save kar rahe hain jaise admin ka kiya tha.
            sql = "INSERT INTO users (name, identifier, password_hash, role) VALUES (%s, %s, %s, 'Supervisor')"
            cursor.execute(sql, (name, username, password))
            conn.commit()
            return True, "Supervisor added successfully."
        except psycopg2.IntegrityError:
            # Agar username pehle se exist karta hai
            return False, "This Username/Email is already taken!"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            database.release_connection(conn)
    return False, "Database connection failed."


def send_real_otp(phone_number, otp):
    """
    Fast2SMS API ka use karke real SMS OTP bhejta hai.
    """

    API_KEY = os.getenv("FAST2SMS_API_KEY", "YOUR_FAST2SMS_API_KEY_HERE")

    url = "https://www.fast2sms.com/dev/bulkV2"

    querystring = {
        "authorization": API_KEY,
        "variables_values": str(otp),
        "route": "otp",
        "numbers": phone_number
    }

    headers = {
        'cache-control': "no-cache"
    }

    try:
        if API_KEY == "YOUR_FAST2SMS_API_KEY_HERE":
            print("⚠️ API Key is missing. Skipping real SMS.")
            return True

        response = requests.request("GET", url, headers=headers, params=querystring)
        result = response.json()

        if result.get('return'):
            return True
        else:
            print(f"SMS Error: {result.get('message')}")
            return False
    except Exception as e:
        print(f"Fast2SMS API Error: {e}")
        return False


def apply_penalty_if_needed(wage, work_date):
    """
    Adds a 10% penalty on wages that remain unpaid beyond 37 days
    (30-day due period + 7-day grace period).
    """
    wage = float(wage)
    today = datetime.now().date()
    work_date = datetime.strptime(str(work_date), "%Y-%m-%d").date()

    due_date = work_date + timedelta(days=30)
    penalty_date = due_date + timedelta(days=7)

    if today > penalty_date:
        wage = wage * 1.10

    return round(wage, 2)


def export_payments_to_excel():
    """
    Exports all payment records to an Excel (.xlsx) file.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        p.payment_id,
        w.name AS worker_name,
        p.amount_paid,
        p.payment_mode,
        p.payment_date
    FROM payments p
    JOIN workers w ON p.worker_id = w.worker_id
    """

    cursor.execute(query)
    data = cursor.fetchall()

    columns = [
        "Payment ID",
        "Worker Name",
        "Amount Paid",
        "Payment Mode",
        "Payment Date"
    ]

    df = pd.DataFrame(data, columns=columns)

    file_name = "payments_report.xlsx"
    df.to_excel(file_name, index=False)

    cursor.close()
    database.release_connection(conn)

    return file_name


def make_payment(entry_id, payment_mode):
    """
    Processes a payment for a work entry:
    1. Fetches the entry
    2. Applies late penalty if applicable
    3. Inserts a record into the payments table
    4. Marks the work entry as 'Paid'
    """
    conn = database.get_connection()
    if not conn:
        return False

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Step 1: Fetch entry
    cursor.execute("SELECT * FROM work_entries WHERE entry_id = %s", (entry_id,))
    entry = cursor.fetchone()

    if not entry:
        database.release_connection(conn)
        return False

    # Step 2: Apply penalty if needed
    wage = entry['wage_calculated']
    work_date = entry['work_date']
    final_amount = apply_penalty_if_needed(wage, work_date)
    worker_id = entry['worker_id']

    # Step 3: Insert into payments table
    cursor.execute("""
        INSERT INTO payments (worker_id, amount_paid, payment_mode)
        VALUES (%s, %s, %s)
    """, (worker_id, final_amount, payment_mode))

    # Step 4: Update status to Paid
    cursor.execute("""
        UPDATE work_entries
        SET status = 'Paid'
        WHERE entry_id = %s
    """, (entry_id,))

    conn.commit()
    cursor.close()
    database.release_connection(conn)

    return True