# ---------------------------------------------------IMPORTS------------------------------------------------------------

import smtplib, ssl
import requests
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------ENTRY CLASS CODE STARTS---------------------------------------------------
class Entry(object):
    def __init__(self):

        self.init_db()

    # ----------------------------------------------DATABASE CODE STARTS------------------------------------------------

    def init_db(self):  # opens database and create tables

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

        '''cur.execute("INSERT INTO HOSTS (FULLNAME, EMAIL, PHONE, ADDRESS) 
                      VALUES ('Paul', 'hah@gmail.com', '1234', 'delhi')"); '''

        conn.commit()
        # print("Records created successfully")
        conn.close()

    def execute_statement(self, s):  # a general method to execute statement in database
        conn = sqlite3.connect('entry.db')
        print("Opened database successfully in execute_statement")

        cur = conn.cursor()
        cur.execute(s)
        if 'select' in s.lower():
            for row in cur:
                print(row)

        conn.commit()
        conn.close()

    # ----------------------------------------------EMAIL ALERT - START-------------------------------------------------

    def email_alert(self, receiver_email, text):

        sender_email = "innovacermanager@gmail.com"  # an account specially made for this project
        # receiver_email = "pc828@snu.edu.in"
        password = "hytfqvxipmgeuett"  # app specific sender email password

        message = MIMEMultipart("alternative")
        message["Subject"] = "Innovacer Entry Notification"
        message["From"] = sender_email
        message["To"] = receiver_email

        html = """\
        <html>
          <body>
            <p>Hi,<br>
               How are you?<br>
               <a href="http://www.realpython.com">Real Python</a> 
               has many great tutorials.
            </p>
          </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        # part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        # message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
            print("Email sent")
        except:
            print("Email not sent")

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
    en = Entry()
    '''now = datetime.now()
    dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    print(dt_string)
    en.execute_statement(
        "INSERT INTO HOSTS (FULLNAME, EMAIL, PHONE, ADDRESS) VALUES ('Parth', 'pc828@snu.edu.in', '9910421931', 'gurgaon')")

    s = "INSERT INTO VISITORS (FULLNAME, EMAIL, PHONE, INTIME) \
                          VALUES ('Abhishek', 'ac425@snu.edu.in', '9760368229', 'dt_string' )".replace("dt_string",
                                                                                                       dt_string)
    en.execute_statement(s)
    en.execute_statement("SELECT * FROM HOSTS")
    en.execute_statement("SELECT * FROM VISITORS")'''
    # en.email_alert('pc828@snu.edu.in', 'Hi Parth, You are selected at Innovacer for summergeeks Internship.\nRegards,\nTeam Innovacer')
    # en.sms_alert('9910421931', 'Hi Parth')
