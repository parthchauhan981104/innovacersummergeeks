# ---------------------------------------------------IMPORTS------------------------------------------------------------

import smtplib, ssl
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------ENTRY CLASS CODE STARTS-------------------------------------------------
class Entry(object):
    def __init__(self):

        self.init_db()

    # ----------------------------------------------DATABASE CODE STARTS------------------------------------------------

    def init_db(self):

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

    def execute_statement(self, s):
        conn = sqlite3.connect('entry.db')
        print("Opened database successfully in execute_statement")

        cur = conn.cursor()
        cur.execute(s)
        if 'SELECT' in s:
            for row in cur:
                print(row)

        conn.commit()
        conn.close()

    # ----------------------------------------------EMAIL ALERT - START-------------------------------------------------

    def email(self, receiver_email, text):

        sender_email = "innovacermanager@gmail.com"
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


if __name__ == '__main__':
    en = Entry()
    now = datetime.now()
    dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    print(dt_string)
    # en.email("rb737@snu.edu.in", "Your application for INNOVACER Summer Internship has been blocked.\n Please consult helpdesk for further clarification.\n Innovacer Team")
    en.execute_statement(
        "INSERT INTO HOSTS (FULLNAME, EMAIL, PHONE, ADDRESS) VALUES ('Parth', 'pc828@snu.edu.in', '1234', 'delhi')")

    en.execute_statement("INSERT INTO VISITORS (FULLNAME, EMAIL, PHONE, INTIME) \
                      VALUES ('Paul', 'hah@gmail.com', '12345', 'dt_string')".replace("'date'", dt_string))
    en.execute_statement("SELECT * FROM HOSTS")
