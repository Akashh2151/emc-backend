from flaskapp import app
from flask import Flask, request, jsonify, session
from flask_session import Session
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from model.forgetpassword_model import ForgotPasswordModel


@app.route("/addproduct")
def addproductt():
    return "add product successful!"    

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def generate_numeric_otp():
    return str(random.randint(100000, 999999))

# def generate_otp_secret():
#     return pyotp.random_base32()

# def generate_otp():
#     return pyotp.random_base32()

def send_email(subject, recipient, message):
    sender_email = "akashdesai2151@gmail.com"
    sender_password = "okhnsnnviavjfsej"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient, msg.as_string())
    server.quit()


forgetmodel = ForgotPasswordModel()
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    
    userin_db=forgetmodel.get_user_by_email(email)
    if not userin_db:
        return jsonify({'error':'user is not found in db'})
    else:
    # Generate and store OTP in session
        otp_code = generate_numeric_otp()
        session['otp_code'] = otp_code
        session['email'] = email

    # Simulate sending the OTP via email
        send_email("Password Reset OTP", email, f"Your OTP is: {otp_code}")

        return jsonify({'message': 'OTP sent'})




@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    otp_code = request.json.get('otp')
    new_password = request.json.get('new_password')

    stored_otp = session.get('otp_code')
    stored_email = session.get('email')
    print("Stored OTP:", stored_otp)
    print("Stored Email:", stored_email)

    if stored_email == email or stored_otp == otp_code:
        user_in_db = forgetmodel.get_user_by_email(email)
        if user_in_db:
            user_in_db['password'] = new_password
            forgetmodel.update_user(user_in_db)
            session.pop('otp_code')
            session.pop('email')
            return jsonify({'message': 'Password reset successful'}), 200
        else:
            return jsonify({'error': 'User not found in the database'}), 400
    else:
        return jsonify({'error': 'Invalid OTP or User not found'}), 400








if __name__ == '__main__':
    app.run(debug=True)
