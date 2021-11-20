from typing import List, Tuple, Union

from kivy.graphics.vertex_instructions import Quad
from kivy.animation import Animation
from shapely.geometry import Polygon

from geometry.helpers import make_flat
from geometry.point import Point
from geometry.cube.enums import SIDES
from geometry.constants import DRAWING_RATIO


class CubeSide:
    DRAWING_RATIO = DRAWING_RATIO

    def __init__(self, side_name: SIDES, corners: Tuple[Point, ...]):
        self.side_name = side_name
        self.corners = corners

        self.polygon = Polygon(map(self._multiply_by_drawing_ratio, [list(*corner.coords) for corner in self.corners]))

        self.drawn_quad = None

    def __contains__(self, point):
        return self.polygon.contains(point)

    def transform(self):
        modified_coord_values = [
            coord - 15
            if idx in [0, 1, 2, 7]
            else coord + 15
            for idx, coord in enumerate(self.get_corners_coords_flat())
        ]

        anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')
        anim += Animation(points=self.get_corners_coords_flat(), duration=0.4, transition='in_back')

        anim.start(self.drawn_quad)

    def draw(self, texture=None):
        assert self.drawn_quad is None, 'Trying to draw already drawn figure'
        self.drawn_quad = Quad(points=self.get_corners_coords_flat(), texture=texture)

        return self.drawn_quad

    def get_corners_coords_flat(self) -> List[int]:
        """
            make list of coords tuples ---------> [(x1, y1), (x2, y2), ...]
            make it flat -----------------------> [x1, y1, x2, y2, ...]
            multiply each element by ratio -----> [x1 * RATIO, y1 * RATIO, x2 * RATIO, y2 * RATIO, ...]
            return
        """
        coords = list(map(self._multiply_by_drawing_ratio, make_flat([list(*corner.coords) for corner in self.corners])))

        return coords

    def _multiply_by_drawing_ratio(self, initial_coords: Union[int, float, tuple, list]):
        assert isinstance(initial_coords, (int, float, tuple, list)), 'Wrong coords type passed to multiplying method'

        if isinstance(initial_coords, (int, float)):
            coords = initial_coords * self.DRAWING_RATIO
        else:
            coords = tuple(coord * self.DRAWING_RATIO for coord in initial_coords)

        return coords
