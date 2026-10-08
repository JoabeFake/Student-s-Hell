import math
import pygame
import sys

class Hitbox:
    def __init__(self, width, height, offset_x = 0, offset_y = 0):
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_vertices(self, x, y):
        center_x = x + self.offset_x
        center_y = y + self.offset_y

        half_width = self.width / 2
        half_height = self.height / 2

        return [
            (center_x - half_width, center_y - half_width),
            (center_x + half_width, center_y - half_width),
            (center_x + half_width, center_y + half_width),
            (center_x - half_width, center_y + half_width)
        ]

def is_outside_screen(obj, screen_width, screen_height, margin = 200):
    vertices = obj.hitbox.get_vertices(obj.x, obj.y)

    min_x = min(x for x, y in vertices)
    max_x = max(x for x, y in vertices)
    min_y = min(y for x, y in vertices)
    max_y = max(y for x, y in vertices)

    if (min_x < -margin or max_x > screen_width + margin or
        min_y < -margin or max_y > screen_height + margin):
        return True
    
    return False

def keep_inside_screen(obj, screen_width, screen_height):
    vertices = obj.hitbox.get_vertices(obj.x, obj.y)

    min_x = min(x for x, y in vertices)
    max_x = max(x for x, y in vertices)
    min_y = min(y for x, y in vertices)
    max_y = max(y for x, y in vertices)

    if min_x < 0:
        obj.x -= min_x

    if max_x > screen_width:
        obj.x -= max_x - screen_width

    if min_y < 0:
        obj.y -= min_y

    if max_y > screen_height:
        obj.y -= max_y - screen_height

def check_collision(obj1, obj2):
    vertices1 = obj1.hitbox.get_vertices(obj1.x, obj1.y)
    vertices2 = obj2.hitbox.get_vertices(obj2.x, obj2.y)

    min_x1 = min(x for x, y in vertices1)
    max_x1 = max(x for x, y in vertices1)
    min_y1 = min(y for x, y in vertices1)
    max_y1 = max(y for x, y in vertices1)

    min_x2 = min(x for x, y in vertices2)
    max_x2 = max(x for x, y in vertices2)
    min_y2 = min(y for x, y in vertices2)
    max_y2 = max(y for x, y in vertices2)

    if max_x1 < min_x2:
        return False
    
    if min_x1 > max_x2:
        return False

    if max_y1 < min_y2:
        return False
    
    if min_y1 > max_y2:
        return False

    return True

def point_direction(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def get_direction_vector(direction):
    radians = math.radians(direction)

    return (
        math.cos(radians),
        math.sin(radians)
    )

def lengthdir_x(length, direction):
    x, _ = get_direction_vector(direction)
    return x * length

def lengthdir_y(length, direction):
    _, y = get_direction_vector(direction)
    return y * length

def identity():
    return [[1,0,0], 
            [0,1,0],
            [0,0,1]]

def multiply_matrixes(a, b):
    result = [[0,0,0],
              [0,0,0],
              [0,0,0]]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += a[i][k] * b[k][j]

    return result

def translation(tx, ty):
    return [[1,0,tx], 
            [0,1,ty], 
            [0,0,1]]

def scale(sx, sy):
    return [[sx, 0, 0], 
            [0,sy, 0], 
            [0,0,1]]

def rotation(theta):
    rad = math.radians(theta)

    c = math.cos(rad)
    s = math.sin(rad)

    return [[c, -s, 0], 
            [s, c, 0], 
            [0,0,1]]

def transform_point(matrix, x, y):
    new_x = (matrix[0][0] * x + 
             matrix[0][1] * y + 
             matrix[0][2])
    
    new_y = (matrix[1][0] * x + 
             matrix[1][1] * y + 
             matrix[1][2])

    return new_x, new_y

def translate_point(x, y, tx, ty):
    matrix = translation(tx, ty)

    return transform_point(matrix, x, y)

def scale_point(x, y, sx, sy):
    matrix = scale(sx, sy)

    return transform_point(matrix, x, y)

def rotate_point(x, y, theta):
    matrix = rotation(theta)

    return transform_point(matrix, x, y)

def rotation_in(theta, cx, cy):
    move_to_origin = translation(-cx, -cy)
    rotate = rotation(theta)
    move_back = translation(cx, cy)

    transformation = multiply_matrixes(move_back, rotate)
    transformation = multiply_matrixes(transformation, move_to_origin)

    return transformation

def scale_in(sx, sy, cx, cy):
        move_to_origin = translation(-cx, -cy)
        scale = scale(sx, sy)
        move_back = translation(cx, cy)
    
        transformation = multiply_matrixes(move_back, scale)
        transformation = multiply_matrixes(transformation, move_to_origin)
    
        return transformation

def transform_polygon(vertices, matrix):
    new_vertices = []

    for x, y in vertices:
        new_x, new_y = transform_point(matrix, x, y)
        new_vertices.append((new_x, new_y))

    return new_vertices

def translate_polygon(vertices, tx, ty):
    matrix = translation(tx, ty)

    return transform_polygon(vertices, matrix)

def rotate_polygon(vertices, theta):
    matrix = rotation(theta)

    return transform_polygon(vertices, matrix)

def rotate_polygon_in(vertices, theta, cx, cy):
    matrix = rotation_in(theta, cx, cy)

    return transform_polygon(vertices, matrix)

def scale_polygon(vertices, sx, sy):
    matrix = scale(sx, sy)

    return transform_polygon(vertices, matrix)

def scale_polygon_in(vertices, sx, sy, cx, cy):
    matrix = scale_in(sx, sy, cx, cy)

    return transform_polygon(vertices, matrix)