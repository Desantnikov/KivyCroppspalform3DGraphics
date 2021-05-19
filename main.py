from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty

from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.utils import platform

__version__ = '0.8.7'


if platform == 'android':
    from android import AndroidService
    from android.permissions import request_permissions, Permission
    from plyer import gps, call, sms


# Declare both screens
class MenuScreen(Screen):
    def menu_func(self):
        print('\r\n MENU FUNC \r\n')


class SettingsScreen(Screen):
    pass


class MyApp(App):
    number = StringProperty(defaultvalue='+380666127932')  # number should be '+38066...s' or '066...'
    gps_location = None
    sms = None
    call = None

    def request_android_permissions(self):
        required_permissions = [
            Permission.ACCESS_COARSE_LOCATION,
            Permission.ACCESS_FINE_LOCATION,
            Permission.CALL_PHONE,
            Permission.SEND_SMS,
            Permission.FOREGROUND_SERVICE,
            Permission.CALL_PRIVILEGED,
        ]

        request_permissions(required_permissions)

    def build(self):
        try:
            gps.configure(on_location=self.on_location)
        except NotImplementedError:
            print('GPS is not implemented for your platform')
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.request_android_permissions()
            print("gps.py: Premissions requested")

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = {'lat': kwargs['lat'], 'lon': kwargs['lon']}

    def sos_signal_activate(self):
        print(f'\r\n SOS ACTIVATED\nnumber: {self.number}; sms: {self.sms}; call: {self.call}; gps: {self.gps_location}\r\n')

        # print('MAKING A CALL')
        # call.makecall(tel=self.number)
        # print('CALL MADE')


        self.service = AndroidService("Started service")#MyService("Started service")

        newline = '\r\n'
        divider = ' ; ----------------->  | '

        # activity = autoclass('org.kivy.android.PythonActivity').mActivity
        # service = autoclass('org.kivy.android.PythonService')  # 'org.test.sos.test.Servicemyservice')
        import random
        # print(f'Activity: {f"{newline}".join([property for property in dir(activity)])}')
        props = [prop for prop in dir(self.service)]
        print(f'service: {newline.join(props)}')

        self.service.start("started service")




    def save_and_return_to_main_menu(self, number, sms, call):
        self.number = number
        self.sms = sms == '+'
        self.call = call == '+'

        self.root.current = 'menu'

        print(f'\r\n SAVED:\r\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


if __name__ == '__main__':
    import re

    version_splitted = __version__.split('.')
    version_splitted[1] = f'{int(version_splitted[1]) + 1}'

    __version__ = '.'.join(version_splitted)

    MyApp().run()

