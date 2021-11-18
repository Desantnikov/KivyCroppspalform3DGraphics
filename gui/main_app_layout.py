from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Quad
from kivy.uix.floatlayout import FloatLayout

from gui.cubes_widget import CubesWidget
from helpers import make_gradient_texture


class MainAppLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainAppLayout, self).__init__(**kwargs)

        # placeholders for Quad objects
        self.floor = self.left_wall = self.back_wall = None

        self.add_widget(CubesWidget(size=(1200, 1200)))
        with self.canvas.before:
            self._draw_background()

    def _draw_background(self):
        Color(rgb=(1, 1, 1))

        floor_texture = make_gradient_texture(150, 'left_bottom_to_right_top', 75, -90)
        self.floor = Quad(points=[10, 10, 450, 450, 1600, 450, 1600, 10], texture=floor_texture)

        left_wall_texture = make_gradient_texture(200, 'left_bottom_to_right_top', 100, 90)
        self.left_wall = Quad(points=[10, 10, 10, 1200, 450, 1200, 450, 450], texture=left_wall_texture)

        back_wall_texture = make_gradient_texture(200, 'left_bottom_to_right_top', 105)
        self.back_wall = Quad(points=[450, 450, 450, 1600, 1600, 1600, 1600, 450], texture=back_wall_texture)