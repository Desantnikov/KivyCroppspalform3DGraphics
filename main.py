from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty

from plyer import gps, call, sms
from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.utils import platform
from kivy import lib

if platform == 'android':
    from android import AndroidService
    from android.permissions import request_permissions, Permission


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

    def __init__(self):
        super(MyApp, self).__init__()
        Window.bind(on_keyboard=self.test_keyboard)

    def test_keyboard(self, window, key, *args):
        print(f'TEST_KEYBOARD\r\nKey: {key}; Args: {args}')

    def request_android_permissions(self):
        request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION, Permission.CALL_PHONE, Permission.SEND_SMS])

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
        print("Before start gps")
        gps.start(minTime, minDistance)
        print("After start gps")

    def stop(self):
        print("Before stop gps")
        gps.stop()
        print("After stop gps")

    @mainthread
    def on_location(self, **kwargs):
        print("on_location start")
        self.gps_location = {'lat': kwargs['lat'], 'lon': kwargs['lon']}  #' '.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        print("on_location end")

    def sos_signal_activate(self):
        print(f'\r\n SOS ACTIVATED\nnumber: {self.number}; sms: {self.sms}; call: {self.call}; gps: {self.gps_location}\r\n')

        print('MAKING A CALL')
        call.makecall(tel=self.number)
        print('CALL MADE')

        import time
        # this loop works with blocked screen and when app works in background but doesn;t work with closed app
        for x in range(15):
            time.sleep(5)
            print(f'SENDING {x}th SMS ')
            sms.send(recipient=self.number, message=f'Lat: {self.gps_location["lat"]}; Lon: {self.gps_location["lon"]}')
            print('SMS  SENT ')
        # self.service = AndroidService('Sevice example', 'service is running')
        # self.service.start('Hello From Service')



    def save_and_return_to_main_menu(self, number, sms, call):
        self.number = number
        self.sms = sms == '+'
        self.call = call == '+'

        self.root.current = 'menu'

        print(f'\r\n SAVED:\r\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


if __name__ == '__main__':
    MyApp().run()
