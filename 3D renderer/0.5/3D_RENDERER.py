import pygame
import math
import sys
import easygui

# ================= VARIABLES ===================

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
    "Settings": pygame.Rect(140, MENU_HEIGHT, 180, 120),
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
    "Show FPS": pygame.Rect(140, MENU_HEIGHT, 180, 40),
    "Smooth Lighting": pygame.Rect(140, MENU_HEIGHT + 40, 180, 40),
}

# ================= OBJ LOADING ===================

def load_obj(filename):
    vertices = []
    faces = []
    face_normals = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))
            elif line.startswith("f "):
                idx = [int(p.split("/")[0]) - 1 for p in line.split()[1:]]
                for i in range(1, len(idx) - 1):
                    faces.append((idx[0], idx[i], idx[i + 1]))
    
    for a, b, c in faces:
        x1, y1, z1 = vertices[a]
        x2, y2, z2 = vertices[b]
        x3, y3, z3 = vertices[c]

        ux, uy, uz = x2 - x1, y2 - y1, z2 - z1
        vx, vy, vz = x3 - x1, y3 - y1, z3 - z1

        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx

        l = math.sqrt(nx * nx + ny * ny + nz * nz)
        if l != 0:
            nx /= l
            ny /= l
            nz /= l

        face_normals.append((nx, ny, nz))

    vertex_normals = [[0.0, 0.0, 0.0] for _ in vertices]

    for (a, b, c), (nx, ny, nz) in zip(faces, face_normals):
        for idx in (a, b, c):
            vertex_normals[idx][0] += nx
            vertex_normals[idx][1] += ny
            vertex_normals[idx][2] += nz

    for i, (x, y, z) in enumerate(vertex_normals):
        l = math.sqrt(x * x + y * y + z * z)
        if l != 0:
            vertex_normals[i] = (x / l, y / l, z / l)
        else:
            vertex_normals[i] = (0.0, 0.0, 0.0)

    return vertices, faces, face_normals, vertex_normals

# ================= UI ===================

def draw_top_menu(surface, mouse_pos, click_pos, font):
    pygame.draw.rect(surface, BAR_COLOR, (0, 0, WIDTH, MENU_HEIGHT))
    x = PADDING_X
    clicked_item = None

    for item in MENU_ITEMS:
        text = font.render(item, True, TEXT_COLOR)
        rect = text.get_rect(midleft=(x, MENU_HEIGHT // 2))
        button = pygame.Rect(x - 8, 0, rect.width + 16, MENU_HEIGHT)

        if button.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, button)

        if click_pos and button.collidepoint(click_pos):
            clicked_item = item

        surface.blit(text, rect)
        x += button.width + 8

    return clicked_item

def draw_menu(surface, items, font, mouse_pos):
    pygame.draw.rect(surface, BAR_COLOR, next(iter(items.values())))
    for item, rect in items.items():
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, HOVER_COLOR, rect)
        text = font.render(item, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=rect.center))

def handle_menu_click(items, mouse_pos):
    for item, rect in items.items():
        if rect.collidepoint(mouse_pos):
            return item
    return None

def draw_fps(surface, font, fps):
    surface.blit(font.render(f"FPS: {fps:.1f}", True, TEXT_COLOR), (10, HEIGHT - 30))

# ================= MAIN ===================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Renderer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    vertices = faces = face_normals = vertex_normals = None

    angle_x = angle_y = 0.0
    cam_dist = 6.0
    rotating = False
    last_mouse = (0, 0)

    draw_wireframe = False
    draw_faces = True
    show_fps = False
    smooth_lighting = False

    active_menu = None

    lx, ly, lz = 0.4, 0.7, -0.6
    ll = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx /= ll; ly /= ll; lz /= ll

    running = True
    while running:
        clock.tick(60)
        fps = clock.get_fps()
        screen.fill((20, 20, 20))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = event.pos
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

        # ================= RENDER =================

        if vertices and faces:
            cosx = math.cos(-angle_x)
            sinx = math.sin(-angle_x)
            cosy = math.cos(-angle_y)
            siny = math.sin(-angle_y)

            projected = []

            for x, y, z in vertices:
                xz = x * cosy + z * siny
                zz = -x * siny + z * cosy

                yz = y * cosx - zz * sinx
                zz = y * sinx + zz * cosx

                zc = zz + cam_dist
                if zc <= 0:
                    projected.append(None)
                else:
                    f = 300 / zc
                    projected.append((int(xz * f + WIDTH // 2),
                                      int(-yz * f + HEIGHT // 2),
                                      zc))

            triangles = []

            for i, (a, b, c) in enumerate(faces):
                p1 = projected[a]
                p2 = projected[b]
                p3 = projected[c]
                if not p1 or not p2 or not p3:
                    continue

                if smooth_lighting:
                    na = vertex_normals[a]
                    nb = vertex_normals[b]
                    nc = vertex_normals[c]

                    ia = na[0] * lx + na[1] * ly + na[2] * lz
                    ib = nb[0] * lx + nb[1] * ly + nb[2] * lz
                    ic = nc[0] * lx + nc[1] * ly + nc[2] * lz

                    wa = 1.0 / p1[2]
                    wb = 1.0 / p2[2]
                    wc = 1.0 / p3[2]

                    intensity = (ia * wa + ib * wb + ic * wc) / (wa + wb + wc)
                else:
                    nx, ny, nz = face_normals[i]
                    intensity = nx * lx + ny * ly + nz * lz

                if intensity < 0.15:
                    intensity = 0.15

                shade = int(255 * intensity)
                zavg = (p1[2] + p2[2] + p3[2]) / 3

                triangles.append((
                    zavg,
                    (shade, shade, shade),
                    ((p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1]))
                ))

            triangles.sort(key=lambda t: t[0], reverse=True)

            for _, color, pts in triangles:
                if draw_faces:
                    pygame.draw.polygon(screen, color, pts)
                if draw_wireframe:
                    pygame.draw.polygon(screen, (40, 40, 40), pts, 1)

        # ================= UI =================

        clicked = draw_top_menu(screen, mouse_pos, mouse_click, font)
        if clicked:
            active_menu = None if active_menu == clicked else clicked

        if active_menu == "File":
            draw_menu(screen, FILE_MENU_RECTS, font, mouse_pos)
            if mouse_click:
                action = handle_menu_click(FILE_MENU_RECTS, mouse_click)
                if action == "Open":
                    path = easygui.fileopenbox(
                        title="Choose an OBJ file to open.",
                        filetypes=["*.obj"],
                        default="models/*.obj"
                    )
                    if path:
                        vertices, faces, face_normals, vertex_normals = load_obj(path)
                    active_menu = None
                elif action == "Exit":
                    running = False

        elif active_menu == "View":
            draw_menu(screen, VIEW_MENU_RECTS, font, mouse_pos)
            if mouse_click:
                action = handle_menu_click(VIEW_MENU_RECTS, mouse_click)
                if action == "Wireframe":
                    draw_wireframe = True
                    draw_faces = False
                    active_menu = None
                elif action == "Solid":
                    draw_faces = True
                    draw_wireframe = False
                    active_menu = None

        elif active_menu == "Settings":
            draw_menu(screen, SETTINGS_MENU_RECTS, font, mouse_pos)
            if mouse_click:
                action = handle_menu_click(SETTINGS_MENU_RECTS, mouse_click)
                if action == "Show FPS":
                    show_fps = not show_fps
                    active_menu = None
                elif action == "Smooth Lighting":
                    smooth_lighting = not smooth_lighting
                    active_menu = None

        if show_fps:
            draw_fps(screen, font, fps)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
