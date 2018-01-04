#!/usr/bin/env python
from Hologram.HologramCloud import HologramCloud

class Hologrammer(object):
    def __init__(self):
        from config import DEVICEKEY
        credentials = {'device_key': DEVICEKEY}
        self.hologram = HologramCloud(credentials, network='cellular')
        
    def get_geo(self):
        l = self.hologram.network.location
        if l:
            return {'lat': l.latitude, 'lon': l.longitude, 'time': l.time}
        else:
            return {'lat': 'NA', 'lon': 'NA', 'time': 'NA'}

    def msg_send(self, msg, geo_stamp=True):
        if geo_stamp:
            lat, lon, tm = self.get_geo()
            msg += ' {} {} {}'.format(lat, lon, tm)
        self.hologram.sendMessage(msg, topics=['poochpak'], timeout=20)
        return

if __name__ == '__main__':
    import sys
    msg = sys.argv[1]
    hh = Hologrammer()
    hh.msg_send(msg)


