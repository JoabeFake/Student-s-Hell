import engine
import math

import random

class Attack:

    def __init__(self):
        self.timer = 0
        self.spawn_timer = 0
        self.name = "Unknown"

    def start(self, enemy):
        self.timer = 0
        self.spawn_timer = 0

    def cancel(self):
        self.timer = 0
        self.spawn_timer = 0

    def update(self, enemy, player=None):
        return False


class SpiralAttack(Attack):

    def __init__(self):
        super().__init__()

        self.name = "Spiral"

        # spawning
        self.spawn_interval = 2

        self.min_spawn_interval = 1
        self.max_spawn_interval = 8

        self.spawn_interval_change = 0
        self.spawn_interval_direction = 1

        self.streams = 5
        self.b_per_stream = 1

        # direction
        self.rotation = 137.5

        self.min_rotation = -137.5
        self.max_rotation = 137.5

        self.rotation_change = 0
        self.rotation_direction = 1

        # bullets
        self.bullet_speed = 1.5
        self.bullet_rotation = 0.25

        self.b_min_rotation = -0.25
        self.b_max_rotation = 0.25

        self.b_rotation_change = 0.0005
        self.b_rotation_direction = 1

        self.directions = []

    def start(self, enemy):
        super().start(enemy)

        self.directions = []

        for i in range(self.streams):
            direction = i * (360 / self.streams)
            self.directions.append(direction)

        self.spawn_interval = 2
        self.spawn_interval_direction = 1

        self.rotation = 137.5
        self.rotation_direction = 1


    def update(self, enemy, player=None):

        self.timer += 1
        self.spawn_timer += 1

        # =========================
        # SPAWN
        # =========================

        self.spawn_interval += (self.spawn_interval_change * self.spawn_interval_direction)

        if self.spawn_interval >= self.max_spawn_interval:
            self.spawn_interval = self.max_spawn_interval
            self.spawn_interval_direction = -1
        elif self.spawn_interval <= self.min_spawn_interval:
            self.spawn_interval = self.min_spawn_interval
            self.spawn_interval_direction = 1

        if self.spawn_timer >= self.spawn_interval:

            self.spawn_timer = 0

            for direction in self.directions:

                self.bullet_rotation += (self.b_rotation_change * self.b_rotation_direction)

                if self.bullet_rotation >= self.b_max_rotation:
                    self.bullet_rotation = self.b_max_rotation
                    self.b_rotation_direction = -1
    
                elif self.bullet_rotation <= self.b_min_rotation:
                    self.bullet_rotation = self.b_min_rotation
                    self.b_rotation_direction = 1
                
                for i in range(self.b_per_stream):

                    enemy.spawn_bullet(
                        enemy.x,
                        enemy.y,
                        self.bullet_speed,
                        direction,
                        self.bullet_rotation
                    )

            #rotation oscilation
            self.rotation += (self.rotation_change * self.rotation_direction)

            if self.rotation >= self.max_rotation:
                self.rotation = self.max_rotation
                self.rotation_direction = -1

            elif self.rotation <= self.min_rotation:
                self.rotation = self.min_rotation
                self.rotation_direction = 1

            # rotate
            for i in range(len(self.directions)):
                self.directions[i] += self.rotation

            # acceleration da rotação
            # self.rotation += self.rotation_accel

        # O Attack não decide quando o spell acaba.
        return False

class AimedCircleAttack(Attack):

    def __init__(self):
        super().__init__()

        self.name = "Aimed Circle"

        # =========================
        # CIRCLE
        # =========================

        self.layers = 3
        self.bullets_per_layer = 16

        self.radius = 30
        self.layer_spacing = 0
        self.layer_offset = True

        #Layer spawn
        self.layer_spawn_delay = 20

        self.min_layer_spawn_delay = 5
        self.max_layer_spawn_delay = 25

        self.layer_spawn_delay_change = 2
        self.layer_spawn_delay_direction = 1

        #Aim

        self.aim_delay = 45

        self.min_aim_delay = 10
        self.max_aim_delay = 50

        self.aim_delay_change = 5
        self.aim_delay_direction = 1

        # =========================
        # ACCELERATION
        # =========================

        self.accel = 0.25
        self.max_speed = 4


        # =========================
        # DIRECTIONS
        # =========================

        self.directions = []
        self.attack_bullets = []


        # =========================
        # LAYERS
        # =========================

        self.current_layer = 0
        self.layer_timer = 0
        self.layer_bullets = []


        # =========================
        # FORMATION
        # =========================

        self.layer_x_spacing = 50

        self.formation = 0
        self.formation_timer = 0
        self.formation_delay = 20


        # controla se a sequência terminou
        self.sequence_finished = False


    def start(self, enemy):

        super().start(enemy)

        self.directions = []
        self.attack_bullets = []
        self.layer_bullets = []

        self.current_layer = 0
        self.layer_timer = 0

        self.formation = 0
        self.formation_timer = 0

        self.sequence_finished = False

        #reset dos timers
        self.layer_spawn_delay = 20
        self.layer_spawn_delay_direction = 1

        self.aim_delay = 45
        self.aim_delay_direction = 1

        # =========================
        # DIREÇÕES DAS CAMADAS
        # =========================

        angle_step = 360 / self.bullets_per_layer

        for layer in range(self.layers):

            directions = []

            if self.layer_offset:
                offset = layer * (angle_step / self.layers)
            else:
                offset = 0

            for i in range(self.bullets_per_layer):

                direction = (i * angle_step + offset)

                directions.append(direction)

            self.directions.append(directions)

    def update(self, enemy, player=None):

        self.timer += 1
        self.layer_timer += 1


        # =========================
        # SPAWN DAS CAMADAS
        # =========================

        if self.current_layer < self.layers:

            if self.layer_timer >= self.layer_spawn_delay:

                layer = self.current_layer

                radius = (
                    self.radius
                    + layer * self.layer_spacing
                )


                # formação esquerda -> direita
                # depois direita -> esquerda

                formations = [
                    [-1, 0, 1],
                    [1, 0, -1]
                ]

                x_offset = (formations[self.formation][layer] * self.layer_x_spacing)

                cx = enemy.x + x_offset
                cy = enemy.y + 30


                bullets = []


                for direction in self.directions[layer]:

                    radians = math.radians(direction)

                    x = (
                        cx
                        + math.cos(radians) * radius
                    )

                    y = (
                        cy
                        + math.sin(radians) * radius
                    )


                    new_bullet = enemy.spawn_bullet(
                        x,
                        y,
                        0,
                        direction,
                        0
                    )

                    bullets.append(new_bullet)
                    self.attack_bullets.append(new_bullet)


                self.layer_bullets.append({
                    "bullets": bullets,
                    "timer": 0,
                    "aimed": False,
                    "aim_delay": self.aim_delay
                })


                self.current_layer += 1
                self.layer_timer = 0

                self.update_spawn_delay()
        # =========================
        # TROCA DE FORMAÇÃO
        # =========================

        else:

            self.formation_timer += 1

            if self.formation_timer >= self.formation_delay:

                self.formation_timer = 0

                self.formation = 1 - self.formation

                self.current_layer = 0
                self.layer_timer = 0
        # =========================
        # AIM + MOVIMENTO
        # =========================

        for layer in self.layer_bullets:

            layer["timer"] += 1


            # ainda não mirou
            if not layer["aimed"]:

                if layer["timer"] >= layer["aim_delay"]:

                    if player is not None:

                        for b in layer["bullets"]:

                            b.direction = engine.point_direction(
                                b.x,
                                b.y,
                                player.x,
                                player.y
                            )

                            b.speed = self.accel

                    layer["aimed"] = True

                    self.update_aim_delay()


            # já mirou
            else:

                for b in layer["bullets"]:

                    b.speed += self.accel

                    if b.speed > self.max_speed:
                        b.speed = self.max_speed
        # =========================
        # VERIFICA SE A SEQUÊNCIA
        # TERMINOU
        # =========================

        if self.current_layer >= self.layers:

            all_aimed = True

            for layer in self.layer_bullets:

                if not layer["aimed"]:
                    all_aimed = False
                    break

            if all_aimed:

                self.sequence_finished = True


        # O Enemy controla a duração do spell.
        return False
    
    def update_spawn_delay(self):
        self.layer_spawn_delay += (
            self.layer_spawn_delay_change
            * self.layer_spawn_delay_direction
        )

        if self.layer_spawn_delay >= self.max_layer_spawn_delay:

            self.layer_spawn_delay = self.max_layer_spawn_delay
            self.layer_spawn_delay_direction = -1

        elif self.layer_spawn_delay <= self.min_layer_spawn_delay:

            self.layer_spawn_delay = self.min_layer_spawn_delay
            self.layer_spawn_delay_direction = 1

    def update_aim_delay(self):
        self.aim_delay += (
            self.aim_delay_change
            * self.aim_delay_direction
        )

        if self.aim_delay >= self.max_aim_delay:

            self.aim_delay = self.max_aim_delay
            self.aim_delay_direction = -1

        elif self.aim_delay <= self.min_aim_delay:

            self.aim_delay = self.min_aim_delay
            self.aim_delay_direction = 1

class SweepAttack(Attack):

    def __init__(self):
        super().__init__()

        self.name = "Sweep"

        # =========================
        # BARRA
        # =========================

        self.bullets_per_wall = 65
        self.wall_spacing = 8

        # =========================
        # DIREÇÃO
        # =========================

        self.direction = "right_down"

        self.directions = [
            "right",
            "right_down",
            "down",
            "left_down",
            "left",
            "left_up",
            "up",
            "right_up"
        ]

        # =========================
        # VELOCIDADE
        # =========================

        self.bullet_speed = 3

        self.min_bullet_speed = 3
        self.max_bullet_speed = 4

        self.bullet_speed_change = 0.1
        self.bullet_speed_direction = 1

        # =========================
        # SPAWN
        # =========================

        self.spawn_interval = 45

        self.min_spawn_interval = 10
        self.max_spawn_interval = 10000

        self.spawn_interval_change = 0
        self.spawn_interval_direction = 1

        self.gap_size = 5
        self.gap_margin = 25

    def start(self, enemy):

        super().start(enemy)

        self.bullet_speed_direction = 1
        self.spawn_interval_direction = 1


    def update(self, enemy, player=None):

        self.timer += 1
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:

            self.spawn_timer = 0

            self.direction = random.choice(self.directions)

            if player is not None:
                self.spawn_wall(enemy, player)

            self.update_bullet_speed()
            self.update_spawn_interval()

        return False

    def spawn_wall(self, enemy, player=None):

        WIDTH = 320
        HEIGHT = 360

        angle = self.get_direction_angle()
        radians = math.radians(angle)

        # Direção em que a parede se move
        dx = math.cos(radians)
        dy = math.sin(radians)

        # Direção perpendicular à parede
        px = -dy
        py = dx

        margin = 5

        # ==========================================
        # POSIÇÃO DE SPAWN
        # ==========================================

        if self.direction == "right":
            center_x = -margin
            center_y = HEIGHT / 2

        elif self.direction == "left":
            center_x = WIDTH + margin
            center_y = HEIGHT / 2

        elif self.direction == "up":
            center_x = WIDTH / 2
            center_y = HEIGHT + margin

        elif self.direction == "down":
            center_x = WIDTH / 2
            center_y = -margin

        # DIAGONAL: DIREITA + CIMA
        elif self.direction == "right_up":
            center_x = -margin
            center_y = HEIGHT

        # DIAGONAL: ESQUERDA + CIMA
        elif self.direction == "left_up":
            center_x = WIDTH + margin
            center_y = HEIGHT

        # DIAGONAL: DIREITA + BAIXO
        elif self.direction == "right_down":
            center_x = -margin
            center_y = -margin

        # DIAGONAL: ESQUERDA + BAIXO
        elif self.direction == "left_down":
            center_x = WIDTH + margin
            center_y = -margin

        else:
            center_x = -margin
            center_y = HEIGHT

        # ==========================================
        # CRIA A PAREDE
        # ==========================================

        half = (self.bullets_per_wall - 1) / 2

        min_gap_start = self.gap_margin
        max_gap_start = self.bullets_per_wall - self.gap_margin - self.gap_size

        gap_start = random.randint(
            min_gap_start,
            max_gap_start
        )

        for i in range(self.bullets_per_wall):

            if gap_start <= i < gap_start + self.gap_size:
                continue

            offset = (i - half) * self.wall_spacing

            x = center_x + px * offset
            y = center_y + py * offset

            enemy.spawn_bullet(
                x,
                y,
                self.bullet_speed,
                angle
            )

    def get_direction_angle(self):

        directions = {
            "right": 0,
            "right_down": 45,
            "down": 90,
            "left_down": 135,
            "left": 180,
            "left_up": 225,
            "up": 270,
            "right_up": 315
        }

        return directions.get(
            self.direction,
            0
        )

    def update_bullet_speed(self):

        self.bullet_speed += (
            self.bullet_speed_change
            * self.bullet_speed_direction
        )

        if self.bullet_speed >= self.max_bullet_speed:

            self.bullet_speed = self.max_bullet_speed
            self.bullet_speed_direction = -1

        elif self.bullet_speed <= self.min_bullet_speed:

            self.bullet_speed = self.min_bullet_speed
            self.bullet_speed_direction = 1

    def update_spawn_interval(self):

        self.spawn_interval += (
            self.spawn_interval_change
            * self.spawn_interval_direction
        )

        if self.spawn_interval >= self.max_spawn_interval:

            self.spawn_interval = self.max_spawn_interval
            self.spawn_interval_direction = -1

        elif self.spawn_interval <= self.min_spawn_interval:

            self.spawn_interval = self.min_spawn_interval
            self.spawn_interval_direction = 1

class RandomRainAttack(Attack):

    def __init__(self):
        super().__init__()

        self.name = "Random Rain"

        # =========================
        # SPAWN
        # =========================

        self.spawn_interval = 5

        self.min_spawn_interval = 2
        self.max_spawn_interval = 10

        self.spawn_interval_change = 0.1
        self.spawn_interval_direction = 1

        # =========================
        # QUANTIDADE
        # =========================

        self.bullets_per_spawn = 4

        # =========================
        # VELOCIDADE
        # =========================

        self.bullet_speed = 3

        self.min_bullet_speed = 3
        self.max_bullet_speed = 4

        self.bullet_speed_change = 0.05
        self.bullet_speed_direction = 1

        # =========================
        # DIREÇÃO
        # =========================

        self.direction = 90

        # Variação inicial da direção
        self.direction_variation = 5

        # =========================
        # OSCILAÇÃO
        # =========================

        self.min_rotation_speed = 0.02
        self.max_rotation_speed = 0.05

    def start(self, enemy):

        super().start(enemy)

        self.spawn_interval_direction = 1
        self.bullet_speed_direction = 1

    def update(self, enemy, player=None):

        self.timer += 1
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_interval:

            self.spawn_timer = 0

            self.spawn_rain(enemy)

            self.update_bullet_speed()
            self.update_spawn_interval()

        return False

    def spawn_rain(self, enemy):

        WIDTH = 320

        margin = 50

        for i in range(self.bullets_per_spawn):

            # ==========================================
            # POSIÇÃO
            # ==========================================

            x = random.randint(
                -margin,
                WIDTH + margin
            )

            y = -margin

            # ==========================================
            # DIREÇÃO
            # ==========================================

            direction = (
                self.direction
                + random.uniform(
                    -self.direction_variation,
                    self.direction_variation
                )
            )

            # ==========================================
            # OSCILAÇÃO
            # ==========================================

            rotation_speed = random.uniform(
                self.min_rotation_speed,
                self.max_rotation_speed
            )

            # Algumas balas oscilam para a esquerda
            if random.random() < 0.5:
                rotation_speed *= -1

            # ==========================================
            # CRIA BALA
            # ==========================================

            enemy.spawn_bullet(
                x,
                y,
                self.bullet_speed,
                direction,
                rotation_speed
            )

    def update_bullet_speed(self):

        self.bullet_speed += (
            self.bullet_speed_change
            * self.bullet_speed_direction
        )

        if self.bullet_speed >= self.max_bullet_speed:

            self.bullet_speed = self.max_bullet_speed
            self.bullet_speed_direction = -1

        elif self.bullet_speed <= self.min_bullet_speed:

            self.bullet_speed = self.min_bullet_speed
            self.bullet_speed_direction = 1

    def update_spawn_interval(self):

        self.spawn_interval += (
            self.spawn_interval_change
            * self.spawn_interval_direction
        )

        if self.spawn_interval >= self.max_spawn_interval:

            self.spawn_interval = self.max_spawn_interval
            self.spawn_interval_direction = -1

        elif self.spawn_interval <= self.min_spawn_interval:

            self.spawn_interval = self.min_spawn_interval
            self.spawn_interval_direction = 1

import random
import math


class PredictiveShotAttack(Attack):

    def __init__(self):
        super().__init__()

        self.name = "Predictive Shot"

        # =========================
        # SHOTGUN
        # =========================

        # Quantos tiros saem em cada burst
        self.shots_per_burst = 5

        # Abertura da shotgun
        self.shot_spread = 12

        # =========================
        # RAJADA AUTOMÁTICA
        # =========================

        # Quantos bursts são disparados
        # antes da pausa maior
        self.bursts_per_sequence = 4

        # Tempo entre cada burst
        self.burst_interval = 8

        # Tempo de espera depois da sequência
        self.sequence_cooldown = 60

        # =========================
        # PREVISÃO
        # =========================

        self.prediction_time = 10

        self.aim_variation = 3

        # =========================
        # VELOCIDADE
        # =========================

        self.bullet_speed = 5

        self.min_bullet_speed = 2
        self.max_bullet_speed = 10

        self.bullet_speed_change = 0
        self.bullet_speed_direction = 1

        # =========================
        # CONTROLE
        # =========================

        self.burst_timer = 0
        self.burst_count = 0

        self.cooldown_timer = 0

    # ==========================================
    # START
    # ==========================================

    def start(self, enemy):

        super().start(enemy)

        self.burst_timer = self.burst_interval
        self.burst_count = 0
        self.cooldown_timer = 0

        self.bullet_speed_direction = 1

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, enemy, player=None):

        self.timer += 1

        # ======================================
        # SE TERMINOU A SEQUÊNCIA
        # ======================================

        if self.burst_count >= self.bursts_per_sequence:

            self.cooldown_timer += 1

            if self.cooldown_timer >= self.sequence_cooldown:

                self.cooldown_timer = 0
                self.burst_timer = self.burst_interval
                self.burst_count = 0

            return False

        # ======================================
        # INTERVALO ENTRE BURSTS
        # ======================================

        self.burst_timer += 1

        if self.burst_timer >= self.burst_interval:

            self.burst_timer = 0

            if player is not None:

                self.spawn_burst(
                    enemy,
                    player
                )

            self.burst_count += 1

            self.update_bullet_speed()

        return False

    # ==========================================
    # BURST DA SHOTGUN
    # ==========================================

    def spawn_burst(self, enemy, player):

        # ======================================
        # PREVÊ POSIÇÃO DO PLAYER
        # ======================================

        predicted_x = (
            player.x
            + player.x_speed * self.prediction_time
        )

        predicted_y = (
            player.y
            + player.y_speed * self.prediction_time
        )

        # ======================================
        # DIREÇÃO CENTRAL
        # ======================================

        center_direction = engine.point_direction(
            enemy.x,
            enemy.y,
            predicted_x,
            predicted_y
        )

        # ======================================
        # TIROS DA SHOTGUN
        # ======================================

        for i in range(self.shots_per_burst):

            # Distribui os tiros dentro
            # da abertura da shotgun

            if self.shots_per_burst > 1:

                t = i / (self.shots_per_burst - 1)

            else:

                t = 0.5

            spread = (
                -self.shot_spread / 2
                + self.shot_spread * t
            )

            # Pequena variação aleatória

            spread += random.uniform(
                -self.aim_variation,
                self.aim_variation
            )

            direction = (
                center_direction
                + spread
            )

            # ==================================
            # DISPARA
            # ==================================

            enemy.spawn_bullet(
                enemy.x,
                enemy.y,
                self.bullet_speed,
                direction
            )

    # ==========================================
    # VELOCIDADE
    # ==========================================

    def update_bullet_speed(self):

        self.bullet_speed += (
            self.bullet_speed_change
            * self.bullet_speed_direction
        )

        if self.bullet_speed >= self.max_bullet_speed:

            self.bullet_speed = self.max_bullet_speed

            self.bullet_speed_direction = -1

        elif self.bullet_speed <= self.min_bullet_speed:

            self.bullet_speed = self.min_bullet_speed

            self.bullet_speed_direction = 1