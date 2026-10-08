import graphic_functions
import engine

class Bullet:
    def __init__(self, x, y, speed, direction, rotation_speed = 0, size = 2):
        self.active = True

        self.x = x
        self.y = y

        self.speed = speed
        self.direction = direction

        self.rotation_speed = rotation_speed

        self.color = (255, 255, 255)

        self.radius = size

        self.hitbox = engine.Hitbox(
            width = size -2,
            height = size -2
        )

        # self.vertices = [
        #     (-1, 0),
        #     (0, 1),
        #     (1, 0),
        #     (0, -1)
        # ]

        # self.rotation_matrix = engine.rotation(
        #     engine.math.radians(direction)
        # )

    def update(self):
        if not self.active:
            return
        
        self.direction += self.rotation_speed

        x_speed = engine.lengthdir_x(self.speed, self.direction)
        y_speed = engine.lengthdir_y(self.speed, self.direction)

        self.x += x_speed
        self.y += y_speed

        # self.rotation_matrix = engine.rotation(
        #     engine.math.radians(self.direction)
        # )

    def draw(self):
        if not self.active:
            return
        
        # new_vertices = self.get_transformed_vertices(self.vertices, round(self.x), round(self.y))

        # graphic_functions.drawPolygonFill(new_vertices, self.color)

        graphic_functions.drawCircleFillSL(
            round(self.x), round(self.y), self.radius, self.color
        )

    # def get_transformed_vertices(self, vertices, mx, my):
    #     vertices = engine.transform_polygon(vertices, self.rotation_matrix)

    #     for i in range(len(vertices)):
    #         x, y = vertices[i]
    #         vertices[i] = (x + mx, y + my)

    #     return vertices

    def is_outside_screen(self, width, height):
        margin = self.radius

        return (self.x < -margin or
                self.x > width + margin or
                self.y < -margin or
                self.y > height + margin)