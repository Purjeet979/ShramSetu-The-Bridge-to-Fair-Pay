from flask import Flask, render_template, request, redirect, url_for, flash
import database
import logic

app = Flask(__name__)
app.secret_key = "shram_setu_secret_key"  # Needed for flash messages


# 1. HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')


# 2. ADD WORKER PAGE
@app.route('/add_worker', methods=['GET', 'POST'])
def add_worker():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        worker_type = request.form['worker_type']

        try:
            rate = float(request.form['rate'])

            # Polymorphism: Create object based on type
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


# 3. RECORD WORK PAGE
@app.route('/record_work', methods=['GET', 'POST'])
def record_work():
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

    # GET Request: Fetch workers for dropdown
    conn = database.get_connection()
    workers = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM workers")
        workers = cursor.fetchall()
        conn.close()

    return render_template('record_work.html', workers=workers)


# 4. PAYMENTS PAGE
@app.route('/payments')
def payments():
    # Use existing logic helper
    pending_data = logic.get_pending_wages()
    return render_template('payments.html', payments=pending_data)


if __name__ == '__main__':
    database.setup_tables()  # Ensure DB tables exist
    app.run(debug=True)