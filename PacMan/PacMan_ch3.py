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


class Sprite:
    def __init__(self, imageList, taille, positionX, positionY):
        self.images = []
        repertoire = os.path.dirname(os.path.abspath(__file__))
        for fichierimage in imageList:
            image = pygame.image.load(os.path.join(
                repertoire, fichierimage)).convert()
            image.set_colorkey((255, 255, 255))
            self.images.append(pygame.transform.scale(image, (taille, taille)))
        self.positionX = positionX
        self.positionY = positionY
        self.vitesseX = 0
        self.vitesseY = 0
        self.taille = taille

    def image(self, costume):
        return self.images[costume]

    def bouge(self):
        self.positionX += self.vitesseX
        self.positionY += self.vitesseY

    def rect(self):
        return pygame.Rect(self.positionX, self.positionY, self.taille, self.taille)


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


def dessine_sprites(surface):
    for fantome in fantomes:
        if pacman.super == 0:
            surface.blit(fantome.image(
                0), (marge_x+fantome.positionX, marge_y+fantome.positionY))
        else:
            surface.blit(fantome.image(
                1), (marge_x+fantome.positionX, marge_y+fantome.positionY))
    surface.blit(pacman.image(
        0), (marge_x+pacman.positionX, marge_y+pacman.positionY))


pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman")
font = pygame.font.Font(None, 100)

nCases_X = len(labyrinthe[0])
nCases_Y = len(labyrinthe)
pixels_par_case = min(height//nCases_Y, width//nCases_X)
marge_x = (width-nCases_X*pixels_par_case)/2
marge_y = (height-nCases_Y*pixels_par_case)/2

fantomes = []
for y in range(nCases_Y):
    for x, symbole in enumerate(labyrinthe[y]):
        if symbole == "P":
            pacman = Sprite(["pacmanimage.png"], pixels_par_case,
                            x*pixels_par_case, y*pixels_par_case)
        if symbole == "F":
            fantomes.append(Sprite(["fantomeimage1.png", "fantomeimage2.png"],
                                   pixels_par_case, x*pixels_par_case, y*pixels_par_case))
pacman.super = 0

clock = pygame.time.Clock()
etat = "joue"
terminé = False
while terminé == False:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminé = True
    screen.fill((0, 0, 64))
    dessine_laby(screen)
    dessine_sprites(screen)
    pygame.display.flip()
pygame.quit()
