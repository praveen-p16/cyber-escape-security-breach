import pygame
import random
import math
import os
from collections import deque

# ============================================================
# CYBER ESCAPE // SECURITY BREACH
# 1920 x 1080 FULL HD VERSION
#
# Features:
#   - BFS enemy AI
#   - Firewall obstacles
#   - 3 lives
#   - Timer and time bonus
#   - 10 levels
#   - Coins and shields
#   - Top-5 local leaderboard
#   - Start / Help / Leaderboard / Pause screens
#   - Neon cyber visual effects
# ============================================================

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1920
HEIGHT = 1080
HUD_HEIGHT = 120
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CYBER ESCAPE // SECURITY BREACH")
clock = pygame.time.Clock()

# ============================================================
# GRID
# ============================================================

GRID_SIZE = 10
CELL = 80

GRID_WIDTH = GRID_SIZE * CELL
GRID_HEIGHT = GRID_SIZE * CELL

GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = 140

# ============================================================
# FONTS
# ============================================================

font_small = pygame.font.SysFont("consolas", 20, bold=True)
font = pygame.font.SysFont("consolas", 28, bold=True)
font_large = pygame.font.SysFont("consolas", 46, bold=True)
font_huge = pygame.font.SysFont("consolas", 64, bold=True)

# ============================================================
# COLORS
# ============================================================

BLACK = (2, 5, 12)
DARK = (6, 13, 28)
PANEL = (8, 20, 40)

WHITE = (235, 245, 255)

CYAN = (0, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 255, 130)
RED = (255, 45, 70)
YELLOW = (255, 220, 0)
PURPLE = (185, 0, 255)
PINK = (255, 0, 160)

GRAY = (100, 115, 135)
GRID_LINE = (15, 70, 100)

# ============================================================
# SETTINGS
# ============================================================

HIGH_SCORE_FILE = "cyber_highscores.txt"

PLAYER_START = (0, GRID_SIZE - 1)

MAX_LIVES = 3
MAX_LEVEL = 10
START_TIME = 55.0

particles = []


# ============================================================
# TEXT
# ============================================================

def draw_text(text, x, y, color, used_font, center=False):

    surface = used_font.render(
        str(text),
        True,
        color
    )

    if center:
        rect = surface.get_rect(
            center=(int(x), int(y))
        )
    else:
        rect = surface.get_rect(
            topleft=(int(x), int(y))
        )

    screen.blit(surface, rect)


# ============================================================
# HIGH SCORES
# ============================================================

def load_scores():

    scores = []

    if not os.path.exists(HIGH_SCORE_FILE):
        return scores

    try:

        with open(
            HIGH_SCORE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:
                    scores.append(int(line))
                except ValueError:
                    continue

    except OSError:
        return []

    scores.sort(reverse=True)

    return scores[:5]


def save_score(score):

    scores = load_scores()

    scores.append(int(score))

    scores.sort(reverse=True)

    scores = scores[:5]

    try:

        with open(
            HIGH_SCORE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            for value in scores:
                file.write(str(value) + "\n")

    except OSError:
        pass


def get_best_score(current_score):

    scores = load_scores()

    if scores:
        return max(
            max(scores),
            current_score
        )

    return current_score


# ============================================================
# GRID HELPERS
# ============================================================

def get_neighbors(position, obstacles):

    x, y = position

    directions = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    )

    result = []

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if (
            0 <= nx < GRID_SIZE
            and 0 <= ny < GRID_SIZE
        ):

            if (nx, ny) not in obstacles:
                result.append((nx, ny))

    return result


def reachable(start, obstacles):

    visited = {start}

    queue = deque([start])

    while queue:

        current = queue.popleft()

        for neighbor in get_neighbors(
            current,
            obstacles
        ):

            if neighbor not in visited:

                visited.add(neighbor)
                queue.append(neighbor)

    return visited


def random_free_position(used, obstacles):

    available = []

    for y in range(GRID_SIZE):

        for x in range(GRID_SIZE):

            position = (x, y)

            if position not in used \
                    and position not in obstacles:

                available.append(position)

    if not available:
        return None

    return random.choice(available)


def create_obstacles(level):

    obstacles = set()

    target = min(
        4 + level,
        15
    )

    attempts = 0

    while (
        len(obstacles) < target
        and attempts < 500
    ):

        attempts += 1

        candidate = (
            random.randint(
                0,
                GRID_SIZE - 1
            ),
            random.randint(
                0,
                GRID_SIZE - 1
            )
        )

        if candidate == PLAYER_START:
            continue

        if candidate in obstacles:
            continue

        test = obstacles | {candidate}

        if len(
            reachable(
                PLAYER_START,
                test
            )
        ) >= 60 - level:

            obstacles.add(candidate)

    return obstacles


def create_game(level):

    player = PLAYER_START

    obstacles = create_obstacles(level)

    obstacles.discard(player)

    used = {player}

    key = random_free_position(
        used,
        obstacles
    )

    if key is None:
        key = (1, GRID_SIZE - 1)

    used.add(key)

    exit_pos = random_free_position(
        used,
        obstacles
    )

    if exit_pos is None:
        exit_pos = (
            GRID_SIZE - 1,
            0
        )

    used.add(exit_pos)

    coin = random_free_position(
        used,
        obstacles
    )

    if coin:
        used.add(coin)

    shield = random_free_position(
        used,
        obstacles
    )

    if shield:
        used.add(shield)

    # --------------------------------------------------------
    # BOTS
    # --------------------------------------------------------

    bots = []

    bot_count = min(
        2 + level,
        7
    )

    for _ in range(bot_count):

        candidates = []

        for y in range(GRID_SIZE):

            for x in range(GRID_SIZE):

                position = (x, y)

                if position in obstacles:
                    continue

                if position in used:
                    continue

                if position in bots:
                    continue

                distance = (
                    abs(position[0] - player[0])
                    +
                    abs(position[1] - player[1])
                )

                if distance >= 4:
                    candidates.append(position)

        if not candidates:
            break

        bot = random.choice(candidates)

        bots.append(bot)

    return {
        "player": player,
        "key": key,
        "exit": exit_pos,
        "coin": coin,
        "shield": shield,
        "bots": bots,
        "obstacles": obstacles
    }


# ============================================================
# BFS AI
# ============================================================

def bfs_next_step(
    start,
    target,
    obstacles
):

    if start == target:
        return start

    queue = deque([start])

    previous = {
        start: None
    }

    while queue:

        current = queue.popleft()

        for neighbor in get_neighbors(
            current,
            obstacles
        ):

            if neighbor in previous:
                continue

            previous[neighbor] = current

            if neighbor == target:

                path = []

                node = target

                while node is not None:

                    path.append(node)

                    node = previous[node]

                path.reverse()

                if len(path) > 1:
                    return path[1]

                return start

            queue.append(neighbor)

    return start


def move_bots(
    bots,
    player,
    obstacles,
    level
):

    new_bots = []

    for bot in bots:

        random_chance = max(
            0.04,
            0.16 - level * 0.01
        )

        if random.random() < random_chance:

            options = get_neighbors(
                bot,
                obstacles
            )

            if options:
                new_position = random.choice(
                    options
                )
            else:
                new_position = bot

        else:

            new_position = bfs_next_step(
                bot,
                player,
                obstacles
            )

        new_bots.append(
            new_position
        )

    return new_bots


# ============================================================
# POSITION
# ============================================================

def grid_position(position):

    x = (
        GRID_X
        + position[0] * CELL
        + CELL // 2
    )

    y = (
        GRID_Y
        + position[1] * CELL
        + CELL // 2
    )

    return x, y


# ============================================================
# GLOW EFFECTS
# ============================================================

def draw_glow_circle(
    x,
    y,
    radius,
    color
):

    radius = max(
        1,
        int(radius)
    )

    size = max(
        32,
        radius * 8
    )

    glow = pygame.Surface(
        (size, size),
        pygame.SRCALPHA
    )

    center = size // 2

    for r in range(
        radius * 3,
        radius,
        -4
    ):

        alpha = max(
            4,
            55 - (r - radius) * 2
        )

        pygame.draw.circle(
            glow,
            (
                color[0],
                color[1],
                color[2],
                alpha
            ),
            (center, center),
            r
        )

    pygame.draw.circle(
        glow,
        color,
        (center, center),
        radius
    )

    screen.blit(
        glow,
        (
            x - center,
            y - center
        )
    )


def draw_glow_rect(
    rect,
    color,
    glow_size=15
):

    glow = pygame.Surface(
        (
            rect.width + glow_size * 2,
            rect.height + glow_size * 2
        ),
        pygame.SRCALPHA
    )

    for i in range(
        glow_size,
        0,
        -3
    ):

        alpha = max(
            5,
            50 - i * 2
        )

        pygame.draw.rect(
            glow,
            (
                color[0],
                color[1],
                color[2],
                alpha
            ),
            (
                glow_size - i // 2,
                glow_size - i // 2,
                rect.width + i,
                rect.height + i
            ),
            2,
            border_radius=8
        )

    screen.blit(
        glow,
        (
            rect.x - glow_size,
            rect.y - glow_size
        )
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        2,
        border_radius=8
    )


# ============================================================
# PARTICLES
# ============================================================

def create_particles(
    x,
    y,
    color,
    amount=20
):

    for _ in range(amount):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            1,
            5
        )

        particles.append({
            "x": float(x),
            "y": float(y),
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.randint(20, 50),
            "size": random.randint(2, 5),
            "color": color
        })


def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vx"] *= 0.95
        particle["vy"] *= 0.95

        particle["life"] -= 1

        if particle["life"] <= 0:
            particles.remove(
                particle
            )


def draw_particles():

    for particle in particles:

        alpha = min(
            255,
            particle["life"] * 5
        )

        layer = pygame.Surface(
            (20, 20),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            layer,
            (
                particle["color"][0],
                particle["color"][1],
                particle["color"][2],
                alpha
            ),
            (10, 10),
            particle["size"]
        )

        screen.blit(
            layer,
            (
                int(particle["x"]) - 10,
                int(particle["y"]) - 10
            )
        )


# ============================================================
# BACKGROUND
# ============================================================

def draw_background(t):

    screen.fill(BLACK)

    # Digital particles
    for i in range(100):

        x = int(
            (
                i * 137
                + t * 0.02
            ) % WIDTH
        )

        y = int(
            (
                i * 73
                +
                math.sin(
                    t * 0.001 + i
                ) * 30
            ) % HEIGHT
        )

        brightness = (
            40
            + (i % 5) * 20
        )

        pygame.draw.circle(
            screen,
            (
                0,
                brightness,
                brightness + 20
            ),
            (x, y),
            1
        )

    # Scan lines
    for y in range(
        0,
        HEIGHT,
        5
    ):

        pygame.draw.line(
            screen,
            (5, 15, 25),
            (0, y),
            (WIDTH, y)
        )


# ============================================================
# HUD
# ============================================================

def draw_hud(game):

    pygame.draw.rect(
        screen,
        PANEL,
        (0, 0, WIDTH, HUD_HEIGHT)
    )

    pygame.draw.line(
        screen,
        CYAN,
        (0, HUD_HEIGHT - 2),
        (WIDTH, HUD_HEIGHT - 2),
        2
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    draw_text(
        "CYBER ESCAPE",
        45,
        20,
        CYAN,
        font_large
    )

    draw_text(
        "// SECURITY BREACH",
        48,
        78,
        BLUE,
        font_small
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    draw_text(
        "SCORE "
        + str(game["score"]).zfill(6),
        620,
        25,
        YELLOW,
        font
    )

    draw_text(
        "LEVEL "
        + str(game["level"]),
        620,
        70,
        GREEN,
        font_small
    )

    # --------------------------------------------------------
    # BEST
    # --------------------------------------------------------

    best = get_best_score(
        game["score"]
    )

    draw_text(
        "BEST "
        + str(best).zfill(6),
        850,
        25,
        PINK,
        font
    )

    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    time_value = max(
        0,
        int(game["time_left"])
    )

    if time_value > 20:
        time_color = GREEN
    else:
        time_color = RED

    draw_text(
        "TIME "
        + str(time_value).zfill(2),
        1100,
        25,
        time_color,
        font
    )

    # --------------------------------------------------------
    # LIVES
    # --------------------------------------------------------

    draw_text(
        "LIVES "
        + str(game["lives"]),
        1300,
        25,
        (
            RED
            if game["lives"] == 1
            else PINK
        ),
        font
    )

    # --------------------------------------------------------
    # KEY
    # --------------------------------------------------------

    key_color = (
        GREEN
        if game["has_key"]
        else WHITE
    )

    draw_text(
        "KEY "
        +
        (
            "ACQUIRED"
            if game["has_key"]
            else "SEARCH"
        ),
        1300,
        70,
        key_color,
        font_small
    )

    # --------------------------------------------------------
    # SHIELD
    # --------------------------------------------------------

    shield_color = (
        PURPLE
        if game["has_shield"]
        else GRAY
    )

    draw_glow_circle(
        1660,
        58,
        14,
        shield_color
    )

    draw_text(
        "S",
        1660,
        58,
        WHITE,
        font_small,
        center=True
    )

    draw_text(
        "SHIELD",
        1690,
        48,
        shield_color,
        font_small
    )


# ============================================================
# GRID
# ============================================================

def draw_grid(
    t,
    obstacles
):

    outer = pygame.Rect(
        GRID_X - 12,
        GRID_Y - 12,
        GRID_WIDTH + 24,
        GRID_HEIGHT + 24
    )

    draw_glow_rect(
        outer,
        CYAN,
        20
    )

    for row in range(
        GRID_SIZE
    ):

        for col in range(
            GRID_SIZE
        ):

            x = (
                GRID_X
                + col * CELL
            )

            y = (
                GRID_Y
                + row * CELL
            )

            pulse = int(
                5
                +
                math.sin(
                    t * 0.003
                    + row
                    + col
                ) * 3
            )

            rect = pygame.Rect(
                x + 4,
                y + 4,
                CELL - 8,
                CELL - 8
            )

            # ------------------------------------------------
            # FIREWALL
            # ------------------------------------------------

            if (col, row) in obstacles:

                pygame.draw.rect(
                    screen,
                    (35, 35, 55),
                    rect,
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    RED,
                    rect,
                    2,
                    border_radius=5
                )

                draw_text(
                    "FW",
                    x + CELL // 2,
                    y + CELL // 2,
                    RED,
                    font_small,
                    center=True
                )

            # ------------------------------------------------
            # NORMAL CELL
            # ------------------------------------------------

            else:

                pygame.draw.rect(
                    screen,
                    (
                        5,
                        16 + pulse,
                        30 + pulse
                    ),
                    rect,
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    GRID_LINE,
                    rect,
                    1,
                    border_radius=5
                )

                # Circuit decoration
                pygame.draw.line(
                    screen,
                    CYAN,
                    (x + 10, y + 10),
                    (x + 22, y + 10),
                    1
                )

                pygame.draw.line(
                    screen,
                    CYAN,
                    (x + 10, y + 10),
                    (x + 10, y + 22),
                    1
                )


# ============================================================
# PLAYER
# ============================================================

def draw_player(
    position,
    t
):

    x, y = grid_position(
        position
    )

    pulse = int(
        math.sin(
            t * 0.008
        ) * 4
    )

    draw_glow_circle(
        x,
        y,
        23 + pulse,
        CYAN
    )

    points = [
        (x, y - 30),
        (x + 30, y),
        (x, y + 30),
        (x - 30, y)
    ]

    pygame.draw.polygon(
        screen,
        WHITE,
        points
    )

    inner = [
        (x, y - 17),
        (x + 17, y),
        (x, y + 17),
        (x - 17, y)
    ]

    pygame.draw.polygon(
        screen,
        CYAN,
        inner
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (x, y),
        5
    )


# ============================================================
# BOT
# ============================================================

def draw_bot(
    position,
    t
):

    x, y = grid_position(
        position
    )

    pulse = int(
        math.sin(
            t * 0.01 + x
        ) * 2
    )

    draw_glow_circle(
        x,
        y,
        20 + pulse,
        RED
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            x - 25,
            y - 20,
            50,
            40
        ),
        border_radius=9
    )

    pygame.draw.rect(
        screen,
        BLACK,
        (
            x - 18,
            y - 11,
            36,
            20
        ),
        border_radius=5
    )

    pygame.draw.circle(
        screen,
        PINK,
        (
            x - 9,
            y - 1
        ),
        4
    )

    pygame.draw.circle(
        screen,
        PINK,
        (
            x + 9,
            y - 1
        ),
        4
    )

    pygame.draw.line(
        screen,
        RED,
        (
            x,
            y - 20
        ),
        (
            x,
            y - 31
        ),
        3
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (
            x,
            y - 32
        ),
        4
    )


# ============================================================
# KEY
# ============================================================

def draw_key(position):

    x, y = grid_position(
        position
    )

    draw_glow_circle(
        x,
        y,
        15,
        YELLOW
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (
            x - 10,
            y
        ),
        10,
        3
    )

    pygame.draw.line(
        screen,
        YELLOW,
        (
            x,
            y
        ),
        (
            x + 23,
            y
        ),
        5
    )

    pygame.draw.line(
        screen,
        YELLOW,
        (
            x + 15,
            y
        ),
        (
            x + 15,
            y + 9
        ),
        4
    )


# ============================================================
# COIN
# ============================================================

def draw_coin(
    position,
    t
):

    if position is None:
        return

    x, y = grid_position(
        position
    )

    pulse = int(
        math.sin(
            t * 0.01
        ) * 3
    )

    draw_glow_circle(
        x,
        y,
        16 + pulse,
        YELLOW
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        (x, y),
        16
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        11,
        2
    )

    draw_text(
        "$",
        x,
        y,
        BLACK,
        font_small,
        center=True
    )


# ============================================================
# SHIELD
# ============================================================

def draw_shield(position):

    if position is None:
        return

    x, y = grid_position(
        position
    )

    draw_glow_circle(
        x,
        y,
        22,
        PURPLE
    )

    points = [
        (x, y - 28),
        (x + 22, y - 13),
        (x + 17, y + 18),
        (x, y + 29),
        (x - 17, y + 18),
        (x - 22, y - 13)
    ]

    pygame.draw.polygon(
        screen,
        PURPLE,
        points
    )

    pygame.draw.polygon(
        screen,
        WHITE,
        points,
        2
    )

    draw_text(
        "S",
        x,
        y,
        WHITE,
        font_small,
        center=True
    )


# ============================================================
# EXIT
# ============================================================

def draw_exit(
    position,
    unlocked,
    t
):

    x, y = grid_position(
        position
    )

    color = (
        GREEN
        if unlocked
        else RED
    )

    pulse = int(
        math.sin(
            t * 0.008
        ) * 5
    )

    rect = pygame.Rect(
        x - 28 - pulse,
        y - 28 - pulse,
        56 + pulse * 2,
        56 + pulse * 2
    )

    draw_glow_rect(
        rect,
        color,
        15
    )

    draw_text(
        "EXIT",
        x,
        y - 11,
        color,
        font_small,
        center=True
    )

    if not unlocked:

        draw_text(
            "LOCK",
            x,
            y + 15,
            RED,
            font_small,
            center=True
        )


# ============================================================
# MENU
# ============================================================

def draw_menu():

    screen.fill(BLACK)

    draw_text(
        "CYBER ESCAPE",
        WIDTH // 2,
        180,
        CYAN,
        font_huge,
        center=True
    )

    draw_text(
        "// SECURITY BREACH",
        WIDTH // 2,
        245,
        GREEN,
        font,
        center=True
    )

    box = pygame.Rect(
        610,
        320,
        700,
        400
    )

    draw_glow_rect(
        box,
        CYAN,
        25
    )

    draw_text(
        "[ ENTER ]  START GAME",
        WIDTH // 2,
        395,
        WHITE,
        font,
        center=True
    )

    draw_text(
        "[ H ]      HOW TO PLAY",
        WIDTH // 2,
        465,
        WHITE,
        font,
        center=True
    )

    draw_text(
        "[ L ]      LEADERBOARD",
        WIDTH // 2,
        535,
        WHITE,
        font,
        center=True
    )

    draw_text(
        "[ ESC ]    EXIT",
        WIDTH // 2,
        605,
        RED,
        font,
        center=True
    )

    draw_text(
        "BFS AI SECURITY BOTS ONLINE",
        WIDTH // 2,
        850,
        BLUE,
        font_small,
        center=True
    )

    draw_text(
        "SYSTEM STATUS: SECURE",
        WIDTH // 2,
        890,
        GREEN,
        font_small,
        center=True
    )


# ============================================================
# HELP
# ============================================================

def draw_help():

    screen.fill(BLACK)

    draw_text(
        "HOW TO PLAY",
        WIDTH // 2,
        80,
        CYAN,
        font_huge,
        center=True
    )

    instructions = [

        (
            "WASD / ARROWS",
            "Move through the network"
        ),

        (
            "YELLOW KEY",
            "Collect it to unlock the exit"
        ),

        (
            "GREEN EXIT",
            "Reach it after getting the key"
        ),

        (
            "PURPLE SHIELD",
            "Blocks one bot collision"
        ),

        (
            "YELLOW $",
            "Collect for bonus points"
        ),

        (
            "RED FW",
            "Firewall obstacle - cannot pass"
        ),

        (
            "RED BOTS",
            "BFS-powered AI security agents"
        ),

        (
            "TIME",
            "Escape before the timer reaches zero"
        ),

        (
            "P",
            "Pause / resume"
        ),

        (
            "ESC",
            "Return to menu"
        )
    ]

    y = 190

    for title, description in instructions:

        draw_text(
            title,
            450,
            y,
            YELLOW,
            font_small
        )

        draw_text(
            description,
            850,
            y,
            WHITE,
            font_small
        )

        y += 62

    draw_text(
        "Press H or ESC to return",
        WIDTH // 2,
        950,
        CYAN,
        font,
        center=True
    )


# ============================================================
# LEADERBOARD
# ============================================================

def draw_leaderboard():

    screen.fill(BLACK)

    draw_text(
        "CYBER LEADERBOARD",
        WIDTH // 2,
        110,
        CYAN,
        font_huge,
        center=True
    )

    scores = load_scores()

    if not scores:

        draw_text(
            "NO SCORES YET",
            WIDTH // 2,
            430,
            GRAY,
            font_large,
            center=True
        )

    else:

        y = 280

        for index, score in enumerate(
            scores,
            start=1
        ):

            draw_text(
                str(index) + ".",
                750,
                y,
                (
                    PINK
                    if index == 1
                    else WHITE
                ),
                font
            )

            draw_text(
                str(score).zfill(6),
                900,
                y,
                YELLOW,
                font
            )

            y += 80

    draw_text(
        "Press L or ESC to return",
        WIDTH // 2,
        950,
        CYAN,
        font,
        center=True
    )


# ============================================================
# PAUSE
# ============================================================

def draw_pause():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 190)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        580,
        350,
        760,
        360
    )

    draw_glow_rect(
        box,
        CYAN,
        25
    )

    draw_text(
        "SYSTEM PAUSED",
        WIDTH // 2,
        440,
        CYAN,
        font_huge,
        center=True
    )

    draw_text(
        "[ P ] RESUME",
        WIDTH // 2,
        540,
        GREEN,
        font,
        center=True
    )

    draw_text(
        "[ ESC ] MENU",
        WIDTH // 2,
        610,
        RED,
        font,
        center=True
    )


# ============================================================
# GAME OVER
# ============================================================

def draw_game_over(game):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 195)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        500,
        300,
        920,
        500
    )

    pygame.draw.rect(
        screen,
        DARK,
        box,
        border_radius=15
    )

    draw_glow_rect(
        box,
        RED,
        30
    )

    draw_text(
        "SYSTEM BREACHED",
        WIDTH // 2,
        400,
        RED,
        font_huge,
        center=True
    )

    draw_text(
        "FINAL SCORE: "
        + str(game["score"]).zfill(6),
        WIDTH // 2,
        510,
        YELLOW,
        font_large,
        center=True
    )

    draw_text(
        "LEVEL REACHED: "
        + str(game["level"]),
        WIDTH // 2,
        575,
        WHITE,
        font_small,
        center=True
    )

    draw_text(
        "[ R ] REBOOT SYSTEM",
        WIDTH // 2,
        660,
        CYAN,
        font,
        center=True
    )

    draw_text(
        "[ ESC ] RETURN TO MENU",
        WIDTH // 2,
        720,
        RED,
        font_small,
        center=True
    )


# ============================================================
# VICTORY
# ============================================================

def draw_victory(game):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 10, 0, 185)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    box = pygame.Rect(
        480,
        300,
        960,
        500
    )

    pygame.draw.rect(
        screen,
        DARK,
        box,
        border_radius=15
    )

    draw_glow_rect(
        box,
        GREEN,
        30
    )

    draw_text(
        "NETWORK SECURED",
        WIDTH // 2,
        400,
        GREEN,
        font_huge,
        center=True
    )

    draw_text(
        "FINAL SCORE: "
        + str(game["score"]).zfill(6),
        WIDTH // 2,
        510,
        YELLOW,
        font_large,
        center=True
    )

    draw_text(
        "ALL 10 LEVELS COMPLETED",
        WIDTH // 2,
        575,
        WHITE,
        font_small,
        center=True
    )

    draw_text(
        "[ R ] PLAY AGAIN",
        WIDTH // 2,
        660,
        CYAN,
        font,
        center=True
    )

    draw_text(
        "[ ESC ] RETURN TO MENU",
        WIDTH // 2,
        720,
        RED,
        font_small,
        center=True
    )


# ============================================================
# LEVEL COMPLETE
# ============================================================

def draw_level_complete(game):

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 215))
    screen.blit(overlay, (0, 0))

    box = pygame.Rect(WIDTH // 2 - 500, HEIGHT // 2 - 280, 1000, 560)
    pygame.draw.rect(screen, DARK, box, border_radius=20)
    draw_glow_rect(box, GREEN, 30)

    draw_text("LEVEL " + str(game["level"]), WIDTH // 2, box.y + 70, CYAN, font_large, center=True)
    draw_text("COMPLETED!", WIDTH // 2, box.y + 135, GREEN, font_huge, center=True)

    pygame.draw.line(screen, GREEN, (box.x + 80, box.y + 190), (box.right - 80, box.y + 190), 2)

    draw_text("SECURITY NODE SUCCESSFULLY BREACHED", WIDTH // 2, box.y + 225, WHITE, font_small, center=True)
    draw_text("SCORE: " + str(game["score"]).zfill(6), WIDTH // 2, box.y + 270, YELLOW, font, center=True)

    replay_box = pygame.Rect(WIDTH // 2 - 390, box.y + 340, 350, 75)
    pygame.draw.rect(screen, PANEL, replay_box, border_radius=10)
    pygame.draw.rect(screen, YELLOW, replay_box, 2, border_radius=10)
    draw_text("[ R ]  REPLAY LEVEL", replay_box.centerx, replay_box.centery, YELLOW, font, center=True)

    next_box = pygame.Rect(WIDTH // 2 + 40, box.y + 340, 350, 75)
    pygame.draw.rect(screen, PANEL, next_box, border_radius=10)
    pygame.draw.rect(screen, CYAN, next_box, 2, border_radius=10)
    draw_text("[ ENTER ]  NEXT LEVEL", next_box.centerx, next_box.centery, CYAN, font, center=True)

    draw_text("[ ESC ]  MAIN MENU", WIDTH // 2, box.y + 470, RED, font_small, center=True)


# ============================================================
# LEVEL MESSAGE
# ============================================================

def draw_level_message(
    level,
    timer
):

    if timer <= 0:
        return

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    alpha = min(
        220,
        max(
            0,
            timer * 3
        )
    )

    box = pygame.Rect(
        580,
        420,
        760,
        240
    )

    pygame.draw.rect(
        overlay,
        (
            5,
            15,
            35,
            alpha
        ),
        box,
        border_radius=15
    )

    pygame.draw.rect(
        overlay,
        (
            CYAN[0],
            CYAN[1],
            CYAN[2],
            alpha
        ),
        box,
        3,
        border_radius=15
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    draw_text(
        "LEVEL " + str(level),
        WIDTH // 2,
        500,
        CYAN,
        font_huge,
        center=True
    )

    draw_text(
        "SECURITY LEVEL INCREASED",
        WIDTH // 2,
        575,
        GREEN,
        font_small,
        center=True
    )


# ============================================================
# NEW GAME
# ============================================================

def new_game():

    level_data = create_game(1)

    return {

        "player":
            level_data["player"],

        "key":
            level_data["key"],

        "exit":
            level_data["exit"],

        "coin":
            level_data["coin"],

        "shield":
            level_data["shield"],

        "bots":
            level_data["bots"],

        "obstacles":
            level_data["obstacles"],

        "score":
            0,

        "level":
            1,

        "lives":
            MAX_LIVES,

        "has_key":
            False,

        "has_shield":
            False,

        "time_left":
            START_TIME,

        "level_timer":
            150,

        "bot_timer":
            0,

        "paused":
            False,

        "game_over":
            False,

        "victory":
            False,

        "level_complete":
            False,

        "score_saved":
            False
    }


# ============================================================
# NEXT LEVEL
# ============================================================

def load_next_level(game):

    game["level"] += 1

    level_data = create_game(
        game["level"]
    )

    game["player"] = \
        level_data["player"]

    game["key"] = \
        level_data["key"]

    game["exit"] = \
        level_data["exit"]

    game["coin"] = \
        level_data["coin"]

    game["shield"] = \
        level_data["shield"]

    game["bots"] = \
        level_data["bots"]

    game["obstacles"] = \
        level_data["obstacles"]

    game["has_key"] = False

    game["has_shield"] = False

    game["time_left"] = max(
        30.0,
        START_TIME
        - (
            game["level"] - 1
        ) * 2.0
    )

    game["level_timer"] = 150

    game["bot_timer"] = 0


# ============================================================
# COLLISION
# ============================================================

def handle_player_bot_collision(game):

    if game["player"] not in game["bots"]:
        return

    x, y = grid_position(
        game["player"]
    )

    # --------------------------------------------------------
    # SHIELD
    # --------------------------------------------------------

    if game["has_shield"]:

        game["has_shield"] = False

        game["bots"].remove(
            game["player"]
        )

        game["score"] += 10

        create_particles(
            x,
            y,
            PURPLE,
            40
        )

        return

    # --------------------------------------------------------
    # LOSE LIFE
    # --------------------------------------------------------

    game["lives"] -= 1

    create_particles(
        x,
        y,
        RED,
        50
    )

    if game["lives"] <= 0:

        game["game_over"] = True

        if not game["score_saved"]:

            save_score(
                game["score"]
            )

            game["score_saved"] = True

        return

    # --------------------------------------------------------
    # PUSH PLAYER
    # --------------------------------------------------------

    options = []

    for position in get_neighbors(
        game["player"],
        game["obstacles"]
    ):

        if position not in game["bots"]:
            options.append(position)

    if options:

        game["player"] = random.choice(
            options
        )


# ============================================================
# MAIN
# ============================================================

def main():

    global particles

    state = "menu"

    game = new_game()

    running = True

    while running:

        dt = (
            clock.tick(FPS)
            / 1000.0
        )

        t = pygame.time.get_ticks()

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            # =================================================
            # MENU
            # =================================================

            if state == "menu":

                if event.key == pygame.K_RETURN:

                    particles.clear()

                    game = new_game()

                    state = "game"

                elif event.key == pygame.K_h:

                    state = "help"

                elif event.key == pygame.K_l:

                    state = "leaderboard"

                elif event.key == pygame.K_ESCAPE:

                    running = False

            # =================================================
            # HELP
            # =================================================

            elif state == "help":

                if event.key in (
                    pygame.K_h,
                    pygame.K_ESCAPE
                ):

                    state = "menu"

            # =================================================
            # LEADERBOARD
            # =================================================

            elif state == "leaderboard":

                if event.key in (
                    pygame.K_l,
                    pygame.K_ESCAPE
                ):

                    state = "menu"

            # =================================================
            # GAME
            # =================================================

            elif state == "game":

                # ---------------------------------------------
                # ESCAPE
                # ---------------------------------------------

                if event.key == pygame.K_ESCAPE:

                    state = "menu"

                    continue

                # ---------------------------------------------
                # LEVEL COMPLETE
                # ---------------------------------------------

                if game["level_complete"]:

                    if event.key == pygame.K_r:
                        current_level = game["level"]
                        current_score = game["score"]
                        current_lives = game["lives"]

                        level_data = create_game(current_level)
                        game["player"] = level_data["player"]
                        game["key"] = level_data["key"]
                        game["exit"] = level_data["exit"]
                        game["coin"] = level_data["coin"]
                        game["shield"] = level_data["shield"]
                        game["bots"] = level_data["bots"]
                        game["obstacles"] = level_data["obstacles"]
                        game["score"] = current_score
                        game["lives"] = current_lives
                        game["has_key"] = False
                        game["has_shield"] = False
                        game["time_left"] = max(30.0, START_TIME - (current_level - 1) * 2.0)
                        game["level_timer"] = 150
                        game["bot_timer"] = 0
                        game["level_complete"] = False
                        game["paused"] = False
                        particles.clear()

                    elif event.key == pygame.K_RETURN:
                        game["level_complete"] = False
                        game["paused"] = False
                        load_next_level(game)

                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"

                    continue

                # ---------------------------------------------
                # PAUSE
                # ---------------------------------------------

                if event.key == pygame.K_p:

                    if (
                        not game["game_over"]
                        and
                        not game["victory"]
                    ):

                        game["paused"] = \
                            not game["paused"]

                    continue

                # ---------------------------------------------
                # RESTART
                # ---------------------------------------------

                if (
                    game["game_over"]
                    or
                    game["victory"]
                ):

                    if event.key == pygame.K_r:

                        particles.clear()

                        game = new_game()

                    continue

                # ---------------------------------------------
                # PAUSED
                # ---------------------------------------------

                if game["paused"]:
                    continue

                # =================================================
                # PLAYER MOVEMENT
                # =================================================

                px, py = game["player"]

                if event.key in (
                    pygame.K_LEFT,
                    pygame.K_a
                ):

                    px -= 1

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d
                ):

                    px += 1

                elif event.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    py -= 1

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    py += 1

                else:
                    continue

                # ---------------------------------------------
                # GRID BOUNDARIES
                # ---------------------------------------------

                px = max(
                    0,
                    min(
                        GRID_SIZE - 1,
                        px
                    )
                )

                py = max(
                    0,
                    min(
                        GRID_SIZE - 1,
                        py
                    )
                )

                new_position = (
                    px,
                    py
                )

                if (
                    new_position
                    == game["player"]
                ):

                    continue

                # ---------------------------------------------
                # FIREWALL
                # ---------------------------------------------

                if (
                    new_position
                    in game["obstacles"]
                ):

                    x, y = grid_position(
                        game["player"]
                    )

                    create_particles(
                        x,
                        y,
                        RED,
                        8
                    )

                    continue

                # ---------------------------------------------
                # MOVE PLAYER
                # ---------------------------------------------

                game["player"] = \
                    new_position

                x, y = grid_position(
                    game["player"]
                )

                create_particles(
                    x,
                    y,
                    CYAN,
                    5
                )

                # =================================================
                # KEY
                # =================================================

                if (
                    game["player"]
                    == game["key"]
                    and
                    not game["has_key"]
                ):

                    game["has_key"] = True

                    game["score"] += 50

                    create_particles(
                        x,
                        y,
                        YELLOW,
                        30
                    )

                # =================================================
                # COIN
                # =================================================

                if (
                    game["coin"] is not None
                    and
                    game["player"]
                    == game["coin"]
                ):

                    game["score"] += 25

                    game["coin"] = None

                    create_particles(
                        x,
                        y,
                        YELLOW,
                        25
                    )

                # =================================================
                # SHIELD
                # =================================================

                if (
                    game["shield"] is not None
                    and
                    game["player"]
                    == game["shield"]
                ):

                    game["has_shield"] = True

                    game["shield"] = None

                    game["score"] += 20

                    create_particles(
                        x,
                        y,
                        PURPLE,
                        30
                    )

                # =================================================
                # BOT COLLISION
                # =================================================

                handle_player_bot_collision(
                    game
                )

                # =================================================
                # EXIT
                # =================================================

                if (
                    game["player"]
                    == game["exit"]
                    and
                    game["has_key"]
                    and
                    not game["game_over"]
                ):

                    time_bonus = int(
                        game["time_left"]
                    ) * 5

                    level_bonus = (
                        100
                        * game["level"]
                    )

                    game["score"] += (
                        time_bonus
                        +
                        level_bonus
                    )

                    create_particles(
                        x,
                        y,
                        GREEN,
                        60
                    )

                    if (
                        game["level"]
                        >= MAX_LEVEL
                    ):

                        game["victory"] = True
                        game["paused"] = False

                        create_particles(
                            WIDTH // 2,
                            HEIGHT // 2,
                            GREEN,
                            120
                        )

                        if not game["score_saved"]:

                            save_score(
                                game["score"]
                            )

                            game["score_saved"] = True

                    else:

                        # Stop here until the player chooses NEXT LEVEL.
                        game["level_complete"] = True
                        game["paused"] = True

                        create_particles(
                            WIDTH // 2,
                            HEIGHT // 2,
                            GREEN,
                            100
                        )

        # ====================================================
        # UPDATE
        # ====================================================

        if (
            state == "game"
            and
            not game["paused"]
            and
            not game["game_over"]
            and
            not game["victory"]
        ):

            # ------------------------------------------------
            # TIMER
            # ------------------------------------------------

            game["time_left"] -= dt

            if game["time_left"] <= 0:

                game["time_left"] = 0

                game["game_over"] = True

                if not game["score_saved"]:

                    save_score(
                        game["score"]
                    )

                    game["score_saved"] = True

            # ------------------------------------------------
            # LEVEL MESSAGE
            # ------------------------------------------------

            if game["level_timer"] > 0:

                game["level_timer"] -= 1

            # ------------------------------------------------
            # BOT MOVEMENT
            # ------------------------------------------------

            game["bot_timer"] -= 1

            if game["bot_timer"] <= 0:

                game["bots"] = move_bots(
                    game["bots"],
                    game["player"],
                    game["obstacles"],
                    game["level"]
                )

                game["bot_timer"] = max(
                    12,
                    35
                    -
                    game["level"] * 2
                )

                handle_player_bot_collision(
                    game
                )

        update_particles()

        # ====================================================
        # DRAW
        # ====================================================

        if state == "menu":

            draw_menu()

        elif state == "help":

            draw_help()

        elif state == "leaderboard":

            draw_leaderboard()

        elif state == "game":

            draw_background(t)

            draw_hud(game)

            draw_grid(
                t,
                game["obstacles"]
            )

            draw_exit(
                game["exit"],
                game["has_key"],
                t
            )

            # KEY
            if not game["has_key"]:

                draw_key(
                    game["key"]
                )

            # COIN
            draw_coin(
                game["coin"],
                t
            )

            # SHIELD
            draw_shield(
                game["shield"]
            )

            # BOTS
            for bot in game["bots"]:

                draw_bot(
                    bot,
                    t
                )

            # PLAYER
            draw_player(
                game["player"],
                t
            )

            # PARTICLES
            draw_particles()

            # ------------------------------------------------
            # BOTTOM CONTROLS
            # ------------------------------------------------

            draw_text(
                "WASD / ARROWS: MOVE",
                35,
                1020,
                CYAN,
                font_small
            )

            draw_text(
                "KEY -> EXIT",
                500,
                1020,
                YELLOW,
                font_small
            )

            draw_text(
                "SURVIVE THE BFS AI BOTS",
                850,
                1020,
                WHITE,
                font_small
            )

            draw_text(
                "P: PAUSE",
                1400,
                1020,
                GREEN,
                font_small
            )

            draw_text(
                "ESC: MENU",
                1620,
                1020,
                RED,
                font_small
            )

            # ------------------------------------------------
            # LEVEL MESSAGE
            # ------------------------------------------------

            draw_level_message(
                game["level"],
                game["level_timer"]
            )

            # ------------------------------------------------
            # LEVEL COMPLETE
            # ------------------------------------------------

            if game["level_complete"]:

                draw_level_complete(
                    game
                )

            # ------------------------------------------------
            # PAUSE
            # ------------------------------------------------

            elif game["paused"]:

                draw_pause()

            # ------------------------------------------------
            # GAME OVER
            # ------------------------------------------------

            elif game["game_over"]:

                draw_game_over(
                    game
                )

            # ------------------------------------------------
            # VICTORY
            # ------------------------------------------------

            elif game["victory"]:

                draw_victory(
                    game
                )

        pygame.display.flip()

    pygame.quit()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
