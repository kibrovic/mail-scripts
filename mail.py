#!/usr/bin/env python3
# Module for sending email. Should have defined:
#   from_addr='email'
#   bcc_addr_list='email'
#   login='email'
#   password='app_password'

import smtplib
import gnupg
import os

from configparser import ConfigParser

gpg = gnupg.GPG(gnupghome='%s/.gnupg/' % os.getenv("HOME"))

# Read userinfo config from ./secrets.ini file
secrets_object = ConfigParser()
secrets_object.read("secrets.ini")

userinfo = secrets_object["DEFAULT"]

signature="""
All the best,
  -- Kenan Ibrovic
"""

# Throws error on port 465 so using 587
def sendemail(to_addr_list, cc_addr_list,
              subject, message,
              from_addr=userinfo["USERNAME"],
              bcc_addr_list=[userinfo["USERNAME"]],
              login=userinfo["USERNAME"], password=userinfo["PASSWORD"],
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
#    header += 'Bcc: %s\n' % ','.join(bcc_addr_list)
    header += 'Subject: %s\n\n' % subject

    # Encrypt the message if possible
    encrypted_message = gpg.encrypt(message+signature,[from_addr,''.join(to_addr_list)], sign=True, always_trust=True)

    # Check if it can be encrypted, otherwise sign only
    if encrypted_message.ok == True:
        print("Message will be encrypted for following recipients: " + from_addr + ', ' + ''.join(to_addr_list))
        message = header + str(encrypted_message)
    else:
        print("MESSAGE WILL NOT BE ENCRYPTED FOR FOLOWING RECIPIENTS: " + from_addr + ', ' + ''.join(to_addr_list))
        #terminate = input("Do you want to abort? [y,N]: ") or 'n'
        #if terminate[0].lower() == 'y':
        #    print("TERMINATING...")
        #    return
        #else:
        signed_message = gpg.sign(message+signature)
        message = header + str(signed_message)

    # if bcc is added in header it becomes visible to recipients
    # needs to be passed as argument to address list
    to_addr_list = [to_addr_list] + cc_addr_list + bcc_addr_list

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
