
import pygame
from threading import Thread
from Position import Position


class PyMap(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pygame.init()

        size = 500, 500
        self.screen = pygame.display.set_mode(size)

        self.empty = pygame.image.load('dvd.pgm')
        self.full = pygame.image.load('creeper.pgm')
        self.ipos = 3
        self.jpos = 3
        key = 65

        while True:
            self.i_j = (self.ipos*key, self.jpos*key)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            for x in range (0,7):
                for y in range (0, 7):
                    self.screen.blit(self.empty, (x*key, y*key))

            self.screen.blit(self.full, self.i_j)

            pygame.display.flip()

    def move(self):
        self.ipos-=1

myMap = PyMap()
myMap.start()
while True:
    try:
        exec(input())
    except KeyboardInterrupt:
        exit(0)
    except Exception as errorMSG:
        print(errorMSG)