import pygame
import math
import sys
import easygui

# ================ VARIABLES ===================

WIDTH, HEIGHT = 800, 600

BAR_COLOR = (30, 30, 30)
TEXT_COLOR = (230, 230, 230)
HOVER_COLOR = (70, 70, 70)

MENU_HEIGHT = 40
PADDING_X = 16
MENU_ITEMS = ["File", "View", "Settings"]

MENU_RECTS = {
    "File": pygame.Rect(0, MENU_HEIGHT, 140, 80),
    "View": pygame.Rect(60, MENU_HEIGHT, 140, 80),
    "Settings": pygame.Rect(140, MENU_HEIGHT, 160, 80),
}
FILE_MENU_RECTS = {
    "Open": pygame.Rect(0, MENU_HEIGHT, 140, 40),
    "Exit": pygame.Rect(0, MENU_HEIGHT + 40, 140, 40),
}

VIEW_MENU_RECTS = {
    "Wireframe": pygame.Rect(60, MENU_HEIGHT, 140, 40),
    "Solid": pygame.Rect(60, MENU_HEIGHT + 40, 140, 40),
}

SETTINGS_MENU_RECTS = {
    "Show FPS":  pygame.Rect(140, MENU_HEIGHT, 140, 40),
}

# ================== OBJ LOADING ===================

def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))

            elif line.startswith("f "):
                parts = line.split()[1:]
                idx = [int(p.split("/")[0]) - 1 for p in parts]
                for i in range(1, len(idx) - 1):
                    faces.append((idx[0], idx[i], idx[i + 1]))

    return vertices, faces


# ================== MATH =====================

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def normalize(v):
    l = math.sqrt(dot(v, v))
    return (0, 0, 0) if l == 0 else (v[0]/l, v[1]/l, v[2]/l)

def rotate_x(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x, y*c - z*s, y*s + z*c)

def rotate_y(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x*c + z*s, y, -x*s + z*c)

def project(p, w, h, scale, cam_dist):
    x, y, z = p
    z += cam_dist
    if z <= 0:
        return None
    f = scale / z
    return (int(x*f + w/2), int(-y*f + h/2))


# ================== USER INTERFACE ========================

def draw_top_menu(surface, mouse_pos, click_pos, font):
    pygame.draw.rect(surface, BAR_COLOR, (0, 0, WIDTH, MENU_HEIGHT))
    x = PADDING_X
    clicked_item = None

    for item in MENU_ITEMS:
        text = font.render(item, True, TEXT_COLOR)
        rect = text.get_rect(midleft=(x, MENU_HEIGHT//2))
        button = pygame.Rect(x-8, 0, rect.width+16, MENU_HEIGHT)

        if button.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, button)

        if click_pos and button.collidepoint(click_pos):
            clicked_item = item

        surface.blit(text, rect)
        x += button.width + 8

    return clicked_item


def draw_file_menu(surface, font, mouse_pos):
    pygame.draw.rect(surface, BAR_COLOR, (0, MENU_HEIGHT, 140, 80))
    for item, rect in FILE_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, rect)
        text = font.render(item, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=rect.center))

def draw_view_menu(surface, font, mouse_pos):
    pygame.draw.rect(surface, BAR_COLOR, (60, MENU_HEIGHT, 140, 80))
    for item, rect in VIEW_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, rect)
        text = font.render(item, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=rect.center))

def draw_settings_menu(surface, font, mouse_pos):
    pygame.draw.rect(surface, BAR_COLOR, (140, MENU_HEIGHT, 140, 40))
    for item, rect in SETTINGS_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, rect)
        text = font.render(item, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=rect.center))

def handle_file_menu_click(mouse_pos):
    for item, rect in FILE_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            return item
    return None

def handle_view_menu_click(mouse_pos):
    for item, rect in VIEW_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            return item
    return None

def handle_settings_menu_click(mouse_pos):
    for item, rect in SETTINGS_MENU_RECTS.items():
        if rect.collidepoint(mouse_pos):
            return item
    return None

def handle_file():
    obj_file = easygui.fileopenbox(
        title="Select OBJ file",
        filetypes=["*.obj"],
        default="*.obj"
    )
    if not obj_file:
        return None

    return load_obj(obj_file)

def draw_fps(surface, font, fps):
    text = font.render(f"FPS: {fps:.2f}", True, TEXT_COLOR)
    surface.blit(text, (10, HEIGHT - 30))

# ================== MAIN ======================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D RENDERER")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    draw_wireframe = False
    draw_faces = True

    vertices, faces = None, None
    angle_x = angle_y = 0.0
    cam_dist = 6.0
    rotating = False
    last_mouse = (0, 0)
    active_menu = None

    show_fps = False

    light_dir = normalize((0.4, 0.7, -0.6))

    running = True
    while running:
        clock.tick(60)
        fps = clock.get_fps()
        screen.fill((20, 20, 20))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click_pos = event.pos
                elif event.button == 3:
                    rotating = True
                    last_mouse = event.pos
                elif event.button == 4:
                    cam_dist = max(2.0, cam_dist - 0.5)
                elif event.button == 5:
                    cam_dist = min(20.0, cam_dist + 0.5)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                rotating = False

            elif event.type == pygame.MOUSEMOTION and rotating:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                angle_y += dx * 0.005
                angle_x += dy * 0.005
                last_mouse = event.pos

        # ======== DRAW OBJ ============
        if vertices and faces:
            triangles = []
            for a, b, c in faces:
                w1, w2, w3 = vertices[a], vertices[b], vertices[c]
                n = normalize(cross(sub(w2, w1), sub(w3, w1)))
                intensity = max(0.15, dot(n, light_dir))
                shade = int(255 * intensity)

                v1 = rotate_x(rotate_y(w1, -angle_y), -angle_x)
                v2 = rotate_x(rotate_y(w2, -angle_y), -angle_x)
                v3 = rotate_x(rotate_y(w3, -angle_y), -angle_x)

                if v1[2]+cam_dist <= 0: continue
                p1 = project(v1, WIDTH, HEIGHT, 300, cam_dist)
                p2 = project(v2, WIDTH, HEIGHT, 300, cam_dist)
                p3 = project(v3, WIDTH, HEIGHT, 300, cam_dist)
                if None in (p1, p2, p3): continue

                triangles.append(((v1[2]+v2[2]+v3[2])/3, (shade,)*3, (p1,p2,p3)))

            triangles.sort(reverse=True)
            for _, color, pts in triangles:
                if draw_faces:
                    pygame.draw.polygon(screen, color, pts)
                if draw_wireframe:
                    pygame.draw.polygon(screen, (40, 40, 40), pts, 1)

        # ======== DRAW UI ===========
        clicked = draw_top_menu(screen, mouse_pos, mouse_click_pos, font)
        if show_fps == True:
            draw_fps(screen, font, fps)

        if clicked:
            active_menu = None if active_menu == clicked else clicked
        # ===== the following ui 'framework' i made is so messed up i dont even wanna add more. . .
        if active_menu == "File":
            draw_file_menu(screen, font, mouse_pos)
            if mouse_click_pos:
                action = handle_file_menu_click(mouse_click_pos)
                if action == "Open":
                    result = handle_file()
                    if result:
                        vertices, faces = result
                    active_menu = None
                elif action == "Exit":
                    running = False
        elif active_menu == "View":
            draw_view_menu(screen, font, mouse_pos)

            if mouse_click_pos:
                action = handle_view_menu_click(mouse_click_pos)

                if action == "Wireframe":
                    draw_wireframe = True
                    draw_faces = False
                    active_menu = None

                elif action == "Solid":
                    draw_faces = True
                    draw_wireframe = False
                    active_menu = None

        elif active_menu == "Settings":
            draw_settings_menu(screen, font, mouse_pos)
            if mouse_click_pos:
                action = handle_settings_menu_click(mouse_click_pos)
                if action == "Show FPS":
                    show_fps = not show_fps
                    active_menu = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()