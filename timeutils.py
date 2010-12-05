#!/usr/bin/env python

"""
Dealing with time.
"""

import datetime
import time

ONEDAY = datetime.timedelta(1)
MONDAY = 0
WEDNESDAY = 2
def mostRecent(weekday):
    if weekday not in range(0,7):
        weekday = MONDAY
    today = datetime.datetime.today()
    cur = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)

    while cur.weekday() != weekday:
        cur -= ONEDAY
    return cur

def weekPrevious(thedate):
    """Given a datetime.datetime, return one week into the past."""
    assert isinstance(thedate, datetime.datetime)
    return thedate - 7 * ONEDAY

def weekForward(thedate):
    """Given a datetime.datetime, return one week into the future."""
    assert isinstance(thedate, datetime.datetime)
    return thedate + 7 * ONEDAY

def isFuture(thedate):
    """Given a date, return True if it's in the future."""
    return thedate > datetime.datetime.today()

def mostRecentMonday():
    """Return the datetime.datetime object for the most recent Monday."""
    return mostRecent(MONDAY)

def onlyDigits(s):
    """Return a string containing just the digits from the input string."""
    return "".join( [c for c in s if c.isdigit()] )

def valid_date(givendt):
    givendt = onlyDigits(givendt)
    ## Acceptable strings are of the form: yyyymmdd
    return len(givendt) == 8

def makedatetime(givendt):
    givendt = onlyDigits(givendt)
    ## Acceptable strings are of the form: yyyymmdd
    assert len(givendt) == 8
    return datetime.datetime.strptime(givendt,"%Y%m%d")

def tostring(thedate):
    assert isinstance(thedate, datetime.datetime)
    return "%04d-%02d-%02d" % (thedate.year, thedate.month, thedate.day)
