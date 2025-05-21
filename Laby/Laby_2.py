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


class Laby:
    px = 0
    py = 0

    def nouveau(self):
        grille.clear()
        for y in range(MAXY):
            grille.append([])
            for x in range(MAXX):
                grille[y].append(0)

        self.px = 1
        self.py = 1
        grille[self.py][self.px] = 2

    def creuse(self):
        random.shuffle(DIR)
        for d in DIR:
            vx = self.px+2*d[0]
            vy = self.py+2*d[1]
            if vx > 0 and vx < MAXX and vy > 0 and vy < MAXY and grille[vy][vx] == 0:
                grille[vy][vx] = 2
                grille[self.py+d[1]][self.px+d[0]] = 2
                self.px = vx
                self.py = vy
                return

    def dessine(self):
        for y in range(MAXY):
            for x in range(MAXX):
                pygame.draw.rect(
                    screen, COULEURS[grille[y][x]], (x*M, y*M, M, M))


laby = Laby()
laby.nouveau()
while not quit:
    clock.tick(10)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True
    laby.creuse()
    laby.dessine()
    pygame.display.flip()
