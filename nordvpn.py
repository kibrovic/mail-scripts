#!/usr/bin/env python3
# Template for NordVPN account access emails
# Edit codes.csv file with (EMAIL,NAME,NORDVPNCODE)
# Run ./nordvpn.py

import os
from string import Template

import mail
# Get list of recipeints in format: [Email, Name, Code]
# located in same directory as this script
import csv

recipients = []

# Get script's path to find nordvpn.csv file
working_dir=os.path.dirname(os.path.abspath(__file__))
users_file=str(working_dir)+'/codes.csv'

with open(users_file) as csvUsers:
    users = csv.reader(csvUsers)
    for user in users:
        recipients.append(user)

print('List of recipients:\n%s' % recipients)
print()


mail_template=Template("""
Hi $NAME,

Here is the activation code for NordVPN: $NORDVPN_CODE

Enter the following URL in to the address bar
https://nordvpn.com/order/activate/

1. Enter or copy/paste $NORDVPN_CODE in the first field
2. Enter $EMAIL email and password of your choice
3. Click on CREATE ACCOUNT button

After you have created your account, go to https://nordvpn.com/download/
and download the most suitable version for your OS.

Install NordVPN, launch the program and type in your account credentials
to start using the service.

You can use the same e-mail and password for 6 different devices, but
they need to be connected to different NordVPN servers

Quick links:
* Windows 10: https://nordvpn.com/tutorials/windows-10/application/
* Linux: https://nordvpn.com/tutorials/linux/application/
* Mac OS:
https://nordvpn.com/tutorials/x-mac-os-x/app-recommended-for-osx-10-10/

* Android: https://nordvpn.com/tutorials/android/application/
* iOS: https://nordvpn.com/tutorials/ios/application/

If you need any help, please let me know.

""")

for recipient in recipients:
    mail_content = mail_template.substitute(EMAIL=recipient[0], NAME=recipient[1], NORDVPN_CODE=recipient[2])
    mail.sendemail(
        to_addr_list = [recipient[0]],
        cc_addr_list = [''],
        subject      = 'NordVPN Account',
        message      = mail_content,
        )
