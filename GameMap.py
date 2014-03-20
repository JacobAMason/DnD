
import pygame, os
from threading import Thread


class PlayerMap(Thread):
    def __init__(self):
        super().__init__()
        self._player_position = player_position
        self._key = 64
        self._visibility = 9
        self._size = self._visibility * self._key
        self._area = self._size, self._size + self._key
        self._players = []
        self._mobs = []
        self._draw = True
        self._message = ""
        


    def run(self):
        pygame.init()

        folder = 'resources'
        screen = pygame.display.set_mode(self._area)
        pygame.display.set_caption('Game Map')
        self.base = pygame.image.load(os.path.join(folder,'15x15map.png'))
        self.player = pygame.image.load(os.path.join(folder,'playstation.png'))
        self.other = pygame.image.load(os.path.join(folder,'droid.png'))
        self.mob = pygame.image.load(os.path.join(folder,'creeperm2.png'))
        TheFont = pygame.font.SysFont(None, 64)
        self.movement_commands = {pygame.K_UP:'north',
                                  pygame.K_w:'north',
                                  pygame.K_DOWN:'south'
                                  pygame.K_s:'south'
                                  pygame.K_LEFT:'west',
                                  pygame.K_a:'west',
                                  pygame.K_RIGHT:'east',
                                  pygame.K_d:'east',
                                  }


        black = 0, 0, 0
        white = 255, 255, 255

        while True:

            if self._draw:   
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pass
                    if event.type == pygame.KEYDOWN:
                        if event.key in self.movement_commands:
                            self._message = ',  you moved ' + self.movement_commands[event.key]
                        else:
                            self._message = ""

                coords = '%s,%s%s' %(self._ipos, self._jpos, self._message)
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
        self._draw = False

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

    def map_update(self):
        self._draw = True

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