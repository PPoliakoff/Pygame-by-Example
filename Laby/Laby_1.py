import pygame
import random

LARGEUR = 700
HAUTEUR = 460
MAXX = 35
MAXY = 23
M = int(min(LARGEUR/MAXX, HAUTEUR/MAXY))
COULEURS = ((0, 0, 255), (255, 255, 255), (255, 0, 0))
DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]

pygame.init()
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
clock = pygame.time.Clock()
grille = []
quit = False


while not quit:
    clock.tick(10)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

    pygame.display.flip()
