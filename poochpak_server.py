#!/usr/bin/env python
import os
import sys
import json
import time
from datetime import datetime
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

###Importing Sensor Dependencies
from utils.body_temp import *
from utils.heartbeat import heart_rate
from utils.accelerometer import accel
#################################

###Importing Hologram Wrapper Module
from hologram_msg import Hologrammer
#################################

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8925 # Poochpak default

class myHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def do_GET(self):
        tm_stmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hh = Hologrammer()
        payload = {'time': tm_stmp, 
                   'temp' : read_temp(), 
                   'accel': accel(), 
                   'heart': heart_rate(),
                   'geo': hh.get_geo()}

	self.send_response(200)
	self.send_header('Content-type','text/html')
	self.end_headers()
	# Send the html message
	self.wfile.write(json.dumps(payload))
	return

httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), myHandler)
sa = httpd.socket.getsockname()

print "Serving HTTP on", sa[0], "port", sa[1]
httpd.serve_forever()
