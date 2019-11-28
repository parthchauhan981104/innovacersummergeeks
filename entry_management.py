# ---------------------------------------------------IMPORTS------------------------------------------------------------

import smtplib
import sqlite3
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests


# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------ENTRY CLASS CODE STARTS---------------------------------------------------
class Entry(object):
    def __init__(self):

        self.init_db()

    # ----------------------------------------------DATABASE CODE STARTS------------------------------------------------

    def init_db(self):  # opens database and create tables

        try:
            conn = sqlite3.connect('entry.db')
            print("Opened database successfully in init_db")

            # conn.execute('''DROP TABLE IF EXISTS COMPANY;''')
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS VISITORS(
                                     FULLNAME         CHAR(50)  NOT NULL,
                                     EMAIL            CHAR(50)  PRIMARY KEY NOT NULL ,
                                     PHONE            CHAR(50)  NOT NULL,
                                     INTIME           CHAR(50)  NOT NULL,
                                     OUTTIME          CHAR(50)  NOT NULL DEFAULT 'NOT CHECKED OUT'
                                     );''')
            print(" VISITORS Table created successfully")

            cur.execute('''CREATE TABLE IF NOT EXISTS HOSTS(
                                     FULLNAME         CHAR(50)  NOT NULL,
                                     EMAIL            CHAR(50)  PRIMARY KEY NOT NULL ,
                                     PHONE            CHAR(50)  NOT NULL,
                                     ADDRESS          CHAR(50)  NOT NULL
                                     );''')
            print(" HOSTS Table created successfully")

            conn.commit()
            # print("Records created successfully")
            conn.close()
            
        except Exception as e:
            print(e)

    def execute_statement(self, s):  # a general method to execute statement in database
        try:
            conn = sqlite3.connect('entry.db')
            print("Opened database successfully in execute_statement")

            cur = conn.cursor()
            cur.execute(s)
            if 'select' in s.lower():
                for row in cur:
                    print(row)

            conn.commit()
            conn.close()
        except Exception as e:
            print(e)

    # ----------------------------------------------EMAIL ALERT - START-------------------------------------------------

    def email_alert(self, receiver_email, text):

        sender_email = "innovacermanager@gmail.com"  # an account specially made for this project
        # receiver_email = "pc828@snu.edu.in"
        password = "hytfqvxipmgeuett"  # app specific sender email password

        message = MIMEMultipart("alternative")
        message["Subject"] = "Innovacer Entry Notification"
        message["From"] = sender_email
        message["To"] = receiver_email

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            print("Email sent")
            return 1
        except:
            print("Email not sent")
            return 0

    # -------------------------------------------------EMAIL ALERT - END------------------------------------------------

    # -------------------------------------------------SMS ALERT - START------------------------------------------------

    def sms_alert(self, receiver_phone, text):  # uses fast2sms API

        try:
            if type(receiver_phone) == 'str':  # if one phone number is sent
                receiver_phone = str(receiver_phone)
            elif type(receiver_phone) == '':  # if list of phone numbers is sent
                receiver_phone = ','.join(str(x).strip() for x in receiver_phone)

            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message=" + text + "&language=english&route=p&numbers=" + receiver_phone
            headers = {
                'authorization': "G5rXPBc3JfkVS2nuQs716omTWlqzb9YNFwve0ipxHdDAILMtyEtHySR2GXwo1NWxArVndQFmMYDZCcIj",
                # API Key
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)

        except Exception as e:
            print(e)

    # ---------------------------------------------------SMS ALERT - END------------------------------------------------


# -----------------------------------------------ENTRY CLASS CODE END---------------------------------------------------


if __name__ == '__main__':
    pass
    #en = Entry()
    #en.execute_statement("SELECT * FROM HOSTS")
    #en.execute_statement("SELECT * FROM VISITORS")
 
