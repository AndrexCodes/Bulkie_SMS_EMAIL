class SMS:
    def __init__(self, sender_id):
        self.base_url = 'https://sms.textsms.co.ke/api/services/sendsms'
        self.payload = {
            "apikey":"5f7157aa5e206f7f5402ffd5abc79c95",
            "partnerID":"9064",
            "message":"Actual Message",
            "shortcode":"sender_id",
            "mobile":"254701910146"
        }

    def SendInstantSMS(self):
        pass

    def SendScheduleSMS(self):
        pass

    def VerifyNumber(self, number):
        return "number:int"