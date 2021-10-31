from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from calculations.cube import Cube
from calculations.pos import Pos
from shadow_texture import make_texture


def front_side_gen(bottom_left_corner: Pos, size: int):
    corners_dict = {
        'front_bottom_left': bottom_left_corner,
        'front_top_left': bottom_left_corner.get_transformed_pos(0, size),
        'front_top_right': bottom_left_corner.get_transformed_pos(size, size),
        'front_bottom_right': bottom_left_corner.get_transformed_pos(size, 0),
    }
    return corners_dict

cubes_lines = []


ROW_LENGTH = 10
POSITION_MULTIPLIER = 4



for line_number in range(1, 11):
    cubes_line = [
        Cube(**front_side_gen(bottom_left_corner=Pos((idx * POSITION_MULTIPLIER) + line_number * POSITION_MULTIPLIER, line_number * POSITION_MULTIPLIER), size=5))# - idx / 2))
        for idx
        in range(20, 0, -2)
    ]
    cubes_lines.extend(cubes_line)



class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        self.cube_sides_color_values = [
            (0.6, 0.6, 0.6),  # top
            (1, 1, 1),
            (0.3, 0.3, 0.3),
        ]



        with self.canvas:
            for cube in reversed(cubes_lines):
                for idx, side in enumerate(cube.SIDES_DRAWING_ORDER):
                    cube.sides[side].draw()
                    Color(rgb=self.cube_sides_color_values[idx])


class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        self.bind(
            size=self._update_rect,
            pos=self._update_rect
        )

        my_widget = MyWidget()
        self.add_widget(my_widget)


        with self.canvas.before:
            Color(rgb=(255, 255, 255))

            left_bottom_corner = Pos(0, 800)

            texture = make_texture()
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=texture)


            # self.back_wall = Rectangle()
            # self.rect = Rectangle(pos=self.pos, size=self.size)

    def _update_rect(self, instance, value):

        self.rect.pos = instance.pos
        # self.rect.pos = 400
        # x, y = self.rect.pos
        # self.rect.pos = (x, y+425)

        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        # Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1400, 800)
        Window.top = 100
        Window.left = 100
        # Window.pos(100,100)

        self.root = root = RootWidgetBoxLayout()

        return root


if __name__ == '__main__':
    MyApp().run()










