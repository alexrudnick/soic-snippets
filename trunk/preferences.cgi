#!/l/python2.6/bin/python 

import cgi
import cgitb
import os
import sqlite3

import templates
import snippetutils
import db

loggedin = snippetutils.get_logged_in_user()
prefs = db.getpreferences(loggedin)

print "Content-type: text/html\n"
templates.printheader(loggedin)
template = templates.loadtemplate("preferences")


ischecked = ""
if prefs["weeklyreminder"]:
    ischecked = "checked"

print template.substitute(CHECKED=ischecked)

templates.printfooter(loggedin)
