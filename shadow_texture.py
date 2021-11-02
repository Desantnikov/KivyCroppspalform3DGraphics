from kivy.graphics.texture import Texture
from PIL import Image, ImageFilter, ImageDraw

RAD_MULT = 0.25

def make_gradient_texture(width, light_direction, rotate=None):
    gradient = Image.new('RGBA', (width, width), color=(1))
    draw = ImageDraw.Draw(gradient, mode='RGBA')

    for x in range(width):
        for y in range(width):
            if light_direction == 'downside':
                start, end = (x, y), (x, y)
            elif light_direction == 'left_to_right':
                start, end = (x, x), (y, x)
            elif light_direction == 'left_bottom_to_right_top':
                start, end = (x, y), (y, x)
            else:
                raise Exception('wrong directon')

            draw.line([start, end],  (255, 255, 255, int((x+y)/2)), width=1)


    # if light_direction == 'right_bottom_to_left_top':
    #     gradient = gradient.rotate(90)
    # if light_direction == 'right_top_to_left_bottom':
    #     gradient = gradient.rotate(90)

    if rotate is not None:
        gradient = gradient.rotate(rotate)

    buf = bytes(gradient.tobytes())

    texture = Texture.create(size=(width, width), bufferfmt='ubyte')
    texture.wrap = 'clamp_to_edge'
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

    # gradient.show()
    return texture