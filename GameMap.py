
import pygame
from threading import Thread


class PlayerMap(Thread):
    def __init__(self, player_position):
        super().__init__()
        self._player = player_position
        self._key = 32
        self._visibility = 9
        self._size = self._visibility * self._key + 1
        self._area = self._size, self._size
        self._ipos = self._player[0]
        self._jpos = self._player[1]
        self._kpos = self._player[2]

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(self._area)
        self.base = pygame.image.load('15x15map.png')
        self.full = pygame.image.load('creeper.png')
        black = 0, 0, 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            screen.fill(black)
            screen.blit(self.base, (-(self._ipos-self._visibility//2)*self._key, -(self._jpos-self._visibility//2)*self._key))
            screen.blit(self.full, (self._visibility//2*self._key, self._visibility//2*self._key))
            pygame.display.update()

    def update(self, position):
        self._ipos = int(position[0])
        self._jpos = int(position[1])

if __name__ == '__main__':
    player_position = [1, 3, 0]
    myMap = PlayerMap(player_position)
    myMap.start()
    while True:
        try:
            exec(input())
        except KeyboardInterrupt:
            exit(0)
        except Exception as errorMSG:
            print(errorMSG)