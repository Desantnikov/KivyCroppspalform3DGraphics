from typing import Tuple

from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Quad
from kivy.animation import Animation

from shapely.geometry import Polygon

from geometry import helpers
from geometry.point import Point
from geometry.enums import SPATIAL_DIRECTION, TRANSFORMATION
from constants import CUBE_SIDE_INITIAL_COLORS_VALUES


class CubeSide:
    INITIAL_COLORS_RGB = CUBE_SIDE_INITIAL_COLORS_VALUES

    def __init__(self, side_name: SPATIAL_DIRECTION, corners: Tuple[Point, ...]):
        self.side_name = side_name
        self.corners = corners
        self.edges = {}
        self.drawn_quad = None

        self._update_edges()

    def __contains__(self, point):
        return Polygon(self.coords).contains(point)

    @property
    def coords(self):  #
        if self.drawn_quad is None:
            return tuple(corner.coords[0] for corner in self.corners)
        else:
            return helpers.pair(self.drawn_quad.points)

    def draw(self):
        assert self.drawn_quad is None, 'Trying to draw already drawn figure'

        self.drawn_quad = Quad(points=helpers.flatten(self.coords))

    def edit_drawing(self, points: Tuple[int, ...]):
        assert self.drawn_quad is not None, 'Trying to edit not drawn figure'

        self.drawn_quad.points = points
        self.corners = helpers.pair(points)
        self._update_edges()

    def transform(self, transformation: TRANSFORMATION):
        if transformation == TRANSFORMATION.MOVE_UP:
            modified_coord_values = [
                coord + 15
                if idx % 2
                else coord
                for idx, coord in enumerate(helpers.flatten(self.coords))
            ]

        elif transformation == TRANSFORMATION.MOVE_DOWN:
            modified_coord_values = [
                coord - 15
                if idx % 2
                else coord
                for idx, coord in enumerate(helpers.flatten(self.coords))
            ]

        elif transformation == TRANSFORMATION.MOVE_RIGHT:
            modified_coord_values = [
                coord + 15
                if not idx % 2
                else coord
                for idx, coord in enumerate(helpers.flatten(self.coords))
            ]

        elif transformation == TRANSFORMATION.MOVE_LEFT:
            modified_coord_values = [
                coord - 15
                if not idx % 2
                else coord
                for idx, coord in enumerate(helpers.flatten(self.coords))
            ]

        anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')
        anim += Animation(points=helpers.flatten(self.coords), duration=0.4, transition='in_back')

        anim.start(self.drawn_quad)

    def _update_edges(self):
        self.edges = {
            SPATIAL_DIRECTION.LEFT: (self.corners[0], self.corners[1]),
            SPATIAL_DIRECTION.TOP: (self.corners[1], self.corners[2]),
            SPATIAL_DIRECTION.RIGHT: (self.corners[2], self.corners[3]),
            SPATIAL_DIRECTION.BOTTOM: (self.corners[3], self.corners[0]),
        }