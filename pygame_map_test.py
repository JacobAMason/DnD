import sys, pygame
pygame.init()

size = width, height = 900, 900

screen = pygame.display.set_mode(size)
speed = [1*65, 0]
empty = pygame.image.load('dvd.pgm')
full = pygame.image.load('creeper.pgm')
full_space = full.get_rect().move((2*65, 2*65))
position = 0

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.time.delay(1000)

    for zone in [(0, 1, 0, 7), (5, 8, 0, 2)]:
        for x in range(zone[0], zone[1]):
            for y in range(zone[2], zone[3]):
                screen.blit(empty, (x*30, y*30))



    full_space = full_space.move(speed)

    if full_space.topleft == 3*65 or 2*65:
        speed[0] = -speed[0]
    screen.blit(full,full_space)

    pygame.display.flip()
