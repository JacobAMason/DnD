
import pygame
from threading import Thread


class PlayerMap(Thread):
    def __init__(self, player_position):
        super().__init__()
        self._player_position = player_position
        self._key = 64
        self._visibility = 9
        self._size = self._visibility * self._key + 1
        self._area = self._size, self._size
        self._ipos = self._player_position[0]
        self._jpos = self._player_position[1]
        self._kpos = self._player_position[2]
        self._players = []
        self._mobs = []

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(self._area)
        self.base = pygame.image.load('15x15map.png')
        self.player = pygame.image.load('playstation.png')
        self.other = pygame.image.load('droid.png')
        self.mob = pygame.image.load('creeper.png')

        black = 0, 0, 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            screen.fill(black)
            screen.blit(self.base, (-(self._ipos-self._visibility//2)*self._key, -(self._jpos-self._visibility//2)*self._key))
            for person in self._players:
                screen.blit(self.other,(person))
            for baddie in self._mobs:
                screen.blit(self.mob,(baddie))
            screen.blit(self.player,(self._visibility//2 * self._key, self._visibility//2 * self._key))
            pygame.display.update()

    def update(self):
        self._ipos, self._jpos = self._new_ipos, self._new_jpos
        self._players = self._new_players
        self._mobs = self._new_mobs

    def character_init(self):
        self._players = []
        self._mobs = []
        self._new_players = []
        self._new_mobs = []

    def client_update(self, position):
        self._new_ipos = int(position[0])
        self._new_jpos = int(position[1])

    def players_update(self, position):
        self._player_i = self._visibility//2 + (int(position[0]) - self._ipos)
        self._player_j = self._visibility//2 + (int(position[1]) - self._jpos)
        self._new_players.append((self._player_i * self._key, self._player_j * self._key))

    def mob_update(self, position):
        self._mob_i = self._visibility//2 + (int(position[0]) - self._ipos)
        self._mob_j = self._visibility//2 + (int(position[1]) - self._jpos)
        self._new_mobs.append((self._mob_i * self._key, self._mob_j * self._key))

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