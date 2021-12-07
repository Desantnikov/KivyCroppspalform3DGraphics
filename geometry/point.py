from typing import Union

from shapely.geometry import point


class Point(point.Point):
    def apply_delta(self, delta_x: Union[int, float], delta_y: Union[int, float]):
        x = self.x + delta_x
        y = self.y + delta_y
        return Point(x, y)

    @property
    def coords_flat(self):
        return self.coords[0]