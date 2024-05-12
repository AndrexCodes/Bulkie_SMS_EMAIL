import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = "ionextechsolutions@gmail.com"
sender_pass = "xjhd nfyr qbib orap"
subject = "HEADINGS"
body = "Body side lings"
to_email = "machariaandrew1428@gmail.com"

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, sender_pass)

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = to_email
message['Subject'] = subject
body = body
message.attach(MIMEText(body, type))
server.send_message(message)
server.close()