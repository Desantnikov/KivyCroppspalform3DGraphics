from kivy.app import App
from kivy.core.window import Window

from gui.main_app_layout import MainAppLayout


class MainApp(App):
    def build(self):
        Window.size = (1400, 1000)
        Window.top = 40
        Window.left = 100
        # Window.clearcolor = (0.9, 0.9, 0.9)

        self.root = root = MainAppLayout()
