import pygame
import random

pygame.init()
nColonnes=12
nRangees=20

screen=pygame.display.set_mode((20*nColonnes,20*nRangees))

Formes=[[[1,1],
         [1,1]],

        [[1,1,1,1]],
        
        [[1,1,1],
         [0,1,0]],

         [[1,1,1],
          [1,0,0]],
          
         [[1,1,1],
          [0,0,1]],

         [[1,1,0],
          [0,1,1]],
          
          [[0,1,1],
           [1,1,0]]
          
         ]

grille=[[0 for _ in range(nColonnes)] for _ in range(nRangees)]
couleur=[(0,0,0),(255,0,0),(0,255,0),(0,0,255),(0,127,127),(127,0,127),(127,127,0),(255,127,0)]

def checkLigne():
    for r in range(nRangees):
        complet=True
        for c in range(nColonnes):
            if grille[r][c]==0:
                complet=False
                break
        if complet:
            for r1 in range(r-1,-1,-1):
                grille[r1+1]=grille[r1]                
            grille[0]=[0 for _ in range(nColonnes)]

class Piece:
    def new():
        Piece.d=random.randrange(4)
        Piece.s=random.randrange(len(Formes))
        Piece.sx=random.randrange(nColonnes-Piece.tailleY())
        Piece.sy=0
        return Piece.collision()
    
    def tailleX():
        return len(Formes[Piece.s]) if Piece.d%2==0 else len(Formes[Piece.s][0])
            
    def tailleY():
        return len(Formes[Piece.s][0]) if Piece.d%2==0 else len(Formes[Piece.s])

    def getPixel(r,c):
        match Piece.d:
            case 0:
                return Formes[Piece.s][r][c]
            case 1:
                return Formes[Piece.s][Piece.tailleY()-c-1][r] 
            case 2:
                return Formes[Piece.s][Piece.tailleX()-r-1][Piece.tailleY()-c-1]
            case 3:
                return Formes[Piece.s][c][Piece.tailleX()-r-1] 
        
    def gauche():
        Piece.sx-=1
        if Piece.collision():
            Piece.sx+=1
        
    def droite():
        Piece.sx+=1
        if Piece.collision():
            Piece.sx-=1
    def tourne():
        d=Piece.d
        x=Piece.sx
        Piece.d=(Piece.d+1)%4
        if Piece.sx+Piece.tailleY()>=nColonnes:
            Piece.sx=nColonnes-Piece.tailleY()
        if Piece.collision():
            Piece.d=d
            Piece.sx=x

    def collision():
        for r in range(Piece.tailleX()):
            for c in range(Piece.tailleY()):
                if Piece.getPixel(r,c):
                    if Piece.sy+r>=nRangees or Piece.sx+c>=nColonnes or Piece.sx<0 or grille[Piece.sy+r][Piece.sx+c]:
                        return True
        return False
    
    def chute():
        Piece.sy+=1
        if Piece.collision():
            Piece.sy-=1
            for r in range(Piece.tailleX()):
                for c in range(Piece.tailleY()):
                    if Piece.getPixel(r,c):
                        grille[Piece.sy+r][Piece.sx+c]=Piece.s+1
            checkLigne()
            return Piece.new()
        return False
    
Piece.new()

clock=pygame.time.Clock()
exit=False
delay=12
while not exit:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            exit=True
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_LEFT:
                Piece.gauche()
            elif e.key==pygame.K_RIGHT:
                Piece.droite()
            elif e.key==pygame.K_UP:
                Piece.tourne()
            elif e.key==pygame.K_DOWN:
                while Piece.sy>0:
                    exit=Piece.chute()

    if delay==0:
        exit=Piece.chute()
        delay=12
    else:
        delay-=1
    screen.fill((127,127,127))
    for r in range(nRangees):
        for c in range(nColonnes):
            pygame.draw.rect(screen,couleur[grille[r][c]],pygame.Rect(c*20,r*20,19,19))
    for r in range(Piece.tailleX()):
        for c in range(Piece.tailleY()):
            if Piece.getPixel(r,c):
                pygame.draw.rect(screen,couleur[Piece.s+1],pygame.Rect((Piece.sx+c)*20,(Piece.sy+r)*20,19,19))
    pygame.display.flip()
