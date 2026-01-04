import pygame
import random

pygame.init()
matrixCols=12
matrixRows=20

screen=pygame.display.set_mode((20*matrixCols,20*matrixRows))
Shapes=[[[1,1],
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
matrix=[[0 for _ in range(matrixCols)] for _ in range(matrixRows)]
color=[(0,0,0),(255,0,0),(0,255,0),(0,0,255),(0,127,127),(127,0,127),(127,127,0),(127,127,127)]

def checkMatrix():
    for r in range(matrixRows):
        fill=True
        for c in range(matrixCols):
            if matrix[r][c]==0:
                fill=False
                break
        if fill:
            for r1 in range(r-1,-1,-1):
                matrix[r1+1]=matrix[r1]                
        matrix[0]=[0 for _ in range(matrixCols)]
class Shape:
    s=0
    sx=0
    sy=0
    d=0
    def new():
        Shape.d=random.randrange(4)
        Shape.s=random.randrange(len(Shapes))
        Shape.sx=random.randrange(matrixCols-Shape.nCols())
        Shape.sy=0
    
    def nRows():
        return len(Shapes[Shape.s]) if Shape.d%2==0 else len(Shapes[Shape.s][0])
            
    def nCols():
        return len(Shapes[Shape.s][0]) if Shape.d%2==0 else len(Shapes[Shape.s])

    def getPixel(r,c):
        match Shape.d:
            case 0:
                return Shapes[Shape.s][r][c]
            case 1:
                return Shapes[Shape.s][Shape.nCols()-c-1][r] 
            case 2:
                return Shapes[Shape.s][Shape.nRows()-r-1][Shape.nCols()-c-1]
            case 3:
                return Shapes[Shape.s][c][Shape.nRows()-r-1] 
        

    def gauche():
        Shape.sx-=1
        if Shape.collision():
            Shape.sx+=1
        
    def droite():
        Shape.sx+=1
        if Shape.collision():
            Shape.sx-=1
    def tourne():
        Shape.d=(Shape.d+1)%4
        if Shape.collision():
            Shape.d=(Shape.d+3)%4

    def collision():
        for r in range(Shape.nRows()):
            for c in range(Shape.nCols()):
                if Shape.getPixel(r,c):
                    if Shape.sy+r>=matrixRows or Shape.sx+c>=matrixCols or Shape.sx<0 or matrix[Shape.sy+r][Shape.sx+c]:
                        return True
        return False
    def drop():
        gameover=False
        Shape.sy+=1
        if Shape.sy+Shape.nRows()>matrixRows or Shape.collision():
            Shape.sy-=1
            for r in range(Shape.nRows()):
                for c in range(Shape.nCols()):
                    if Shape.getPixel(r,c):
                        matrix[Shape.sy+r][Shape.sx+c]=Shape.s+1
            checkMatrix()
            Shape.new()
            gameover= Shape.collision()
        return gameover
    def draw():
        for r in range(Shape.nRows()):
            for c in range(Shape.nCols()):
                if Shape.getPixel(r,c):
                    pygame.draw.rect(screen,color[Shape.s+1],pygame.Rect((Shape.sx+c)*20,(Shape.sy+r)*20,19,19))


def drawMatrix():
    for r in range(matrixRows):
        for c in range(matrixCols):
            pygame.draw.rect(screen,color[matrix[r][c]],pygame.Rect(c*20,r*20,19,19))
    
Shape.new()

clock=pygame.time.Clock()
exit=False
delay=6
while not exit:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            exit=True
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_LEFT:
                Shape.gauche()
            elif e.key==pygame.K_RIGHT:
                Shape.droite()
            elif e.key==pygame.K_UP:
                Shape.tourne()
    if delay==0:
        exit=Shape.drop()
        delay=6
    else:
        delay-=1
    drawMatrix()
    Shape.draw()
    pygame.display.flip()
    