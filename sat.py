from math import sqrt, cos, sin, pi
from copy import deepcopy
from typing import List
import pygame


class Vector:
    """
    Helper class representing vector in 2D space.
    Every point will be considered as a vector.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: int) -> 'Vector':
        return Vector(self.x * multiplier, self.y * multiplier)

    def to_tuple(self):
        return tuple((self.x, self.y))


class Shape:
    """
    Helper class holding list of vertices.
    Every vertex is an instance of class Vector.
    Vertices of all shapes have to be declared in the same direction (clockwise or counterclockwise).
    """
    def __init__(self, vertices: List[Vector]):
        # List of oryginal vertices:
        self.oryginal_vertices = vertices
        # List of transformed vertices:
        self.vertices = deepcopy(vertices)
        # Variables used to transform verticesCpy ("move" the shape):
        self.position = Vector(400, 200)
        self.angle = 0
        self.progressive_speed = 3
        self.angular_speed = 2
        # Initial update of verticesCpy list:
        self.update()

    def forward(self):
        self.position.x += self.progressive_speed * cos(self.angle * pi / 180)
        self.position.y += self.progressive_speed * sin(self.angle * pi / 180)
        self.update()

    def backwards(self):
        self.position.x -= self.progressive_speed * cos(self.angle * pi / 180)
        self.position.y -= self.progressive_speed * sin(self.angle * pi / 180)
        self.update()

    def turn_right(self):
        self.angle += self.angular_speed
        self.angle %= 360
        self.update()

    def turn_left(self):
        self.angle -= self.angular_speed
        self.angle %= 360
        self.update()

    def update(self):
        """
        Updates verticesCpy.
        :return: None.
        """
        cos_angle = cos(self.angle * pi / 180)
        sin_angle = sin(self.angle * pi / 180)
        for v, ov in zip(self.vertices, self.oryginal_vertices):
            v.x = ov.x * cos_angle - ov.y * sin_angle + self.position.x
            v.y = ov.x * sin_angle + ov.y * cos_angle + self.position.y

    def draw(self, screen, color=(0, 0, 0), width=1):
        number_pairs = [(v.x, v.y) for v in self.vertices]
        pygame.draw.polygon(screen, color, number_pairs, width)
        # Draw a line to show direction in which shape will move:
        length = 40
        cos_angle = cos(self.angle * pi / 180)
        sin_angle = sin(self.angle * pi / 180)
        pygame.draw.line(screen, color, self.position.to_tuple(),
                         (length * cos_angle + self.position.x,
                          length * sin_angle + self.position.y), width)


def unit_norm(v1: Vector, v2: Vector) -> Vector:
    """
    Helper function. Calculates unit normal vector to a v1 - v2 vector.
    :param v1: Vector.
    :param v2: Vector.
    :return: Vector.
    """
    v = v1 - v2
    # Calculate normal:
    tmp = v.x
    v.x = -v.y
    v.y = tmp
    # Calculate magnitude (length) of v:
    length = sqrt(v.x**2 + v.y**2)
    # Reduce to unit:
    v.x /= length
    v.y /= length
    # Return unit normal vector:
    return v


def dot(v1: Vector, v2: Vector) -> float:
    """
    Helper function. Calculates dot product of two 2D vectors.
    :param v1: Vector.
    :param v2: Vector.
    :return: Float.
    """
    return v1.x * v2.x + v1.y * v2.y


def sat(shape1: Shape, shape2: Shape) -> bool:
    """
    Collision detection based on Separating Axis Theorem.
    This implementation only returns True or False.
    :param shape1: Shape.
    :param shape2: Shape.
    :return: Bool.
    """
    # Make a list of all unique unit normals to sides of a shape:
    def list_unorms(vertices: List[Vector]) -> List[Vector]:
        unorms_ = []
        for i, vertex in enumerate(vertices):
            unorm_ = unit_norm(vertices[i - 1], vertex)
            if unorm_ not in unorms_:
                unorms_.append(unorm_)
        return unorms_

    # Easier to iterate through shapes than to check them separately:
    shapes = [shape1, shape2]
    for shape in shapes:
        unorms = list_unorms(shape.vertices)
        # For every unique unit normal in a shape...
        for unorm in unorms:
            # ...calculate dot product of every vertex for both shapes:
            shape1_dots = []
            shape2_dots = []
            for vec_s1 in shape1.vertices:
                shape1_dots.append(dot(vec_s1, unorm))
            for vec_s2 in shape2.vertices:
                shape2_dots.append(dot(vec_s2, unorm))
            # This gave us projections of both shapes along unorm.
            # If those projections are not overlapping ...
            if min(shape1_dots) > max(shape2_dots) or min(shape2_dots) > max(shape1_dots):
                # ... there is no collision:
                return False
    # If projections of shapes along all axes are overlapping, there is collision:
    return True


def sat_resolve(shape1: Shape, shape2: Shape) -> bool:
    """
    Collision detection based on Separating Axis Theorem.
    This implementation resolves collision translating shape1 by Minimum Translate Vector.
    Checking for collision is similar to sat. The difference is that a list of translate vectors is created.
    :param shape1: Shape.
    :param shape2: Shape.
    :return: Bool.
    """
    def list_unorms(vertices: List[Vector]) -> List[Vector]:
        unorms_ = []
        for i, vertex in enumerate(vertices):
            unorm_ = unit_norm(vertices[i - 1], vertex)
            if unorm_ not in unorms_:
                unorms_.append(unorm_)
        return unorms_

    # A list of translate vectors:
    tvs = []

    shapes = [shape1, shape2]
    for shape in shapes:
        unorms = list_unorms(shape.vertices)
        for unorm in unorms:
            shape1_dots = []
            shape2_dots = []
            for vec_s1 in shape1.vertices:
                shape1_dots.append(dot(vec_s1, unorm))
            for vec_s2 in shape2.vertices:
                shape2_dots.append(dot(vec_s2, unorm))

            # Calculating extremes:
            shape1_min = min(shape1_dots)
            shape1_max = max(shape1_dots)
            shape2_min = min(shape2_dots)
            shape2_max = max(shape2_dots)

            if shape1_min > shape2_max or shape2_min > shape1_max:
                return False

            # Calculating length of projections overlap:
            overlap = min(shape1_max, shape2_max) - max(shape1_min, shape2_min)
            # Checking the sign (direction) of that overlap:
            sign = 1 if shape1_min < shape2_min else -1

            tvs.append((unorm * sign, overlap))

    # Resolving collision with MTV:
    unorm, overlap = min(tvs, key=lambda v: v[1])
    # Translating shape1:
    shape1.position.x -= unorm.x * overlap
    shape1.position.y -= unorm.y * overlap

    # Since the collision has been resolved, there is no collision:
    return False
