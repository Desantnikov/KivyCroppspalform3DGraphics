from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty
from plyer import gps, call, sms
from kivy.app import App, Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Line, Rectangle, Quad, Color, Point, Translate, RenderContext, ApplyContextMatrix
from kivy.graphics import PushMatrix, PopMatrix, UpdateNormalMatrix, Rotate, Scale
from kivy.graphics.transformation import Matrix
from kivy.clock import mainthread
from kivy.utils import platform
from kivy import kivy_examples_dir
from kivy.uix.button import Button

from enum import Enum, IntEnum
from dataclasses import dataclass

from typing import List


from kivy.graphics import UpdateNormalMatrix

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

from kivy.graphics.opengl import glViewport
import time

@dataclass
class CubeSide:
    side: CUBE_SIDES
    corners: List[Pos]


class MyWidget(Widget):
    def __init__(self, **kwargs):
        # self.canvas = RenderContext()#use_parent_modelview=True)

        super(MyWidget, self).__init__(**kwargs)
        self.canvas = RenderContext(use_parent_projection=True)

    def first(self, *args):
        with self.canvas:
            self.rect = Rectangle(pos=(0,0), size=(250, 250))

        print('Rect done')

    def second(self, *args):
        # self.qwe()

        # self.render_context['modelview_mat'] = projection_mat
        # with self.render_context:

        # glViewport(0, 0, 800, 600)

        self.canvas['modelview_mat'] = Matrix().scale(1.5,1,1)
        # self.canvas['projection_mat'] = Matrix().scale(1,2,1)

            # Scale(1, 1, 2)

        # mtr = PushMatrix(projection_mat)

        self.canvas.ask_update()

        print('Second done')
        return
        # with self.canvas:
        # # self.add_widget()
        #     Rectangle(size=(150, 50), pos=(25, 25))
        # return

        from math import radians
        w, h = 800, 600
        w2, h2 = w / 2., h / 2.
        r = radians(45)

        projection_mat = Matrix()
        projection_mat.view_clip(0.0, w, 0.0, h, -1.0, 1.0, 0)
        # self.render_context['projection_mat'] = projection_mat

        # do modelview matrix
        modelview_mat = Matrix().translate(w2, h2, 0)
        modelview_mat = modelview_mat.multiply(Matrix().rotate(r, 0, 0, 1))

        w, h = self.size
        w2, h2 = w / 2., h / 2.
        modelview_mat = modelview_mat.multiply(Matrix().translate(-w2, -h2, 0))
        modelview_mat = Matrix().scale(1,2,1)
        # self.render_context['modelview_mat'] = projection_mat




class RootWidgetBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)
        my_widget = MyWidget()

        self.add_widget(my_widget)

        btn1 = Button(text="asdqwdqwdq", size_hint=(0.3, 0.5))
        btn1.bind(on_press=my_widget.first)

        btn2 = Button(text="Second", size_hint=(0.3, 0.5))
        btn2.bind(on_press=my_widget.second)

        self.add_widget(btn1)
        self.add_widget(btn2)



class MyApp(App):
    def build(self):
        self.root = root = RootWidgetBoxLayout()
        # self.root.add_widget(Button(text="asdasdas"))
        # self.root.add_widget(Button(text="asdasdas"))
        # with root.canvas.before:
        #     Color(0, 1, 0, 1)  # green; colors range from 0-1 not 0-255
        #     self.rect = Rectangle(size=root.size, pos=root.pos)

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