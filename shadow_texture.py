from kivy.graphics.texture import Texture
from PIL import Image, ImageFilter, ImageDraw

RAD_MULT = 0.25

def make_gradient_texture(width=500, height=None, light_direction='left_to_right', rotate=None, brightness_increase=None):
    if height is None:
        height = width

    gradient = Image.new('RGBA', (width, height), color=(1))
    draw = ImageDraw.Draw(gradient, mode='RGBA')

    for x in range(width):
        for y in range(height):
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

            if brightness_increase is not None and  color < brightness_increase:
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