
import pygame
from threading import Thread
from Position import Position
from Entity import Entity

class PyMap(Thread):
    def __init__(self, my_list):
        super().__init__()
        self.my_list = my_list
    def run(self):
        pygame.init()

        size = 500, 500
        self.screen = pygame.display.set_mode(size)

        self.empty = pygame.image.load('dvd.pgm')
        self.full = pygame.image.load('creeper.pgm')
        self.ipos = 3
        self.jpos = 3
        key = 64

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.time.delay(5)
            for x in range(0, 7):
                for y in range(0, 7):
                    self.screen.blit(self.empty, (x*key, y*key))

            for guy in self.my_list:
                self.local = guy.get_position()
                self.location =(self.local[0]*key, self.local[1]*key)
                self.screen.blit(self.full, self.location)

            pygame.display.flip()

    def update(self, position):
        print('hey')

if __name__ == '__main__':
    my_list = [Entity('alex', Position([0,0,0])), Entity('caleb', Position([2,4,0]))]

    myMap = PyMap(my_list)
    myMap.start()
    while True:
        try:
            exec(input())
        except KeyboardInterrupt:
            exit(0)
        except Exception as errorMSG:
            print(errorMSG)