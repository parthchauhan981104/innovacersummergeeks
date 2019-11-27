# innovaccersummergeeks - Entry Management Software.

## Problem Statement
Given the visitors that are there in offices and outside, there is a need to for an entry management
software.
## Description
The application captures the Name, email address, phone no of the visitor and
same information is also captured for the host on the front end.
At the back end, once the visitor enters the information in the form, the backend stores all of
the information with time stamp of the entry.
After host enters information, an email and a SMS are triggered to the host informing him of the details of the visitor.
Later the visitor can checkout, and checkout time is also added to database, this triggers an email to the guest with the complete form which includes:
1. Name
2. Phone
3. Check-in time
4. Check-out time
5. Host name
6. Address visited
## Instructions
Clone the repository, install dependencies using pip install requirements.txt and run GUI.py.
## Approach
Python implemented backend logic.
Used PyQT for GUI.
Sqlite3 for database.
Fast2sms API used to send sms.
Emails sent using email python package.
Two separate files, one with database, email/sms alert related code. The other with GUI and interconnection code.

Basic viable app is made, with minimal GUI.
