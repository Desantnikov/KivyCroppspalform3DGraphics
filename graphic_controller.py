import itertools

from PIL import Image, ImageDraw
from kivy.graphics.texture import Texture
from kivy.graphics.context_instructions import Color

from geometry.enums import SPATIAL_DIRECTION


class GraphicController:
    def __init__(self):
        pass

    @staticmethod
    def set_color(color_tuple):
        color_tuple_length = len(color_tuple)

        if color_tuple_length == 3:
            Color(rgb=color_tuple)

        elif color_tuple_length == 4:
            Color(rgba=color_tuple)

    @classmethod
    def adjust_brightness(cls, side, initial_color, cube_idx, row_idx, plot_idx) -> None:
        """
            used to adjust brightness (shadow) according to current cube's position and side
        """

        side_shadow_multiplier_map = {
            SPATIAL_DIRECTION.TOP: (cube_idx / ((cube_idx + row_idx) / 2)),
            SPATIAL_DIRECTION.FRONT: cube_idx / ((cube_idx + row_idx + cube_idx) / 3),
            SPATIAL_DIRECTION.RIGHT: cube_idx / ((cube_idx + row_idx + row_idx) / 3),
            SPATIAL_DIRECTION.LEFT: cube_idx / ((cube_idx + row_idx + row_idx) / 3),
            SPATIAL_DIRECTION.BACK: cube_idx / ((cube_idx + row_idx + row_idx) / 3),
        }

        side_shadow_multiplier = side_shadow_multiplier_map[side]

        recalculated_color = (color_part * side_shadow_multiplier for color_part in initial_color)

        cls.set_color(tuple(recalculated_color) + tuple([100]))

    @staticmethod
    def make_gradient_texture(width=500, light_direction='left_to_right', brightness_increase=None, rotate=None, height=None):
        if height is None:
            height = width

        gradient = Image.new('RGBA', (width, height), color=1)
        draw = ImageDraw.Draw(gradient, mode='RGBA')

        for x, y in itertools.product(range(width), range(height)):
            color = int((x+y)/2)

            if light_direction == 'downside':
                start, end = (y, x), (y, x)
                color = x

            elif light_direction == 'left_to_right':
                start, end = (x, y), (x, y)
                color = y

            elif light_direction == 'left_bottom_to_right_top':
                start, end = (x, y), (y, x)
            else:
                raise Exception('wrong directon')

            if brightness_increase is not None and color < brightness_increase:
                color = brightness_increase

            draw.line([start, end],  (255, 255, 255, color), width=1)

        # if light_direction == 'right_bottom_to_left_top':
        #     gradient = gradient.rotate(90)
        # if light_direction == 'right_top_to_left_bottom':
        #     gradient = gradient.rotate(90)
        # gradient.show()

        if rotate is not None:
            gradient = gradient.rotate(rotate)

        buf = bytes(gradient.tobytes())

        texture = Texture.create(size=(width, height), bufferfmt='ubyte')
        texture.wrap = 'clamp_to_edge'
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

        return texture
