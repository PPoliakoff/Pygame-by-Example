import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invaders")

clock = pygame.time.Clock()

exit = False
while not exit:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit=True

    screen.fill((0, 0, 0))
    pygame.display.flip()

