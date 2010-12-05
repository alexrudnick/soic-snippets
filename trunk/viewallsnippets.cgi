#!/usr/bin/env python

import cgi
import cgitb
import os
import sqlite3

import templates
import db
import snippetutils
import timeutils

print "Content-type: text/html\n"

loggedin = snippetutils.get_logged_in_user()
templates.printheader(loggedin)

# Get the start date. By default, it's the most recent Monday.
data = cgi.FieldStorage();
if data.has_key("start") and timeutils.valid_date(data["start"].value):
    start = timeutils.makedatetime(data["start"].value)
else:
    start = timeutils.mostRecentMonday()

templates.print_week_links(start, "viewallsnippets")

end = timeutils.weekForward(start)
rows = db.getallsnippets(timeutils.tostring(start), timeutils.tostring(end))

template = templates.loadtemplate("onesnippet")
if not rows:
    print "<p>No matching snippets found?</p>"
for row in rows:
    username = cgi.escape(row["username"])
    snip = snippetutils.linebreaks(cgi.escape(row["snip"]))
    time = row["time"]
    print template.substitute(USERNAME=username, TIMESTAMP=time, SNIP=snip)

templates.print_week_links(start, "viewallsnippets")
templates.printfooter(loggedin)
