#!/l/python2.6/bin/python 

import sqlite3
import datetime

THEDB = "/u/alexr/cgi-pub/snippets/db/snippetdb"

def savesnippet(snippet, user):
    """Save the snippet to the database, for the specified user, with the
    current time."""

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    # Insert a row of data
    c.execute("insert into snippets values (?,?,?)",
        (snippet, user, datetime.datetime.now()))
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the cursor if we are done with it
    c.close()

def getallsnippets(start=None, end=None):
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if (not start) or (not end):
        rows = (c.execute("select * from snippets order by time desc")
                 .fetchall())
    else:
        rows = c.execute("""select * from snippets
                            where time > ?
                              and time < ?
                         order by time desc""", (start, end)).fetchall()
    return rows

def getsnippetsfor(username):
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("select * from snippets "
                     + "where username = ? "
                     + "order by time desc "
                     , (username,)).fetchall()
    return rows

def getonesnippetfor(username):
    """Get the most recent snippet for the specified user and return it. If
    there are no snippets for that user, return None."""
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    row = c.execute("select * from snippets "
                     + "where username = ? "
                     + "order by time desc "
                     , (username,)).fetchone()
    return row

def getallusers():
    outset = set()
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("select username from snippets "
                     + "order by username desc").fetchall()
    for row in rows:
        outset.add(row["username"])
    out = list(outset)
    out.sort()
    return out

def savesubscription(subscriber, subscribee):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("insert into subscriptions values (?,?)",
        (subscriber, subscribee))
    conn.commit()
    c.close()

def removesubscription(subscriber, subscribee):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("delete from subscriptions " +
              "where subscriber = ? and subscribee = ?",
        (subscriber, subscribee))
    conn.commit()
    c.close()

def getsubscriptions(username):
    """Return a list of all the usernames that the given user is subscribed
    to, in alphabetical order."""
    outset = set()
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rows = c.execute("select * from subscriptions "
                     + "where subscriber = ? "
                     , (username,)).fetchall()
    for row in rows:
        outset.add(row["subscribee"])
    out = list(outset)
    out.sort()
    return out

def getsubscribedsnippets(subscriber, start=None, end=None):
    conn = sqlite3.connect(THEDB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if (not start) or (not end):
        rows = c.execute(
            """select username,snip,time from snippets,subscriptions 
                where subscriptions.subscriber = ? 
                  and subscriptions.subscribee = snippets.username 
             order by time desc """, (subscriber,)).fetchall()
    else:
        rows = c.execute(
            """select username,snip,time from snippets, subscriptions 
                where subscriptions.subscriber = ? 
                  and subscriptions.subscribee = snippets.username 
                  and snippets.time > ?
                  and snippets.time < ?
             order by time desc """, (subscriber,start,end)).fetchall()
    return rows

def getsubscribers(username):
    """Return a list of all the usernames that are subscribed to the given
    user, in alphabetical order."""
    subscriberset = set()
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("select subscriber from subscriptions " \
                "where subscribee=?",
                (username,))
    rows = c.fetchall()
    for r in rows:
        subscriberset.add(r[0])
    subscribers = list(subscriberset)
    subscribers.sort()
    return subscribers

def getallsubscribers():
    """Return a list of all the usernames that are subscribed to anybody,
    in alphabetical order."""
    subscribers = []
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("select distinct subscriber from subscriptions " \
              "order by subscriber")
    rows = c.fetchall()
    for r in rows:
        subscribers.append(r[0])
    return subscribers

def getremindees():
    remindees = []
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("select distinct username from preferences " \
              "where weeklyreminder = 1")
    rows = c.fetchall()
    for r in rows:
        remindees.append(r[0])
    return remindees

def geteverybody():
    """Returns the list of everyone in the system -- everybody who has ever
    posted a snippet or subscribed to someone."""

    subscribers = getallsubscribers()
    posters = getallusers()
    both = set(subscribers + posters)
    everybody = list(both)
    everybody.sort()
    return everybody

def getpreferences(username):
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("select weeklyreminder from preferences " \
              "where username = ?",
              (username,))
    rows = c.fetchall()

    out = {"weeklyreminder":False}
    if len(rows) == 1:
        out["weeklyreminder"] = bool(rows[0][0])
    return out

def savepreferences(username, prefs):
    weeklyreminder = prefs["weeklyreminder"]
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute("insert or replace into preferences values (?,?)",
        (username, weeklyreminder))
    conn.commit()
    c.close()

def main():
    """Initialize tables that we'll need if they're not already created and
    print out all the db contents, just to see what we have."""
    conn = sqlite3.connect(THEDB)
    c = conn.cursor()

    # Create tables that we'll need.
    c.execute("""create table if not exists snippets
    (snip text, username text, time timestamp)""")
 
    c.execute("""create table if not exists subscriptions
    (subscriber text, subscribee text)""")

    c.execute("""create table if not exists preferences
    (username text primary key, weeklyreminder integer)""")

    conn.commit()
    c.close()

    db = sqlite3.connect(THEDB)
    print db.execute("SELECT * FROM snippets").fetchall()
    print db.execute("SELECT * FROM subscriptions").fetchall()
    db.close()

if __name__ == "__main__": main()
