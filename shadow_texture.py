from kivy.graphics.texture import Texture

def make_texture():
    TEXTURE_SIZE = 25
    texture = Texture.create(size=(TEXTURE_SIZE, TEXTURE_SIZE), bufferfmt='ubyte')
    texture.wrap = 'clamp_to_edge'

    import itertools

    buf = []
    for y in range(10, TEXTURE_SIZE):
        buf.append([])
        # print(f'Y: {y}')
        for x in range(TEXTURE_SIZE):
            buf[-1].extend([1, 1, 1, y * 10])  # - gradient from up to down

    for row_number, row_data in enumerate(buf[::]):
        buf[row_number] = bytes(row_data)

    # buf = [[x, y] for x, y in itertools.product(range(size), range(size))]

    buf = b''.join(itertools.chain(buf))

    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

    return texture