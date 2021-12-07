from kivy.app import App
from kivy import Config
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Quad

from core_app.cubes_widget import CubesWidget
from constants import WINDOW_SIZE
from graphic_controller import GraphicController


class MainApp(App):
    def build(self):
        Window.size = WINDOW_SIZE
        Window.top = 30
        Window.left = 30
        # Window.clearcolor = (0.9, 0.9, 0.9)
        # Window.fullscreen = True

        self.root = CubesWidget()

        with self.root.canvas.before:
            self._draw_background()

    @staticmethod
    def _draw_background():
        GraphicController.set_color((1, 1, 1))

        # drawing floor
        floor_texture = GraphicController.make_gradient_texture(150, 'left_bottom_to_right_top', 75, -90)
        Quad(points=[0, 0, 450, 450, 1640, 450, 1640, 0], texture=floor_texture)

        # drawing left wall
        left_wall_texture = GraphicController.make_gradient_texture(200, 'left_bottom_to_right_top', 100, 90)
        Quad(points=[0, 0, 0, 1200, 450, 1200, 450, 450], texture=left_wall_texture)

        # drawing back wall
        back_wall_texture = GraphicController.make_gradient_texture(200, 'left_bottom_to_right_top', 105)
        Quad(points=[450, 450, 450, 1640, 1640, 1640, 1640, 450], texture=back_wall_texture)
