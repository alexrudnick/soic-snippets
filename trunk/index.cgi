#!/usr/bin/env python

import cgi
import cgitb
import os
import sqlite3

import templates
import snippetutils
import db

print "Content-type: text/html\n"

loggedin = snippetutils.get_logged_in_user()
templates.printheader(loggedin)

template = templates.loadtemplate("inputbox")
print template.substitute(LOGGEDIN=loggedin)

row = db.getonesnippetfor(loggedin)
if row:
    print "<p>Your most recent snippet:</p>"
    template = templates.loadtemplate("onesnippet")
    username = cgi.escape(row["username"])
    snip = snippetutils.linebreaks(cgi.escape(row["snip"]))
    time = row["time"]
    print template.substitute(USERNAME=username, TIMESTAMP=time, SNIP=snip)

templates.printfooter(loggedin)
