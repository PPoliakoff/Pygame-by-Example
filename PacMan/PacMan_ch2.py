import pygame
import random
import os

labyrinthe = [
    "MMMMMMMMMMMMMMMMM",
    "M***************M",
    "M@MFMMMM*MMMMFM@M",
    "M***************M",
    "MMM*MMMMMMMMM*MMM",
    "M***************M",
    "M*M*MMMM.MMMM*M*M",
    "M*M***.....***M*M",
    "M*MMM*MMPMM*MMM*M",
    "M*M***.....***M*M",
    "M*M*MMMM.MMMM*M*M",
    "M***************M",
    "MMMM*MMMMMMM*MMMM",
    "M***************M",
    "M@MMFMMM*MMMFMM@M",
    "M***************M",
    "MMMMMMMMMMMMMMMMM"]


def dessine_laby(surface):
    for y in range(nCases_Y):
        for x, symbole in enumerate(labyrinthe[y]):
            if symbole == 'M':
                pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(
                    marge_x+x*pixels_par_case, marge_y+y*pixels_par_case, pixels_par_case, pixels_par_case))
            elif symbole == '@':
                pygame.draw.circle(surface, (127, 32, 0), (marge_x+x*pixels_par_case+pixels_par_case/2, marge_y+y*pixels_par_case+pixels_par_case/2),
                                   pixels_par_case/3)
            elif symbole == '*':
                pygame.draw.circle(surface, (127, 127, 0), (marge_x+x*pixels_par_case+pixels_par_case/2, marge_y+y*pixels_par_case+pixels_par_case/2),
                                   pixels_par_case/6)


pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman")

nCases_X = len(labyrinthe[0])
nCases_Y = len(labyrinthe)
pixels_par_case = min(height//nCases_Y, width//nCases_X)
marge_x = (width-nCases_X*pixels_par_case)/2
marge_y = (height-nCases_Y*pixels_par_case)/2


clock = pygame.time.Clock()
terminé = False
while terminé == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminé = True
    screen.fill((0, 0, 64))
    dessine_laby(screen)
    pygame.display.flip()
pygame.quit()
