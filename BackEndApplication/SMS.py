import requests
import json

class Sms:
    def __init__(self, sender_id):
        self.base_url = 'https://sms.textsms.co.ke/api/services/sendsms'
        self.payload = {
            "apikey":"5f7157aa5e206f7f5402ffd5abc79c95",
            "partnerID":"9064",
            "message":"Testing Sender ID: %s"%(sender_id),
            "shortcode":sender_id,
            "mobile":"254701910146"
        }

    def sendBulkSMS(self, sms_details):
        sendToNumbers = []
        groups = sms_details["groups"]
        acc_data = sms_details["acc_data"]
        subject = sms_details["subject"]
        body = sms_details["body"]
        self.payload["message"] = "%s\n%s"%(subject, body)
        for x in acc_data:
            if x["group_name"] in groups:
                for y in x["phone_book"]:
                    sendToNumbers.append(self.correctNumber(y["phone"]))
        for x in sendToNumbers:
            self.payload["mobile"] = x
            try:
                self.response = requests.post(self.base_url, data=self.payload)
                self.response = json.loads(self.response.text)
                print(self.response)
                self.response = self.response["responses"][0]
                if self.response["response-code"] == 200:
                    self.state = True
                    print("Message Sent Successfully")
                else:
                    self.state = False
                    print("Error Sending Message ....")
            except:
                print("Request failed")

    def sendScheduled(self, sms_details, timeToSend):
        sendToNumbers = []
        groups = sms_details["groups"]
        acc_data = sms_details["acc_data"]
        subject = sms_details["subject"]
        body = sms_details["body"]
        self.payload["message"] = "%s\n%s"%(subject, body)
        for x in acc_data:
            if x["group_name"] in groups:
                for y in x["phone_book"]:
                    sendToNumbers.append(self.correctNumber(y["phone"]))
        print(sendToNumbers)
        timeToSend = str(timeToSend)
        self.payload["timeToSend"] = f"{timeToSend.split("T")[0]} {timeToSend.split("T")[1]}"
        for x in sendToNumbers:
            self.payload["mobile"] = x
            try:
                self.response = requests.post(self.base_url, data=self.payload)
                self.response = json.loads(self.response.text)
                print(self.response)
                self.response = self.response["responses"][0]
                if self.response["response-code"] == 200:
                    self.state = True
                    print("Message Sent Successfully")
                else:
                    self.state = False
                    print("Error Sending Message ....")
            except:
                print("Request failed")

    def correctNumber(self, number):
        number = str(number)
        if len(number) == 10:
            if number[:2] == "07":
                numbers = number[2:]
                new_number = "2547"+numbers
                return new_number
            else:
                numbers = number[2:]
                new_number = "2541"+numbers
                return new_number
        else:
            return "254795359098"

    def countSMS(self, sms_details):
        sendToNumbers = []
        groups = sms_details["groups"]
        acc_data = sms_details["acc_data"]
        subject = sms_details["subject"]
        body = sms_details["body"]
        self.payload["message"] = "%s\n%s"%(subject, body)
        for x in acc_data:
            if x["group_name"] in groups:
                for y in x["phone_book"]:
                    sendToNumbers.append(self.correctNumber(y["phone"]))
        return len(sendToNumbers)

    def testSenderID(self):
        try:
            self.response = requests.post(self.base_url, data=self.payload)
            self.response = json.loads(self.response.text)
            self.response = self.response["responses"][0]
            print(self.response)
            if self.response["response-code"] == 200:
                print("Message Sent Successfully")
                return True
            else:
                print("Error Sending Message ....")
                return False
        except:
            print("Error occured")
            return False

x = Sms("TextSMS")
x.testSenderID()