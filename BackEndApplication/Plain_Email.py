import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = 'info@ionextechsolutions.com'
receiver_email = 'machariaandrew1428@gmail.com'
subject = 'Test Email from Python'
body = 'Hello, this is a test email sent from Python.'

# SMTP server configuration
smtp_server = 'mail.ionextechsolutions.com'
smtp_port = 465  # Port for TLS encryption

# Sender's credentials (replace with your own)
smtp_username = 'info@ionextechsolutions.com'
smtp_password = '^iLsFBk~-d1Y'

# Create a multipart message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject



# Attach the message body
message.attach(MIMEText(body, 'plain'))
print("jjjjjj")
# Connect to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    print("Sending Email...")
    server.starttls()  # Secure the connection
    server.login(smtp_username, smtp_password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print('Email sent successfully!')
