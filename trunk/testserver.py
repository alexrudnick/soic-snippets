#!/usr/bin/env python

"""
Test server for running Snippets system without having to set up Apache.

Run this from the main snippets directory and it'll serve executable files in
your current working directory.

./testserver.py

Or specify a port:
./testserver.py 8888

Probably don't run this on a machine on the open Internet; for
development/testing purposes only.
"""

import CGIHTTPServer
import BaseHTTPServer

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    cgi_directories = ["", "/"]

    def is_executable(self, path):
        """Overrides the superclass is_executable."""
        if (CGIHTTPServer.CGIHTTPRequestHandler.is_executable(self, path)):
            return True
        if self.is_python(path):
            return True
        return False

    def is_python(self, path):
        """Return True if the superclass thinks its true, or if the path ends
        with .cgi"""
        if (CGIHTTPServer.CGIHTTPRequestHandler.is_python(self, path)):
            return True
        if path.endswith(".cgi"):
            return True
        return False

    def is_cgi(self):
        if CGIHTTPServer.CGIHTTPRequestHandler.is_cgi(self):
            path = self.translate_path(self.path)
            if self.is_executable(path) or path.endswith(".cgi"):
                return True
        return False

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.cgi"
        return CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)

import sys
def main(argv=[]):
    PORT = 8000
    if len(argv) > 1:
        PORT = int(argv[1])

    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    print ("Serving snippets at: http://localhost:%d/" % (PORT,))
    httpd.serve_forever()

if __name__ == "__main__": main(sys.argv)
