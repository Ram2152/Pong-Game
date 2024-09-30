import pygame
import sys

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle settings
paddle_width, paddle_height = 10, 100
paddle_speed = 5

paddle1 = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball settings
ball_radius = 7
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 4, 4  # Ball movement speed

# Score settings
score1, score2 = 0, 0
font = pygame.font.Font(None, 36)

# Function to reset the ball to the center after a point is scored
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx *= -1  # Change direction of ball to give the other player a chance

# Function to draw the paddles, ball, and score
def draw_elements():
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, paddle1)
    pygame.draw.rect(window, WHITE, paddle2)
    pygame.draw.circle(window, WHITE, (ball_x, ball_y), ball_radius)

    # Render and draw score
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    window.blit(score_text, (WIDTH // 2 - 30, 20))

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Paddle movement (Player 1: W/S keys, Player 2: UP/DOWN arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy *= -1

    # Ball collision with paddles
    if paddle1.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius*2, ball_radius*2)):
        ball_dx *= -1
    if paddle2.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius*2, ball_radius*2)):
        ball_dx *= -1

    # Check if the ball goes out of bounds (score condition)
    if ball_x - ball_radius <= 0:  # Player 2 scores
        score2 += 1
        reset_ball()
    if ball_x + ball_radius >= WIDTH:  # Player 1 scores
        score1 += 1
        reset_ball()

    # Draw elements on the window
    draw_elements()

    # Update the display
    pygame.display.flip()

    # Maintain 60 frames per second
    clock.tick(60)
