import pygame
import random

LARGEUR=800
HAUTEUR =600
MAXX=35
MAXY=25
CARRE=int(min(LARGEUR/MAXX,HAUTEUR/MAXY))
MARGEX=(LARGEUR-CARRE*MAXX)/2
MARGEY=(HAUTEUR-CARRE*MAXY)/2
DIR=[(0,1),(1,0),(0,-1),(-1,0)]

pygame.init()
screen=pygame.display.set_mode((LARGEUR,HAUTEUR))
grille=[]
class Laby:
    def nouveau(self):
        self.px=1
        self.py=1
        grille.clear()
        for y in range(MAXY):
            grille.append([])
            for x in range(MAXX):
                grille[y].append(0)
        grille[self.py][self.px]=1

    def creuse(self):
        random.shuffle(DIR)
        for d in DIR:
            x1=self.px+d[0]
            x2=self.px+d[0]*2
            y1=self.py+d[1]
            y2=self.py+d[1]*2
            if x2>0 and y2>0 and x2<MAXX and y2<MAXY and grille[y2][x2]==0:
                grille[y1][x1]=1
                grille[y2][x2]=1
                self.px=x2
                self.py=y2
                return
        for d in DIR:
            x1=self.px+d[0]
            x2=self.px+d[0]*2
            y1=self.py+d[1]
            y2=self.py+d[1]*2
            if x1>0 and y1>0 and x1<MAXX and y1<MAXY and grille[y1][x1]==1:
                grille[y1][x1]=2
                grille[y2][x2]=2
                self.px=x2
                self.py=y2
                return
    def affiche(self):
        for y in range(MAXY):
            for x in range(MAXX):
                if grille[y][x]==0:
                    color=(0,0,255)
                else:
                    color=(255,255,255)
                pygame.draw.rect(screen,color,(MARGEX+x*CARRE,MARGEY+y*CARRE,CARRE,CARRE))
quit=False
clock=pygame.time.Clock()
laby=Laby()
laby.nouveau()
while not quit:
    clock.tick(50)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            quit=True
        if e.type==pygame.KEYDOWN:
            laby.nouveau()
    laby.creuse()
    laby.affiche()
    pygame.display.flip()