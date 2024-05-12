import requests
import json

home_url = "http://127.0.0.1:5001"

class SMTPServer:
    def __init__(self, email, password):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587  # SSL: 465, TLS/STARTTLS: 587
        self.sender_email = email  # Replace with your Gmail address
        self.password = password

        self.next_api = {
            "type": "",
            "sender_email": "",
            "sender_pass": "",
            "receiver_email": [],
            "subject": "",
            "body": ""
        }

    def sendBulkie(self, data):
        subject = data["subject"]
        body = data["body"]
        receive_emails = []
        for x in data["acc_data"]:
            if x["group_name"] in data["groups"]:
                for y in x["phone_book"]:
                    receive_emails.append(y["email"])
        print(self.sender_email)
        print(self.password)
        print(receive_emails)
        self.next_api["type"] = "plain"
        self.next_api["sender_email"] = self.sender_email
        self.next_api["sender_pass"] = self.password
        self.next_api["receiver_email"] = receive_emails
        self.next_api["subject"] = subject
        self.next_api["body"] = body
        response = requests.post(f"{home_url}/sendEmails", json=self.next_api)
        # try:
        #     server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        #     server.starttls()
        #     server.login(self.sender_email, self.password)
        #     for x in receive_emails:
        #         message = MIMEMultipart()
        #         message['From'] = self.sender_email
        #         message['To'] = x
        #         message['Subject'] = subject
        #         body = body
        #         message.attach(MIMEText(body, 'plain'))
        #         server.send_message(message)
        #     print("Sent Email")
        # except:
        #     print("Failed to send Email")
        # server.close()

    def sendScheduledEmails(self, data):
        subject = data["subject"]
        body = data["body"]
        receive_emails = []
        for x in data["acc_data"]:
            if x["group_name"] in data["groups"]:
                for y in x["phone_book"]:
                    receive_emails.append(y["email"])
        print(self.sender_email)
        print(self.password)
        print(receive_emails)
        return receive_emails

    # def sendSingle(self, data):
    #     receiver_email = data["email_receiver"]
    #     subject = data["subject"]
    #     body = data["body"]
    #     try:
    #         server = smtplib.SMTP(self.smtp_server, self.smtp_port)
    #         server.starttls()
    #         server.login(self.sender_email, self.password)
    #         message = MIMEMultipart()
    #         message['From'] = self.sender_email
    #         message['To'] = receiver_email
    #         message['Subject'] = subject
    #         body = body
    #         message.attach(MIMEText(body, 'plain'))
    #         server.send_message(message)
    #         print("Sent Email")
    #     except:
    #         print("Failed to send Email")
    #     server.close()

    def countEmails(self, data):
        receive_emails = []
        for x in data["acc_data"]:
            if x["group_name"] in data["groups"]:
                for y in x["phone_book"]:
                    receive_emails.append(y["email"])
        return len(receive_emails)

    def adminSend(self, data):
        self.next_api["type"] = "html"
        self.next_api["sender_email"] = self.sender_email
        self.next_api["sender_pass"] = self.password
        self.next_api["receiver_email"] = [data["to_email"]]
        self.next_api["subject"] = data["subject"]
        self.next_api["body"] = data["body"]
        response = requests.post(f"{home_url}/sendEmails", json=self.next_api)
        # try:
        #     server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        #     server.starttls()
        #     server.login(self.sender_email, self.password)
        #     message = MIMEMultipart()
        #     message['From'] = self.sender_email
        #     message['To'] = data["to_email"]
        #     message['Subject'] = data["subject"]
        #     body = data["body"]
        #     message.attach(MIMEText(body, 'html'))
        #     server.send_message(message)
        #     print("Sent Email")
        #     return "Successful"
        # except:
        #     return "Failed"
        # server.close()
        
    def testPasswordLogin(self):
        data = {
            "Sender_email": self.sender_email,
            "Sender_pass": self.password
        }
        response = requests.post(f"{home_url}/testlogin", json=data)
        response = json.loads(response.text)
        print("Response: %s"%(response))
        return response
        # try:
        #     server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        #     server.starttls()
        #     server.login(self.sender_email, self.password)
        #     return True
        # except:
        #     return False
