import pgzrun

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors (Christmas theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 20  # Increased size for bauble effect

# Speeds
PADDLE_SPEED = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
BALL_SPEED_INCREMENT = 0.5

# Paddles and ball positions
paddle1 = Rect((30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2 = Rect((WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT))
ball = Rect((WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)

# Ball direction
ball_dx = BALL_SPEED_X
ball_dy = BALL_SPEED_Y

# Game state
game_over = False

# Scores
score1 = 0
score2 = 0

# Ball color state
ball_color = RED

# Ball trail
trail = []

def reset_game():
    global ball_dx, ball_dy, game_over, ball_color, trail
    paddle1.y = (HEIGHT - PADDLE_HEIGHT) // 2
    paddle2.y = (HEIGHT - PADDLE_HEIGHT) // 2
    ball.x = (WIDTH - BALL_SIZE) // 2
    ball.y = (HEIGHT - BALL_SIZE) // 2
    ball_dx = BALL_SPEED_X
    ball_dy = BALL_SPEED_Y
    ball_color = RED
    trail = []
    game_over = False

def draw_start_button():
    start_button = Rect((WIDTH - 200) // 2, (HEIGHT - 50) // 2, 200, 50)
    screen.draw.filled_rect(start_button, GREEN)
    screen.draw.text("Start", center=(start_button.center), fontsize=36, color=BLACK)
    return start_button

def draw_christmas_tree():
    # Draw the tree using white triangles
    tree_base = HEIGHT - 50
    tree_height = 200
    tree_width = 150
    for i in range(3):
        screen.draw.filled_polygon([
            (WIDTH // 2, tree_base - i * tree_height // 3),
            (WIDTH // 2 - tree_width // 2 + i * 20, tree_base - (i + 1) * tree_height // 3),
            (WIDTH // 2 + tree_width // 2 - i * 20, tree_base - (i + 1) * tree_height // 3)
        ], WHITE)
    # Draw the tree trunk
    screen.draw.filled_rect(Rect(WIDTH // 2 - 15, tree_base, 30, 50), WHITE)

def update():
    global ball_dx, ball_dy, ball_color, score1, score2, game_over

    if not game_over:
        # Move paddles
        if keyboard.w and paddle1.top > 0:
            paddle1.y -= PADDLE_SPEED
        if keyboard.s and paddle1.bottom < HEIGHT:
            paddle1.y += PADDLE_SPEED
        if keyboard.up and paddle2.top > 0:
            paddle2.y -= PADDLE_SPEED
        if keyboard.down and paddle2.bottom < HEIGHT:
            paddle2.y += PADDLE_SPEED

        # Move ball
        ball.x += ball_dx
        ball.y += ball_dy

        # Add ball position to trail
        trail.append((ball.x, ball.y))
        if len(trail) > 10:  # Limit trail length
            trail.pop(0)

        # Ball collision with top and bottom
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy = -ball_dy

        # Ball collision with paddles
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_dx = -ball_dx
            ball_dx += BALL_SPEED_INCREMENT if ball_dx > 0 else -BALL_SPEED_INCREMENT
            ball_dy += BALL_SPEED_INCREMENT if ball_dy > 0 else -BALL_SPEED_INCREMENT
            ball_color = GOLD if ball_color == RED else RED

        # Ball out of bounds
        if ball.left <= 0:
            score2 += 1
            game_over = True
        if ball.right >= WIDTH:
            score1 += 1
            game_over = True

def draw():
    screen.fill(DARK_GREEN)

    # Draw Christmas tree background
    draw_christmas_tree()

    # Draw paddles
    screen.draw.filled_rect(paddle1, RED)
    screen.draw.filled_rect(paddle2, RED)

    # Draw ball trail
    for pos in trail:
        screen.draw.filled_ellipse(Rect(pos[0], pos[1], BALL_SIZE, BALL_SIZE), ball_color)

    # Draw ball
    screen.draw.filled_ellipse(ball, ball_color)

    # Draw scores
    screen.draw.text(str(score1), center=(WIDTH // 4, 20), fontsize=74, color=WHITE)
    screen.draw.text(str(score2), center=(WIDTH * 3 // 4, 20), fontsize=74, color=WHITE)

    if game_over:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=74, color=RED)
        start_button = draw_start_button()

pgzrun.go()
