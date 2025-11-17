from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'govaid-secret-key-2025'

# Database initialization
def init_db():
    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Student profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS student_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        state TEXT,
        category TEXT,
        annual_income INTEGER,
        dob DATE,
        gender TEXT,
        education_level TEXT,
        course TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )''')

    # Entrepreneur profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS entrepreneur_profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        state TEXT,
        age INTEGER,
        industry_type TEXT,
        startup_stage TEXT,
        annual_turnover INTEGER,
        funding_needs INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )''')

    # Schemes table
    c.execute('''CREATE TABLE IF NOT EXISTS schemes (
        scheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        eligibility TEXT,
        provider TEXT,
        benefits TEXT,
        link TEXT,
        target_group TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        try:
            conn = sqlite3.connect('govaid.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)',
                     (name, email, password_hash, role))
            conn.commit()
            user_id = c.lastrowid
            conn.close()

            session['user_id'] = user_id
            session['name'] = name
            session['role'] = role

            flash('Registration successful!', 'success')
            return redirect(url_for('profile'))

        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Hardcoded Admin Login

        email = request.form['email']
        password = request.form['password']
        if email == "admin@gmail.com" and password == "123456":
            session['admin'] = True
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_dashboard'))

        conn = sqlite3.connect('govaid.db')
        c = conn.cursor()
        c.execute('SELECT user_id, name, password_hash, role FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['role'] = user[3]

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    if request.method == 'POST':
        conn = sqlite3.connect('govaid.db')
        c = conn.cursor()

        if role == 'student':
            # Handle student profile
            c.execute('DELETE FROM student_profiles WHERE user_id = ?', (user_id,))
            c.execute('''INSERT INTO student_profiles 
                        (user_id, state, category, annual_income, dob, gender, education_level, course)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (user_id, request.form['state'], request.form['category'], 
                      request.form['annual_income'], request.form['dob'], request.form['gender'],
                      request.form['education_level'], request.form['course']))
        else:
            # Handle entrepreneur profile
            c.execute('DELETE FROM entrepreneur_profiles WHERE user_id = ?', (user_id,))
            c.execute('''INSERT INTO entrepreneur_profiles 
                        (user_id, state, age, industry_type, startup_stage, annual_turnover, funding_needs)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (user_id, request.form['state'], request.form['age'], request.form['industry_type'],
                      request.form['startup_stage'], request.form['annual_turnover'], request.form['funding_needs']))

        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Get existing profile data
    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()

    profile_data = {}
    if role == 'student':
        c.execute('SELECT * FROM student_profiles WHERE user_id = ?', (user_id,))
        profile = c.fetchone()
        if profile:
            profile_data = {
                'state': profile[2], 'category': profile[3], 'annual_income': profile[4],
                'dob': profile[5], 'gender': profile[6], 'education_level': profile[7], 'course': profile[8]
            }
    else:
        c.execute('SELECT * FROM entrepreneur_profiles WHERE user_id = ?', (user_id,))
        profile = c.fetchone()
        if profile:
            profile_data = {
                'state': profile[2], 'age': profile[3], 'industry_type': profile[4],
                'startup_stage': profile[5], 'annual_turnover': profile[6], 'funding_needs': profile[7]
            }

    conn.close()

    return render_template('profile.html', role=role, profile_data=profile_data)

@app.route('/switch_role/<new_role>')
def switch_role(new_role):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Update role in database
    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()
    c.execute('UPDATE users SET role = ? WHERE user_id = ?', (new_role, user_id))
    conn.commit()
    conn.close()

    session['role'] = new_role
    flash(f'Role switched to {new_role.title()}!', 'success')

    return redirect(url_for('profile'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    # Get user profile
    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()

    if role == 'student':
        c.execute('SELECT * FROM student_profiles WHERE user_id = ?', (user_id,))
        profile = c.fetchone()

        profile_dict = {
            "state": profile[2],
            "category": profile[3],
            "income": int(profile[4]) if profile[4] else 0,
            "dob": profile[5],
            "gender": profile[6],
            "education": profile[7],
            "course": profile[8]
        }

    else:
        c.execute('SELECT * FROM entrepreneur_profiles WHERE user_id = ?', (user_id,))
        profile = c.fetchone()

        profile_dict = {
            "state": profile[2],
            "age": int(profile[3]) if profile[3] else 0,
            "industry": profile[4],
            "startup_stage": profile[5],
            "turnover": int(profile[6]) if profile[6] else 0,
            "funding_needs": int(profile[7]) if profile[7] else 0
        }

    if not profile:
        conn.close()
        flash('Please complete your profile first!', 'warning')
        return redirect(url_for('profile'))

    # Fetch schemes for this role
    c.execute("SELECT scheme_id, name, eligibility, provider, benefits, link, target_group FROM schemes WHERE target_group = ?", (role,))
    all_schemes = c.fetchall()
    conn.close()

    filtered_schemes = []

    # ------- Eligibility Filter Function -------
    def is_eligible(eligibility_text, pdata):
        if not eligibility_text or eligibility_text.strip() == "":
            return True  # If no eligibility rules, show it

        conditions = eligibility_text.split(";")

        for cond in conditions:
            cond = cond.strip().lower()

            # Income filter
            if "income" in cond and "<" in cond:
                limit = int(cond.split("<")[1].strip())
                if pdata.get("income", 0) > limit:
                    return False

            # Turnover filter
            if "turnover" in cond and "<" in cond:
                limit = int(cond.split("<")[1].strip())
                if pdata.get("turnover", 0) > limit:
                    return False

            # Category filter
            if "category" in cond and "=" in cond:
                allowed = cond.split("=")[1].strip()
                if allowed != "any":
                    if pdata.get("category", "").lower() not in allowed.lower():
                        return False

            # Gender filter
            if "gender" in cond and "=" in cond:
                allowed = cond.split("=")[1].strip()
                if allowed != "any" and pdata.get("gender", "").lower() != allowed.lower():
                    return False

            # State filter
            if "state" in cond and "=" in cond:
                allowed = cond.split("=")[1].strip().lower()
                if allowed != "any" and pdata.get("state", "").lower() != allowed:
                    return False

            # Startup stage filter
            if "startup_stage" in cond and "=" in cond:
                allowed = cond.split("=")[1].strip()
                if allowed != "any" and pdata.get("startup_stage", "").lower() != allowed.lower():
                    return False

            # Industry filter
            if "industry" in cond and "=" in cond:
                allowed = cond.split("=")[1].strip()
                if allowed != "any" and pdata.get("industry", "").lower() not in allowed.lower():
                    return False

            # Age filter (entrepreneurs)
            if "age" in cond and "<" in cond:
                limit = int(cond.split("<")[1].strip())
                if pdata.get("age", 0) > limit:
                    return False

        return True
    # ------------------------------------------

    for scheme in all_schemes:
        sid, name, eligibility, provider, benefits, link, tg = scheme
        if is_eligible(eligibility, profile_dict):
            filtered_schemes.append({
                "name": name,
                "eligibility": eligibility,
                "provider": provider,
                "benefits": benefits,
                "link": link
            })


    return render_template('dashboard.html', schemes=filtered_schemes, role=role)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()

    # Fetch Schemes
    c.execute("SELECT scheme_id, name, target_group FROM schemes")
    schemes = c.fetchall()

    # Fetch Users
    c.execute("SELECT user_id, name, email, role FROM users")
    users = c.fetchall()

    conn.close()

    return render_template("admindashboard.html", schemes=schemes, users=users)

@app.route('/admin/add_scheme', methods=['GET', 'POST'])
def add_scheme():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        eligibility = request.form['eligibility']
        provider = request.form['provider']
        benefits = request.form['benefits']
        link = request.form['link']
        target_group = request.form['target_group']

        conn = sqlite3.connect('govaid.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO schemes (name, eligibility, provider, benefits, link, target_group)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, eligibility, provider, benefits, link, target_group))
        conn.commit()
        conn.close()

        flash("Scheme added successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("addscheme.html")

@app.route('/admin/delete_scheme/<int:scheme_id>')
def delete_scheme(scheme_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()
    c.execute("DELETE FROM schemes WHERE scheme_id = ?", (scheme_id,))
    conn.commit()
    conn.close()

    flash("Scheme deleted!", "info")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_scheme/<int:scheme_id>', methods=['GET', 'POST'])
def edit_scheme(scheme_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        eligibility = request.form['eligibility']
        provider = request.form['provider']
        benefits = request.form['benefits']
        link = request.form['link']
        target_group = request.form['target_group']

        c.execute("""
            UPDATE schemes 
            SET name=?, eligibility=?, provider=?, benefits=?, link=?, target_group=?
            WHERE scheme_id=?
        """, (name, eligibility, provider, benefits, link, target_group, scheme_id))
        
        conn.commit()
        conn.close()

        flash("Scheme updated!", "success")
        return redirect(url_for('admin_dashboard'))

    # GET request — fetch scheme
    c.execute("SELECT * FROM schemes WHERE scheme_id=?", (scheme_id,))
    scheme = c.fetchone()
    conn.close()

    return render_template("editscheme.html", scheme=scheme)

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('govaid.db')
    c = conn.cursor()
    
    # Delete user's profile also
    c.execute("DELETE FROM student_profiles WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM entrepreneur_profiles WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    
    conn.commit()
    conn.close()

    flash("User deleted!", "info")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("Admin logged out!", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
