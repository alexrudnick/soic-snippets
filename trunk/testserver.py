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
    cgi_directories = [""]

    def is_cgi(self):
        if CGIHTTPServer.CGIHTTPRequestHandler.is_cgi(self):
            if self.is_executable(self.translate_path(self.path)):
                return True
        return False

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.cgi"
        return CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)

import sys
def main():
    PORT = 8000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])

    httpd = BaseHTTPServer.HTTPServer(("", PORT), Handler)
    print ("Serving snippets at: http://localhost:%d/" % (PORT,))
    httpd.serve_forever()

if __name__ == "__main__": main()
