from flask import Flask, request, jsonify, json, render_template, make_response
from flask_cors import CORS
from passlib.hash import sha256_crypt
from CodeMaker import genCode
from threading import Thread
from Emails import SMTPServer
import DeleteLoop
from SMS import Sms
import Crypter
import constants
import mysql.connector as db
from datetime import datetime
import time

conn = db.connect(user=constants.user, password=constants.password, database=constants.database, host=constants.host)
cursor = conn.cursor()

def createTables():
    sql_query = """create table if not exists applications (
                id varchar(255),
                activity varchar(255),
                state varchar(255),
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)
    
    sql_query = """create table if not exists accounts (
                id varchar(255),
                name varchar(255),
                email varchar(255),
                phone varchar(255),
                password varchar(255),
                phonebook longtext,
                api_sms varchar(255),
                api_email longtext,
                state varchar(255),
                app_id varchar(255),
                acc_type varchar(255),
                datetime varchar(255),
                endpoint varchar(255),
                verify_code varchar(255),
                history varchar(255),
                deletion varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists scheduled_comm(
                acc_id varchar(255),
                app_id varchar(255),
                comm_type varchar(255),
                email varchar(255),
                app_pass longtext,
                raw_data longtext,
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists sent_bulkies (
                acc_id varchar(255),
                app_id varchar(255),
                comm_type varchar(255),
                FSRatio varchar(255),
                datetime varchar(255)
                )"""
    # cursor.execute()
    # FSRatio = {
    #     "failed": 1,
    #     "success": 3,
    #     "failed_data": [0712345678],
    #     "success_data": [0701910146, 0791216702, 0795359098]
    # }

    conn.commit()

def clearTables():
    tables = ["applications", "accounts"]
    for x in tables:
        sql_query = """delete from %s"""%(x)
        cursor.execute(sql_query)
    conn.commit()

# clearTables()
createTables()

admin_email = constants.admin_email
admin_password = constants.admin_password
home_url = constants.home_url
reset_keys = []

app = Flask(__name__)
CORS(app)

def SendScheduledEmails():
    while True:
        main_current_datetime = datetime.now()
        # print(current_datetime)
        main_current_datetime = str(main_current_datetime)
        current_datetime = main_current_datetime.split(" ")
        current_datetime = current_datetime[0] + " " + current_datetime[1].split(".")[0]
        current_datetime = current_datetime[:16]
        sql_query = """select * from scheduled_comm where datetime = %s"""
        cursor.execute(sql_query, [current_datetime])
        response = cursor.fetchall()
        if response:
            response = response[0]
            sql_query = """delete from scheduled_comm where acc_id = %s and datetime = %s"""
            cursor.execute(sql_query, [response[0], response[6]])
            conn.commit()
            x = SMTPServer(response[3], Crypter.PassDecrypter(json.loads(response[4])[0], json.loads(response[4])[1]))
            email_thread = Thread(target=x.sendBulkie(json.loads(response[5])))
            email_thread.daemon = True
            email_thread.start()
        
        cur_date = str(datetime.now())
        cur_date = cur_date.split(" ")
        cur_date = cur_date[0]
        cur_date = cur_date.split("-")
        endpoint = f"{int(cur_date[0])}-{cur_date[1]}-{cur_date[2]}"
        sql_query = """select * from accounts where endpoint = %s"""
        cursor.execute(sql_query, [endpoint])
        response = cursor.fetchall()
        if response:
            print(response)
            response = response[0]
            account_id = response[0]
            api_email = {
                "email": json.loads(response[7])["email"],
                "password": json.loads(response[7])["password"],
                "balance": 0
            }
            api_sms = {
                "sender_id": json.loads(response[6])["sender_id"],
                "balance": 0
            }
            sql_query = """update accounts set api_sms = %s, api_email = %s, state = %s where id = %s"""
            cursor.execute(sql_query, [json.dumps(api_sms), json.dumps(api_email), "Locked", account_id])
            conn.commit()
        
        time.sleep(55)

test_thread = Thread(target=SendScheduledEmails)
test_thread.start()

@app.route("/")
def home():
    sql_query = """select * from accounts"""
    cursor.execute(sql_query)
    return str(cursor.fetchall())

@app.route("/newDownload", methods = ["POST", "GET"])
def ApplicationSetUp():
    if request.get_json():
        new_born_key = request.get_json()["new_born_key"]
        if new_born_key == "ZITD0JL2LCZMJVQENIFH2Y7VXZ5JMLGWMAHQ9K7STV8FIBW9PARNFKWXL6VMFRK24IBJ5YJUKLYS3NBRKO8GCG67M5BF4RKMT8AYKW9B9I7W5YBLW1V942O16NVKDBLWPGG7LQKQEEAWLWR9J593RH2TR88EY91OJ7NUVF58UGGKGFKVVY9P01I5WYF4NO42TXNB93Q8AU0EHN3I6GGOHDO9MVEJXIGNXPZJJNAWTJB649JLLEHX5B1X5NKNWYXL2O5E9GS0HR4P94US4FNVOFZHOQZZY0KB2KYFK37P2B3PEKV1DLVH62ZBUS2URLAAOCVDW6CIHH5F9LTNQJ00JT7VR9KPHHTYAX5NTL0K6H6ZTH480XL8NPJZ4V54D88BM0M3USK4QMZV9Q7XOAH55YCIAZWNB7OPRJLW1LEFGP13ZYQ2WF5IR3SS2IR44E7MLXKN6U1H1IHACYCGG09EJG67DJFC6B4GFKNRKAQGX00X338P6JGGYU2Q38OBR9IJBWD6R8LK5KLDI6PKYHHQ3RZ6UUVV0VVMYECNZ2CP3SUL8C7TZIF4NPLR24CAOBLLJGR0DC6VLPD3LBDPAUU5TDVNBYJPWAGW69SK2YZVCWZ49R135DVJLKNOSVLK0L0PHT8KKHWSULOQJYD1VKFAILFF1CPT3UJZD5BV23DAOIXVU1O220KR5P1QE6GWYLUQ1M1CF3ZHIKXR0986WODXYMHNQGGGYESNFZBAIS2N8QH6HOBBOEW2D2V3RQ60LIGITXCX6CUM38VMN45UGHI5T691R478H24QMZCLW5H5A25GQUWVNDX6C4VEBNC9KX00UGREHHJN5Q7VYHETVMYW21OBJQATUKWI9YAIAX9EUCBIS94WYC75E160RE4S75OFJ70JBUJ67C2WINSJXGSJH1G65EQYJ208UYV8PUYEN5X8SC3M98XNEZOQDOIE0QTKNXC2NOLOBZRMILR1TOTEX7G3BEV3A722Y8EZSHOS":
            app_id = genCode(50)
            sql_query = """insert into applications (id, activity, state, datetime)
                            values(%s, %s, %s, %s)"""
            sql_data = [app_id, json.dumps([]), "Active",str(datetime.now())]
            cursor.execute(sql_query, sql_data)
            conn.commit()

            return jsonify({
                "state": True,
                "app_id": app_id
            })
        else:
            return jsonify({
            "state": False
        })
    else:
        return jsonify({
            "state": False
        })

@app.route("/signup", methods = ["POST", "GET"])
def newAccount():
    request_data = request.form
    if request_data:
        app_id = request_data.get("app_id")
        while True:
            acc_id = genCode(50)
            sql_query = """select * from accounts where id = %s"""
            cursor.execute(sql_query, [acc_id])
            response = cursor.fetchall()
            if not response:
                break
        fname = request_data.get("fname")
        lname = request_data.get("lname")
        name = fname+lname
        phone = request_data.get("phone")
        email = request_data.get("email")
        password = request_data.get("password")
        sql_query = """select * from applications where id = %s"""
        cursor.execute(sql_query, [app_id])
        response = cursor.fetchall()
        if response:
            sql_query = """select * from accounts where email = %s or name = %s"""
            cursor.execute(sql_query, [email, name])
            response = cursor.fetchall()
            if not response:
                x = SMTPServer(admin_email, admin_password)
                x.adminSend({
                    "to_email": "machariaandrew1428@gmail.com",
                    "subject": "NEWLY REGISTERED ACCOUNT",
                    "body": """
                            <html>
                                <body>
                                    <p>Account Details: <br>
                                        Name: %s <br>
                                        Phone: %s <br>
                                        Email: %s <br>
                                    </p>
                                    <p style="background: lightblue; border-radius: 10px; width: max-content; padding: 4px 5px 4px 5px"><a href="%s/accountSetUp/%s">Account Set Up</a></p>
                                </body>
                            </html>
                        """%(name, phone, email, home_url, acc_id)
                })
                time.sleep(3)
                verify_code = genCode(4)
                x.adminSend({
                    "to_email": email,
                    "subject": "ACCOUNT VERIFICATION",
                    "body": """
                            <html>
                                <body>
                                    <p>Verification code:</p>
                                    <h1>%s</h1>
                                </body>
                            </html>
                        """%(verify_code)
                })
                api_sms_data = {
                    "sender_id": None,
                    "balance": 0
                }

                api_email_data = {
                    "email": email,
                    "password": None,
                    "balance": 0
                }

                sql_query = """insert into accounts (id, name, email, phone, password, phonebook, api_sms, api_email, state, app_id, acc_type, datetime, verify_code)
                                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                sql_data = [acc_id, name, email, phone, sha256_crypt.hash(password), json.dumps([]), json.dumps(api_sms_data), json.dumps(api_email_data), "Inactive", app_id, "Prepaid", str(datetime.now()), verify_code]
                cursor.execute(sql_query, sql_data)
                conn.commit()
                return jsonify({
                    "state": True,
                    "acc_id": acc_id
                })
            else:
                return jsonify({
                "state": False,
                "message": "Account Already Exists"
                })
        else:
            return jsonify({
            "state": False
        })
    else:
        return jsonify({
            "state": False
        })

@app.route("/signin", methods = ["POST", "GET"])
def setUpOldAccount():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        email = request_data["email"]
        password = request_data["password"]
        sql_query = """select * from accounts where email = %s"""
        cursor.execute(sql_query, [email])
        response = cursor.fetchall()
        if response:
            response = response[0]
            if sha256_crypt.verify(password, response[4]):
                sql_query = """delete from applications where id = %s"""
                cursor.execute(sql_query, [app_id])
                conn.commit()
                return jsonify({
                    "state": True,
                    "app_id": response[9],
                    "acc_id": response[0],
                    "phone_book": json.loads(response[5]),
                    "acc_details": {
                        "name": response[1],
                        "sms_id": [json.loads(response[6])["sender_id"], json.loads(response[6])["balance"]],
                        "email_id": [json.loads(response[7])["email"], json.loads(response[7])["balance"]],
                        "app_pass": "<cloudstored>",
                        "phone": response[3],
                        "state": response[8]
                    }
                })
            else:
                return jsonify({
                    "state": False,
                    "message": "Faild Login \n Invalid Credentuials"
                })
        else:
            return jsonify({
                    "state": False,
                    "message": "Faild Login \n Account Does not Exists"
            })
    else:
       return jsonify({
                "state": False,
                "message": "Failed"
            })

@app.route("/codeResend", methods = ["POST", "GET"])
def redoCode():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        acc_id = request_data["acc_id"]
        sql_query = """select * from accounts where id = %s and app_id = %s"""
        cursor.execute(sql_query, [acc_id, app_id])
        response = cursor.fetchall()
        if response:
            response = response[0]
            x = SMTPServer(admin_email, admin_password)
            verify_code = response[13]
            x.adminSend({
                "to_email": response[2],
                "subject": "ACCOUNT VERIFICATION",
                "body": """
                        <html>
                            <body>
                                <p>Verification code:</p>
                                <h1>%s</h1>
                            </body>
                        </html>
                    """%(verify_code)
            })
            return jsonify({
                "state": True,
                "message": "Verification code sent to %s"%(response[2])
            })
    else:
        return False

@app.route("/verifyAccount", methods = ["POST", "GET"])  
def verification():
    request_data = request.form
    if request_data:
        app_id = request_data.get("app_id")
        acc_id = request_data.get("acc_id")
        ver_code = request_data.get("ver_code")
        sql_query = """select * from accounts where id = %s and app_id = %s and verify_code = %s"""
        cursor.execute(sql_query, [acc_id, app_id, ver_code])
        response = cursor.fetchall()
        if response:
            sql_query = """update accounts set verify_code = %s where id = %s and app_id = %s"""
            cursor.execute(sql_query, ["True", acc_id, app_id])
            conn.commit()
            return jsonify({
                "state": True,
                "message": "Account Verified Successfullu"
            })
        else:
            return jsonify({
                "state": False,
                "message": "Account Verification Failed"
            })

@app.route("/restPassword", methods = ["POST", "GET"])
def RESTPASS():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        email = request_data["email"]
        sql_query = """select * from applications where id = %s"""
        cursor.execute(sql_query, [app_id])
        response = cursor.fetchall()
        sql_query = """select * from accounts where email = %s"""
        cursor.execute(sql_query, [email])
        response_2 = cursor.fetchall()
        if response and response_2:
            response = response[0]
            unit_reset_key = genCode(50)
            reset_keys.append(unit_reset_key)
            args = "email=%s&app_id=%s&reset_key=%s"%(email, app_id, unit_reset_key)
            data = {
                "to_email": email,
                "subject": "BULKIES PASSWORD RESET",
                "body": """
                <html>
                    <body>
                        <p>Dear %s, <br>
                            Please reset you account password with the link below. <br>
                            No Charges apply for this service. Thankyou for choosing ionextechsolutions for you tech <br>
                            needs.
                            For inquires or complaints, contact us through:
                            Email: ionextechsolutions@gmail.com
                            Phone: 0795359098/ 0791216702
                        </p>
                        <p style="background: lightblue; border-radius: 10px; width: max-content; padding: 4px 5px 4px 5px"><a href="%s/restTemplate?%s">PASSWORD RESET</a></p>
                    </body>
                </html>
                """%(email, home_url, args)
            }
            x = SMTPServer(admin_email, admin_password)
            x.adminSend(data)
            return jsonify({
                "state": True
            })
        else:
            return jsonify({
                "state": False,
                "message": "Invalid Email Account"
            })

    return jsonify(False)

@app.route("/ActualReseter", methods = ["POST", "GET"])
def ActualReseter():
    request_form = request.form
    app_id = request.cookies.get("app_id")
    email = request.cookies.get("email")
    print(request_form)
    print(request.cookies)
    if request_form:
        sql_query = """select * from applications where id = %s"""
        cursor.execute(sql_query, [app_id])
        response = cursor.fetchall()
        if response:
            new_password = request_form.get("sender_id")
            sql_query = """update accounts set password = %s where email = %s"""
            cursor.execute(sql_query, [sha256_crypt.hash(new_password), email])
            conn.commit()
            return "Password Reset Successful"
        

    return "Reseter Response"

@app.route("/restTemplate", methods = ["POST", "GET"])
def restTemplates():
    request_data = request.args
    if request_data:
        email = request_data.get("email")
        app_id = request_data.get("app_id")
        unit_reset_key = request_data.get("reset_key")
        if unit_reset_key in reset_keys:
            reset_keys.remove(unit_reset_key)
            edit_template = render_template("reset.html", email=email)
            new_response = make_response(edit_template)
            new_response.set_cookie("app_id", app_id)
            new_response.set_cookie("email", email)
            return new_response
        else:
            return "Invalid Reset Key"

@app.route("/remoteStorage", methods = ["POST", "GET"])
def CloudStorage():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        acc_id = request_data["acc_id"]
        arg = request_data["arg"]
        data = request_data["data"]
        sql_query = """select * from accounts where id = %s and app_id = %s"""
        cursor.execute(sql_query, [acc_id, app_id])
        response = cursor.fetchall()
        if response:
            response = response[0]
            if response[15] == "True":
                arg = "download"
                sql_query = """update accounts set deletion = %s where id = %s and app_id = %s"""
                cursor.execute(sql_query, ["False", acc_id, app_id])
                conn.commit()
            if arg == "download":
                return jsonify({
                    "state": True,
                    "data": json.loads(response[5])
                })
            
            elif arg == "upload":
                if len(str(data)) > len(str(json.loads(response[5]))):
                    sql_query = """update accounts set phonebook = %s where id = %s and app_id = %s"""
                    cursor.execute(sql_query, [json.dumps(data), acc_id, app_id])
                    conn.commit()
                    return jsonify({
                        "state": True,
                        "data": data
                    })
                else:
                    new_data = DeleteLoop.CorrectbyGroupNumber(json.loads(response[5]), data)
                    new_data = DeleteLoop.CorrectbyGroupMagnitude(new_data, data)
                    sql_query = """update accounts set phonebook = %s where id = %s and app_id = %s"""
                    cursor.execute(sql_query, [json.dumps(new_data), acc_id, app_id])
                    conn.commit()
                    return jsonify({
                        "state": True,
                        "data": new_data
                    })
        else:
            return jsonify({
                "state": False,
                "message": "Account Doesnt Exists"
            })
    else:
        return "Invalid Request"

@app.route("/phoneBookModify", methods = ["POST", "GET"])
def phoneBookModify():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        acc_id = request_data["acc_id"]
        deltype = request_data["deltype"]
        groups = request_data["groups"]
        sql_query = """select * from accounts where id = %s and app_id = %s"""
        cursor.execute(sql_query, [acc_id, app_id])
        response = cursor.fetchall()
        if response:
            response = response[0]
            if deltype == "group":
                phone_book = json.loads(response[5])
                phone_book = DeleteLoop.deleteGroup(phone_book, groups)
                sql_query = """update accounts set deletion = %s, phonebook = %s where id = %s and app_id = %s"""
                cursor.execute(sql_query, ["True", json.dumps(phone_book), acc_id, app_id])
                conn.commit()
                return jsonify({
                    "state": True,
                    "phone_book": phone_book
                })
            elif deltype == "contact":
                pass
        else:
            return False

@app.route("/updateAccount", methods = ["POST", "GET"])
def AccountUpdates():
    request_data = request.get_json()
    if request_data:
        app_id = request_data["app_id"]
        acc_id = request_data["acc_id"]
        name = request_data["name"]
        app_pass = request_data["app_pass"]
        phone = request_data["phone"]
        sql_query = """select * from accounts where id = %s and app_id = %s"""
        cursor.execute(sql_query, [acc_id, app_id])
        response = cursor.fetchall()
        if response:
            response = response[0]
            if json.loads(response[7])["password"]:
                app_pass = json.loads(response[7])["password"]
                api_email = {
                    "email": json.loads(response[7])["email"],
                    "password": app_pass,
                    "balance": json.loads(response[7])["balance"]
                }
            else:
                x = SMTPServer(json.loads(response[7])["email"], app_pass)
                test_pass = x.testPasswordLogin()
                if not test_pass:
                    return jsonify({
                        "state": False,
                        "message": "Update Failed: Email App Password Incorrect"
                    })
                raw_data = Crypter.PassEncrypter(app_pass)
                api_email = {
                    "email": json.loads(response[7])["email"],
                    "password": [raw_data["cypher_text"], raw_data["privateKey"]],
                    "balance": json.loads(response[7])["balance"]
                }
            sql_query = """update accounts set name = %s, phone = %s, api_email = %s where id = %s and app_id = %s"""
            cursor.execute(sql_query, [name, phone, json.dumps(api_email), acc_id, app_id])
            conn.commit()

            sql_query = """select * from accounts where id = %s and app_id = %s"""
            cursor.execute(sql_query, [acc_id, app_id])
            response = cursor.fetchall()
            response = response[0]
            return jsonify({
                "state": True,
                "updates": {
                    "app_pass": "<cloudstored>",
                    "email_id": [json.loads(response[7])["email"], json.loads(response[7])["balance"]],
                    "name": response[1],
                    "phone": response[3],
                    "sms_id": [json.loads(response[6])["sender_id"], json.loads(response[6])["balance"]],
                    "state": response[8]
                }
            })
        else:
            return jsonify({
                "state": False,
                "message": "Your Account is Inactive.<br> Please Activate"
            })

    else:
        return ""

@app.route("/APISend", methods = ["POST", "GET"])
def sendBulkie():
    request_data = request.get_json()
    print(request_data)
    if request_data:
        acc_id = request_data["acc_id"]
        app_id = request_data["app_id"]
        groups = request_data["groups"]
        sms = request_data["sms"]
        email = request_data["email"]
        subject = request_data["subject"]
        body = request_data["body"]
        schedulde = request_data["schedule"]
        final_response = "Communication Results:<br>"
        sql_query = """select * from accounts where id = %s and app_id = %s and state = %s"""
        cursor.execute(sql_query, [acc_id, app_id, "Activate"])
        response = cursor.fetchall()
        if response:
            response = response[0]
            # EMAIL DETAILS
            email_sender = json.loads(response[7])["email"]

            app_pass = Crypter.PassDecrypter(json.loads(response[7])["password"][0], json.loads(response[7])["password"][1])
            
            email_data = {
                    "groups": groups,
                    "acc_data": json.loads(response[5]),
                    "subject": subject,
                    "body": body
                    }
            x = SMTPServer(email_sender, app_pass)
            no_emails = x.countEmails(email_data)
            email_balance = json.loads(response[7])["balance"]
            no_emails = {
                    "email":email_sender,
                    "balance": email_balance - no_emails,
                    "password": [json.loads(response[7])["password"][0], json.loads(response[7])["password"][1]]
                    }
            
            # SMS DETAILS
            sms_sender_id = json.loads(response[6])["sender_id"]
            sms_balance = json.loads(response[6])["balance"]
            sms_data = {
                    "groups": groups,
                    "acc_data": json.loads(response[5]),
                    "subject": subject,
                    "body": body
                            }
            y = Sms(sms_sender_id)
            no_sms = y.countSMS(sms_data)
            no_sms = {
                "sender_id": sms_sender_id,
                "balance": sms_balance - no_sms
            }
                            
            if not schedulde:
                if email:
                    if not app_pass:
                        final_response = final_response + "Email App Password not Set <br>"
                    else:
                        if email_balance > 0:
                            email_thread = Thread(target=x.sendBulkie(email_data))
                            email_thread.daemon = True
                            email_thread.start()
                            final_response = final_response + "Emails sent Successfully <br>"
                        else:
                            final_response = final_response + "Email Insufficient Funds. <br>"
                
                if sms:
                    print("SMS Active")
                    if not sms_sender_id:
                        final_response = final_response + "Sender Id not Found <br>"
                    else:
                        if sms_balance > 0:
                            sms_thread = Thread(target=y.sendBulkSMS(sms_data))
                            sms_thread.daemon = True
                            sms_thread.start()
                            final_response = final_response + "SMS Sent Successfully <br>"
                        else:
                            final_response = final_response + "SMS Insufficient Funds <br>"

            else:
                if email:
                    app_pass = [json.loads(response[7])["password"][0], json.loads(response[7])["password"][1]]
                    sql_query = """insert into scheduled_comm (acc_id, app_id, comm_type, email, app_pass, raw_data, datetime)
                                    values(%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql_query, [acc_id, app_id, "Schedule_Email", email_sender, json.dumps(app_pass), json.dumps(email_data), f"{schedulde.split('T')[0]} {schedulde.split('T')[1]}"])
                    conn.commit()
                    final_response = final_response + "Emails Scheduled Successfully."

                if sms:
                    schedule_sms_thread = Thread(target=y.sendScheduled(sms_data, schedulde))
                    schedule_sms_thread.daemon = True
                    schedule_sms_thread.start()
                    final_response = final_response + f"SMS Scheduled Successfully. <br> DateTime:{schedulde} <br>"

            sql_query = """update accounts set api_email = %s, api_sms = %s where id = %s and app_id = %s"""
            cursor.execute(sql_query, [json.dumps(no_emails), json.dumps(no_sms), acc_id, app_id])
            conn.commit()
            return jsonify({
                "state": True,
                "message": final_response
            })
        else:
            return jsonify({
                "state": False,
                "message": "Your Account is Inactive || Locked. <br>Please Activate"
            })

    else:
        return jsonify({
            "state": False
        })

@app.route("/accountSetUp/<account_id>", methods = ["POST", "GET"])
def VerifySetUp(account_id):
    if account_id:
        sql_query = """select * from accounts where id = %s"""
        cursor.execute(sql_query, [account_id])
        response = cursor.fetchall()
        if response:
            response = response[0]
            if response[8] == "Inactive":
                response_template = render_template("index.html")
                response_template = make_response(response_template)
                response_template.set_cookie("account_id", account_id)
                return response_template
            elif response[8] == "Locked":
                response_template = render_template("index.html")
                response_template = make_response(response_template)
                response_template.set_cookie("account_id", account_id)
                return response_template
            else:
                response_template = render_template("index.html")
                response_template = make_response(response_template)
                response_template.set_cookie("account_id", account_id)
                return response_template
        else:
            return "invalid Token used"
    else:
        return "invalid Token used"

@app.route("/activateAccount", methods = ["POST", "GET"])
def accountActivation():
    request_form = request.form
    account_id = request.cookies.get("account_id")
    sender_id = request_form["sender_id"]
    app_password = request_form["app_password"]

    sql_query = """select * from accounts where id = %s"""
    cursor.execute(sql_query, [account_id])
    response = cursor.fetchall()
    if response:
        response = response[0]
        x = SMTPServer(json.loads(response[7])["email"], app_password)
        y = Sms(sender_id)
        email_pass_validation = x.testPasswordLogin()
        sms_senderid_validation = y.testSenderID()
        if json.loads(response[7])["password"]:
            email_pass_validation = True
        if email_pass_validation and sms_senderid_validation:
            raw_cred = Crypter.PassEncrypter(app_password)
            api_email = {
                "email": json.loads(response[7])["email"],
                "password": [raw_cred["cypher_text"], raw_cred["privateKey"]] if not json.loads(response[7])["password"] else json.loads(response[7])["password"],
                "balance": 60000
            }
            api_sms = {
                "sender_id": sender_id,
                "balance": 60000
            }
            cur_date = str(datetime.now())
            cur_date = cur_date.split(" ")
            cur_date = cur_date[0]
            cur_date = cur_date.split("-")
            endpoint = f"{int(cur_date[0])+1}-{cur_date[1]}-{cur_date[2]}"
            print(endpoint)
            sql_query = """update accounts set api_sms = %s, api_email = %s, state = %s, endpoint = %s where id = %s"""
            cursor.execute(sql_query, [json.dumps(api_sms), json.dumps(api_email), "Activate", endpoint, account_id])
            conn.commit()
            x = SMTPServer(admin_email, admin_password)
            x.adminSend({
                "to_email": json.loads(response[7])["email"],
                "subject": "SUCCESSFUL ACCOUNT ACTIVATION",
                "body": """
                <html>
                    <body>
                        <p>Dear client, <br>
                            We would like to inform you that your account has been successfully activated. <br>
                            Your account has been successfully activated! You can now use our services.<br>
                            Thank you for choosing ionextechsolutions
                            For inquires or complaints, contact us through: <br>
                            Email: ionextechsolutions@gmail.com <br>
                            Phone: 0795359098/ 0791216702
                        </p>
                    </body>
                </html>
            """
            })
            return "Successful"
        else:
            return f"Credentials Failed. System results Email: {email_pass_validation} and SMS: {sms_senderid_validation}"
    else:
        return "Failed"

if __name__ == "__main__":
    app.run(debug=True)