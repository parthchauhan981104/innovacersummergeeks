# ---------------------------------------------------IMPORTS------------------------------------------------------------
import sqlite3
import sys
from datetime import datetime
from functools import partial

import entry_management
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

# -----------------------------------------------Global Variables-------------------------------------------------------

text = ''  # text to send as email/sms
currentguest_email = ''
currenthost_email = ''
i = 0  # a variable to help manage the flow of control in guest_submit and host_submit methods


# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------Entry_gui CLASS CODE STARTS-------------------------------------------------

class Entry_gui(object):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon("ui\logoicon.ico"))
        self.mainui = uic.loadUi("ui\main_screen.ui")  # load the ui files
        self.host = uic.loadUi("ui\host.ui")
        self.guest = uic.loadUi('ui\guest.ui')
        self.checkout = uic.loadUi('ui\checkout.ui')
        self.message = uic.loadUi('ui\message.ui')
        self.main_screen()
        self.en = entry_management.Entry()

    def main_screen(self):
        self.checkout.close()
        self.mainui.show()
        self.mainui.guestButton.clicked.connect(self.guest_screen)

    def guest_screen(self):
        self.mainui.close()
        self.guest.show()
        self.guest.guest_submit.clicked.connect(self.guest_submit)

    def host_screen(self):
        self.guest.close()
        self.message.close()
        self.host.show()
        self.host.host_submit.clicked.connect(self.host_submit)

    def checkout_screen(self):
        self.host.close()
        self.message.close()
        self.checkout.show()
        self.checkout.checkout_button.clicked.connect(self.checkout_submit)

    def message_guest(self, message):
        self.message.message_label.setText(message)
        self.message.yes.clicked.connect(self.host_screen)
        self.message.show()

    def message_host(self, message):
        self.message.message_label.setText(message)
        self.message.yes.clicked.connect(self.checkout_screen)
        self.message.show()

    def guest_submit(self):      # action on clicking submit button by guest
        global text
        global currentguest_email
        global i
        name = str(self.guest.nameLineEdit.text())
        phone = str(self.guest.phoneLineEdit.text())
        email = str(self.guest.emailLineEdit.text())
        currentguest_email = email

        now = datetime.now()
        dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))

        conn = sqlite3.connect('entry.db')
        cur = conn.cursor()
        statement = "INSERT INTO VISITORS (FULLNAME, EMAIL, PHONE, INTIME) \
                          VALUES ('name', 'email', 'phone', 'dt_string' )".replace("dt_string", dt_string).replace(
            "name", name).replace("email", email).replace("phone", phone)
        text = 'Guest Visiting\n' + 'Name : ' + name.ljust(12) + '\nPhone : ' + phone.ljust(
            12) + '\nEmail : ' + email.ljust(12)
        try:
            cur.execute(statement)
            conn.commit()
            conn.close()

            self.host_screen()  # ask for host details
        except Exception as e:
            print(e)
            if i == 0:
                i = 1
                self.message_guest(
                    "You have visited before. \nClose dialog and click Submit again to update details. "
                    "\nClick yes if you want previous details to remain.")
                conn.close()
            else:
                ot = "NOT CHECKED OUT"
                statement = "Update VISITORS set OUTTIME = '" + ot + "', FULLNAME = '" + name + "', PHONE = '" + \
                            phone + "'', INTIME = '" + dt_string + "' where EMAIL = '" + currentguest_email + "'"
                print("Details updated for guest")
                conn.commit()
                i = 0
                conn.close()
                self.host_screen()

    def host_submit(self):   # action on clicking submit button by host
        global i
        global currenthost_email
        name = str(self.host.nameLineEdit_2.text())
        phone = str(self.host.phoneLineEdit_2.text())
        email = str(self.host.emailLineEdit_2.text())
        address = str(self.host.addressLineEdit.text())
        currenthost_email = email

        conn = sqlite3.connect('entry.db')
        cur = conn.cursor()
        statement = "INSERT INTO HOSTS (FULLNAME, EMAIL, PHONE, ADDRESS) \
                                  VALUES ('name', 'email', 'phone', 'address' )".replace("address", address).replace(
            "name", name).replace("email", email).replace("phone", phone)
        try:
            cur.execute(statement)
            valid = self.en.email_alert(email, text)  # send email and sms to host with guest details
            self.en.sms_alert(phone, text)
            if valid == 0:
                conn.rollback()  # email incorrect\
                print("Incorrect email")
                self.message_host(
                    "Your email is incorrect. \nClose dialog and click Submit again \nafter inputting correct email."
                    "\nClick yes to continue to checkout screen without email.")
            else:
                conn.commit()
                conn.close()
                self.checkout_screen()
        except Exception as e:
            print(e)
            if i == 0:
                i = 1
                self.message_host(
                    "Your email is already in database. \nClose dialog and click Submit again to update details. "
                    "\nClick yes if you want previous details to persist.")
                conn.close()
            else:
                statement = "Update HOSTS set ADDRESS = '" + address + "', FULLNAME = '" + name + "', PHONE = '" + \
                            phone + "' where EMAIL = '" + currenthost_email + "'"
                print("Details updated for host")
                conn.commit()
                i = 0
                conn.close()
                self.host_screen()

    def checkout_submit(self):   # action on clicking checkout button by guest
        global text
        global i
        now = datetime.now()
        dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))

        conn = sqlite3.connect('entry.db')
        statement = "Update VISITORS set OUTTIME = '" + dt_string + "' where EMAIL = '" + currentguest_email + "'"
        conn.execute(statement)
        conn.commit()

        statement = "SELECT FULLNAME, PHONE, INTIME, OUTTIME FROM VISITORS WHERE EMAIL = '" + currentguest_email + "'"
        cur = conn.cursor()
        cur.execute(statement)
        for row in cur:
            text = 'Visit Details\n' + 'Name : ' + row[0].ljust(12) + '\nPhone : ' + row[1].ljust(
                12) + '\nIn-Time : ' + row[2].ljust(12) + '\nOut-Time : ' + row[3].ljust(12)

        print(text)

        statement = "SELECT FULLNAME, ADDRESS FROM HOSTS WHERE EMAIL = '" + currenthost_email + "'"
        cur = conn.cursor()
        cur.execute(statement)
        for row in cur:
            print(row)
            text += '\n Host Name : ' + row[0].ljust(12) + '\nAddress : ' + row[1].ljust(
                12)
        print(text)
        self.en.email_alert(currentguest_email, text)  # send email to guest with visit details
        i = 0
        conn.close()

        self.main_screen()


# -----------------------------------------Entry_gui CLASS CODE ENDS----------------------------------------------------

# Driver Code
egui = Entry_gui()
sys.exit(egui.app.exec_())
