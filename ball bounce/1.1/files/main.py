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

# ======================
# GLOBAL STATE
# ======================
in_menu = True
fullscreen = False

screen = pygame.display.set_mode((700, 900))
pygame.display.set_caption("baller.")
clock = pygame.time.Clock()

# ======================
# PLATE
# ======================
rect_width = 100
rect_height = 10
rect = pygame.Rect(0, 0, rect_width, rect_height)
rect.center = (
    screen.get_width() // 2,
    screen.get_height() // 2 - screen.get_height() // 2 * -0.9
)

x = rect.centerx - rect_width // 2
rect.x = x

velocity = 0
acceleration = 0.1
friction = 0.9
max_speed = 5

# ======================
# BALL
# ======================
ball_radius = 30
ball_x = screen.get_width() // 2
ball_y = 50
ball_velocity_x = random.randint(-5, 5)
ball_velocity_y = 0
gravity = 0.05
bounce_factor = 1.002
ball_friction = 0.999

collisions_count = 0

# ======================
# SOUND
# ======================
def play_sound(file_path, volume=1.0, loop=0):
    try:
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        sound.play(loops=loop)
    except Exception as e:
        print(f"Error playing sound '{file_path}': {e}")

play_sound("assets/ambient.mp3", 0.5, -1)

def draw_vertical_gradient(surface, top_color, bottom_color):
    width, height = surface.get_size()
    for y in range(height):
        t = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

# ======================
# COLOR MAPS
# ======================
def lerp(a, b, t):
    """
    Linear interpolation from a -> b
    t is 0.0 -> 1.0
    """
    return a + (b - a) * t

def map_color(value, max_value, color_start, color_end):
    t = max(0, min(value / max_value, 1))  # clamp 0..1
    r = int(lerp(color_start[0], color_end[0], t))
    g = int(lerp(color_start[1], color_end[1], t))
    b = int(lerp(color_start[2], color_end[2], t))
    return (r, g, b)

# ======================
# TEXT
# ======================
def draw_text(text, x, y, font_size=30, color=(255,255,255), center=False):
    font = pygame.font.Font("assets/font.ttf", font_size)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

# ======================
# BUTTON
# ======================
def draw_button(text, y, padding_x=30, padding_y=15,
                color=(50,150,50), hover_color=(80,200,80),
                text_color=(255,255,255), font_size=30):

    global in_menu

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()

    width = text_rect.width + padding_x * 2
    height = text_rect.height + padding_y * 2

    x_btn = screen.get_width() // 2 - width // 2
    button_rect = pygame.Rect(x_btn, y, width, height)

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=20)
        if mouse_pressed:
            in_menu = False
    else:
        pygame.draw.rect(screen, color, button_rect, border_radius=20)

    draw_text(text, button_rect.centerx, button_rect.centery,
              font_size=font_size, color=text_color, center=True)

# ======================
# GAME LOGIC
# ======================
def move():
    global x, velocity
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y
    global collisions_count

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        velocity -= acceleration
    elif keys[pygame.K_RIGHT]:
        velocity += acceleration
    else:
        velocity *= friction

    velocity = max(-max_speed, min(max_speed, velocity))
    x += velocity

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

    if ball_x - ball_radius < 0:
        ball_x = ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor
    elif ball_x + ball_radius > screen.get_width():
        ball_x = screen.get_width() - ball_radius
        ball_velocity_x = -ball_velocity_x * bounce_factor

    if ball_y - ball_radius > screen.get_height():
        ball_y = -ball_radius
    elif ball_y + ball_radius < 0:
        ball_y = screen.get_height() + ball_radius
    if (
        ball_velocity_y > 0 and
        ball_y < rect.top and
        rect.left < ball_x < rect.right and
        ball_y + ball_radius >= rect.top
    ):
        ball_y = rect.top - ball_radius
        ball_velocity_y = -ball_velocity_y * bounce_factor
        ball_velocity_x += velocity * 0.1
        collisions_count += 1
        play_sound("assets/bounce.mp3")

# ======================
# RENDER
# ======================
def render_game():
    draw_vertical_gradient(screen, (248, 177, 149), (53, 92, 125))
    draw_text(f"fullscreen - F11", screen.get_width()-220, 10, color=((53, 92, 125)))
    pygame.draw.rect(screen, (248, 177, 149), rect, border_radius=3)
    pygame.draw.circle(
        screen,
        map_color(ball_y, screen.get_height(), (53, 92, 125), (248, 177, 149)),
        (int(ball_x), int(ball_y)),
        ball_radius
    )
    
    draw_text(f"{collisions_count}", ball_x-ball_radius/2, ball_y-ball_radius/2,
              color=(map_color(ball_y, screen.get_height(), (248, 177, 149), (53, 92, 125))))

def render_menu():
    draw_vertical_gradient(screen, (53, 92, 125), (248, 177, 149) )
    draw_button("PLAY", 400, 50, 10, (248, 177, 149), (53, 92, 125), (97, 42, 12))

# ======================
# MAIN LOOP
# ======================
running = True
while running:
    clock.tick(165)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((700,900))

    if in_menu:
        render_menu()
    else:
        move()
        render_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
