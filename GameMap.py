
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
        pygame.display.set_caption('Game Map')
        self.base = pygame.image.load('15x15map.png')
        self.player = pygame.image.load('playstation.png')
        self.other = pygame.image.load('droid.png')
        self.mob = pygame.image.load('creeperm2.png')
        TheFont = pygame.font.SysFont(None, 64)

        black = 0, 0, 0
        white = 255, 255, 255

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
            coords = '%s,%s' %(self._ipos,self._jpos)
            text = TheFont.render(coords,True,white,black)

            screen.fill(black)
            screen.blit(self.base, (-(self._ipos-self._visibility//2)*self._key, -(self._jpos-self._visibility//2) * self._key + self._key))
            
            for baddie in self._mobs:
                screen.blit(self.mob,(baddie))
            for person in self._players:
                screen.blit(self.other,(person))
            screen.blit(self.player,(self._visibility//2 * self._key, self._visibility//2 * self._key + self._key))
            pygame.draw.rect(screen,black,(0,0,self._size,self._key))
            screen.blit(text,(0,0))
            pygame.display.update()


    def character_init(self):
        self._players = []
        self._mobs = []

    def client_update(self, position):
        self._ipos = int(position[0])
        self._jpos = int(position[1])

    def players_update(self, position):
        self._player_i = self._visibility//2 + (int(position[0]) - self._ipos)
        self._player_j = self._visibility//2 + (int(position[1]) - self._jpos)
        self._players.append((self._player_i * self._key, self._player_j * self._key + self._key))

    def mob_update(self, position):
        self._mob_i = self._visibility//2 + (int(position[0]) - self._ipos)
        self._mob_j = self._visibility//2 + (int(position[1]) - self._jpos)
        self._mobs.append((self._mob_i * self._key, self._mob_j * self._key + self._key))

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