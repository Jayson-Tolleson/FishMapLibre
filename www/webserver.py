import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler
import ssl
webdir = '/var/www/'
port = 443
os.chdir(webdir)
srvaddr=('', port)
srvobj = HTTPServer(srvaddr, CGIHTTPRequestHandler)
srvobj.socket = ssl.wrap_socket (srvobj.socket, keyfile='/var/security/lftr.biz.key', certfile='/var/security/lftr.biz.crt', server_side=True)
CGIHTTPRequestHandler.have_fork=False # Force the use of a subprocess
srvobj.serve_forever()
