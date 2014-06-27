# coding=utf-8
__author__ = 'Wenju'
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.

# Create a text/plain message
msg = MIMEText("This is a test.......")


msg['Subject'] = 'Bill Audit list'
msg['From'] = "svc@mscc.cn"
msg['To'] = "wenju.sun@samsung.com"

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('mail.svc.mscc.cn')
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
