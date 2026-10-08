import graphic_functions
import engine

class Bullet:
    def __init__(self, x, y, direction, damage = 1, homing = False):
        self.damage = damage

        self.active = True

        self.x = x
        self.y = y

        self.speed = 8
        self.direction = direction

        self.homing = homing
        self.turn_speed = 8

        self.PURPLE = (118, 66, 138)

        self.width = 3
        self.height = 5

        self.hitbox = engine.Hitbox(
            width = 3,
            height = 5
        )

    def update(self, enemy = None):
        if not self.active:
            return

        if self.homing and enemy is not None:
            target_direction = engine.point_direction(
                self.x, self.y, enemy.x, enemy.y
            )

            self.direction = self.rotate_towards(
                self.direction, target_direction, self.turn_speed
            )

        x_speed = engine.lengthdir_x(self.speed, self.direction)
        y_speed = engine.lengthdir_y(self.speed, self.direction)

        self.x += x_speed
        self.y += y_speed

    def draw(self):
        if not self.active:
            return
        vertices = self.hitbox.get_vertices(self.x, self.y)

        graphic_functions.drawPolygonFill(vertices, self.PURPLE)

    def rotate_towards(self, current, target, amount):
        diff = (target - current + 180) % 360 - 180

        if diff > amount:
            diff = amount

        if diff < -amount:
            diff = -amount

        return current + diff