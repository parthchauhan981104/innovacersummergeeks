# ---------------------------------------------------IMPORTS------------------------------------------------------------
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from functools import partial
from datetime import datetime
import entry_management

# -----------------------------------------------Global Variables-------------------------------------------------------

text = ''
currentguest_email = ''
currenthost_email = ''


# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------Entry_gui CLASS CODE STARTS-------------------------------------------------

class Entry_gui(object):
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main = uic.loadUi("main_screen.ui")  # load the ui files
        self.host = uic.loadUi("host.ui")
        self.guest = uic.loadUi('guest.ui')
        self.checkout = uic.loadUi('checkout.ui')
        self.main_screen()
        self.en = entry_management.Entry()

    def main_screen(self):
        self.main.show()
        self.main.guestButton.clicked.connect(self.guest_screen)
        self.main.hostButton.clicked.connect(self.host_screen)

    def guest_screen(self):
        self.guest.show()
        self.guest.guest_submit.clicked.connect(self.guest_submit)

    def host_screen(self):
        self.host.show()
        self.host.host_submit.clicked.connect(self.host_submit)

    def checkout_screen(self):
        self.checkout.show()
        self.checkout.checkout_button.clicked.connect(self.checkout_submit)

    def guest_submit(self):
        global text
        global currentguest_email
        name = str(self.guest.nameLineEdit.text())
        phone = str(self.guest.phoneLineEdit.text())
        email = str(self.guest.emailLineEdit.text())
        currentguest_email = email

        now = datetime.now()
        dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
        statement = "INSERT INTO VISITORS (FULLNAME, EMAIL, PHONE, INTIME) \
                          VALUES ('name', 'email', 'phone', 'dt_string' )".replace("dt_string", dt_string).replace(
            "name", name).replace("email", email).replace("phone", phone)
        self.en.execute_statement(statement)

        text = 'Guest Visiting\n' + 'Name : ' + name.ljust(12) + '\nPhone : ' + phone.ljust(
            12) + '\nEmail : ' + email.ljust(12)

        self.host_screen()  # ask for host details

    def host_submit(self):
        name = str(self.guest.nameLineEdit2.text())
        phone = str(self.guest.phoneLineEdit2.text())
        email = str(self.guest.emailLineEdit2.text())
        address = str(self.guest.addressLineEdit.text())

        statement = "INSERT INTO HOSTS (FULLNAME, EMAIL, PHONE, ADDRESS) \
                                  VALUES ('name', 'email', 'phone', 'address' )".replace("address", address).replace(
            "name", name).replace("email", email).replace("phone", phone)
        self.en.execute_statement(statement)

        self.en.email_alert(email, text)  # send email and sms to host with guest details
        self.en.sms_alert(phone, text)

    def checkout_submit(self):
        global text
        now = datetime.now()
        dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
        statement = "Update VISITORS set OUTTIME = '" + dt_string + "' where EMAIL = '" + currentguest_email + "'"
        self.en.execute_statement(statement)


        conn = sqlite3.connect('entry.db')

        statement = " SELECT FULLNAME, PHONE, INTIME, OUTTIME FROM VISITORS WHERE EMAIL = '" + currentguest_email + "')"
        cursor = conn.cursor()
        cursor.execute(statement)
        for row in cursor:
            text = 'Visit Details\n' + 'Name : ' + row[0].ljust(12) + '\nPhone : ' + row[1].ljust(
                12) + '\nIn-Time : ' + row[2].ljust(12) + '\nOut-Time : ' + row[3].ljust(12)

        statement = " SELECT FULLNAME, ADDRESS FROM HOSTS WHERE EMAIL = '" + currenthost_email + "')"
        cursor = conn.cursor()
        cursor.execute(statement)
        for row in cursor:
            text += '\n Host Name : ' + row[0].ljust(12) + '\nAddress : ' + row[1].ljust(
                12)

        self.en.email_alert(currentguest_email, text)  # send email to guest with visit details
        conn.close()

        self.main_screen()


# -----------------------------------------Entry_gui CLASS CODE ENDS----------------------------------------------------

egui = Entry_gui()

sys.exit(egui.app.exec_())
