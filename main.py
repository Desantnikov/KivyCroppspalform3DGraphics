from itertools import chain

from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from calculations.cube import Cube
from calculations.pos import Pos
from shadow_texture import make_texture


ROW_LENGTH = 7
Y_OFFSET = 1
POSITION_MULTIPLIER = 6
HEIGHT_MULTIPLIER = 9
CUBE_SIZE = 6


cubes_array = []
for height_level in range(ROW_LENGTH): #Y_OFFSET, ROW_LENGTH + Y_OFFSET):

    cubes_plot = []
    for row_number in range(ROW_LENGTH):#Y_OFFSET, ROW_LENGTH + Y_OFFSET):

        cubes_row = []
        for cube_number in range(ROW_LENGTH * 2, 0, -2):
            pos = Pos(
                cube_number * POSITION_MULTIPLIER + row_number * POSITION_MULTIPLIER,
                row_number * POSITION_MULTIPLIER + (5 + height_level * HEIGHT_MULTIPLIER),
            )
            cubes_row.append(Cube(front_bottom_left=pos, size=CUBE_SIZE))
        cubes_plot.append(cubes_row)
    cubes_array.append(cubes_plot)


class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        self.cube_sides_color_values = [
            (0.6, 0.6, 0.6),
            (1, 1, 1),
            (0.3, 0.3, 0.3),
        ]

        self.sides = []
        with self.canvas:
            Color(rgb=(self.cube_sides_color_values[2]))

            for plot in cubes_array:
                for row in reversed(plot):
                    for cube in reversed(row):
                        for idx, side in enumerate(cube.SIDES_DRAWING_ORDER):
                            self.sides.append(cube.sides[side].draw())

                            Color(rgb=self.cube_sides_color_values[idx])

        from kivy.animation import Animation
        from calculations.cube import SIDE

        initial_coord_values = cubes_plot[0][0].sides[SIDE.TOP].get_coords()

        modified_coord_values = [
            idx + coord * 20
            if idx % 2
            else
            coord * idx
            for idx, coord
            in enumerate(initial_coord_values)
        ]

        anim = Animation(points=modified_coord_values, duration=3)
        # anim.start(self.sides[-22])
        # anim.start(self.sides[-5])
        # anim.start(self.sides[-30])


class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        self.bind(on_resize=self._update_rect)
        self.draw_background()

        my_widget = MyWidget(size=(500,500))
        self.add_widget(my_widget)

    def draw_background(self):
        with self.canvas.before:
            Color(rgb=(228, 228, 228))

            self.rect = Rectangle(pos=self.pos, size=self.size, texture=make_texture())

            points = [Pos(10, 10), Pos(450, 450), Pos(1600, 450), Pos(1600, 10)]



            pos_coords = chain(*[pos.coords() for pos in points])

            Color(rgb=(0.9, 0.4, 0.4))
            self.rect_two = Quad(points=pos_coords)  # , texture=make_texture(1000))  # , texture=texture)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        self.bind(on_resize=self._update_rect)

        Window.size = (1400, 800)
        Window.top = 100
        Window.left = 100
        # Window.clearcolor = (0.9, 0.9, 0.9, 0.5)

        self.root = root = RootWidgetBoxLayout()

        return root

    def _update_rect(self, instance, value):
        self.top = instance.top
        self.left = instance.left
        self.size = instance.size


if __name__ == '__main__':
    MyApp().run()
