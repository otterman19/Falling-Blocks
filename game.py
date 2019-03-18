import pygame
import sys
import random

pygame.init()


# Display
screen_height = 800
screen_width = 600
background_color = (169, 169, 169)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
  
# Player
player_color = (81, 156, 213)
player_size = 50
player_pos = [(screen_height / 2), screen_width - 2 * player_size]

# Obstacles
enemy_color = red
enemy_size = 50
enemy_speed = 5
enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
enemy_list = [enemy_pos]


screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Avoid the blocks!")

game_over = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont("consolas", 35)


def set_level(score, enemy_speed):
    if score < 20:
        emeny_speed = 5
    elif score < 40:
        enemy_speed = 8
    elif score < 60:
        enemy_speed = 12
    else:
        enemy_speed = 15
    return enemy_speed

def detect_collision(player_pos, enemy_pos):
    player_x = player_pos[0]
    player_y = player_pos[1]
    enemy_x = enemy_pos[0]
    enemy_y = enemy_pos[1]

    if (enemy_x >= player_x and enemy_x < (player_x + player_size)) or (player_x >= enemy_x and player_x < (enemy_x + enemy_size)):
        if (enemy_y >= player_y and enemy_y < (player_y + player_size)) or (player_y>= enemy_y and player_y < (enemy_y + enemy_size)):
            return True
    else:
        return False


def spawn_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
    
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, enemy_color, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_pos(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(i)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Quits the game
            sys.exit()
               
        if event.type == pygame.KEYDOWN:

            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_RIGHT:
                x += player_size            
            elif event.key == pygame.K_LEFT:
                x -= player_size
            
            player_pos = [x, y]

    screen.fill(background_color)


    spawn_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    enemy_speed = set_level(score, enemy_speed)


    text = "Score:" + str(score)
    text_surface = myfont.render(text, False, blue)
    screen.blit(text_surface, (screen_width - 5, 550))
    
    if collision_check(enemy_list, player_pos):
       game_over = True
    
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size), 0) # Draws the player   
    
    clock.tick(30)

    pygame.display.update()

 
