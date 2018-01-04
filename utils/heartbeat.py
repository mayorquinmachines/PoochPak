#!/usr/bin/env python

def heart_rate():
    from pulsesensor import Pulsesensor
    p = Pulsesensor()
    p.startAsyncBPM()
    try:
	bpm = p.BPM
	if bpm == 0:
	    bpm  = "No Heartbeat found"
	p.stopAsyncBPM()
	return bpm
    except:
        p.stopAsyncBPM()
        return

def test():
    hr_result = heart_rate()
    if hr_result:
        print(hr_result)
        print('Pulse sensor test PASSED')
        return 'PASSED'
    else:
        return

if __name__ == '__main__':
    test()
