from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify, make_response, send_from_directory
import database
import logic
import psycopg2
from psycopg2 import extras
import random
import os
from translations import TRANSLATIONS
from functools import wraps
from dotenv import load_dotenv
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    set_access_cookies, unset_jwt_cookies, get_jwt_identity, get_jwt,
    verify_jwt_in_request
)
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
import time

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "shram_setu_secret_key")

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False 
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"

# File Upload Configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

jwt = JWTManager(app)

# OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.context_processor
def inject_user_and_translations():
    user_dict = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            claims = get_jwt()
            user_dict = {
                'name': claims.get('name'),
                'role': claims.get('role'),
                'identifier': identity
            }
    except:
        pass
    
    def get_translation(key):
        lang = session.get('lang', 'en')
        return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
        
    return {
        'current_user': user_dict,
        'os': os,
        '_': get_translation
    }

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            if isinstance(required_role, list):
                if user_role not in required_role:
                    flash(f"🚫 Access Denied: Requires {required_role} role.", "danger")
                    return redirect(url_for('index'))
            else:
                if user_role != required_role:
                    flash(f"🚫 Access Denied: Requires {required_role} role.", "danger")
                    return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_required(f):
    @wraps(f)
    @jwt_required(optional=True)
    def decorated_function(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        conn = database.get_connection()
        if conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM users WHERE identifier = %s", (identifier,))
            user = cursor.fetchone()
            database.release_connection(conn)

            if user and user['password_hash'] == password:
                access_token = create_access_token(
                    identity=user['identifier'],
                    additional_claims={'role': user['role'], 'name': user['name']}
                )
                response = redirect(url_for('index'))
                set_access_cookies(response, access_token)
                flash(f"Welcome {user['name']} ({user['role']})!", "success")
                return response
            else:
                flash("Invalid credentials!", "error")

    return render_template('login.html')

@app.route('/google-login')
def google_login():
    return google.authorize_redirect(url_for('google_auth', _external=True))

@app.route('/google-auth')
def google_auth():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    email = user_info['email']

    conn = database.get_connection()
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE identifier = %s", (email,))
        user = cursor.fetchone()
        database.release_connection(conn)

        if user:
            access_token = create_access_token(
                identity=user['identifier'],
                additional_claims={'role': user['role'], 'name': user['name']}
            )
            response = redirect(url_for('index'))
            set_access_cookies(response, access_token)
            flash(f"Welcome {user['name']} ({user['role']})!", "success")
            return response
        else:
            flash("Unauthorized Google Account. Please use your registered email.", "danger")
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/worker_login', methods=['GET', 'POST'])
def worker_login():
    if request.method == 'POST':
        phone = request.form['phone']

        conn = database.get_connection()
        if conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM workers WHERE phone = %s", (phone,))
            worker = cursor.fetchone()
            database.release_connection(conn)

            if worker:
                otp = random.randint(1000, 9999)
                session['temp_otp'] = str(otp)
                session['temp_phone'] = phone
                print(f"🔔 [DEBUG] OTP for {phone} is: {otp}")
                logic.send_real_otp(phone, otp)
                flash("OTP sent successfully to your phone!", "success")
                return redirect(url_for('verify_otp'))
            else:
                flash("Phone number not found. Ask Admin to register you.", "error")

    return render_template('worker_login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'temp_phone' not in session:
        return redirect(url_for('worker_login'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        saved_otp = session.get('temp_otp')

        if entered_otp == saved_otp:
            phone = session.get('temp_phone')
            conn = database.get_connection()
            if conn:
                cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cursor.execute("SELECT * FROM workers WHERE phone = %s", (phone,))
                worker = cursor.fetchone()
                database.release_connection(conn)

                access_token = create_access_token(
                    identity=worker['phone'],
                    additional_claims={'role': 'Worker', 'name': worker['name']}
                )
                session.clear()
                response = redirect(url_for('index'))
                set_access_cookies(response, access_token)
                flash(f"Login Successful! Welcome {worker['name']}.", "success")
                return response
        else:
            flash("Invalid OTP. Please try again.", "error")

    return render_template('verify_otp.html')

@app.route('/dispute/<int:entry_id>', methods=['POST'])
@role_required('Worker')
def dispute_entry(entry_id):
    reason = request.form.get('reason', '').strip()
    conn = database.get_connection()
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Fetch supervisor_id for rating update
        cursor.execute("SELECT supervisor_id FROM work_entries WHERE entry_id = %s", (entry_id,))
        row = cursor.fetchone()
        supervisor_id = row['supervisor_id'] if row else None

        cursor.execute(
            "UPDATE work_entries SET is_disputed = TRUE, approval_status = 'Pending', dispute_reason = %s WHERE entry_id = %s",
            (reason, entry_id)
        )
        conn.commit()

        # Update supervisor rating
        if supervisor_id:
            logic.update_supervisor_rating(supervisor_id)

        cursor.close()
        database.release_connection(conn)
        flash("Dispute raised successfully. Admin has been notified and payment is on hold.", "success")
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    response = redirect(url_for('login'))
    unset_jwt_cookies(response)
    session.pop('lang', None)
    flash("Successfully logged out.", "success")
    return response

@app.route('/')
@login_required
def index():
    claims = get_jwt()
    user_role = claims.get('role')
    identifier = get_jwt_identity()

    if user_role == 'Worker':
        stats, entries = logic.get_worker_stats(identifier)
        return render_template('worker_dashboard.html', stats=stats, entries=entries)

    stats = logic.get_dashboard_stats()
    chart_data = logic.get_chart_data()
    comp_data = logic.get_composition_data()
    return render_template('index.html', stats=stats, chart_data=chart_data, comp_data=comp_data)

@app.route('/admin/approve_logs')
@role_required('Admin')
def approve_logs():
    conn = database.get_connection()
    logs = []
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
            SELECT e.*, w.name as worker_name, w.worker_type, u.name as supervisor_name 
            FROM work_entries e 
            JOIN workers w ON e.worker_id = w.worker_id 
            LEFT JOIN users u ON e.supervisor_id = u.user_id
            WHERE e.approval_status = 'Pending' AND (e.hours_worked > 8 OR e.is_disputed = TRUE)
            ORDER BY e.work_date DESC
        """
        cursor.execute(query)
        logs = cursor.fetchall()
        database.release_connection(conn)
    return render_template('approve_logs.html', logs=logs)

@app.route('/admin/verify_entry/<int:entry_id>', methods=['POST'])
@role_required('Admin')
def verify_entry(entry_id):
    action = request.form.get('action') 
    remark = request.form.get('remark')
    
    claims = get_jwt()
    admin_obj = logic.Admin(claims.get('name'), get_jwt_identity())
    success = admin_obj.update_entry_status(entry_id, action, remark)

    if success:
        flash(f"Entry #{entry_id} has been {action}.", "success")
    else:
        flash("Error updating entry.", "danger")
    return redirect(url_for('approve_logs'))

@app.route('/add_supervisor', methods=['GET', 'POST'])
@role_required('Admin')
def add_supervisor():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        site_lat = request.form.get('site_lat') or None
        site_lng = request.form.get('site_lng') or None
        if site_lat: site_lat = float(site_lat)
        if site_lng: site_lng = float(site_lng)
        success, message = logic.add_supervisor_to_db(name, username, password, site_lat, site_lng)
        if success:
            flash(f"✅ Success: Supervisor {name} created!", "success")
            return redirect(url_for('add_supervisor'))
        else:
            flash(f"❌ Error: {message}", "error")
    return render_template('add_supervisor.html')

@app.route('/add_worker', methods=['GET', 'POST'])
@role_required(['Admin', 'Supervisor'])
def add_worker():
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
@role_required(['Admin', 'Supervisor'])
def record_work():
    if request.method == 'POST':
        worker_id = request.form['worker_id']
        hours = float(request.form['hours'])
        work_type = request.form.get('work_type', 'General')
        notes = request.form.get('notes', '')
        gps_location = request.form.get('gps_location', '')
        
        # --- Per-Supervisor Geofencing ---
        # Fetch supervisor from DB to get their site coordinates
        conn_geo = database.get_connection()
        site_lat_db = site_lng_db = None
        current_supervisor_id = None
        if conn_geo:
            cur_geo = conn_geo.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur_geo.execute("SELECT user_id, site_lat, site_lng FROM users WHERE identifier = %s", (get_jwt_identity(),))
            sup_row = cur_geo.fetchone()
            if sup_row:
                current_supervisor_id = sup_row['user_id']
                site_lat_db = sup_row['site_lat']
                site_lng_db = sup_row['site_lng']
            cur_geo.close()
            database.release_connection(conn_geo)

        if site_lat_db and site_lng_db:
            if not gps_location:
                flash("❌ Error: GPS location is mandatory to verify you are on site.", "danger")
                return redirect(url_for('record_work'))
            try:
                sup_lat, sup_lng = map(float, gps_location.split(','))
                distance = logic.calculate_distance(sup_lat, sup_lng, float(site_lat_db), float(site_lng_db))
                if distance > 500:
                    flash(f"❌ Geofence Error: You are {int(distance)}m from the work site (Max: 500m).", "danger")
                    return redirect(url_for('record_work'))
            except Exception:
                flash("❌ Error: Invalid GPS coordinates.", "danger")
                return redirect(url_for('record_work'))
        # ----------------------------------

        photo_path = None
        if hours > 8:
            if 'photo' not in request.files or request.files['photo'].filename == '':
                flash("❌ Error: Photo is mandatory for entries > 8 hours.", "danger")
                return redirect(url_for('record_work'))
            file = request.files['photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                # --- Upload to Supabase Storage ---
                supabase_url = os.getenv("SUPABASE_URL")
                supabase_key = os.getenv("SUPABASE_KEY")
                if supabase_url and supabase_key and 'your_supabase' not in supabase_url:
                    try:
                        from supabase import create_client
                        sb = create_client(supabase_url, supabase_key)
                        file_bytes = file.read()
                        sb.storage.from_("overtime-photos").upload(
                            path=filename,
                            file=file_bytes,
                            file_options={"content-type": file.content_type}
                        )
                        photo_path = f"{supabase_url}/storage/v1/object/public/overtime-photos/{filename}"
                    except Exception as e:
                        print(f"Supabase upload error: {e}. Falling back to local storage.")
                        file.seek(0)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        photo_path = f"uploads/{filename}"
                else:
                    # Fallback: local storage
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    photo_path = f"uploads/{filename}"
                # ----------------------------------

        conn = database.get_connection()
        if conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if current_supervisor_id is None:
                cursor.execute("SELECT user_id FROM users WHERE identifier = %s", (get_jwt_identity(),))
                user = cursor.fetchone()
                current_supervisor_id = user['user_id'] if user else None
            cursor.close()
            database.release_connection(conn)

            success = logic.add_work_entry(
                worker_id=worker_id,
                hours_worked=hours,
                supervisor_id=current_supervisor_id,
                work_type=work_type,
                gps_location=gps_location,
                photo_path=photo_path
            )
            if success:
                flash("✅ Work recorded successfully!", "success")
            else:
                flash("❌ Error recording work.", "error")
        return redirect(url_for('record_work'))


    conn = database.get_connection()
    workers = []
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM workers")
        workers = cursor.fetchall()
        database.release_connection(conn)
    
    from datetime import datetime
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('record_work.html', workers=workers, today_date=today_date)

@app.route('/history')
@login_required
def history():
    claims = get_jwt()
    user_role = claims.get('role')
    identifier = get_jwt_identity()

    conn = database.get_connection()
    history_data = []

    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if user_role == 'Worker':
            query = """
                SELECT e.*, w.name as worker_name, u.name as supervisor_name 
                FROM work_entries e 
                JOIN workers w ON e.worker_id = w.worker_id 
                LEFT JOIN users u ON e.supervisor_id = u.user_id
                WHERE w.phone = %s 
                ORDER BY e.work_date DESC
            """
            cursor.execute(query, (identifier,))
        else:
            query = """
                SELECT e.*, w.name as worker_name, u.name as supervisor_name 
                FROM work_entries e 
                JOIN workers w ON e.worker_id = w.worker_id 
                LEFT JOIN users u ON e.supervisor_id = u.user_id
                ORDER BY e.work_date DESC
            """
            cursor.execute(query)

        history_data = cursor.fetchall()
        database.release_connection(conn)

    return render_template('history.html', history=history_data)

@app.route('/payments')
@role_required('Admin')
def payments():
    approved_data = logic.get_all_approved_wages()
    return render_template('payments.html', payments=approved_data)

@app.route('/pay/<int:entry_id>', methods=['POST'])
@role_required('Admin')
def pay(entry_id):
    payment_mode = request.form.get('payment_mode', 'Cash')
    success = logic.make_payment(entry_id, payment_mode)
    if success:
        flash(f"✅ Payment for Entry #{entry_id} processed successfully!", "success")
    else:
        flash(f"❌ Error: Could not process payment for Entry #{entry_id}.", "danger")
    return redirect(url_for('payments'))

@app.route('/export_payments')
@role_required('Admin')
def export_payments():
    file_path = logic.export_payments_to_excel()
    return send_file(file_path, as_attachment=True)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'hi']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/admin/supervisor_ratings')
@role_required('Admin')
def supervisor_ratings():
    conn = database.get_connection()
    supervisors = []
    if conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT user_id, name, identifier, rating, total_disputes, site_lat, site_lng
            FROM users WHERE role = 'Supervisor'
            ORDER BY rating ASC
        """)
        supervisors = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        database.release_connection(conn)
    return render_template('supervisor_ratings.html', supervisors=supervisors)

@app.route('/admin/delete_supervisor/<int:user_id>', methods=['POST'])
@role_required('Admin')
def delete_supervisor(user_id):
    conn = database.get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s AND role = 'Supervisor'", (user_id,))
        conn.commit()
        cursor.close()
        database.release_connection(conn)
        flash("✅ Supervisor removed successfully.", "success")
    else:
        flash("❌ Could not connect to database.", "danger")
    return redirect(url_for('supervisor_ratings'))

if __name__ == '__main__':
    database.setup_tables()
    app.run(debug=True)
