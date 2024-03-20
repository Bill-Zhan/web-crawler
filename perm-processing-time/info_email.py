"""
Send crawl result via email
"""
import json
import smtplib
from perm_crawler import crawl_processing_time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_email_config(file_path="email_pwd.json"):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["send_email"], data["send_email_pwd"]

def inform_processing_time(receiving_email: str):
    sender_email, sender_pwd = read_email_config()
    processing_time = crawl_processing_time()  # Make sure this function is defined and returns a string
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "PERM Processing Time Update"
    message["From"] = sender_email
    message["To"] = receiving_email
    
    # Define email body
    text = f"Hi,\nHere is the latest PERM processing time: {processing_time}"
    html = f"""\
    <html>
      <body>
        <p>Hi,<br>
           Here is the latest <b>PERM processing time</b>: {processing_time}
        </p>
      </body>
    </html>
    """
    
    # Convert to MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    # Attach parts to the message
    message.attach(part1)
    message.attach(part2)
    
    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Replace 'smtp.example.com' with your SMTP server
            server.login(sender_email, sender_pwd)
            server.sendmail(sender_email, receiving_email, message.as_string())
        print(f"Processing time information sent to {receiving_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")