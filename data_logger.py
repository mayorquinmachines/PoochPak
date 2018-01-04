#!/usr/bin/env python
import os
import requests
import ast
import time
import numpy as np
from datetime import datetime
from hologram_msg import Hologrammer

INTERVAL_SEC = 30

def night_mode():
    now = datetime.now()
    if now.replace(hour=12) > now > now.replace(hour=4):
        return True
    else:
        return False


while True:
    try:
        r = requests.get('http://localhost:8925')
        if r.status_code == 200:
            data = ast.literal_eval(r.text)
            if not os.path.exists('./poochpak_log.txt'):
                f = open('poochpak_log.txt', 'w')
                f.write('time,temp,heart,acc_x,acc_y,acc_z,geo_lat,geo_lon\n'
                f.close()
            else:
                f = open('poochpak_log.txt', 'a')
                acc = data['accel']
                geo = data['geo']
                if geo:
                    lat, lon = geo.lat, geo.lon
                else:
                    lat, lon = 'NA', 'NA'
                f.write('{},{},{},{},{},{},{},{}\n'.format(data.time, data.temp, data.heart, 
                                                           acc.x, acc.y, acc.z,
                                                           lat, lon))
                f.close()
                body = 'Notification Log \n Time: {}\n'.format(data['time'])
                if data['heart'] > 150:
                    body += 'Heart Rate Elevated: {} \n'.format(data['heart'])
                if np.abs(data['temp'] - 102) > 5:
                    body += 'Temperature Warning: {} F\n'.format(data['temp'])
                if data['accel'] != {'x': 0, 'y': 0, 'z': 0}:
                    body += 'Motion Detected: {}\n'.format(data['accel'])
                if ('Warning' in body) or ('Motion' in body) or ('Elevated' in body):
                    print(body)
        else:
            pass
        time.sleep(INTERVAL_SEC)
    except:
	print('Exceptions!')
        time.sleep(INTERVAL_SEC)

"""
                email_usr = os.environ['email_usr']
                email_pwd = os.environ['email_pwd']
                email_addr = os.environ['email_addr']
                subject = 'system stats'
                if night_mode():
                    client.messages.create(to=os.environ['rec_num'], 
                                           from_=os.environ['twilio_num'], 
                                           body=body)
                else:
                    send_email(email_usr, email_pwd, email_addr, subject, body)

"""
