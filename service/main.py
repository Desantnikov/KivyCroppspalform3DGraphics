import os
import time
from kivy.utils import platform
from oscpy.server import OSCThreadServer
from time import sleep


def callback(*values):
    print("got values: {}".format(values))
    from plyer import gps, call, sms

    for i in range(15):
        print('SERVICE WORKING WHILE TRUE!!!')
        # sms.send(recipient='+380666127932', message=f'Service working: {i}th iteration')
        time.sleep(5)


osc = OSCThreadServer()  # See sources for all the arguments

# You can also use an \*nix socket path here
sock = osc.listen(address='0.0.0.0', port=8000, default=True)
osc.bind(b'/address', callback)
sleep(1000)
# osc.stop()  # Stop the default socket

# osc.stop_all()  # Stop all sockets

# Here the server is still alive, one might call osc.listen() again

# osc.terminate_server()  # Request the handler thread to stop looping
# osc.join_server()  # Wait for the handler thread to finish pending tasks and exit

# while True:
#     # this will print 'Hello From Service' continually, even when the application is switched
#     print('SERVICE WORKING WHILE TRUE!!!')
#     sms.send(recipient='+380666127932', message=f'Service working: {i}th iteration')
#     time.sleep(5)
#     # i += 1