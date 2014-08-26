#!/l/python2.6/bin/python 

import cgi
import cgitb
import os
import sqlite3

import templates
import snippetutils
import db

loggedin = snippetutils.get_logged_in_user()

weeklyreminder = False
data = cgi.FieldStorage();
if (('REQUEST_METHOD' in os.environ)
    and (os.environ["REQUEST_METHOD"] == "POST")):
    if data.has_key("weeklyreminder"):
        weeklyreminder = bool(data["weeklyreminder"].value)

prefs = {"weeklyreminder":weeklyreminder}
db.savepreferences(loggedin, prefs)

print "Content-type: text/html\n"
templates.printheader(loggedin)
print "<p>OK!</p>"

print prefs

templates.printfooter(loggedin)
