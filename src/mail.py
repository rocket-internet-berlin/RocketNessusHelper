#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A Nessus Helper
:copyright: (c) 2016 Rocket Internet SE
:license: GPLv3+, see LICENSE for more details.
"""

__author__ = "Levon Kayan"
__email__ = "levon.kayan@rocket-internet.de"

# own imports


# system imports
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Mail:
    """ Simple mail handler class """

    def __init__(self):
        """ init """

        return

    def buildMail(self, email, files=None):
        """ Build email header and body. Attach files if present. """

        mail = MIMEMultipart()

        mail['Subject'] = email['subject']
        mail['From'] = email['from']
        mail['To'] = email['to']

        mail.attach(MIMEText(email['message']))

        if files:
            for f in files:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(f, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                        'attachment; filename="{0}"'.format(os.path.basename(f)))
                mail.attach(part)

        return mail

    def sendMail(self, server, mail, login=None, tls=False):
        """ Send out an email """

        s = smtplib.SMTP(host=server['addr'], port=int(server['port']))

        if tls:
            s.starttls()
        if login:
            s.login(login['user'], login['pass'])

        s.send_message(mail)
        s.quit()

        return


# EOF
