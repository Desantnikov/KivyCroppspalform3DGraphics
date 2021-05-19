
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty

from plyer import gps
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

    screen_manager = ObjectProperty()

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            print("callback start")
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

            print("callback end")
        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

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

    @mainthread
    def on_status(self, stype, status):
        print("on_status start")
        self.gps_status = 'type={}\n{}'.format(stype, status)
        print("on_status end")

    def sos_signal_activate(self):
        print('\r\n SOS ACTIVATED\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')
        self.root.children[0].add_widget(Button(text=f'LOCATION: {self.gps_location}'))

    def save_and_return_to_main_menu(self, number, sms, call):
        self.number = number
        self.sms = sms == '+'
        self.call = call == '+'

        self.root.current = 'menu'

        print(f'\r\n SAVED:\r\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


if __name__ == '__main__':
    MyApp().run()
