from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.graphics import *
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Quad
from kivy.uix.floatlayout import FloatLayout

from geometry.cube import Cube
from geometry.pos import Pos
from shadow_texture import make_gradient_texture

ROW_LENGTH = 4 # should be dividable by 2
HEIGHT = 1
DEPTH = 4

# multipliers
SPACES_X = 9 # two-axis coords

CUBE_SIZE = 10

BRIGHTNESS_MULTIPLIER = 0.15 #

#direct values
X_OFFSET = 3
Y_OFFSET = 2

SPACES_Y = 15

INITIAL_BRIGHTNESS = .7

cubes_array = []
for plot_number in range(HEIGHT): #Y_OFFSET, ROW_LENGTH + Y_OFFSET):
    cubes_plot = []
    for row_number in range(DEPTH):#Y_OFFSET, ROW_LENGTH + Y_OFFSET):

        cubes_row = []
        for real_cube_nuber, cube_number in enumerate(range(ROW_LENGTH * 2, 0, -2)):
            pos = Pos(
                x=(cube_number * SPACES_X + row_number * SPACES_X + X_OFFSET),
                y=(row_number * SPACES_X + (5 + plot_number * SPACES_Y)) + Y_OFFSET,
            )
            cubes_row.append(Cube(front_side_bottom_left_corner_pos=pos, size=CUBE_SIZE))


        cubes_plot.append(cubes_row)


    cubes_array.append(cubes_plot)




class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        self.sides_color_values = [
            (0.6, 0.6, 0.6),  # front
            (0.80, 0.80, 0.80),  # top
            (0.95, 0.95, 0.95),  # right
        ]

        from geometry.cube import SIDE
        #

        # self.sides_color_values = {
        #     side: (
        #         INITIAL_BRIGHTNESS,
        #         INITIAL_BRIGHTNESS,
        #         INITIAL_BRIGHTNESS,
        #     )
        #     for side
        #     in Cube.SIDES_DRAWING_ORDER
        # }


        self.sides = []
        with self.canvas:
            for plot_idx, plot in enumerate(cubes_array, start=2):  # height (z)

                for row_idx, row in enumerate(reversed(plot), start=2):  # rows from back to front

                    for cube_idx, cube in enumerate(reversed(row), start=2):  # cubes from left to right  #

                        for side_idx, side in enumerate(cube.SIDES_DRAWING_ORDER):  # cube sides

                            def _colors_update(color_tuple, side_shadow_multiplier):
                                color = []
                                for color_part in color_tuple:
                                    color.append(color_part * side_shadow_multiplier * BRIGHTNESS_MULTIPLIER)

                                return color

                            side_shadow_multiplier_map = {
                                SIDE.TOP:  (plot_idx + plot_idx + plot_idx + cube_idx + row_idx + SPACES_Y + SPACES_X) / 7,
                                SIDE.FRONT: (plot_idx + row_idx + cube_idx + row_idx + row_idx + SPACES_Y + SPACES_X) / 7,
                                SIDE.RIGHT: (cube_idx + plot_idx + cube_idx + row_idx + cube_idx + SPACES_Y + SPACES_X) / 7,
                            }

                            side_shadow_multiplier = side_shadow_multiplier_map[side]

                            color = self.sides_color_values[side]
                            color_updated = _colors_update(color_tuple=color, side_shadow_multiplier=side_shadow_multiplier)


                            Color(rgb=color_updated)
                            cube.sides[side].draw()


    def on_touch_up(self, touch):
        print(touch)
        for z in reversed(cubes_array):
            for x in reversed(z):
                for cube in reversed(x):
                    for side in cube.sides.values():
                        if not side.drawn:
                            continue

                        touch_x = touch.pos[0]
                        touch_y = touch.pos[1]

                        if touch_x > side.corners[0].x * 10 and touch_y > side.corners[0].y * 10:
                            if touch_x < side.corners[2].x * 10 and touch_y < side.corners[2].y * 10:


                                initial_coord_values = side.get_coords()

                                modified_coord_values = [
                                    coord - 15
                                    if idx in [0, 1, 2, 7] else

                                    coord + 15

                                    for idx, coord
                                    in enumerate(initial_coord_values)
                                ]

                                from geometry.cube import SIDE

                                from kivy.animation import Animation
                                anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')

                                anim += Animation(points=initial_coord_values, duration=0.4, transition='in_back')
                                anim.start(side.drawn)


class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        # placeholders for Quad objects
        self.floor = self.left_wall = self.back_wall = None

        self.add_widget(MyWidget(size=(1200, 1200)))
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


class MainApp(App):
    def build(self):
        self.bind(on_resize=self._update_rect)

        Window.size = (1400, 1000)
        Window.top = 40
        Window.left = 100
        # Window.clearcolor = (0.9, 0.9, 0.9)

        self.root = root = RootWidgetBoxLayout()

        return root

    def _update_rect(self, instance, value):
        self.top = instance.top
        self.left = instance.left
        self.size = instance.size


if __name__ == '__main__':
    MainApp().run()


