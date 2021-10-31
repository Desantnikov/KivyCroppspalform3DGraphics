from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty
from plyer import gps, call, sms
from kivy.app import App, Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Line, Rectangle, Quad, Color, Point, Translate, RenderContext, ApplyContextMatrix
from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.clock import mainthread
from kivy.utils import platform
from kivy import kivy_examples_dir
from kivy.uix.button import Button

from enum import Enum, IntEnum
from dataclasses import dataclass

from typing import List, Union, Dict, Tuple



class CUBE_SIDES(IntEnum):
    FRONT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


@dataclass
class Pos:
    x: Union[int, float]
    y: Union[int, float]

    def get_transformed_pos(self, transform_x, transform_y):
        x = self.x + transform_x
        y = self.y + transform_y
        return Pos(x, y)

    def coords(self, coeffitient=10):
        return self.x * coeffitient, self.y * coeffitient

@dataclass
class CubeSide:
    side: CUBE_SIDES
    corners: Tuple[Pos, ...]

    def get_edge_length(self):
        return self.corners[1].y - self.corners[0].y

    def get_coords(self):
        coords = []
        for corner in self.corners:
            coords.extend(corner.coords())

        return coords

    def draw(self):
        Quad(points=self.get_coords())

class Cube:
    def __init__(self, front_side):
        self.sides = {
            CUBE_SIDES.FRONT: front_side,
        }

        self.half_edge_length = self.sides[CUBE_SIDES.FRONT].get_edge_length() / 2

        self.sides[CUBE_SIDES.BACK] = self._calc_back_side()

        self.half_edge_length =

        self.sides[CUBE_SIDES.TOP] = self._calc_top_side()
        self.sides[CUBE_SIDES.RIGHT] = self._calc_right_side()

    def _calc_back_side(self) -> CubeSide:
        back_side = CubeSide(
            side=CUBE_SIDES.BACK,
            corners=tuple(
                corner.get_transformed_pos(
                    transform_x=self.half_edge_length,
                    transform_y=self.half_edge_length,
                )
                for corner in front_side.corners
            ),
        )

        return back_side

    def _calc_top_side(self):
        front_top_edge = self.sides[CUBE_SIDES.FRONT].corners[1], self.sides[CUBE_SIDES.FRONT].corners[2]
        back_top_edge = self.sides[CUBE_SIDES.BACK].corners[1], self.sides[CUBE_SIDES.BACK].corners[2]

        top_side = CubeSide(
            side=CUBE_SIDES.TOP,
            corners=front_top_edge + back_top_edge,
        )

        return top_side

    def _calc_right_side(self):
        front_right_edge = self.sides[CUBE_SIDES.FRONT].corners[2], self.sides[CUBE_SIDES.FRONT].corners[3]
        back_right_edge = self.sides[CUBE_SIDES.BACK].corners[2], self.sides[CUBE_SIDES.BACK].corners[3]

        right_side = CubeSide(
            side=CUBE_SIDES.RIGHT,
            corners=front_right_edge + back_right_edge,
        )

        return right_side


front_bottom_left = Pos(10, 10)
front_top_left = Pos(10, 20)
front_top_right = Pos(20, 20)
front_bottom_right = Pos(20, 10)

front_side = CubeSide(
    side=CUBE_SIDES.FRONT,
    corners=(
        front_bottom_left,
        front_top_left,
        front_top_right,
        front_bottom_right,
    ),
)

cube = Cube(front_side=front_side)










class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        with self.canvas:
            cube.sides[CUBE_SIDES.BACK].draw()
            Color(0, 255, 0)
            #
            # cube.sides[CUBE_SIDES.BACK].draw()
            # Color(255, 0, 0)

            cube.sides[CUBE_SIDES.FRONT].draw()

            Color(0,255,0)
            cube.sides[CUBE_SIDES.TOP].draw()


class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        my_widget = MyWidget()
        self.add_widget(my_widget)


class MyApp(App):
    def build(self):
        self.root = root = RootWidgetBoxLayout()

        return root


if __name__ == '__main__':
    MyApp().run()













# class Cube:
#     def __init__(self, front_side_square_corners: List[Point]):
#         self.front_side_square_corners = front_side_square_corners
#
#         self.size = size
#
#     def _calc_all_vertices(self):
#         top_left_corner = Point().add_point(self.bottom_left_corner.x, 12)



    # def on_pre_enter(self, *args):
    #
    #     TEXTURE_SIZE = 25
    #     import itertools
    #
    #     border_width = 5
    #
    #     buf = []
    #     for y in range(TEXTURE_SIZE):
    #         buf.append([])
    #         # print(f'Y: {y}')
    #         for x in range(TEXTURE_SIZE):
    #             buf[-1].extend([255, 255, 255, y + 1])  # - gradient from up to down
    #
    #
    #     for row_number, row_data in enumerate(buf[::]):
    #         buf[row_number] = bytes(row_data)
    #
    #     # buf = [[x, y] for x, y in itertools.product(range(size), range(size))]
    #
    #     buf = b''.join(itertools.chain(buf))
    #     # then, convert the array to a ubyte string
    #     # buf = ''.join(map(chr, buf)).encode()
    #
    #     self.texture = Texture.create(size=(TEXTURE_SIZE, TEXTURE_SIZE), bufferfmt='ubyte')
    #     self.texture.wrap = 'clamp_to_edge'
    #     # then blit the buffer
    #     self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    #
    #     rect_size = TEXTURE_SIZE
    #     with self.canvas:
    #         Color(255, 0, 0)
    #         self.rect = Rectangle(size=[100, 200], pos=[0,0])#, size=(50,50), joint=False, close=False)


    # def te(self, *args, **kwargs):
    #     print(f'{args}\n{kwargs}')
    #     # with self.
    #     from math import radians
    #
    #     # do projection matrix
    #
    #     w, h = 700, 700
    #     # w2, h2 = w / 2., h / 2.
    #     # r = radians(45)
    #
    #     # projection_mat = Matrix()
    #     # projection_mat.view_clip(0.0, w, 0.0, h, -1.0, 1.0, 0)
    #     # self.canvas['projection_mat'] = projection_mat
    #     #
    #     # # do modelview matrix
    #     # modelview_mat = Matrix().translate(w2, h2, 0)
    #     # modelview_mat = modelview_mat.multiply(Matrix().rotate(r, 0, 0, 1))
    #     #
    #     # w, h = self.size
    #     # w2, h2 = w / 2., h / 2.
    #     # modelview_mat = modelview_mat.multiply(Matrix().translate(-w2, -h2, 0))
    #     projection_mat = Matrix().scale(1,2,1)
    #     self.canvas['projection_mat'] = projection_mat
    #
    #     self.canvas.ask_update()
    #     # self.canvas.rect.scale(2)