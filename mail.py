import smtplib
from email.mime.text import MIMEText

def send_mail(username):
    try:
        sender_email = "kskkoushik135@outlook.com"
        receiver_email = "koradalakshmi1977@gmail.com"
        password = "KSKkoushik789..."

        message = MIMEText(f"Click the following link to take the skill test: http://localhost:5000/skill_test/{username}")
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Skill Test Invitation"

        # Establish a connection to the SMTP server
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()  # Start TLS for security
            server.login(sender_email, password)  # Login to the server
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email

        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to send email")

send_mail('radhakrishn')
