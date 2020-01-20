#!/usr/bin/env python3
# Template for MulvadVPN account access emails
# Edit codes.csv file with (EMAIL,NAME,MULLVADVPNCODE)
# Run ./mulvad.py

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

Here is the activation code for MullvadVPN: $MULLVADVPN_CODE

Enter the following URL in to the address bar
https://mullvad.net/en/

1. Click on "Generate account" button
2. Save your account number in KeePassXC. Don't lose it! It's the only identifier to access Mullvad
3. Click on "Voucher" button and enter $MULLVADVPN_CODE
4. Download MulvadVPN app from: https://mullvad.net/en/download/

You can use the same account for 5 different devices.

Quick links:
* MacOS: https://mullvad.net/en/help/install-mullvad-app-macos/
* Windows: https://mullvad.net/en/help/install-mullvad-app-windows/
* Linux: https://mullvad.net/en/help/install-mullvad-app-linux/

Android has tree options, choose one:
* Mullvad App: https://mullvad.net/en/help/install-mullvad-app-android/
* WireGuard: https://mullvad.net/en/help/wireguard-android/
* OpenVPN: https://mullvad.net/en/help/installing-mullvad-android-devices/

iOS has two options, chose one:
* OpenVPN: https://mullvad.net/en/help/installing-mullvad-iphone-and-ipad/
* WireGuard: https://mullvad.net/en/help/wireguard-ios/

If you need any help, please let me know.

""")

for recipient in recipients:
    mail_content = mail_template.substitute(EMAIL=recipient[0], NAME=recipient[1], MULLVADVPN_CODE=recipient[2])
    mail.sendemail(
        to_addr_list = [recipient[0]],
        cc_addr_list = [''],
        subject      = 'MullvadVPN Account',
        message      = mail_content,
        )
