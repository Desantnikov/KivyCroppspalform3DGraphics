from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty
from plyer import gps, call, sms
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Line, Rectangle, Quad, Color, Point, Translate, RenderContext
from kivy.graphics import PushMatrix, PopMatrix, UpdateNormalMatrix, Rotate
from kivy.graphics.transformation import Matrix
from kivy.clock import mainthread
from kivy.utils import platform
from kivy import kivy_examples_dir

from enum import Enum, IntEnum
from dataclasses import dataclass

from typing import List




class CUBE_SIDES(IntEnum):
    FRONT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


@dataclass
class Pos:
    x: int
    y: int


@dataclass
class CubeSide:
    side: CUBE_SIDES
    corners: List[Pos]


# class Cube:
#     def __init__(self, front_side_square_corners: List[Point]):
#         self.front_side_square_corners = front_side_square_corners
#
#         self.size = size
#
#     def _calc_all_vertices(self):
#         top_left_corner = Point().add_point(self.bottom_left_corner.x, 12)


class MenuScreen(Screen):
    layout = ObjectProperty(rebind=True)

    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.canvas = RenderContext(use_parent_projection=True)
        Window.bind(on_keyboard=self.te)

    def on_pre_enter(self, *args):

        TEXTURE_SIZE = 125

        import itertools

        border_width = 5

        buf = []
        for y in range(TEXTURE_SIZE):
            buf.append([])
            # print(f'Y: {y}')
            for x in range(TEXTURE_SIZE):
                buf[-1].extend([255, 255, 255, y + 1])  # - gradient from up to down


        for row_number, row_data in enumerate(buf[::]):
            buf[row_number] = bytes(row_data)

        # buf = [[x, y] for x, y in itertools.product(range(size), range(size))]

        buf = b''.join(itertools.chain(buf))
        # then, convert the array to a ubyte string
        # buf = ''.join(map(chr, buf)).encode()

        self.texture = Texture.create(size=(TEXTURE_SIZE, TEXTURE_SIZE), bufferfmt='ubyte')
        self.texture.wrap = 'clamp_to_edge'
        # then blit the buffer
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

        rect_size = TEXTURE_SIZE
        with self.canvas:
            self.rect = Rectangle(size=(rect_size, rect_size), pos=(rect_size*2, rect_size*2))#, size=(50,50), joint=False, close=False)


    def te(self, *args, **kwargs):
        print(f'{args}\n{kwargs}')
        # with self.

        # with self.canvas:
        projection_mat = Matrix()
        print(projection_mat)
        # projection_mat.rotate(45, 1, 1, 0)
        projection_mat.scale(1.5, 0.5, 5)
        self.canvas['modelview_mat'] = projection_mat
        print(projection_mat)
        # PushMatrix()
            # self.quad = Quad(points=(10, 10, 10, 100, 100, 100, 200, 10))
            # PopMatrix()

        self.canvas.ask_update()
        # self.canvas.rect.scale(2)


class MyApp(App):
    pass

if __name__ == '__main__':
    MyApp().run()
