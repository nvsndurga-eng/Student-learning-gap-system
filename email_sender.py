import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    EMAIL = "yourdemoemail@gmail.com"
    PASSWORD = "your_app_password"

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
