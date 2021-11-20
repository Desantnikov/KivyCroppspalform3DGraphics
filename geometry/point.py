from typing import Union

from shapely.geometry import point


class Point(point.Point):
    def get_transformed_point(self, add_to_x: Union[int, float], add_to_y: Union[int, float]):
        x = self.x + add_to_x
        y = self.y + add_to_y
        return Point(x, y)
