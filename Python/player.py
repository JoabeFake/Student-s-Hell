import pygame
import math

import graphic_functions
import input
import engine
import player_shot

Player_Shot = "HOMING"

SHOT_TYPES = {
    "SINGLE":{
        "amount" : 1,
        "damage" : 15,
        "cooldown" : 18,
        "pattern" : "forward",
    },
    "TRIPLE":{
        "amount" : 3,
        "damage" : 5,
        "cooldown" : 12,
        "pattern" : "spread",
    },
    "HOMING":{
        "amount" : 2,
        "damage" : 5,
        "cooldown" : 16,
        "pattern" : "side_homing",
    },
}

class Player:
    def __init__(self, x, y):
        self.lives = 2
        self.score = 0

        self.state = "normal"

        self.invincible = False
        self.invincibility_timer = 0

        self.blink_timer = 0

        self.explosion_timer = 0
        self.explosion_duration = 60

        self.respawn_speed = .5
        self.respawn_y = 330

        self.fragments = []

        #position
        self.x = x
        self.y = y

        self.x_speed = 0
        self.y_speed = 0

        self.normal_spd = 3
        self.focus_spd = 1.5
        self.spd = self.normal_spd

        #sprite
        self.radius = 3
        self.image_angle = 0

        self.width = 16
        self.height = 16

        self.tex = pygame.image.load("spr_player_touhou.png").convert_alpha()
        self.vertices = [
                            (self.x - self.width, self.y - self.height),
                            (self.x + self.width, self.y - self.height),
                            (self.x + self.width, self.y + self.height),
                            (self.x - self.width, self.y + self.height)
                        ]
        self.uvs = [(0, 0),(1, 0),(1, 1),(0, 1)]

        #hitbox
        self.hitbox = engine.Hitbox(
            width = 4,
            height = 4
        )

        #bullets
        self.bullets = []

        self.shot_timer = 0

        #colors
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)



    def update(self, enemy = None):
        if self.state == "exploding":
            self.update_explosion()
            return

        if self.state == "respawning":
            self.update_respawn()
            return

        if self.shot_timer > 0:
            self.shot_timer -= 1

        self.update_movement()
        self.update_shooting()

        for bullet in self.bullets:
            bullet.update(enemy)

        self.bullets = [bullet for bullet in self.bullets if bullet.active]

        self.update_invincibility()

    def draw(self):
        self.vertices = [
                            (self.x - self.width, self.y - self.height),
                            (self.x + self.width, self.y - self.height),
                            (self.x + self.width, self.y + self.height),
                            (self.x - self.width, self.y + self.height)
                        ]


        if self.state == "exploding":
            self.draw_fragments()
            return

        for bullet in self.bullets:
                    bullet.draw()

        if self.state != "respawning":
            if self.invincible:
                if (self.blink_timer // 5) % 2 == 0:
                    return

        graphic_functions.scanlineTexture(self.vertices, self.uvs, self.tex, graphic_functions.logical_surface)

        graphic_functions.drawCircleFillSL(
            self.x, self.y, self.radius, self.RED
        )

        # vertices_hb = self.hitbox.get_vertices(self.x, self.y)

        # graphic_functions.drawPolygonFill(vertices_hb, self.RED)

    def die(self):
        if self.invincible:
            return

        if self.state != "normal":
            return 
        
        self.lives -= 1

        if self.lives <= 0:
            self.lives = 0
            print("Game Over")
            return 

        self.start_death_sequence()

    def start_death_sequence(self):
        self.state = "exploding"

        self.explosion_timer = 0

        self.x_speed = 0
        self.y_speed = 0

        self.bullets.clear()

        self.create_fragments()

    def create_fragments(self):
        self.fragments = []

        size = 5

        angles = [0, 60, 120, 180, 240, 300]

        for angle in angles:
            radians = math.radians(angle)

            fragment = {
                "x": self.x,
                "y": self.y,

                "vx": math.cos(radians) * 1.5,
                "vy": math.sin(radians) * 1.5,

                "size": size
            }

            self.fragments.append(fragment)

    def update_explosion(self):
        self.explosion_timer += 1

        for fragment in self.fragments:
            fragment["x"] += fragment["vx"]
            fragment["y"] += fragment["vy"]

        if self.explosion_timer >= self.explosion_duration:
            self.start_respawn()

    def start_respawn(self):
        self.state = "respawning"

        self.x = graphic_functions.logical_width // 2
        self.y = graphic_functions.logical_height + 10

        self.x_speed = 0
        self.y_speed = 0

        self.invincible = True

    def update_respawn(self):
        self.y -= self.respawn_speed

        if self.y <= self.respawn_y:
            self.y = self.respawn_y

            self.state = "normal"

            self.invincibility_timer = 120

    def update_invincibility(self):
        if not self.invincible:
            return

        self.invincibility_timer -= 1
        self.blink_timer += 1

        if self.invincibility_timer <= 0:
            self.invincibility_timer = 0
            self.invincible = False
            self.blink_timer = 0

    def update_movement(self):
        key_right = input.isDown(pygame.K_d)
        key_left = input.isDown(pygame.K_a)
        key_down = input.isDown(pygame.K_s)
        key_up = input.isDown(pygame.K_w)

        key_focus = input.isDown(pygame.K_LSHIFT)

        horizontal_movement = key_right - key_left
        vertical_movement = key_down - key_up

        moving_direction = engine.point_direction(
            0, 0, horizontal_movement, vertical_movement
        )

        is_moving = horizontal_movement != 0 or vertical_movement != 0

        if key_focus:
            self.spd = self.focus_spd
        else:
            self.spd = self.normal_spd
        
        self.x_speed = engine.lengthdir_x(
            is_moving * self.spd, moving_direction
        )

        self.y_speed = engine.lengthdir_y(
            is_moving * self.spd, moving_direction
        )

        self.x, self.y = engine.translate_point(
            self.x, self.y, self.x_speed, self.y_speed
        )

    def update_shooting(self):
        key_shot = input.isDown(pygame.K_UP)

        if key_shot and self.shot_timer <= 0:
            self.shoot()

    def draw_fragments(self):
        for fragment in self.fragments:
            x = fragment["x"]
            y = fragment["y"]
            size = fragment["size"]

            vertices = [
                (x - size, y - size),
                (x + size, y - size),
                (x + size, y + size),
                (x - size, y + size)
            ]

            graphic_functions.drawPolygonFill(vertices, self.RED)

    def shoot(self):
        config = SHOT_TYPES[Player_Shot]

        damage = config["damage"]

        if config["pattern"] == "forward":
            bullet = player_shot.Bullet(
                self.x, self.y, -90, damage
            )

            self.bullets.append(bullet)

        elif config["pattern"] == "spread":
            angles = [-100, -90, -80]

            for angle in angles:
                bullet = player_shot.Bullet(
                    self.x, self.y, angle, damage
                )

                self.bullets.append(bullet)

        elif config["pattern"] == "side_homing":
            angles = [-180, 0]

            for angle in angles:
                bullet = player_shot.Bullet(
                    self.x, self.y, angle, damage, homing = True
                )

                self.bullets.append(bullet)

        self.shot_timer = config["cooldown"]

    def add_score(self, amount):
        self.score += amount