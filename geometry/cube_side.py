from typing import Tuple

from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Quad, Line
from kivy.animation import Animation, Parallel

from shapely.geometry import Polygon

from geometry import helpers
from geometry.point import Point
from geometry.enums import SPATIAL_DIRECTION, TRANSFORMATION
from constants import CUBE_SIDE_INITIAL_COLORS_VALUES, TRANSFORMATION_DISTANCE


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
        return Polygon(helpers.pair(self.coords_flat)).contains(point)

    @property
    def coords_flat(self):
        return helpers.flatten(corner.coords_flat for corner in self.corners)

    def draw_side(self):
        assert self.drawn_quad is None, 'Trying to draw already drawn figure'

        self.drawn_quad = Quad(points=self.coords_flat)

    def draw_edges(self):
        assert not self.drawn_edges, 'Trying to draw already drawn edge'

        from operator import attrgetter

        for edge in self.edges.values():
            line = Line(points=list(map(attrgetter('coords_flat'), edge)))
            self.drawn_edges.append(line)

    def edit_drawing(self, new_points: Tuple[int, ...]):
        assert self.drawn_quad is not None, 'Trying to edit not drawn figure'

        self.drawn_quad.points = new_points
        self.corners = list(map(Point, helpers.pair(new_points)))
        self._update_edges()

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

    def transform(self, transformation: TRANSFORMATION):
        if transformation == TRANSFORMATION.MOVE_UP:
            modified_coord_values = [
                coord + TRANSFORMATION_DISTANCE
                if idx % 2
                else coord
                for idx, coord in enumerate(self.coords_flat)
            ]

        elif transformation == TRANSFORMATION.MOVE_DOWN:
            modified_coord_values = [
                coord - TRANSFORMATION_DISTANCE
                if idx % 2
                else coord
                for idx, coord in enumerate(self.coords_flat)
            ]

        elif transformation == TRANSFORMATION.MOVE_RIGHT:
            modified_coord_values = [
                coord + TRANSFORMATION_DISTANCE
                if not idx % 2
                else coord
                for idx, coord in enumerate(self.coords_flat)
            ]

        elif transformation == TRANSFORMATION.MOVE_LEFT:
            modified_coord_values = [
                coord - TRANSFORMATION_DISTANCE
                if not idx % 2
                else coord
                for idx, coord in enumerate(self.coords_flat)
            ]

        elif transformation == TRANSFORMATION.EXPAND_AND_ROTATE:
            if self.side_name == SPATIAL_DIRECTION.FRONT:
                modified_coord_values = [
                    coord + TRANSFORMATION_DISTANCE
                    if idx // 4 == 1
                    else coord - TRANSFORMATION_DISTANCE
                    for idx, coord in enumerate(self.coords_flat, start=1)
                ]
            # another points order for non-front sides
            elif self.side_name == SPATIAL_DIRECTION.RIGHT:
                print('asd')
                modified_coord_values = [
                    coord + TRANSFORMATION_DISTANCE
                    if not idx // 4 == 1
                    else coord - TRANSFORMATION_DISTANCE
                    for idx, coord in enumerate(self.coords_flat, start=1)
                ]
            elif self.side_name == SPATIAL_DIRECTION.TOP:
                modified_coord_values = [
                    coord + TRANSFORMATION_DISTANCE if idx in [2,3,4,6,8]
                    else coord - (TRANSFORMATION_DISTANCE * 3) if idx == 7
                    else coord - TRANSFORMATION_DISTANCE
                    for idx, coord in enumerate(self.coords_flat, start=1)
                ]
            elif self.side_name == SPATIAL_DIRECTION.LEFT:
                modified_coord_values = [
                    coord + TRANSFORMATION_DISTANCE if idx in [4, 6, ]
                    else coord - (TRANSFORMATION_DISTANCE * 3) if idx in [5,7]
                    else coord - TRANSFORMATION_DISTANCE
                    for idx, coord in enumerate(self.coords_flat, start=1)
                ]


        else:
            raise KeyError(f'No such transformation: {transformation}')


        # cube side animation
        anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')
        anim += Animation(points=self.coords_flat, duration=0.4, transition='in_back')

        anim.start(self.drawn_quad)

        # cube edges animation
        anim = Animation(points=modified_coord_values[:4], duration=0.4, transition='out_back')
        anim += Animation(points=self.coords_flat[:4], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[0])

        anim = Animation(points=modified_coord_values[2:6], duration=0.4, transition='out_back')
        anim += Animation(points=self.coords_flat[2:6], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[1])

        anim = Animation(points=modified_coord_values[4:8], duration=0.4, transition='out_back')
        anim += Animation(points=self.coords_flat[4:8], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[2])

        anim = Animation(points=modified_coord_values[6:] + modified_coord_values[:2], duration=0.4, transition='out_back')
        anim += Animation(points=self.coords_flat[6:] + self.coords_flat[:2], duration=0.4, transition='in_back')
        anim.start(self.drawn_edges[3])

