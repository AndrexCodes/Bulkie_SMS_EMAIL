from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

smtp_server = 'smtp.gmail.com'
smtp_port = 587
admin_key = ""

@app.route("/sendEmails", methods = ["POST", "GET"])
def sendEmail():
    request_data = request.get_json()
    print(request_data)
    if request_data:
        type = request_data["type"]
        sender_email = request_data["sender_email"]
        sender_pass = request_data["sender_pass"]
        subject = request_data["subject"]
        body = request_data["body"]
        destinations = request_data["receiver_email"]
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_pass)
        for x in destinations:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = x
            message['Subject'] = subject
            body = body
            message.attach(MIMEText(body, type))
            server.send_message(message)
        server.close()
    return "p"

@app.route("/testlogin", methods = ["POST", "GET"])
def loginTest():
    request_data = request.get_json()
    print(request_data)
    if request_data:
        email = request_data["Sender_email"]
        password = request_data["Sender_pass"]
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)
            return jsonify(True)
        except:
            return jsonify(False)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
