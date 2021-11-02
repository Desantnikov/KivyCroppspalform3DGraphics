from kivy.graphics.texture import Texture
from PIL import Image, ImageFilter, ImageDraw

RAD_MULT = 0.25

def make_texture(width):
    gradient = Image.new('RGBA', (width, width), color=(1))
    draw = ImageDraw.Draw(gradient, mode='RGBA')

    for x in range(width):
        for y in range(width):
            start, end = (x, y), (x, y)
            draw.line([start, end],  (255, 255, 255, x), width=1)

    from PIL.Image import BILINEAR, BOX, BICUBIC
    # gradient = gradient.rotate(angle=41, resample=BICUBIC,expand=True, translate=(95, 50))
    # gradient = gradient.effect_spread(distance=10)

    # for line in range(width):
    #     draw.line([(line, line), (width, width)], (1,1,1,line), width=1)
    buf = bytes(gradient.tobytes())

    texture = Texture.create(size=(width, width), bufferfmt='ubyte')
    texture.wrap = 'clamp_to_edge'
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

    # gradient.show()
    return texture