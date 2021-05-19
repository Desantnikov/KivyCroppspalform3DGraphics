from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


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

    def sos_signal_activate(self):
        print('\r\n SOS ACTIVATED\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


    def save_and_return_to_main_menu(self, number, sms, call):
        self.number = number
        self.sms = sms == '+'
        self.call = call == '+'

        self.root.current = 'menu'

        print(f'\r\n SAVED:\r\nnumber: {self.number}; sms: {self.sms}; call: {self.call}\r\n')


if __name__ == '__main__':
    MyApp().run()
