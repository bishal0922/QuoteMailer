import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, message, to_emails):
    print("Sending Email")

    print("Subject:", subject)
    print("Message:", message)
    print("To:", to_emails)
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SMTP_USER')  # Change to your actual email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))  # Ensure this is an int
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Create an SMTP_SSL object
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_user, smtp_password)  # Log in to the server
    text = msg.as_string()  # Convert the message to a string
    server.sendmail(smtp_user, to_emails, text)  # Send the email
    server.quit()  # Close the connection

