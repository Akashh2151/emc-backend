import smtplib
from email.mime.text import MIMEText

def send_email(subject, recipient, message):
    try:
        sender_email = "akashdesai2151@gmail.com"
        sender_password = "okhnsnnviavjfsej"

        msg = MIMEText(message)
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email sending failed:", str(e))
