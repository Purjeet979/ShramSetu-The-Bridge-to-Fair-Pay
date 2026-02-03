import database

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
            conn.close()
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
def add_work_entry(worker_id, hours_worked):
    conn = database.get_connection()
    if not conn: return False

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workers WHERE worker_id = %s", (worker_id,))
    data = cursor.fetchone()

    if data:
        # Create Object based on Type
        if data['worker_type'] == "Skilled":
            worker = SkilledWorker(data['name'], float(data['wage_rate']))
        else:
            worker = UnskilledWorker(data['name'], float(data['wage_rate']))

        wage = worker.calculate_wage(float(hours_worked))

        # Save Entry
        sql = "INSERT INTO work_entries (worker_id, work_date, hours_worked, wage_calculated, status) VALUES (%s, CURDATE(), %s, %s, 'Pending')"
        cursor.execute(sql, (worker_id, hours_worked, wage))
        conn.commit()
        conn.close()
        return True
    return False

def get_pending_wages():
    conn = database.get_connection()
    result = []
    if conn:
        cursor = conn.cursor()
        sql = "SELECT w.name, e.entry_id, e.work_date, e.wage_calculated FROM work_entries e JOIN workers w ON e.worker_id = w.worker_id WHERE e.status = 'Pending'"
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
    return result