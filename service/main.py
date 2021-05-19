import os
import time
from plyer import gps, call, sms


i = 0

while True:
    # this will print 'Hello From Service' continually, even when the application is switched
    print('SERVICE WORKING WHILE TRUE!!!')
    sms.send(recipient='+380666127932', message=f'Service working: {i}th iteration')
    time.sleep(5)
    i += 1