from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from calculations.cube import Cube
from calculations.pos import Pos


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
        Cube(**front_side_gen(bottom_left_corner=Pos((idx * 10) + line_number * 10, line_number * 10), size=10))# - idx / 2))
        for idx
        in range(0, 11, 2)
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

        with self.canvas:
            for cube in cubes_lines:
                for idx, side in enumerate(cube.SIDES_DRAWING_ORDER):
                    cube.sides[side].draw()
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