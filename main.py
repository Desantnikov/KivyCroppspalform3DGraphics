from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import ObjectProperty, StringProperty
from plyer import gps, call, sms
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.graphics import Line, Rectangle, Quad, Color
from kivy.clock import mainthread
from kivy.utils import platform
from kivy import kivy_examples_dir

class MyApp(App):
    pass



# class Square:
#     def __init__(self, top_left, top_right, ):

class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)

        Window.bind(on_keyboard=self.te)

    def on_enter(self, *args):

        TEXTURE_SIZE = 255
        texture = Texture.create(size=(TEXTURE_SIZE, TEXTURE_SIZE), bufferfmt='ubyte')
        texture.wrap = 'clamp_to_edge'


        import itertools



        border_width = 5

        buf = []
        for y in range(TEXTURE_SIZE):
            buf.append([])
            # print(f'Y: {y}')
            for x in range(TEXTURE_SIZE):
                buf[-1].extend([255, 255, 255, y + 1]) # - gradient from up to down


        for row_number, row_data in enumerate(buf[::]):
            buf[row_number] = bytes(row_data)

        # buf = [[x, y] for x, y in itertools.product(range(size), range(size))]

        buf = b''.join(itertools.chain(buf))
        # then, convert the array to a ubyte string
        # buf = ''.join(map(chr, buf)).encode()

        # then blit the buffer
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

        rect_size = TEXTURE_SIZE
        with self.canvas:
            Color(rgb=(1, 1, 1))
            rect = Rectangle(texture=texture, pos=(150, 250), size=(rect_size, rect_size))#, size=(50,50), joint=False, close=False)

    def te(self, *args, **kwargs):
        print(f'{args}\n{kwargs}')
        # with self.

        self.canvas.add(Line(points=(50, 10, 150, 150), width=2))

        # self.canvas.rect.scale(2)

if __name__ == '__main__':
    MyApp().run()
