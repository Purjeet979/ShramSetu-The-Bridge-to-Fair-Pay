from flask import Flask, render_template, request, redirect, url_for, flash
import database
import logic
import random

from flask import session
from functools import wraps

app = Flask(__name__)
app.secret_key = "shram_setu_secret_key"  # Needed for flash messages

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        conn = database.get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE identifier = %s", (identifier,))
            user = cursor.fetchone()
            conn.close()

            if user and user['password_hash'] == password:
                session['user_id'] = user['user_id']
                session['user_role'] = user['role']
                session['user_name'] = user['name']
                # NEW: Save identifier so we can look up worker details later
                session['identifier'] = user['identifier']

                flash(f"Welcome {user['name']} ({user['role']})!", "success")
                return redirect(url_for('index'))
            else:
                flash("Invalid credentials!", "error")

    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/worker_login', methods=['GET', 'POST'])
def worker_login():
    if request.method == 'POST':
        phone = request.form['phone']

        # 1. Check if worker exists in database
        conn = database.get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM workers WHERE phone = %s", (phone,))
            worker = cursor.fetchone()
            conn.close()

            if worker:
                # 2. Generate 4-digit OTP
                otp = random.randint(1000, 9999)

                # 3. Save OTP and Phone in session temporarily
                session['temp_otp'] = str(otp)
                session['temp_phone'] = phone

                # 4. Print in console (Development ke liye easy testing)
                print(f"🔔 [DEBUG] OTP for {phone} is: {otp}")

                # 5. Send Real SMS
                logic.send_real_otp(phone, otp)

                flash("OTP sent successfully to your phone!", "success")
                return redirect(url_for('verify_otp'))
            else:
                flash("Phone number not found. Ask Admin to register you.", "error")

    return render_template('worker_login.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    # Agar phone number session mein nahi hai, toh wapas bhej do
    if 'temp_phone' not in session:
        return redirect(url_for('worker_login'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        saved_otp = session.get('temp_otp')

        if entered_otp == saved_otp:
            phone = session.get('temp_phone')

            # Fetch worker details for login session
            conn = database.get_connection()
            if conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM workers WHERE phone = %s", (phone,))
                worker = cursor.fetchone()
                conn.close()

                # Set official session variables
                session.clear()  # Clear temp stuff
                session['user_id'] = worker['worker_id']
                session['user_role'] = 'Worker'
                session['user_name'] = worker['name']
                session['identifier'] = worker['phone']

                flash(f"Login Successful! Welcome {worker['name']}.", "success")
                return redirect(url_for('index'))
        else:
            flash("Invalid OTP. Please try again.", "error")

    return render_template('verify_otp.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/')
@login_required
def index():

    if session.get('user_role') == 'Worker':
        # Fetch data specifically for this worker
        identifier = session.get('identifier')
        stats, entries = logic.get_worker_stats(identifier)
        return render_template('worker_dashboard.html', stats=stats, entries=entries)

    stats = logic.get_dashboard_stats()
    chart_data = logic.get_chart_data()
    comp_data = logic.get_composition_data()
    return render_template('index.html',
                           stats=stats,
                           chart_data=chart_data,
                           comp_data=comp_data)


@app.route('/admin/approve_logs')
@login_required
def approve_logs():
    if session.get('user_role') != 'Admin':
        flash("Unauthorized Access!", "danger")
        return redirect(url_for('index'))

    conn = database.get_connection()
    logs = []
    if conn:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT e.entry_id, w.name as worker_name, w.worker_type, e.work_date, 
                   e.hours_worked, e.wage_calculated 
            FROM work_entries e
            JOIN workers w ON e.worker_id = w.worker_id
            WHERE e.approval_status = 'Pending'
        """
        cursor.execute(query)
        logs = cursor.fetchall()
        conn.close()
    return render_template('approve_logs.html', logs=logs)


@app.route('/admin/verify_entry/<int:entry_id>', methods=['POST'])
@login_required
def verify_entry(entry_id):
    if session.get('user_role') != 'Admin':
        return "Unauthorized", 403

    action = request.form.get('action')  # 'Approved' ya 'Rejected'
    remark = request.form.get('remark')


    admin_obj = logic.Admin(session['user_name'], session['user_id'])
    success = admin_obj.update_entry_status(entry_id, action, remark)

    if success:
        flash(f"Entry #{entry_id} has been {action}.", "success")
    else:
        flash("Error updating entry.", "danger")

    return redirect(url_for('approve_logs'))


@app.route('/add_supervisor', methods=['GET', 'POST'])
@login_required
def add_supervisor():
    # RBAC: Sirf Admin hi Supervisor add kar sakta hai
    if session.get('user_role') != 'Admin':
        flash("🚫 Access Denied: Only Admins can add Supervisors.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        success, message = logic.add_supervisor_to_db(name, username, password)

        if success:
            flash(f"✅ Success: Supervisor {name} created!", "success")
            return redirect(url_for('add_supervisor'))
        else:
            flash(f"❌ Error: {message}", "error")

    return render_template('add_supervisor.html')


# 2. ADD WORKER PAGE
@app.route('/add_worker', methods=['GET', 'POST'])
@login_required
def add_worker():
    # RBAC Check: Only Admin can register workers
    if session.get('user_role') != 'Admin':
        flash("🚫 Access Denied: Only Admins can register workers.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        worker_type = request.form['worker_type']
        try:
            rate = float(request.form['rate'])
            if worker_type == "Skilled":
                worker = logic.SkilledWorker(name, rate)
            else:
                worker = logic.UnskilledWorker(name, rate)
            worker.save_to_db(phone)
            flash(f"✅ Success: Worker {name} added!", "success")
            return redirect(url_for('add_worker'))
        except ValueError:
            flash("❌ Error: Rate must be a number.", "error")

    return render_template('add_worker.html')



@app.route('/record_work', methods=['GET', 'POST'])
@login_required
def record_work():
    # RBAC Check: Worker cannot log their own hours
    if session.get('user_role') not in ['Admin', 'Supervisor']:
        flash("🚫 Access Denied: Workers cannot log their own hours.", "danger")
        return redirect(url_for('index'))

    # ... (Baaki code same rahega) ...
    if request.method == 'POST':
        worker_id = request.form['worker_id']
        hours = request.form['hours']
        try:
            success = logic.add_work_entry(worker_id, hours)
            if success:
                flash("✅ Work recorded successfully!", "success")
            else:
                flash("❌ Error: Worker ID not found.", "error")
        except Exception as e:
            flash(f"❌ Error: {str(e)}", "error")
        return redirect(url_for('record_work'))

    # GET Request
    conn = database.get_connection()
    workers = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM workers")
        workers = cursor.fetchall()
        conn.close()
    return render_template('record_work.html', workers=workers)

@app.route('/history')
@login_required
def history():
    user_role = session.get('user_role')
    user_id = session.get('user_id')
    identifier = session.get('identifier')  # Phone or Email

    conn = database.get_connection()
    history_data = []

    if conn:
        cursor = conn.cursor(dictionary=True)

        if user_role == 'Worker':
            query = """
                SELECT e.*, w.name FROM work_entries e 
                JOIN workers w ON e.worker_id = w.worker_id 
                WHERE w.phone = %s 
                ORDER BY e.work_date DESC
            """
            cursor.execute(query, (identifier,))
        else:
            query = """
                SELECT e.*, w.name FROM work_entries e 
                JOIN workers w ON e.worker_id = w.worker_id 
                ORDER BY e.work_date DESC
            """
            cursor.execute(query)

        history_data = cursor.fetchall()
        conn.close()

    return render_template('history.html', history=history_data)

# 4. PAYMENTS PAGE
@app.route('/payments')
@login_required
def payments():
    if session.get('user_role') != 'Admin':
        flash(" Access Denied: Only Admins can release payments.", "danger")
        return redirect(url_for('index'))

    pending_data = logic.get_pending_wages()
    return render_template('payments.html', payments=pending_data)

@app.route('/my_status')
@login_required
def my_status():
    return redirect(url_for('index'))

if __name__ == '__main__':
    database.setup_tables()
    app.run(debug=True)