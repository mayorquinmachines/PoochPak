#!/usr/bin/env python

def accel():
    from adxl345 import ADXL345
    adxl345 = ADXL345()
    try:
        return adxl345.getAxes(True)
    except:
        return

def test():
    ac_result = accel()
    if ac_result:
        print('Accelerometer test PASSED')
        return 'PASSED'
    else:
        return

if __name__ == '__main__':
    test()
