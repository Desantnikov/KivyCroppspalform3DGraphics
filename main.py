from itertools import chain

from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from calculations.cube import Cube, SIDE
from calculations.pos import Pos
from shadow_texture import make_texture


ROW_LENGTH = 5

# multipliers
SPACES_X = 6  # two-axis coords
SPACES_Y = 8
CUBE_SIZE = 6

SHADOW_MULTIPLIER = 0.1
SHADOW_DELTA_MULTIPLIER = 0.1

#direct values
X_OFFSET = 0
Y_OFFSET = 0

INITIAL_BRIGHTNESS = 0.8


cubes_array = []
for height_level in range(ROW_LENGTH): #Y_OFFSET, ROW_LENGTH + Y_OFFSET):

    cubes_plot = []
    for row_number in range(ROW_LENGTH):#Y_OFFSET, ROW_LENGTH + Y_OFFSET):

        cubes_row = []
        for cube_number in range(ROW_LENGTH * 2, 0, -2):
            pos = Pos(
                cube_number * SPACES_X + row_number * SPACES_X + X_OFFSET,
                row_number * SPACES_X + (5 + height_level * SPACES_Y),
            )
            cubes_row.append(Cube(front_bottom_left=pos, size=CUBE_SIZE))
        cubes_plot.append(cubes_row)
    cubes_array.append(cubes_plot)



class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        # self.cube_sides_color_values = [
        #     (0.6, 0.6, 0.6),
        #     (1, 1, 1),
        #     (0.3, 0.3, 0.3),
        # ]

        from calculations.cube import SIDE


        self.sides_color_values = {
            side: (
                INITIAL_BRIGHTNESS,
                INITIAL_BRIGHTNESS,
                INITIAL_BRIGHTNESS,
            )
            for side
            in Cube.SIDES_DRAWING_ORDER
        }


        self.sides = []
        with self.canvas:
            for plot_idx, plot in enumerate(cubes_array):  # height (z)

                for row_idx, row in enumerate(reversed(plot)):  # rows from back to front


                    for cube_idx, cube in enumerate(reversed(row)):  # cubes from left to right  #

                        for side_idx, side in enumerate(cube.SIDES_DRAWING_ORDER):


                            def _colors_update(color_tuple, side_shadow_multiplier):
                                if side_shadow_multiplier == 0:
                                    side_shadow_multiplier = 1

                                side_shadow_multiplier = side_shadow_multiplier * SHADOW_MULTIPLIER

                                return [color_part * side_shadow_multiplier for color_part in color_tuple[::]]

                            side_shadow_multiplier_map = {
                                SIDE.TOP: (plot_idx * SPACES_Y) * SHADOW_DELTA_MULTIPLIER,
                                SIDE.FRONT: row_idx * SHADOW_DELTA_MULTIPLIER,
                                SIDE.RIGHT: cube_idx * (SPACES_X + SPACES_Y) * SHADOW_DELTA_MULTIPLIER,
                            }


                            color = self.sides_color_values[side]





                            color_updated = _colors_update(color_tuple=color, side_shadow_multiplier=side_shadow_multiplier_map[side])

                            Color(rgb=color_updated)
                            self.sides.append(cube.sides[side].draw())




                    # list(map(self.canvas.remove, self.sides[-row_idx:]))

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

        Window.size = (1400, 1000)
        Window.top = 20
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
