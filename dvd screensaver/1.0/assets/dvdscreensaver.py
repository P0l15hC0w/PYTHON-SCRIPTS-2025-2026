import pygame
from pygame.locals import *
import random
import time
import os
import configparser

class App:

    fullscreen = False

    config = configparser.ConfigParser()
    config.read("config.cfg")

    framerate = int(config["fps"]["maxfps"])

    def __init__(self):
        self._running = True
        self._display_surf = None

        self.rect_x = 120
        self.rect_y = 120
        self.rect_width = 300
        self.rect_height = 156

        self.speed = 3
        self.dx = self.speed
        self.dy = self.speed

        self.color = self.random_color()

        self.clock = pygame.time.Clock()

        

    def random_color(self):
        return (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def on_init(self):
        pygame.init()

        os.system('cls' if os.name == 'nt' else 'clear')
        print('PRESS F11 TO FULLSCREEN')
        pygame.display.set_caption("DVD SCREENSAVER")

        self._display_surf = pygame.display.set_mode((720, 480), pygame.RESIZABLE)

        self.pyicon = pygame.image.load("pyicon.png").convert_alpha()
        pygame.display.set_icon(self.pyicon)

        try:
            self.image = pygame.image.load("dvd_logo.png").convert_alpha()
        except:
            print('error during image loading . . . ')
            for ex in range(5):
                time.sleep(1)
                print(f'exiting in {ex+1}. . . ')
            exit()

        self.image = pygame.transform.scale(
            self.image, (self.rect_width, self.rect_height)
        )

        return True

        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.size
            self._display_surf = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE
            )

    def on_loop(self):

        self.fps = self.framerate
        self.width, self.height = self._display_surf.get_size()

        self.rect_x += self.dx/(self.fps/60)
        self.rect_y += self.dy/(self.fps/60)

        bounced = False

        if self.rect_x <= 0 or self.rect_x + self.rect_width >= self.width:
            self.dx = -self.dx
            bounced = True

        if self.rect_y <= 0 or self.rect_y + self.rect_height >= self.height:
            self.dy = -self.dy
            bounced = True

        if bounced:
            self.color = self.random_color()

        self.rect_x = max(0, min(self.rect_x, self.width - self.rect_width))
        self.rect_y = max(0, min(self.rect_y, self.height - self.rect_height))

    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        tinted = self.image.copy()
        tinted.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)

        self._display_surf.blit(tinted, (self.rect_x, self.rect_y))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
        os.system('cls' if os.name == 'nt' else 'clear')

    def on_execute(self):

        
        if not self.on_init():
            self._running = False

        while self._running:
            
            self.clock.tick(self.framerate)

            for event in pygame.event.get():
                self.on_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self._display_surf = pygame.display.set_mode(
                                (0, 0), pygame.FULLSCREEN
                            )
                        else:
                            self._display_surf = pygame.display.set_mode(
                                (720, 480), pygame.RESIZABLE
                            )

            self.on_loop()
            self.on_render()

        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()