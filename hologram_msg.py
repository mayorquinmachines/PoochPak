#!/usr/bin/env python

class Hologrammer(object):
    def __init__(self):
        from Hologram.HologramCloud import HologramCloud
        from config import DEVICEKEY
        credentials = {'device_key': DEVICEKEY}
        self.hologram = HologramCloud(credentials, network='cellular')
        
    def get_geo(self):
        l = self.hologram.network.location
        if l:
            return {'lat': l.latitude, 'lon': l.longitude, 'time': l.time}
        else:
            return

    def msg_send(self, msg, geo_stamp=True):
        if geo_stamp:
            lat, lon, tm = self.get_geo()
            msg += ' {} {} {}'.format(lat, lon, tm, topics=['poochpak'])
        hologram.sendMessage(msg)
        return

if __name__ == '__main__':
    hh = Hologrammer()
    msg = 'TEST MESSAGE'
    hh.msg_send(msg)


