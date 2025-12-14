
import time
import os
import sys
import random

 # WARNING: the app is ran on windows and im kinda lazy to implement other os's :PP

try:
    import pygame
    os.system('cls')
except:
    print('YOU NEED TO INSTALL PYGAME BEFORE RUNNING\ntry using "pip install pygame" and replay the file.')
    for i in range(5):
        print('.')
        time.sleep(1)
    quit()

print('\n\nCLOSING THIS WINDOW MAY RESULT IN THE GAME EXITING.')

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((700, 900))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

fullscreen = False #default setting for fullscreen

rect_width = 100
rect_height = 10
rect = pygame.Rect(0, 0, rect_width, rect_height)  
rect.center = (screen.get_width() // 2, screen.get_height() // 2 - screen.get_height() // 2 * -0.9)

x = rect.centerx - rect_width // 2
rect.x = x

velocity = 0
acceleration = 0.1
friction = 0.9
max_speed = 5

# Ball properties
ball_radius = 15
ball_x = screen.get_width() // 2
ball_y = 50
ball_velocity_x = random.randint(-5, 5)
ball_velocity_y = 0
gravity = 0.05
bounce_factor = 1.002  # higher values might be funny lmao
ball_friction =0.999  # over 1 ts just tweaks away so leave this like that or decrease it
collisions_count = 0

def play_sound(file_path, volume=1.0, loop=0):
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume) # don't set it higher than 5 okay-
        sound.play(loops=loop)
    except Exception as e:
        print(f"Error playing sound '{file_path}': {e}")

def map_color_x(value, max_value=screen.get_width()): #i felt funny and tried that..
    center = max_value / 2

    value = max(0, min(value, max_value)) # that shiht js took way too long for my level to figure out-

    g = 255
    r = 0

    if value <= center:
        b = int((value / center) * 127)
    else:
        b = int(127 + ((value - center) / center) * 128)

    b = max(0, min(b, 255)) # just in case okay-

    return (r, g, b)


def map_color_y(value, max_value=screen.get_height()):

    value = max(0, min(value, max_value)) # i learned my lesson last time

    r = int((value / max_value) * 255)
    g = 255 - r
    b = 0

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))

    return (r, g, b)

def draw_text(text, x, y, font_size=30, color=(255, 255, 255), center=False):
    font = pygame.font.Font("assets/font.ttf", font_size)  # if u don't wanna use the font just set this to None
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    screen.blit(text_surface, text_rect)

def move():
    global x, velocity, ball_y, ball_velocity_y, ball_x, ball_velocity_x, collisions_count #i keep forgetting to set this to global istg
    keys = pygame.key.get_pressed() 

    if keys[pygame.K_LEFT]:
        velocity -= acceleration
    elif keys[pygame.K_RIGHT]:
        velocity += acceleration
    else:
        velocity *= friction

    velocity = max(-max_speed, min(velocity, max_speed))

    x += velocity

    # paddle collisions \|/
    if x < 0:
        x = 0
        velocity = -velocity
    elif x > screen.get_width() - rect_width:
        x = screen.get_width() - rect_width
        velocity = -velocity  

    rect.x = x  

    ball_velocity_y += gravity
    ball_velocity_x *= ball_friction 
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # the cornball screen collisions \|/
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor
    elif ball_x + ball_radius > screen.get_width():
        ball_x = screen.get_width() - ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor

    # phase trough the screen top and bottom (idk why i did that, it was supposed to be game over when u touch the bottom)
    if ball_y - ball_radius > screen.get_height():
        ball_y = 0 - ball_radius
    elif ball_y + ball_radius < 0:
        ball_y = screen.get_height() + ball_radius

    # cornball collisions \|/
    if (ball_x > rect.x and ball_x < rect.x + rect_width) and (ball_y + ball_radius >= rect.top) and (ball_y + ball_radius <= rect.top + ball_velocity_y):
        ball_y = rect.top - ball_radius
        ball_velocity_y = -ball_velocity_y * bounce_factor
        ball_velocity_x += velocity * 0.1
        collisions_count += 1
        play_sound("assets/bounce.mp3")

    elif (ball_y > rect.top and ball_y < rect.bottom) and (ball_x + ball_radius >= rect.left) and (ball_x + ball_radius <= rect.left + ball_velocity_x):
        ball_x = rect.left - ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor
        ball_velocity_x += velocity * 0.1
        collisions_count += 1
        play_sound("assets/bounce.mp3")

    elif (ball_y > rect.top and ball_y < rect.bottom) and (ball_x - ball_radius <= rect.right) and (ball_x - ball_radius >= rect.right + ball_velocity_x):
        ball_x = rect.right + ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor
        ball_velocity_x += velocity * 0.1
        collisions_count += 1
        play_sound("assets/bounce.mp3")

play_sound('assets/ambient.mp3', 0.5, -1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((700, 900))

    move()
    clock.tick(165)

    # now render that mess bro
    
    screen.fill((0, 0, 0)) 
    draw_text(f"score: {collisions_count}", 10, 10)
    draw_text(f"ball velocities:", 10, 40)
    draw_text(f"y:{abs(ball_velocity_y):.2f}", 210, 40)
    draw_text(f"x:{abs(ball_velocity_x):.2f}", 300, 40)
    draw_text(f"plate velocity: {abs(velocity):.2f}", 10, 70)
    draw_text(f"guide:", screen.get_width()-220, 10)
    draw_text(f"fullscreen - F11", screen.get_width()-220, 40)
    draw_text(f"move - left, right", screen.get_width()-220, 70)
    draw_text
    pygame.draw.rect(screen, map_color_x(x), rect, border_radius=3)
    pygame.draw.circle(screen, map_color_y(ball_y), (int(ball_x), int(ball_y)), ball_radius)  # cornball

    #update ts
    pygame.display.flip()
    
print('QUITTING . . .')
pygame.quit()
print('QUIT . . .')
sys.exit()