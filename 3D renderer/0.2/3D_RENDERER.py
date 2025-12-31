import pygame
import math
import sys
import easygui


# ---------- OBJ LOADER ----------
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
                face = []
                for part in parts:
                    index = part.split("/")[0]
                    face.append(int(index) - 1)
                faces.append(face)

    return vertices, faces


# ---------- VECTOR MATH ----------
def subtract(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


# ---------- 3D TRANSFORMS ----------
def rotate_y(p, angle):
    x, y, z = p
    c = math.cos(angle)
    s = math.sin(angle)
    return (x * c + z * s, y, -x * s + z * c)


def rotate_x(p, angle):
    x, y, z = p
    c = math.cos(angle)
    s = math.sin(angle)
    return (x, y * c - z * s, y * s + z * c)


def project(p, w, h, scale, distance):
    x, y, z = p
    z += distance
    if z <= 0:
        z = 0.001
    f = scale / z
    return (
        int(x * f + w / 2),
        int(-y * f + h / 2)
    )


# ---------- FACE CULLING ----------
def is_face_visible(face, vertices):
    a = vertices[face[0]]
    b = vertices[face[1]]
    c = vertices[face[2]]

    ab = subtract(b, a)
    ac = subtract(c, a)

    normal = cross(ab, ac)

    # Camera looks down +Z
    return normal[2] < 0


# ---------- MAIN ----------
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
    pygame.display.set_caption("OBJ Viewer – RMB Rotate + Scroll Zoom")
    clock = pygame.time.Clock()

    vertices, faces = load_obj(obj_file)

    angle_x = 0.0
    angle_y = 0.0

    camera_distance = 5.0
    zoom_speed = 0.5
    min_distance = 1.5
    max_distance = 20.0

    rotating = False 
    last_mouse_pos = (0, 0)
    sensitivity = 0.005

    running = True
    while running:
        clock.tick(60)
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right mouse button
                    rotating = True
                    last_mouse_pos = event.pos

                elif event.button == 4:  # Scroll up
                    camera_distance -= zoom_speed

                elif event.button == 5:  # Scroll down
                    camera_distance += zoom_speed

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    rotating = False

            elif event.type == pygame.MOUSEMOTION and rotating:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]

                angle_y += dx * sensitivity
                angle_x += dy * sensitivity

                last_mouse_pos = event.pos

        # Clamp zoom distance
        camera_distance = max(
            min_distance,
            min(max_distance, camera_distance)
        )

        # Transform vertices into camera space
        transformed = []
        for v in vertices:
            v = rotate_y(v, -angle_y)
            v = rotate_x(v, -angle_x)
            transformed.append(v)

        projected = [
            project(v, 800, 600, scale=200, distance=camera_distance)
            for v in transformed
        ]

        # Draw wireframe with face culling
        for face in faces:
            if len(face) < 3:
                continue

            if not is_face_visible(face, transformed):
                continue

            points = [projected[i] for i in face]
            pygame.draw.polygon(screen, (200, 200, 200), points, 1)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
