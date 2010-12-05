#!/l/python2.6/bin/python

"""
templates.py: code for doing simple HTML templating.

Alex Rudnick and Dustin Dannenhauer, Spring 2010
"""

import string
import timeutils

def loadtemplate(name):
    """Create and return a string template object from the file
    templates/<name>.template"""

    try:
        with open("templates/" + name + ".template", "r") as infile:
            bytes = infile.read()
            out = string.Template(bytes)
            return out
    except:
        return string.Template("(template didn't load)")

def printheader(loggedin):
    template = loadtemplate("header")
    print template.substitute(LOGGEDIN=loggedin)

def printfooter(loggedin):
    template = loadtemplate("footer")
    print template.substitute(LOGGEDIN=loggedin)

def print_week_links(start, pagename):
    """Print out the links to move the page one week into the future or into
    the past. start should be passed as a datetime.datetime object, and
    pagename as a string. pagename shouldn't include the .cgi ending -- that's
    appended for you."""

    # Always go one week at a time.
    end = timeutils.weekForward(start)
    prevweek = timeutils.weekPrevious(start)

    print "<p>"
    pagename = "viewallsnippets"
    template = loadtemplate("prevweeklink")
    print template.substitute(START=timeutils.tostring(prevweek),
                              PAGENAME=pagename)

    if not timeutils.isFuture(end):
        template = loadtemplate("nextweeklinks")
        print template.substitute(START=timeutils.tostring(end),
                                  PAGENAME=pagename)
    print "</p>"
