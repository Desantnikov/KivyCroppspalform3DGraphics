from typing import Tuple
import random

import graphic_controller
from kivy.properties import AliasProperty
from kivy.event import EventDispatcher

from geometry.cube_side import CubeSide
from geometry.point import Point
from geometry.enums import SPATIAL_DIRECTION, TRANSFORMATION
from geometry import helpers
from constants import CUBE_SIDE_INITIAL_COLORS_VALUES, CUBE_SIZE, SPACES_X, SPACES_Y, X_OFFSET, Y_OFFSET, TRANSFORMATION_DISTANCE, FLAT_SQUARE


class Cube:
    __slots__ = ['position_within_parent_cube', 'size', 'sides', 'transformation_in_progress']
    SQUARE_SIDES = set([SPATIAL_DIRECTION.FRONT, SPATIAL_DIRECTION.BACK])
    SIDES_DRAWING_ORDER = [SPATIAL_DIRECTION.BACK, SPATIAL_DIRECTION.LEFT, SPATIAL_DIRECTION.TOP, SPATIAL_DIRECTION.RIGHT, SPATIAL_DIRECTION.FRONT]

    def __init__(self, position_within_parent_cube: Point, size: int = CUBE_SIZE):
        self.position_within_parent_cube = position_within_parent_cube
        self.size = size

        self.transformation_in_progress = False
        self.sides = {}
        self._set_sides(flat_square=FLAT_SQUARE)

    def __contains__(self, point):
        return any(point in side for side in self.drawn_sides)

    @property
    def drawn_sides(self):
        return filter(lambda side: side.drawn_quad, self.sides.values())

    def draw_sides(self):
        for side_name in self.SIDES_DRAWING_ORDER:
            cube_idx, row_idx, plot_idx = self.position_within_parent_cube.coords_flat

            graphic_controller.GraphicController.adjust_brightness(
                side=side_name,
                initial_color=CUBE_SIDE_INITIAL_COLORS_VALUES[side_name.name],
                cube_idx=cube_idx + 1,
                row_idx=row_idx + 1,
                plot_idx=plot_idx + 1,
            )

            self.sides[side_name].draw_side()

    def change_textures(self):
        for side in filter(lambda x: x.drawn_quad, self.sides.values()):
            side.drawn_quad.texture = graphic_controller.GraphicController.make_gradient_texture(
                width=4,
                height=4,
                light_direction='fill',
                fill_color=(255, 1, 1, 255),
            )

    # def change_front_side_points(self, new_points):
    #     for side in filter(lambda x: x.drawn_quad, self.sides.values()):
    #         side.edit_drawing(new_points=new_points)

    def touched(self, touch):
        if touch.button == 'right':
            for side in filter(lambda x: x.drawn_quad, self.sides.values()):
                side.edit_drawing(new_points=[0,0,0,0,0,0,0,0])


        elif touch.button == 'left' and touch.is_double_tap:
            # if touch.is_double_tap:
            self.change_textures()
                # return

        elif touch.button == 'left':
            self._transform(transformation=TRANSFORMATION.EXPAND_AND_ROTATE)

        elif touch.button == 'middle':
            self._transform(transformation=TRANSFORMATION.MOVE_UP)

        elif touch.button == 'scrolldown':
            for side in filter(lambda x: x.drawn_quad, self.sides.values()):
                initial_points = side.drawn_quad.points
                if side.side_name in [SPATIAL_DIRECTION.FRONT, SPATIAL_DIRECTION.BACK, SPATIAL_DIRECTION.LEFT]:
                    to_increment = [3, 5]
                elif side.side_name in [SPATIAL_DIRECTION.RIGHT]:
                    to_increment = [1, 7]
                else:
                    to_increment = [1, 3, 5, 7]

                updated_points = [
                    point + TRANSFORMATION_DISTANCE
                    if idx in to_increment #[3,5, ]
                    else point
                    for idx, point in enumerate(initial_points)
                ]
                side.edit_drawing(new_points=updated_points)

        elif touch.button == 'scrollup':
            for side in filter(lambda x: x.drawn_quad, self.sides.values()):
                initial_points = side.drawn_quad.points
                if side.side_name in [SPATIAL_DIRECTION.FRONT, SPATIAL_DIRECTION.BACK, SPATIAL_DIRECTION.LEFT]:
                    to_increment = [3, 5]
                elif side.side_name in [SPATIAL_DIRECTION.RIGHT]:
                    to_increment = [1, 7]
                else:
                    to_increment = [1, 3, 5, 7]

                updated_points = [
                    point - TRANSFORMATION_DISTANCE
                    if idx in to_increment #[3,5, ]
                    else point
                    for idx, point in enumerate(initial_points)
                ]
                side.edit_drawing(new_points=updated_points)

    def _transform(self, transformation: TRANSFORMATION = None):
        if transformation is None:
            transformation = random.choice(list(TRANSFORMATION))

        for side in self.drawn_sides:
            side.transform(transformation=transformation)

    def _set_sides(self, flat_square: bool):
        # calc square (front and back) sides first
        for side_name in self.SQUARE_SIDES:
            corners = self._calc_square_corners(side_name=side_name, flat_square=flat_square)
            self.sides[side_name] = CubeSide(side_name=side_name, corners=corners)

        # use already calculated front/back side corners to calc remaining sides
        for side_name in set(SPATIAL_DIRECTION) - self.SQUARE_SIDES:
            # corners order should be preserved for correct drawing
            corners = self.sides[SPATIAL_DIRECTION.FRONT].edges[side_name]
            corners += self.sides[SPATIAL_DIRECTION.BACK].edges[side_name][::-1]

            self.sides[side_name] = CubeSide(side_name=side_name, corners=corners)

    def _calc_initial_point(self, side_name: SPATIAL_DIRECTION = SPATIAL_DIRECTION.FRONT) -> Point:
        """
        returns initial point for a side of a cube based on a cube's position within parent cube
        these x and y transformations were chosen randomly but cubes positions looks more or less ok after them
        """

        depth, width, height = self.position_within_parent_cube.coords_flat

        x = ((8 - width * 2) * SPACES_X + depth * SPACES_X + X_OFFSET)
        y = depth * SPACES_X + (5 + height * SPACES_Y) + Y_OFFSET

        side_to_point_map = {
            SPATIAL_DIRECTION.FRONT: Point(x, y),
            SPATIAL_DIRECTION.BACK: Point(x, y).apply_delta(delta_x=self.size / 2, delta_y=self.size / 2),
        }

        return side_to_point_map[side_name]

    def _calc_square_corners(self, side_name: SPATIAL_DIRECTION, flat_square=False):
        initial_point = self._calc_initial_point(side_name=side_name)

        if flat_square:
            # results in a 2-d parralelogram that can be made 3-d by mouse scroll
            return (
                initial_point,  # bottom left
                initial_point.apply_delta(0, 0),  # top left
                initial_point.apply_delta(self.size, 0),  # top right
                initial_point.apply_delta(self.size, 0),  # bottom right
            )

        return (
            initial_point,  # bottom left
            initial_point.apply_delta(0, self.size, ),  # top left
            initial_point.apply_delta(self.size, self.size, ),  # top right
            initial_point.apply_delta(self.size, 0),  # bottom right
        )

