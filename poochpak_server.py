#!/usr/bin/env python
import os
import sys
import json
import time
from datetime import datetime
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

###Importing Sensor Dependencies
from pulsesensor import Pulsesensor
from adxl345 import ADXL345
from body_temp import *
#################################

#Initializing sensor readings
p = Pulsesensor()
p.startAsyncBPM()
adxl345 = ADXL345()



if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8925

#TODO: Compute MOVING_HR_AVG
MOVING_HR_AVG = 100


class myHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def do_GET(self):
        #result = instance.read()
        #if result.is_valid():
        tm_stmp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = read_temp()[1]
        heart = p.BPM
        accl = adxl345.getAxes(True)
        payload = {'time': tm_stmp, 'temp' : temp, 'accl': accl, 'heart': heart}

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
