import itertools

from kivy.uix.widget import Widget

from geometry.cube_from_cubes import CubeFromCubes
from geometry.point import Point

from graphic_controller import GraphicController
from kivy.graphics import RenderContext, Color, Rectangle, BindTexture

class CubesWidget(Widget):
    def __init__(self, **kwargs):
        super(CubesWidget, self).__init__(**kwargs)

        import time
        start_time = time.time()

        self.cube_from_cubes = CubeFromCubes()

        cube_from_cubes_creation_time = time.time() - start_time




        with self.canvas:
            GraphicController.set_color((0.5, 0.5, 0.5))
            # grad = GraphicController.make_gradient_texture(100, 'left_bottom_to_right_top', 75, -90)
            # Color(rgb=(0.5,0.5,0.5))

            self._draw_cubes()



        drawing_time = time.time() - (start_time + cube_from_cubes_creation_time)

        print(f'\nCalculating cubes: {cube_from_cubes_creation_time}\n'
              f'Drawing cubes: {drawing_time}\n')

    # def on_touch_up(self, touch):
    #     import time
    #
    #     start_time = time.time()
    #
    #     touch_point = Point(*touch.pos)
    #
    #
    #     for plot in self.cube_from_cubes.array[::-1]:
    #         for row in plot:
    #             for cube in row[::-1]:
    #                 if touch_point in cube:
    #                     cube.transform()
    #                     print(f'Took: {time.time() - start_time}')
    #                     return

    def _draw_cubes(self):
        for plot in self.cube_from_cubes.array:  # height (z)
            for row in plot[::-1]:  # rows from back to front
                for cube in row[::-1]:  # cubes from left to right  #
                    # GraphicController.set_color((1.1, 1, 1))
                    cube.draw()
