#!/l/python2.6/bin/python 
 
# Import smtplib for the actual sending function
# Import the email modules we'll need
import smtplib
from email.mime.text import MIMEText

import db

REMINDER = "/u/alexr/cgi-pub/snippets/reminder.txt"

def buildmessage():
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    with open(REMINDER, 'rb') as fp:
        msg = MIMEText(fp.read())
    msg['Subject'] = 'weekly automatic snippet reminder!'
    msg['From'] = "snippets-noreply@cs.indiana.edu"
    msg['To'] = "alexr@indiana.edu"
    return msg

def sendemails(usernames,ask):
    msg = buildmessage()
    s = smtplib.SMTP("localhost")

    recipients = [("%s@indiana.edu" % (u,)) for u in usernames]
    # print "Sending emails to..."
    # print recipients

    if ask:
        yes = raw_input("OK? (type yes) ")
    else:
        yes = "yes"
    if yes == "yes":
        s.sendmail("snippets-noreply@cs.indiana.edu",
                   recipients,
                   msg.as_string())
        s.quit()
    else:
        print "ok skipping"

import sys
def main():
    if "blast" in sys.argv[1:]:
        usernames = db.geteverybody()
    else:
        usernames = db.getremindees()
    ask = False
    if "ask" in sys.argv[1:]:
        ask = True
    sendemails(usernames, ask)

if __name__ == "__main__": main()
