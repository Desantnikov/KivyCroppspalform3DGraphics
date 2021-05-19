
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty
from android.permissions import request_permissions, Permission
from plyer import gps, call, sms
from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.utils import platform


# Declare both screens
class MenuScreen(Screen):
    def menu_func(self):
        print('\r\n MENU FUNC \r\n')


class SettingsScreen(Screen):
    pass


class MyApp(App):
    number = None
    sms = None
    call = None

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
        self.gps_location = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        print("on_location end")

    def sos_signal_activate(self):
        print(f'\r\n SOS ACTIVATED\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')
        # self.root.children[0].add_widget(Button(text=f'LOCATION: {self.gps_location}'))
        # call.makecall(tel=self.number)
        call.makecall(tel=int(self.number))
        sms.send(recipient=self.number, message='Message avakov chort')

    def save_and_return_to_main_menu(self, number, sms, call):
        self.number = number
        self.sms = sms == '+'
        self.call = call == '+'

        self.root.current = 'menu'

        print(f'\r\n SAVED:\r\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


if __name__ == '__main__':
    MyApp().run()
