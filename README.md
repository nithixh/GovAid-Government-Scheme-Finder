# GovAid-Government-Scheme-Finder
GovAid is a Flask-based web application that helps students and entrepreneurs discover the most suitable government scholarships and startup funding schemes based on their personal or business profile. The system uses smart filtering logic to match users with schemes that fit their eligibility, and also includes an admin dashboard for managing schemes and users.

🚀 Features
🔹 User Module

User registration & login

Role selection: Student or Entrepreneur

Dynamic profile forms

Student: state, category, income, gender, DOB, education level, course

Entrepreneur: state, age, industry, startup stage, turnover, funding needs

Personalized dashboard showing only eligible schemes

Direct application via official scheme links

🔹 Eligibility Matching Engine

Matches user profile with scheme conditions like:

Income

Category

Gender

State

Industry

Startup stage

Turnover

Age

Schemes appear only if eligibility conditions match

🔹 Admin Module

Admin login (hardcoded)

Add, edit, delete schemes

Manage users

Clean, table-based dashboard

🛠️ Tech Stack
Component	Technology
Backend	Flask (Python)
Database	SQLite
Frontend	HTML, CSS, Bootstrap 5
Hosting	Local / Deployment-ready
Security	Password hashing (Werkzeug)
📦 Project Structure
/
├── app.py
├── govaid.db
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── dashboard.html
│   ├── admindashboard.html
│   ├── addscheme.html
│   ├── editscheme.html
│   └── base.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── README.md

⚙️ How to Run the Project Locally
1️⃣ Clone the repository
git clone https://github.com/<your-username>/govaid.git
cd govaid

2️⃣ Install dependencies
pip install flask werkzeug

3️⃣ Run the app
python app.py

4️⃣ Open in browser
http://127.0.0.1:5000/

🔐 Admin Login
Email: admin@gmail.com
Password: 123456

📚 Future Enhancements

AI-based scheme recommendation

Search and filter options

Email notifications

Mobile app version

Auto-updating scheme data from APIs
