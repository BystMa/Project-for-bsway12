import random
import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Konstanty
FPS = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20
MENU_FONT_SIZE = 60
MENU_FONT_COLOR = WHITE

# Barvy


# Inicializace Pygame
pygame.init()

# Vytvoření okna
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Attack")

# Fonty
font_score = pygame.font.Font(None, 30)
font_game_over = pygame.font.Font(None, 60)
font_menu = pygame.font.Font(None, MENU_FONT_SIZE)

# Zvukové efekty
sound_rotate = pygame.mixer.Sound("rotate.wav")
sound_place = pygame.mixer.Sound("place.wav")
sound_remove = pygame.mixer.Sound("remove.wav")
sound_game_over = pygame.mixer.Sound("game_over.wav")

# Funkce pro vytvoření nového kousku
def new_block():
    # Náhodná kombinace Pac-Manů a předmětů
    shapes = [
        [[1, 1], [1, 1]],  # blok
        [[1, 1, 1], [0, 1, 0]],  # L tvar
        [[0, 1, 0], [1, 1, 1]],  # zpětný L tvar
        [[1, 1, 0], [0, 1, 1]],  # zpětný zub
        [[0, 1, 1], [1, 1, 0]],  # zub
        [[1, 1, 1], [0, 1, 0], [0, 1, 0]],  # T tvar
        [[0, 1, 0], [0, 1, 0], [1, 1, 1]],  # I tvar
    ]
    # Náhodný výběr tvaru
    shape = random.choice(shapes)
    # Vytvoření nového kousku
    block = {
        "shape": shape,
        "color": random.choice([YELLOW, RED, BLUE]),
        "x": int(SCREEN_WIDTH
        / 2 - BLOCK_SIZE * len(shape[0]) / 2),
        "y": 0,
        "rotation": 0,
    }
    return block

# Funkce pro rotaci kousku
def rotate_block(block):
    # Změna velikosti matice
    new_shape = [[0 for _ in range(len(block["shape"]))] for _ in range(len(block["shape"][0]))]
    # Rotace matice
    for i in range(len(block["shape"])):
        for j in range(len(block["shape"][0])):
            new_shape[j][len(block["shape"]) - i - 1] = block["shape"][i][j]
    # Kontrola kolize
    if check_collision(block["x"], block["y"], new_shape):
        return
    # Aktualizace tvaru kousku
    block["shape"] = new_shape
    # Přehrání zvukového efektu
    sound_rotate.play()

# Funkce pro kontrolu kolize
def check_collision(x, y, shape):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == 1:
                if (
                    x + j < 0
                    or x + j >= GRID_WIDTH
                    or y + i >= GRID_HEIGHT
                    or (y + i >= 0 and grid[y + i][x + j] != BLACK)
                ):
                    return True
    return False

# Funkce pro přidání kousku na herní desku
def place_block(block):
    for i in range(len(block["shape"])):
        for j in range(len(block["shape"][0])):
            if block["shape"][i][j] == 1:
                grid[block["y"] + i][block["x"] + j] = block["color"]
    # Přehrání zvukového efektu
    sound_place.play()

# Funkce pro odstranění plných řádků
def remove_full_rows():
    rows_removed = 0
    y = GRID_HEIGHT - 1
    while y >= 0:
        if BLACK not in grid[y]:
            del grid[y]
            rows_removed += 1
            continue
        y -= 1
    for _ in range(rows_removed):
        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    # Přehrání zvukového efektu
    sound_remove.play()
    return rows_removed

# Funkce pro zobrazení skóre
def show_score(score):
    text = font_score.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH - 100, 10))

# Funkce pro zobrazení "Game Over" zprávy
def show_game_over():
    text = font_game_over.render("Game Over", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))

# Funkce pro zobrazení menu
# Funkce pro zobrazení menu
def show_menu():
    screen.fill(BLACK)
    title = font_title.render("Pac-Attack", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 100))
    # Tlačítka pro výběr režimu hry
    singleplayer_button = pygame.Rect(
        SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, 200, 40)
    multiplayer_button = pygame.Rect(
        SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 50, 200, 40)
    # Text na tlačítkách
    singleplayer_text = font_menu.render("Singleplayer", True, WHITE)
    multiplayer_text = font_menu.render("Multiplayer", True, WHITE)
    # Kreslení tlačítek
    pygame.draw.rect(screen, BLUE, singleplayer_button)
    pygame.draw.rect(screen, BLUE, multiplayer_button)
    # Kreslení textu na tlačítkách
    screen.blit(singleplayer_text, (SCREEN_WIDTH / 2 - singleplayer_text.get_width() / 2, SCREEN_HEIGHT / 2 - 40))
    screen.blit(multiplayer_text, (SCREEN_WIDTH / 2 - multiplayer_text.get_width() / 2, SCREEN_HEIGHT / 2 + 60))
    pygame.display.update()

# Hlavní smyčka hry
def main_loop():
    running = True
    game_over = False
    paused = False
    score = 0
    blocks = []
    next_block = create_block()
    rows_removed = 0
    FALL_SPEED = fall_speed
    fall_speed = FALL_SPEED
    clock = pygame.time.Clock()

    # Hlavní smyčka hry
    while running:
        # Ošetření událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif not game_over:
                    if event.key == pygame.K_LEFT:
                        move_block(blocks[0], -1)
                    elif event.key == pygame.K_RIGHT:
                        move_block(blocks[0], 1)
                    elif event.key == pygame.K_DOWN:
                        fall_speed = FALL_SPEED_FAST
                    elif event.key == pygame.K_UP:
                        rotate_block(blocks[0])
                    elif event.key == pygame.K_SPACE:
                        while move_block(blocks[0], 0, 1):
                            pass
                        place_block(blocks[0])
                        rows_removed += remove_full_rows()
                        score += 10 * rows_removed
                        rows_removed = 0
                        blocks.pop(0)
                        blocks.append(next_block)
                        next_block = create_block()
                    elif event.key == pygame.K_p:
                       

