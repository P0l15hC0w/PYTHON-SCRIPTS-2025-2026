import pygame
import math
import sys
import easygui

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


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )


def normalize(v):
    l = math.sqrt(dot(v, v))
    if l == 0:
        return (0, 0, 0)
    return (v[0]/l, v[1]/l, v[2]/l)


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


def main():
    obj_file = easygui.fileopenbox(
        title="Select OBJ file",
        filetypes=["*.obj"],
        default="*.obj"
    )
    if not obj_file:
        return

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("RENDER")
    clock = pygame.time.Clock()

    vertices, faces = load_obj(obj_file)

    angle_x = 0.0
    angle_y = 0.0
    cam_dist = 6.0

    rotating = False
    last_mouse = (0, 0)

    light_dir = normalize((0.4, 0.7, -0.6))

    running = True
    while running:
        clock.tick(60)
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    rotating = True
                    last_mouse = event.pos
                elif event.button == 4:
                    cam_dist = max(2.0, cam_dist - 0.5)
                elif event.button == 5:
                    cam_dist = min(20.0, cam_dist + 0.5)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    rotating = False

            elif event.type == pygame.MOUSEMOTION and rotating:
                dx = event.pos[0] - last_mouse[0]
                dy = event.pos[1] - last_mouse[1]
                angle_y += dx * 0.005
                angle_x += dy * 0.005
                last_mouse = event.pos

        triangles = []

        for a, b, c in faces:
            w1 = vertices[a]
            w2 = vertices[b]
            w3 = vertices[c]


            n_world = normalize(cross(sub(w2, w1), sub(w3, w1)))


            intensity = max(0.15, dot(n_world, light_dir))
            shade = int(255 * intensity)
            color = (shade, shade, shade)


            v1 = rotate_y(w1, -angle_y)
            v1 = rotate_x(v1, -angle_x)

            v2 = rotate_y(w2, -angle_y)
            v2 = rotate_x(v2, -angle_x)

            v3 = rotate_y(w3, -angle_y)
            v3 = rotate_x(v3, -angle_x)
        
            if (
                v1[2] + cam_dist <= 0 and
                v2[2] + cam_dist <= 0 and
                v3[2] + cam_dist <= 0
            ):
                continue

            n_view = cross(sub(v2, v1), sub(v3, v1))
            if n_view[2] >= 0:
                continue

            p1 = project(v1, 800, 600, 300, cam_dist)
            p2 = project(v2, 800, 600, 300, cam_dist)
            p3 = project(v3, 800, 600, 300, cam_dist)
            if None in (p1, p2, p3):
                continue

            avg_z = (v1[2] + v2[2] + v3[2]) / 3
            triangles.append((avg_z, color, (p1, p2, p3)))

        triangles.sort(key=lambda t: t[0], reverse=True)

        for _, color, pts in triangles:
            pygame.draw.polygon(screen, color, pts) 
            # pygame.draw.polygon(screen, (40, 40, 40), pts, 1) #draw wireframe

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
