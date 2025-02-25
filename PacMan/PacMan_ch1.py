import pygame

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()
terminé = False
while terminé == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminé = True
    screen.fill((0, 0, 64))
    pygame.display.flip()
pygame.quit()
