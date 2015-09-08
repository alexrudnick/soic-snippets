# Introduction #
In these instructions, we'll walk through getting set up so that you can run Snippets on your own computer, so you can help with development. For these instructions, you shouldn't have to install or configure any software other than Python and Subversion.

# Checking out the code #
Go here for how to check out the code:
http://code.google.com/p/soic-snippets/source/checkout

# Making the local database #
Snippets needs a local database to run. So in the directory where you checked out the snippets code, make a directory called "db".

On Linux or Mac (from the command line):
```
## Go to the directory with the snippets code, then make the directory.
$ mkdir -p db
$ ./db.py
```

On Windows (from the command line):
```
REM Go to the directory with the snippets code, then make the directory.
mkdir db
REM Replace this with the path to your Python executable.
c:\Python27\python.exe db.py
```

# Run the test server #
Now just run `testserver.py`. You can optionally specify which port you want to run it on; the default is 8000.

It will print out the url of your snippets test server! By default, this is http://localhost:8000 .

On Windows, it's best to do this from the command line:
```
c:\Python27\python.exe testserver.py
```