from kivy.graphics.texture import Texture
from PIL import Image, ImageFilter, ImageDraw

RAD_MULT = 0.25

def make_texture(width=500):
    gradient = Image.new('RGBA', (width, width), color=(1,255,1,1))
    draw = ImageDraw.Draw(gradient)

    for x in reversed(range(width)):
        for y in reversed(range(width)):
            start = (x, y)
            end = (y, x)
            draw.line([start, end],  (1, 1, 1, int(x)), width=1)

    # for line in range(width):
    #     draw.line([(line, line), (width, width)], (1,1,1,line), width=1)
    buf = gradient.tobytes()

    texture = Texture.create(size=(500, 500), bufferfmt='ubyte')
    texture.wrap = 'clamp_to_edge'
    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
    # gradient.show()
    return texture