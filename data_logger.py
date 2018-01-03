#!/usr/bin/env python
import os
import requests
import ast
import time
import numpy as np
from datetime import datetime

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
            f = open('poochpak_log.txt', 'a')
            x = data['accl']['x']
            y = data['accl']['y']
            z = data['accl']['z']
            f.write('{},{},{},{},{},{}\n'.format(data['time'], data['temp'], data['heart'], x, y, z))
            f.close()
            body = 'Notification Log \n Time: {}\n'.format(data['time'])
            if data['heart'] > 150:
                body += 'Heart Rate Elevated: {} \n'.format(data['heart'])
            if np.abs(data['temp'] - 102) > 5:
                body += 'Temperature Warning: {} F\n'.format(data['temp'])
            if data['accl'] != {'x': 0, 'y': 0, 'z': 0}:
                body += 'Motion Detected: {}\n'.format(data['accl'])
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
