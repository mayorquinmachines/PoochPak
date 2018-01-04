import ..utils.accelerometer 
import ..utils.body_temp
import ..utils.heartbeat

if __name__ == '__main__':
    print('Running tests...')
    accel = accelerometer.test()
    temp = body_temp.test()
    pulse = heartbeat.test()
    if not accel:
        print('NOT PASSED')
        print('Is IC2 enabled? Try enabling it using "sudo raspi-config"')
    if not temp:
        print('NOT PASSED')
        print('Is the line "dtoverlay=w1-gpio" at the end of your /boot/config.txt file?')
        print('Did you run sudo modprobe w1-gpio ?')
        print('Did you run sudo modprobe w1-therm')
        print('If the first item is true, run "sudo reboot" ,then run: "sudo modprobe w1-gpio && sudo modprobe w1-therm"')
    elif not pulse:
        print('NOT PASSED')
        print('Try running "sudo pip install adafruit-mcp3008"')
