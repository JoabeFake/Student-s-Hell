import pygame
import input
import graphic_functions
import engine

import player
import enemy

WIDTH = 320
HEIGHT = 360

VIEWPORT_WIDTH = 640
VIEWPORT_HEIGHT = 360

viewport_mode = "minimap"

MINIMAP_X = 336
MINIMAP_Y = 235
MINIMAP_WIDTH = 110
MINIMAP_HEIGHT = 110

VIEWPORT_AREA = (MINIMAP_X, MINIMAP_Y, MINIMAP_WIDTH, MINIMAP_HEIGHT)

window = None
running = False
clock = None

enemy_instance = None
player_instance = None

MAIN_MENU_BG = "Students_Hell_MM_BG.jpg"
DIFFICULTY_BG = "BackGround_Touhou_Diff_select.jpg"
SHOT_MENU_BG = "Background_Touhou_Shot_Type.jpg"
GAME_BG = "BackGround_Touhou_Paraguai.jpg"
GAME_OVER_BG = "Background_Game_Over.jpg"
VICTORY_BG = "Background_Victory.jpg"

# bg_tex = None
# bg_surface = None

font = None

# ---------------------------------------------------------
# ESTADO DO JOGO
# ---------------------------------------------------------

game_state = "main_menu"

# ---------------------------------------------------------
# CONFIGURAÇÕES ESCOLHIDAS PELO JOGADOR
# ---------------------------------------------------------

selected_difficulty = "easy"
selected_shot = "SINGLE"

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------

main_menu_options = [
    "JOGAR",
    "SAIR"
]

difficulty_options = [
    "EASY",
    "MEDIUM",
    "HARD",
    "INFINITE"
]

shot_options = [
    "SINGLE",
    "TRIPLE",
    "HOMING"
]

main_menu_index = 0
difficulty_index = 0
shot_index = 0

# Controle para não repetir a tecla
menu_key_delay = 0

# ---------------------------------------------------------
# BACKGROUND
# ---------------------------------------------------------

bg_vert = [
    (0, 0),
    (0, 360),
    (640, 360),
    (640, 0)
]

bg_uvs = [
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 0)
]


# =========================================================
# INICIALIZAÇÃO
# =========================================================

def init():
    global window
    global running
    global clock
    global main_menu_surface, diff_menu_surface, shot_menu_surface, game_bg_surface, game_over_surface, victory_surface
    global font_small, font_medium, font_large

    pygame.init()

    clock = pygame.time.Clock()

    window = pygame.display.set_mode(
        (VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    )

    graphic_functions.set_surface(window)

    pygame.display.set_caption("Touhou do Paraguai")

    # -----------------------------------------------------
    # BACKGROUND
    # -----------------------------------------------------

    main_menu_surface = load_background(MAIN_MENU_BG)
    diff_menu_surface = load_background(DIFFICULTY_BG)
    shot_menu_surface = load_background(SHOT_MENU_BG)
    game_bg_surface = load_background(GAME_BG)

    game_over_surface = load_background(GAME_OVER_BG)
    victory_surface = load_background(VICTORY_BG)

    # -----------------------------------------------------
    # FONTE
    # -----------------------------------------------------

    # font_file = "videotype.otf"
    # font_size = 32
    # font = pygame.font.Font(font_file, font_size)
    font_small = pygame.font.Font("videotype.otf", 12)
    font_medium = pygame.font.Font("videotype.otf", 16)
    font_large = pygame.font.Font("videotype.otf", 32)

    running = True


# =========================================================
# INICIAR PARTIDA
# =========================================================

def start_game():
    global enemy_instance
    global player_instance
    global game_state

    # -----------------------------------------------------
    # PLAYER
    # -----------------------------------------------------

    player.Player_Shot = selected_shot

    player_instance = player.Player(
        WIDTH // 2,
        180
    )

    # -----------------------------------------------------
    # ENEMY
    # -----------------------------------------------------

    enemy_instance = enemy.Enemy(
        WIDTH // 2,
        40
    )

    enemy_instance.set_difficulty(
        selected_difficulty
    )

    game_state = "game"

    print(
        "Game Start - "
        f"Difficulty: {selected_difficulty} - "
        f"Shot: {selected_shot}"
    )


# =========================================================
# INPUT DO MENU
# =========================================================

def update_menu_input():
    global menu_key_delay
    global selected_difficulty
    global selected_shot
    global main_menu_index
    global difficulty_index
    global shot_index
    global running

    if menu_key_delay > 0:
        menu_key_delay -= 1

    keys = pygame.key.get_pressed()

    if menu_key_delay > 0:
        return

    # -----------------------------------------------------
    # MENU PRINCIPAL
    # -----------------------------------------------------

    if game_state == "main_menu":

        if keys[pygame.K_UP]:
            global main_menu_index

            main_menu_index -= 1

            if main_menu_index < 0:
                main_menu_index = len(main_menu_options) - 1

            menu_key_delay = 10

        elif keys[pygame.K_DOWN]:
            main_menu_index += 1

            if main_menu_index >= len(main_menu_options):
                main_menu_index = 0

            menu_key_delay = 10

        elif keys[pygame.K_RETURN]:

            if main_menu_index == 0:
                # JOGAR
                change_state("difficulty_menu")

            elif main_menu_index == 1:
                # SAIR
                global running
                running = False

            menu_key_delay = 10

    # -----------------------------------------------------
    # MENU DE DIFICULDADE
    # -----------------------------------------------------

    elif game_state == "difficulty_menu":

        global difficulty_index

        if keys[pygame.K_LEFT]:

            difficulty_index -= 1

            if difficulty_index < 0:
                difficulty_index = len(difficulty_options) - 1

            menu_key_delay = 10

        elif keys[pygame.K_RIGHT]:

            difficulty_index += 1

            if difficulty_index >= len(difficulty_options):
                difficulty_index = 0

            menu_key_delay = 10

        elif keys[pygame.K_RETURN]:

            selected_difficulty = difficulty_options[
                difficulty_index
            ].lower()

            change_state("shot_menu")

            menu_key_delay = 10

        elif keys[pygame.K_ESCAPE]:

            change_state("main_menu")

            menu_key_delay = 10

    # -----------------------------------------------------
    # MENU DE TIRO
    # -----------------------------------------------------

    elif game_state == "shot_menu":

        global shot_index

        if keys[pygame.K_LEFT]:

            shot_index -= 1

            if shot_index < 0:
                shot_index = len(shot_options) - 1

            menu_key_delay = 10

        elif keys[pygame.K_RIGHT]:

            shot_index += 1

            if shot_index >= len(shot_options):
                shot_index = 0

            menu_key_delay = 10

        elif keys[pygame.K_RETURN]:

            selected_shot = shot_options[
                shot_index
            ]

            start_game()

            menu_key_delay = 10

        elif keys[pygame.K_ESCAPE]:

            change_state("difficulty_menu")

            menu_key_delay = 10
    
    elif game_state == "game_over":

        if keys[pygame.K_RETURN]:

            change_state("main_menu")

            menu_key_delay = 10

    elif game_state == "victory":

        if keys[pygame.K_RETURN]:

            change_state("main_menu")

            menu_key_delay = 10
        


# =========================================================
# TROCAR ESTADO
# =========================================================

def change_state(new_state):
    global game_state
    game_state = new_state


# =========================================================
# UPDATE DO JOGO
# =========================================================

def update_game():
    input.update()

    player_instance.update(
        enemy_instance
    )

    enemy_instance.update(
        player_instance
    )

    # -----------------------------------------------------
    # BALAS DO INIMIGO
    # -----------------------------------------------------

    for b in enemy_instance.bullets:

        if engine.is_outside_screen(
            b,
            WIDTH,
            HEIGHT
        ):
            b.active = False

        if engine.check_collision(
            player_instance,
            b
        ):
            player_instance.die()
            b.active = False

            if player_instance.lives <= 0:
                change_state("game_over")        

    # -----------------------------------------------------
    # BALAS DO PLAYER
    # -----------------------------------------------------

    for b in player_instance.bullets:

        if engine.is_outside_screen(
            b,
            WIDTH,
            HEIGHT
        ):
            b.active = False

        if engine.check_collision(
            enemy_instance,
            b
        ):
            enemy_instance.take_damage(
                b.damage,
                player_instance
            )

            b.active = False

            # Pontuação fixa por acerto
            player_instance.add_score(10)

    # -----------------------------------------------------
    # PLAYER DENTRO DA ARENA
    # -----------------------------------------------------

    engine.keep_inside_screen(
        player_instance,
        WIDTH,
        HEIGHT
    )

    if not enemy_instance.alive:
        change_state("victory")


# =========================================================
# UPDATE GERAL
# =========================================================

def update():

    if game_state == "game":
        update_game()

    else:
        update_menu_input()


# =========================================================
# DESENHAR TEXTO
# =========================================================

def draw_text(text, x, y, font, middle=False, selected=False, direction="right"):
    if selected:
        color = (255, 0, 0)
        
        offset = 16

        if direction == "up":
            offset_x = 0
            offset_y = -offset
        elif direction == "down":
            offset_x = 0
            offset_y = offset
        elif direction == "left":
            offset_x = -offset
            offset_y = 0
        else:
            offset_x = offset
            offset_y = 0
        
    else:
        color = (255, 255, 255)
        offset_x = 0
        offset_y = 0

    rendered_text = font.render(
        text,
        True,
        color
    )

    text_width = rendered_text.get_width()
    if middle:
        window.blit(
            rendered_text,
            (x - text_width // 2 + offset_x, y + offset_y)
        )
    else:
        window.blit(
            rendered_text,
            (x + offset_x, y + offset_y)
        )


# =========================================================
# MENU PRINCIPAL
# =========================================================

def draw_main_menu():

    window.blit(
        main_menu_surface,
        (0, 0)
    )

    for i in range(len(main_menu_options)):

        draw_text(
            main_menu_options[i],
            60,
            215 + i * 48,
            font_large,
            False,
            i == main_menu_index
        )


# =========================================================
# MENU DE DIFICULDADE
# =========================================================

def draw_difficulty_menu():
    # global font_size

    curr_font_size = 16
    window.blit(
        diff_menu_surface,
        (0, 0)
    )

    # draw_text(
    #     "DIFICULDADE",
    #     260,
    #     70,
    #     font_medium
    # )

    for i in range(len(difficulty_options)):

        draw_text(
            difficulty_options[i],
            82 + i * 160,
            180,
            font_medium,
            True,
            i == difficulty_index,
            "up"
        )

    draw_text(
        "ESC - VOLTAR",
        250,
        300,
        font_medium
    )


# =========================================================
# MENU DE TIRO
# =========================================================

def draw_shot_menu():

    window.blit(
        shot_menu_surface,
        (0, 0)
    )

    for i in range(len(shot_options)):

        draw_text(
            shot_options[i],
            160 + i * 160,
            160,
            font_medium,
            True,
            i == shot_index,
            "up"
        )

    draw_text(
        "ESC - VOLTAR",
        250,
        300,
        font_medium
    )

#Game over
def draw_game_over():

    window.blit(
        game_over_surface,
        (0, 0)
    )

    draw_text(
        f"SCORE: {player_instance.score}",
        320,
        250,
        font_medium,
        True
    )

    draw_text(
        "ENTER - MENU PRINCIPAL",
        320,
        230,
        font_medium,
        True
    )

#Victory
def draw_victory():

    window.blit(
        victory_surface,
        (0, 0)
    )

    draw_text(
        f"SCORE: {player_instance.score}",
        320,
        250,
        font_medium,
        True
    )

    draw_text(
        "ENTER - MENU PRINCIPAL",
        320,
        230,
        font_medium,
        True
    )

#draw minimap
def draw_minimap():
    janela_minimapa = (
        0,
        0,
        WIDTH,
        HEIGHT
    )

    viewport_minimap = (
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_X + MINIMAP_WIDTH,
        MINIMAP_Y + MINIMAP_HEIGHT
    )

    # -----------------------------------------------------
    # FUNDO
    # -----------------------------------------------------

    graphic_functions.drawRectFillSL(
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_WIDTH,
        MINIMAP_HEIGHT,
        (10, 10, 15),
        window
    )

    # -----------------------------------------------------
    # PLAYER
    # -----------------------------------------------------

    player_x = player_instance.x
    player_y = player_instance.y

    player_pontos = [
        (player_x - 4, player_y + 4),
        (player_x, player_y - 5),
        (player_x + 4, player_y + 4)
    ]

    player_minimap = graphic_functions.transformViewport(
        player_pontos,
        janela_minimapa,
        viewport_minimap
    )

    graphic_functions.drawPolygonFill(
        player_minimap,
        (255, 255, 255),
        window
    )

    # -----------------------------------------------------
    # ENEMY
    # -----------------------------------------------------

    enemy_x = enemy_instance.x
    enemy_y = enemy_instance.y

    enemy_pontos = [
        (enemy_x - 8, enemy_y - 8),
        (enemy_x + 8, enemy_y - 8),
        (enemy_x + 8, enemy_y + 8),
        (enemy_x - 8, enemy_y + 8)
    ]

    enemy_minimap = graphic_functions.transformViewport(
        enemy_pontos,
        janela_minimapa,
        viewport_minimap
    )

    graphic_functions.drawPolygonFill(
        enemy_minimap,
        (255, 0, 0),
        window
    )

    # -----------------------------------------------------
    # BORDA
    # -----------------------------------------------------

    graphic_functions.drawRectangle(
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_WIDTH,
        MINIMAP_HEIGHT,
        (255, 255, 255),
        window
    )

def draw_zoom_viewport():
    # -----------------------------------------------------
    # ÁREA DO VIEWPORT
    # -----------------------------------------------------

    viewport_zoom = (
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_X + MINIMAP_WIDTH,
        MINIMAP_Y + MINIMAP_HEIGHT
    )

    # -----------------------------------------------------
    # JANELA DO MUNDO
    # -----------------------------------------------------

    centro_x = player_instance.x
    centro_y = player_instance.y

    zoom = 2.0

    janela_zoom = graphic_functions.criarJanelaZoom(
        centro_x,
        centro_y,
        WIDTH,
        HEIGHT,
        zoom
    )

    # Não deixa a câmera sair da arena
    janela_zoom = graphic_functions.limitarJanela(
        janela_zoom,
        (
            0,
            0,
            WIDTH,
            HEIGHT
        )
    )

    # -----------------------------------------------------
    # FUNDO DO VIEWPORT
    # -----------------------------------------------------

    graphic_functions.drawRectFillSL(
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_WIDTH,
        MINIMAP_HEIGHT,
        (10, 10, 15),
        window
    )

    # -----------------------------------------------------
    # CLIPPING
    # -----------------------------------------------------

    graphic_functions.definirClipping(
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_X + MINIMAP_WIDTH - 1,
        MINIMAP_Y + MINIMAP_HEIGHT - 1
    )

    graphic_functions.desenharTexturaCompletaViewport(
        game_bg_surface,
        janela_zoom,
        viewport_zoom,
        window
    )

    # -----------------------------------------------------
    # PLAYER
    # -----------------------------------------------------

    player_vertices = [
        (
            player_instance.x - player_instance.width,
            player_instance.y - player_instance.height
        ),
        (
            player_instance.x + player_instance.width,
            player_instance.y - player_instance.height
        ),
        (
            player_instance.x + player_instance.width,
            player_instance.y + player_instance.height
        ),
        (
            player_instance.x - player_instance.width,
            player_instance.y + player_instance.height
        )
    ]

    player_zoom = graphic_functions.transformViewport(
        player_vertices,
        janela_zoom,
        viewport_zoom
    )

    graphic_functions.desenharTexturaViewport(
        player_vertices,
        player_instance.uvs,
        player_instance.tex,
        janela_zoom,
        viewport_zoom,
        window
    )

    for bullet in enemy_instance.bullets:
        if not bullet.active:
            continue

        bullet_zoom = graphic_functions.transformViewport(
            [(bullet.x, bullet.y)],
            janela_zoom,
            viewport_zoom
        )

        x = round(bullet_zoom[0][0])
        y = round(bullet_zoom[0][1])

        graphic_functions.drawCircleFillSL(
            x,
            y,
            bullet.radius,
            bullet.color,
            window
        )

    # -----------------------------------------------------
    # INIMIGO
    # -----------------------------------------------------

    enemy_vertices = [
        (
            enemy_instance.x - enemy_instance.width,
            enemy_instance.y - enemy_instance.height
        ),
        (
            enemy_instance.x + enemy_instance.width,
            enemy_instance.y - enemy_instance.height
        ),
        (
            enemy_instance.x + enemy_instance.width,
            enemy_instance.y + enemy_instance.height
        ),
        (
            enemy_instance.x - enemy_instance.width,
            enemy_instance.y + enemy_instance.height
        )
    ]

    graphic_functions.desenharTexturaViewport(
        enemy_vertices,
        enemy_instance.uvs,
        enemy_instance.sprite,
        janela_zoom,
        viewport_zoom,
        window
    )

    # -----------------------------------------------------
    # REMOVE CLIPPING
    # -----------------------------------------------------

    graphic_functions.removerClipping()

    # -----------------------------------------------------
    # BORDA
    # -----------------------------------------------------

    graphic_functions.drawRectangle(
        MINIMAP_X,
        MINIMAP_Y,
        MINIMAP_WIDTH,
        MINIMAP_HEIGHT,
        (255, 255, 255),
        window
    )

# =========================================================
# DRAW DO JOGO
# =========================================================

def draw_game():
    hud_x = 350
    hud_y = 125
    line_height = 20

    # -----------------------------------------------------
    # BACKGROUND
    # -----------------------------------------------------

    window.blit(
        game_bg_surface,
        (0, 0)
    )

    graphic_functions.logical_surface.blit(
        game_bg_surface,
        (0, 0),
        (0, 0, WIDTH, HEIGHT)
    )

    # -----------------------------------------------------
    # PLAYER
    # -----------------------------------------------------

    player_instance.draw()

    # -----------------------------------------------------
    # ENEMY
    # -----------------------------------------------------

    enemy_instance.draw()

    if viewport_mode == "minimap":
        draw_minimap()
    else:
        draw_zoom_viewport()

    # -----------------------------------------------------
    # HUD
    # -----------------------------------------------------

    draw_text(
        f"LIVES: {player_instance.lives}",
        hud_x, hud_y,
        font_small
    )

    # SCORE
    draw_text(
        f"SCORE: {player_instance.score}",
        hud_x, hud_y + line_height,
        font_small
    )

    # Difficulty
    draw_text(
        f"DIFFICULTY: {selected_difficulty}",
        hud_x, hud_y + line_height * 2,
        font_small
    )

    # Shot Type
    draw_text(
        f"SHOT TYPE: {player.Player_Shot}",
        hud_x, hud_y + line_height * 3,
        font_small
    )

    # Total Damage
    draw_text(
        f"TOTAL DAMAGE: {enemy_instance.total_damage}",
        hud_x, hud_y + line_height * 4,
        font_small
    )

    # ENEMY HEALTH
    draw_text(
        f"ENEMY HEALTH: ",
        hud_x, hud_y - line_height * 5,
        font_small
    )

    draw_health_bar(hud_x + 100, hud_y - line_height * 5, 160, 16, enemy_instance.health_points, enemy_instance.max_health)

    if enemy_instance.max_phases is None:
        phase_text = (
            f"PHASE: "
            f"{enemy_instance.current_phase}"
        )
    else:
        phase_text = (
            f"PHASE: "
            f"{enemy_instance.current_phase} / "
            f"{enemy_instance.max_phases}"
        )

    draw_text(
        phase_text,
        hud_x, hud_y - line_height * 4,
        font_small
    )

    #current Spell
    draw_text(
        f"ATTACK: {enemy_instance.current_spell}",
        hud_x,
        hud_y - line_height * 3,
        font_small
    )

    remaining_frames = (enemy_instance.spell_duration - enemy_instance.spell_timer)

    spell_seconds = remaining_frames / 60
    if spell_seconds <= 0:
        spell_seconds = 0

    # SPELL TIMER
    draw_text(
        f"SPELL TIMER: {spell_seconds:.1f}",
        hud_x, hud_y - line_height * 2,
        font_small
    )

    # -----------------------------------------------------
    # GAMEPLAY
    # -----------------------------------------------------

    window.blit(
        graphic_functions.logical_surface,
        (0, 0)
    )

def draw_health_bar(
    x,
    y,
    width,
    height,
    current_health,
    max_health
):
    if max_health <= 0:
        return

    health_ratio = current_health / max_health

    if health_ratio < 0:
        health_ratio = 0

    if health_ratio > 1:
        health_ratio = 1

    # Fundo da barra
    graphic_functions.drawRectFillSL(x, y, width, height, (50, 0, 50), window)

    # Vida atual
    graphic_functions.drawRectFillSL(x, y, int(width * health_ratio), height, (255, 0, 0), window)


# =========================================================
# DRAW GERAL
# =========================================================

def draw():

    if game_state == "main_menu":

        draw_main_menu()

    elif game_state == "difficulty_menu":

        draw_difficulty_menu()

    elif game_state == "shot_menu":

        draw_shot_menu()

    elif game_state == "game":

        draw_game()

    elif game_state == "game_over":

        draw_game_over()

    elif game_state == "victory":

        draw_victory()

    pygame.display.flip()


# =========================================================
# LOOP PRINCIPAL
# =========================================================

def run():

    global running, viewport_mode

    init()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    if viewport_mode == "minimap":
                        viewport_mode = "zoom"
                    else:
                        viewport_mode = "minimap"


        update()
        draw()

        clock.tick(60)

    pygame.quit()

def load_background(filename):
    texture = pygame.image.load(filename).convert()

    surface = pygame.Surface(
        (VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    )

    surface.fill((0, 0, 0))

    graphic_functions.scanlineTexture(
        bg_vert,
        bg_uvs,
        texture,
        surface
    )

    return surface