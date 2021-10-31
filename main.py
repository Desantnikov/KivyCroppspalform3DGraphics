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

for line_number in range(10):
    cubes_line = [
        Cube(**front_side_gen(bottom_left_corner=Pos((idx * 7) + line_number * 7, line_number * 7), size=10))# - idx / 2))
        for idx
        in range(11, 0, -2)
    ]
    cubes_lines.extend(cubes_line)



class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        self.cube_sides_color_values = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (122, 122, 0),
        ]

        texture = make_texture()
        from calculations.cube import SIDE
        with self.canvas:
            for cube in reversed(cubes_lines):
                for idx, side in enumerate(cube.SIDES_DRAWING_ORDER):
                    cube.sides[side].draw(texture=texture if side == SIDE.FRONT else None)
                    Color(*self.cube_sides_color_values[idx])


class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):

        # Window.height = 1200

        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        my_widget = MyWidget()
        self.add_widget(my_widget)


class MyApp(App):
    def build(self):
        Window.size = (1000, 800)
        Window.top = 100

        self.root = root = RootWidgetBoxLayout()

        return root


if __name__ == '__main__':
    MyApp().run()










