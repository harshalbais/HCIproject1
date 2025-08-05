from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import random
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'secret123'  # 🔐 In production, store this securely (e.g., environment variable)

# ✅ PostgreSQL config for Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://harsh:AQueJMvWr5qVE6jxl5WxvHvx87khQPSN@dpg-d28dknmuk2gs73f6lqcg-a.oregon-postgres.render.com/harshhhh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Email config (use your Gmail and app password)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hbphysics332@gmail.com'  # 🔒 Use environment variables in production
app.config['MAIL_PASSWORD'] = 'vmqg wove rsin ryqy'  # 🔑 App Password (not Gmail password)

mail = Mail(app)
db = SQLAlchemy(app)

# 📦 User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aadhaar = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


def generate_otp():
    return str(random.randint(100000, 999999))


# 🏠 Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        aadhaar = request.form.get('aadhaar')
        password = request.form.get('password')
        email = request.form.get('email')

        if len(aadhaar) == 12 and password and email:
            otp = generate_otp()
            session['otp'] = otp
            session['email'] = email

            msg = Message('Your OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f'Your OTP is: {otp}'
            mail.send(msg)

            new_user = User(aadhaar=aadhaar, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()

            return render_template('otp.html')
        else:
            flash("⚠️ Please enter valid Aadhaar, password, and email.")
            return redirect('/')

    return render_template('login.html')


# 🔐 OTP Verification Route
@app.route('/verify', methods=['POST'])
def verify():
    entered_otp = request.form.get('otp')
    if entered_otp == session.get('otp'):
        return "<h2>✅ OTP Verified! Welcome to the Scholarship Portal.</h2>"
    else:
        flash("❌ Invalid OTP. Please try again.")
        return redirect('/')


# 🚀 Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
