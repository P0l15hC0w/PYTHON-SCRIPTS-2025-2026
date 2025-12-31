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


# ---------- 3D MATH ----------
def rotate_y(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x * cos_a + z * sin_a,
        y,
        -x * sin_a + z * cos_a
    )


def rotate_x(point, angle):
    x, y, z = point
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        x,
        y * cos_a - z * sin_a,
        y * sin_a + z * cos_a
    )


def project(point, width, height, scale=200, distance=5):
    x, y, z = point
    z += distance
    if z == 0:
        z = 0.001
    factor = scale / z
    x = x * factor + width / 2
    y = -y * factor + height / 2
    return int(x), int(y)


# ---------- MAIN APP ----------
def main():
    obj_file = easygui.fileopenbox(
        title="Select an OBJ file",
        filetypes=["*.obj"]
    )

    if not obj_file:
        print("No file selected. Exiting.")
        return

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("OBJ Viewer (EasyGUI + Pygame)")
    clock = pygame.time.Clock()

    vertices, faces = load_obj(obj_file)

    angle_x = 0
    angle_y = 0

    running = True
    while running:
        clock.tick(60)
        screen.fill((20, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle_y += 0.01
        angle_x += 0.005

        transformed = []
        for v in vertices:
            v = rotate_y(v, angle_y)
            v = rotate_x(v, angle_x)
            transformed.append(v)

        projected = [
            project(v, 800, 600)
            for v in transformed
        ]

        # Draw wireframe
        for face in faces:
            points = [projected[i] for i in face]
            pygame.draw.polygon(screen, (200, 200, 200), points, 1)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
