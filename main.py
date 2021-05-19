from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class Container(GridLayout):

    text_input = ObjectProperty()
    button = ObjectProperty()
    label = ObjectProperty()

    def change_test(self):
        self.button.text = self.text_input.text


class MyApp(App):
    def build(self):

        return Container()


if __name__ == '__main__':
    MyApp().run()

