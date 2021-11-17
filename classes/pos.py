from typing import Union, Tuple


class Pos:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = int(x)
        self.y = int(y)

    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_transformed_pos(self, add_to_x: int, add_to_y: int):
        x = self.x + add_to_x
        y = self.y + add_to_y
        return Pos(x, y)
