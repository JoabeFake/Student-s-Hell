import random
import pygame

import graphic_functions
import engine

import bullet
import enemy_attacks

class Enemy:
    def __init__(self, x, y):
        self.total_damage = 0
        self.max_health = 1000
        self.health_points = self.max_health

        self.difficulty = "medium"

        self.max_phases = random.randint(2, 5)
        self.current_phase = 1

        self.sprite = None

        self.x = x
        self.y = y

        self.width = 32
        self.height = 32

        self.sprite = pygame.image.load("Pf_Segredo.png").convert_alpha()
        self.vertices = [
                    (self.x - self.width, self.y - self.height),
                    (self.x + self.width, self.y - self.height),
                    (self.x + self.width, self.y + self.height),
                    (self.x - self.width, self.y + self.height)
                ]
        self.uvs = [(0, 0),(1, 0),(1, 1),(0, 1)]

        self.PINK = (255, 0, 255)

        self.alive = True

        #states
        #"idle"
        #"cooldown"
        #"spell"
        #"dead"

        self.state = "cooldown"

        self.bullets = []

        #spell
        self.current_spell = None

        self.spell_duration = 3000
        self.spell_timer = 0

        self.spell_cooldown_duration = 60
        self.spell_cooldown = 0

        self.spell_phase = 0

        self.attacks = [
            {"attack": enemy_attacks.PredictiveShotAttack(),
             "difficulty": "easy"},
            {"attack": enemy_attacks.SweepAttack(),
             "difficulty": "medium"},
            {"attack": enemy_attacks.AimedCircleAttack(),
             "difficulty": "medium"},
            {"attack": enemy_attacks.SpiralAttack(),
             "difficulty": "hard"},
            {"attack": enemy_attacks.RandomRainAttack(),
             "difficulty": "hard"},
        ]

        self.infinite_attacks = []

        self.attack = None
        self.previous_attack = None
        self.used_attacks = []

        self.attack_timer = 0

        #dificuldade
        self.difficulty_settings = {
            "easy": {
                "phases": 2
            },
            "medium": {
                "phases": 3
            },
            "hard": {
                "phases": 5
            },
            "infinite": {
                "phases": None
            }
        }
        
        #movimento
        self.move_spd = 0

        self.move_direction = 0

        self.move_timer = 0
        self.move_duration = 0

        self.move_wait_timer = 0
        self.move_wait_duration = 0

        self.moving = False

        #"still"
        #"constant"
        #"random"
        self.movement_type = "still"

        self.arena_width = 320
        self.arena_height = 140

        self.movement_margin = 40

        #hitbox
        self.hitbox = engine.Hitbox(self.width, self.height)

    def update(self, player = None):
        if not self.alive:
            return

        for b in self.bullets:
            b.update()

        self.bullets = [b for b in self.bullets if b.active]

        if self.state == "cooldown":
            self.update_cooldown()
        elif self.state == "spell":
            self.update_spell(player)

    def draw(self):
        self.vertices = [
                            (self.x - self.width, self.y - self.height),
                            (self.x + self.width, self.y - self.height),
                            (self.x + self.width, self.y + self.height),
                            (self.x - self.width, self.y + self.height)
                        ]

        for b in self.bullets:
            b.draw()

        # graphic_functions.drawPolygonFill(vertices, self.PINK)
        graphic_functions.scanlineTexture(self.vertices, self.uvs, self.sprite, graphic_functions.logical_surface)

    def update_movement(self):
        #parado
        if self.movement_type == "still":
            return

        #esperando
        if not self.moving:
            self.move_wait_timer += 1

            if self.move_wait_timer >= self.move_wait_duration:
                self.move_wait_timer = 0
                self.choose_movement_direction()
            return

        #movendo
        self.move_timer += 1

        dx = engine.lengthdir_x(self.move_spd, self.move_direction)
        dy = engine.lengthdir_y(self.move_spd, self.move_direction)

        self.x += dx
        self.y += dy

        min_x = self.movement_margin
        max_x = self.arena_width - self.movement_margin
        
        min_y = self.movement_margin
        max_y = self.arena_height - self.movement_margin

        #colisão com borda
        if self.x <= min_x:

            self.x = min_x

            if self.movement_type == "constant":
                self.move_direction = 180 - self.move_direction

            else:
                self.choose_movement_direction()

        elif self.x >= max_x:

            self.x = max_x

            if self.movement_type == "constant":
                self.move_direction = 180 - self.move_direction

            else:
                self.choose_movement_direction()

        if self.y <= min_y:

            self.y = min_y

            if self.movement_type == "constant":
                self.move_direction = -self.move_direction

            else:
                self.choose_movement_direction()

        elif self.y >= max_y:

            self.y = max_y

            if self.movement_type == "constant":
                self.move_direction = -self.move_direction

            else:
                self.choose_movement_direction()

        if self.move_timer >= self.move_duration:
            self.moving = False

            self.move_timer = 0
            self.move_wait_timer = 0

    def update_cooldown(self):
        self.spell_cooldown += 1

        if self.spell_cooldown >= self.spell_cooldown_duration:
            self.start_spell()

    def update_spell(self, player):
        self.spell_timer += 1
        self.attack_timer += 1

        #movimento
        self.update_movement()

        #ataque
        self.attack.update(self, player)

        if self.spell_timer >= self.spell_duration:
            self.end_spell(reason= "timeout")
            return

        if self.health_points <= 0:
            self.die()
            return

    def start_spell(self):

        print("Spell card")

        self.choose_attack()

        self.state = "spell"

        self.spell_phase = 1

        self.spell_timer = 0
        self.attack_timer = 0

        self.spell_cooldown = 0

        self.current_spell = self.attack.name

        print("Attack: ", self.current_spell)

        self.attack.start(self)
        self.configure_movement()

    def end_spell(self, reason="timeout"):

        print("Spell End: ", reason)

        self.attack.cancel()

        self.clear_bullets()

        self.spell_phase = 0
        self.spell_timer = 0
        self.attack_timer = 0

        self.current_spell = None

        if self.alive:
            self.state = "cooldown"
            self.spell_cooldown = 0

    def get_spell_progress(self):

        if self.spell_duration <= 0:
            return 0

        return self.spell_timer / self.spell_duration

    def spawn_bullet(self, x, y, speed, direction, rotation_speed = 0, size = 2):
        new_bullet = bullet.Bullet(
            x, y, speed, direction, rotation_speed, size
        )

        self.bullets.append(new_bullet)

        return new_bullet

    def clear_bullets(self):
        self.bullets.clear()

    def take_damage(self, amount, player=None):
        if not self.alive:
            return
            
        damage = min(amount, self.health_points)

        self.health_points -= damage
        self.total_damage += damage

        if self.health_points > 0:
            return

        self.health_points = 0

        #infinito
        if self.difficulty == "infinite":
            if player is not None:
                player.add_score(1000)

            self.change_phase()
            return

        #normal
        if self.current_phase < self.max_phases:
            if player is not None:
                player.add_score(1000)

            self.change_phase()
        else:
            self.die(player)

    def change_phase(self):
        print(
            f"Phase Change: "
            f"{self.current_phase} -> "
            f"{self.current_phase + 1}"
        )

        # Cancela o spell atual
        self.end_spell(reason="phase_change")

        # Avança a fase
        self.current_phase += 1

        # Nova vida
        self.max_health = 1000
        self.health_points = self.max_health

        # Prepara cooldown
        self.spell_cooldown = 0

        self.state = "cooldown"

    def die(self, player=None):
        if not self.alive:
            return 

        if player is not None:
            player.add_score(5000)

        print("Morri")

        self.alive = False
        self.state = "dead"

        self.health_points = 0

        self.clear_bullets()

    def configure_movement(self):
        #spiral
        if self.current_spell == "Spiral":
            self.movement_type = "constant"

            self.move_spd = 0.5

            self.move_duration = 180
            self.move_wait_duration = 300
        #aimedcircle
        elif self.current_spell == "Aimed Circle":
            self.movement_type = "random"
            
            self.move_spd = 0.6
            
            self.move_duration = 90
            self.move_wait_duration = 45
        #sweep
        elif self.current_spell == "Sweep":
            self.movement_type = "still"
            
            self.move_spd = 0
        #random rain
        elif self.current_spell == "Random Rain":
            self.movement_type = "constant"

            self.move_spd = 0.25

            self.move_duration = 150
            self.move_wait_duration = 30
        #predictive shot
        elif self.current_spell == "Predictive Shot":
            self.movement_type = "random"

            self.move_spd = 4

            self.move_duration = 10
            self.move_wait_duration = 75
        #padrão
        else:
            self.movement_type = "still"
            self.move_spd = 0

        self.move_timer = 0
        self.move_wait_timer = 0

        self.moving = False

        self.choose_movement_direction()

    # ==========================================
    # ESCOLHE DIREÇÃO
    # ==========================================

    def choose_movement_direction(self):

        self.move_direction = random.uniform(
            0,
            360
        )

        self.moving = True

        self.move_timer = 0
        self.move_wait_timer = 0

    def choose_attack(self):
        if self.difficulty == "infinite":

            if len(self.infinite_attacks) == 0:
                self.prepare_infinite_attacks()

            self.attack = self.infinite_attacks.pop(0)

        else:
            possible_attacks = self.get_available_attacks()

            # Se todos os ataques disponíveis já foram usados,
            # começa uma nova sequência.
            if len(self.used_attacks) >= len(possible_attacks):
                self.used_attacks = []

            # Pega somente ataques que ainda não foram usados
            available = [
                attack
                for attack in possible_attacks
                if attack not in self.used_attacks
            ]

            # Evita começar uma nova sequência com o mesmo
            # ataque que terminou a sequência anterior.
            if len(available) > 1:
                available_without_previous = [
                    attack
                    for attack in available
                    if attack != self.previous_attack
                ]

                if available_without_previous:
                    available = available_without_previous

            self.attack = random.choice(available)

            self.used_attacks.append(self.attack)

        self.previous_attack = self.attack

        print(
            f"Phase {self.current_phase} - "
            f"Attack: {self.attack.name}"
        )

    def set_difficulty(self, diff):
        if diff not in self.difficulty_settings:
            return

        self.difficulty = diff

        if diff == "easy":
            self.sprite = pygame.image.load("Pf_Segredo.png").convert_alpha()
        elif diff == "medium":
            self.sprite = pygame.image.load("pf_ismayle.png").convert_alpha()
        elif diff == "hard":
            self.sprite = pygame.image.load("pf_ph.png").convert_alpha()
        elif diff == "infinite":
            self.sprite = pygame.image.load("pf_pereira.png").convert_alpha()

        phases = self.difficulty_settings[diff]["phases"]

        if phases is None:
            self.max_phases = None
            self.prepare_infinite_attacks()
        else:
            self.max_phases = phases
            self.infinite_attacks = []

    def get_available_attacks(self):
        available = []

        for data in self.attacks:
            attack = data["attack"]
            attack_diff = data["difficulty"]

            #facil
            if self.difficulty == "easy":
                if attack_diff == "easy":
                    available.append(attack)

            #medio
            elif self.difficulty == "medium":
                if attack_diff in ["easy", "medium"]:
                    available.append(attack)

            #dificil
            elif self.difficulty == "hard":
                if attack_diff in ["easy", "medium", "hard"]:
                    available.append(attack)

            #infinito
            elif self.difficulty == "infinite":
                available.append(attack)

        return available

    def prepare_infinite_attacks(self):

        self.infinite_attacks = [
            data["attack"]
            for data in self.attacks
        ]

        random.shuffle(self.infinite_attacks)