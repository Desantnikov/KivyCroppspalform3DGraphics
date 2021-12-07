from typing import Tuple

from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Quad, Line
from kivy.animation import Animation, Parallel

from shapely.geometry import Polygon

from geometry import helpers
from geometry.point import Point
from geometry.enums import SPATIAL_DIRECTION, TRANSFORMATION
from constants import CUBE_SIDE_INITIAL_COLORS_VALUES


class CubeSide:
    __slots__ = ['side_name', 'corners', 'edges', 'drawn_quad', 'drawn_edges']

    INITIAL_COLORS_RGB = CUBE_SIDE_INITIAL_COLORS_VALUES

    def __init__(self, side_name: SPATIAL_DIRECTION, corners: Tuple[Point, ...]):
        self.side_name = side_name
        self.corners = corners
        self.edges = {}
        self.drawn_quad = None
        self.drawn_edges = []

        self._update_edges()

    def __contains__(self, point):
        return Polygon(self.coords).contains(point)

    @property
    def coords(self):  #
        if self.drawn_quad is None:
            return tuple(corner.coords_flat for corner in self.corners)
        else:
            return helpers.pair(self.drawn_quad.points)

    def draw_side(self):
        assert self.drawn_quad is None, 'Trying to draw already drawn figure'

        self.drawn_quad = Quad(points=helpers.flatten(self.coords))

    def draw_edges(self):
        assert not self.drawn_edges, 'Trying to draw already drawn edge'

        from operator import attrgetter

        for edge in self.edges.values():
            line = Line(points=list(map(attrgetter('coords_flat'), edge)))
            self.drawn_edges.append(line)

    def edit_drawing(self, points: Tuple[int, ...]):
        assert self.drawn_quad is not None, 'Trying to edit not drawn figure'

        self.drawn_quad.points = points
        self.corners = list(map(Point, helpers.pair(points)))
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

        else:
            raise KeyError(f'No such transformation: {transformation}')


        # cube side animation
        side_anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')
        side_anim += Animation(points=helpers.flatten(self.coords), duration=0.4, transition='in_back')

        side_anim.start(self.drawn_quad)

        # cube edges animation
        anim = Animation(points=modified_coord_values[:4], duration=0.4, transition='out_back')
        anim += Animation(points=helpers.flatten(self.coords)[:4], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[0])

        anim = Animation(points=modified_coord_values[2:6], duration=0.4, transition='out_back')
        anim += Animation(points=helpers.flatten(self.coords)[2:6], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[1])

        anim = Animation(points=modified_coord_values[4:8], duration=0.4, transition='out_back')
        anim += Animation(points=helpers.flatten(self.coords)[4:8], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[2])

        anim = Animation(points=modified_coord_values[6:] + modified_coord_values[:2], duration=0.4, transition='out_back')
        anim += Animation(points=helpers.flatten(self.coords)[6:] + helpers.flatten(self.coords)[:2], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[3])

    def _update_edges(self):
        self.edges = {
            SPATIAL_DIRECTION.LEFT: (self.corners[0], self.corners[1]),
            SPATIAL_DIRECTION.TOP: (self.corners[1], self.corners[2]),
            SPATIAL_DIRECTION.RIGHT: (self.corners[2], self.corners[3]),
            SPATIAL_DIRECTION.BOTTOM: (self.corners[3], self.corners[0]),
        }

        for idx, drawn_edge in enumerate(self.drawn_edges):
            if idx == 3:
                drawn_edge.points = self.corners[idx].coords_flat + self.corners[0].coords_flat
                continue

            drawn_edge.points = self.corners[idx].coords_flat + self.corners[idx + 1].coords_flat