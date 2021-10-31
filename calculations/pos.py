from dataclasses import dataclass
from typing import Union


@dataclass
class Pos:
    x: Union[int, float]
    y: Union[int, float]

    def get_transformed_pos(self, transform_x, transform_y):
        x = self.x + transform_x
        y = self.y + transform_y
        return Pos(x, y)

    def coords(self):
        return self.x, self.y