from kivy.graphics.texture import Texture
from PIL import Image, ImageFilter, ImageDraw

RAD_MULT = 0.25

def make_texture(width=600):
    gradient = Image.new('RGBA', (width, width+200), color=(1,255,1,1))
    draw = ImageDraw.Draw(gradient)

    for x in range(width + 400):
        for y in range(width):
            start = (x, y)
            end = (y, x)
            draw.line([start, end],  (1, 1, 1, int(x)), width=1)

    from PIL.Image import BILINEAR
    gradient = gradient.rotate(angle=35, resample=BILINEAR,expand=True)
    # for line in range(width):
    #     draw.line([(line, line), (width, width)], (1,1,1,line), width=1)
    buf = bytes(gradient.tobytes())

    texture = Texture.create(size=(width, width+200), bufferfmt='ubyte', callback=print)
    texture.wrap = 'clamp_to_edge'
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    # gradient.show()
    return texture