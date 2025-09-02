import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1300, 700))

# Title and icon
pygame.display.set_caption("StarWeb")
icon = pygame.image.load('spider.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('superhero.png')
playerX = 300
playerY = 400
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = pygame.image.load('shield.png')

# List to hold multiple enemies
num_of_enemies = 30
enemies = []

for i in range(num_of_enemies):
    enemyX = random.randint(0, 1300)
    enemyY = random.randint(-100, -50)
    enemyY_change = random.uniform(0.2, 0.6)
    enemies.append([enemyX, enemyY, enemyY_change])

# Border properties
border_thickness = 20
border_color = (255, 0, 0)  # Red color

# Define font for start, timer, game over, and win messages
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 40)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def is_collision(playerX, playerY, enemyX, enemyY):
    player_width = playerImg.get_width()
    player_height = playerImg.get_height()
    enemy_width = enemyImg.get_width()
    enemy_height = enemyImg.get_height()

    if (enemyX < playerX + player_width and enemyX + enemy_width > playerX and
            enemyY < playerY + player_height and enemyY + enemy_height > playerY):
        return True
    return False


def show_game_over():
    screen.fill((0, 0, 0))
    text = font.render('You Lost', True, (255, 0, 0))  # Red color for 'You Lost' text
    text_rect = text.get_rect(center=(1300 // 2, 700 // 2))

    restart_text = small_font.render('Press R to Restart', True, (255, 255, 255))  # White color for restart message
    restart_rect = restart_text.get_rect(center=(1300 // 2, (700 // 2) + 100))  # Below 'You Lost'

    screen.blit(text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()


def show_win_screen():
    screen.fill((0, 0, 0))
    win_text = font.render('You Win!', True, (0, 255, 0))  # Green color for win text
    win_rect = win_text.get_rect(center=(1300 // 2, 700 // 2))

    restart_text = small_font.render('Press R to Restart', True, (255, 255, 255))  # White for restart message
    restart_rect = restart_text.get_rect(center=(1300 // 2, (700 // 2) + 100))

    screen.blit(win_text, win_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.update()


def show_start_screen():
    screen.fill((0, 0, 0))
    title_text = font.render('StarWeb', True, (255, 255, 255))  # White text for the title
    title_rect = title_text.get_rect(center=(1300 // 2, 200))

    start_text = small_font.render('Press ENTER to Start', True, (255, 255, 255))  # White text for the start prompt
    start_rect = start_text.get_rect(center=(1300 // 2, 300))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.update()


def wait_for_start():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Check for Enter/Return key
                    waiting = False  # Exit the waiting loop to start the game


# Game loop
running = True
game_over = False
game_won = False
start_ticks = pygame.time.get_ticks()

# Show the start screen and wait for the player to press ENTER
show_start_screen()
wait_for_start()

while running:
    if not game_over and not game_won:
        screen.fill((0, 0, 0))

        # Draw borders
        pygame.draw.rect(screen, border_color, (0, 0, border_thickness, 700))  # Left border
        pygame.draw.rect(screen, border_color, (1300 - border_thickness, 0, border_thickness, 700))  # Right border
        pygame.draw.rect(screen, border_color, (0, 0, 1300, border_thickness))  # Top border
        pygame.draw.rect(screen, border_color, (0, 700 - border_thickness, 1300, border_thickness))  # Bottom border

        # Calculate elapsed time
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = small_font.render(f'Time: {seconds}', True, (255, 255, 255))  # White text for the timer
        screen.blit(timer_text, (10, 10))  # Display timer at top left corner

        # Check if player survived for 60 seconds
        if seconds >= 60:
            game_won = True
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2
                if event.key == pygame.K_UP:
                    playerY_change = -2
                if event.key == pygame.K_DOWN:
                    playerY_change = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        # Update player position
        playerX += playerX_change
        playerY += playerY_change

        # Prevent player from moving outside the borders
        if playerX < border_thickness:
            playerX = border_thickness
        elif playerX > 1300 - border_thickness - playerImg.get_width():
            playerX = 1300 - border_thickness - playerImg.get_width()

        if playerY < border_thickness:
            playerY = border_thickness
        elif playerY > 700 - border_thickness - playerImg.get_height():
            playerY = 700 - border_thickness - playerImg.get_height()

        # Enemy movement and collision detection
        for i in range(num_of_enemies):
            enemyX, enemyY, enemyY_change = enemies[i]
            enemyY += enemyY_change

            if enemyY > 700:
                enemyY = random.randint(-100, -50)
                enemyX = random.randint(0, 1300)
                enemyY_change = random.uniform(0.2, 0.6)

            if is_collision(playerX, playerY, enemyX, enemyY):
                game_over = True
                break

            enemies[i] = [enemyX, enemyY, enemyY_change]
            enemy(enemyX, enemyY)

        player(playerX, playerY)

        pygame.display.update()

    elif game_won:
        show_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart
                    game_won = False
                    playerX = 300
                    playerY = 400
                    start_ticks = pygame.time.get_ticks()
                    enemies = [[random.randint(0, 1300), random.randint(-100, -50), random.uniform(0.2, 0.6)] for _ in
                               range(num_of_enemies)]

    else:
        show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart
                    game_over = False
                    playerX = 300
                    playerY = 400
                    start_ticks = pygame.time.get_ticks()
                    enemies = [[random]]
# Continue from where the code was cut off

                    enemies = [[random.randint(0, 1300), random.randint(-100, -50), random.uniform(0.2, 0.6)] for _ in range(num_of_enemies)]

    pygame.display.update()

pygame.quit()
