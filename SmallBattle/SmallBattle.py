import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480),  pygame.RESIZABLE)

GRIDSIZE=32

player_drawing1=[
    "XXX XXX ",
    " X   X  ",
    " XXXXX  ",    
    " XXXXXXX",    
    " XXXXXXX",    
    " XXXXX  ",    
    " X   X  ",    
    "XXX XXX ",

]

player_drawing2=[
    "   XX   ",
    "X  XX  X",
    "XXXXXXXX",    
    "X XXXX X",
    "  XXXX ",
    "X XXXX X",
    "XXXXXXXX",    
    "X      X",    
]

player_drawing3=[
    " XXX XXX",
    "  X   X ",
    "  XXXXX ",    
    "XXXXXXX ",    
    "XXXXXXX ",    
    "  XXXXX ",    
    "  X   X ",    
    " XXX XXX",

]

player_drawing4=[
    "X      X",
    "XXXXXXXX",    
    "X XXXX X",
    "  XXXX ",
    "X XXXX X",
    "XXXXXXXX",    
    "X  XX  X",    
    "   XX   ",
]

    

def PrepareImage(mat, color1, color2):
    image = pygame.Surface((GRIDSIZE, GRIDSIZE), flags=pygame.SRCALPHA)
    image.fill(color2)
    for y in range(min(8, len(mat))):
        for x in range(min(8, len(mat[y]))):
            if mat[y][x] != ' ':
                pygame.draw.rect(image, color1, (x*4, y*4, 4, 4))
    return image



class mySprite(pygame.sprite.Sprite):
    def __init__(self,images):
        self.images=images
        self.selectCostume(0)
        self.rect=pygame.Rect(0,0,GRIDSIZE,GRIDSIZE)
        super().__init__()

    def selectCostume(self,costume):
        self.costume=costume
        self.image=self.images[self.costume]




class GameScreen:

    def __init__(self, gameWidth, gameHeight):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.screen = pygame.Surface((self.gameWidth, self.gameHeight))

    def resize(self, screen_width, screen_height):
        margin = screen_width/32
        if (screen_width-margin*2) / self.gameWidth < (screen_height-margin*2)/self.gameHeight:
            self.scale = (screen_width-margin*2)/self.gameWidth
        else:
            self.scale = (screen_height-margin*2)/self.gameHeight

        self.topMargin = (screen_height-self.gameHeight*self.scale)/2
        self.leftMargin = (screen_width-self.gameWidth*self.scale)/2

    def display(self,screen):
        screen.fill((0, 0, 255))
        screen.blit(pygame.transform.scale_by(self.screen, self.scale),
                    (self.leftMargin, self.topMargin))
        pygame.display.flip()

class Game:

    def __init__(self):
        self.hiscore=0
        self.player=mySprite([
            PrepareImage(player_drawing1,(255,0,0),(0,0,0,0)),
            PrepareImage(player_drawing2,(255,0,0),(0,0,0,0)),
            PrepareImage(player_drawing3,(255,0,0),(0,0,0,0)),
            PrepareImage(player_drawing4,(255,0,0),(0,0,0,0)),
            ])
        self.allSprites=pygame.sprite.Group(self.player)
        self.newGame()

    def newGame(self):
        self.paused=True
        self.gameOver=False
        self.lives = 3
        self.score = 0
        self.level=1
        self.resetLevel()

        self.vx=0
        self.vy=0

    def resetLevel(self):
        map1=["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
              "X            X     X                  X                  X",
              "X                  X                                     X",
              "X            X     X                                     X",
              "X  XXXXXX XXXXXX   X                  X                  X",
              "X     X                               XXXXXXXXXXXXXXX  XXX",
              "X     X  P   X                        X      X           X",
              "X     X      X     XXXXXXXXXXXXXXXXXXXX      X           X",
              "X     X            X                         X           X",
              "X     XXXX         X                         X           X",
              "X                  X                  X      X           X",
              "XXXXXXXXXXXXXXXXXXXXXX  XXXXXX  XXXXXXXXX  XXXXXXX  XXXXXX",
              "X                  X      X           X       X          X",
              "X     XXXX         X      X                   X          X",
              "X     X            X      XXXXXXXXXXXXX       X          X",
              "X     X            X      X                   X          X",
              "X     X                   X           XXXXXXXXXXXXXXX  XXX",
              "X     X                   X           X                  X",
              "X     X            XXXXXXXX     XXXXXXX                  X",
              "X     X            X                                     X",
              "X     XXXX         X                                     X",
              "X                  X                  X                  X",
              "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                  ]

        self.map=[]
        for y,s in enumerate(map1):
            self.map.append([])
            for x,c in enumerate(s):
                if c=='X':
                    self.map[y].append('X')
                else:
                    self.map[y].append(' ')
                if c=='P':
                    self.mapOffsetX=0
                    self.mapOffsetY=0
                    self.player.rect.topleft=(GRIDSIZE*x,GRIDSIZE*y)



    def update(self,keys):
        if self.gameOver:
            if keys[pygame.K_y]:
                self.newGame()
            elif keys[pygame.K_n]:
                #quit
                return True
        else:
            self.player.rect.left+=self.vx*2
            self.player.rect.top+=self.vy*2
            if self.player.rect.top%GRIDSIZE==0 and self.player.rect.left%GRIDSIZE==0:
                if self.player.rect.left//GRIDSIZE>20:
                    self.player.rect.left=0
                    self.mapOffsetX+=19
                elif self.player.rect.left//GRIDSIZE<0:
                    self.player.rect.left=20*GRIDSIZE
                    self.mapOffsetX-=19
                if self.player.rect.top//GRIDSIZE>11:
                    self.player.rect.top=0
                    self.mapOffsetY+=11
                elif self.player.rect.top//GRIDSIZE<0:
                    self.player.rect.top=10*GRIDSIZE
                    self.mapOffsetY-=11

                if keys[pygame.K_LEFT] and self.player.rect.top :
                    self.player.selectCostume(2)
                    self.vx=-1
                    self.vy=0
                elif keys[pygame.K_RIGHT]:
                    self.player.selectCostume(0)
                    self.vx=1
                    self.vy=0
                elif keys[pygame.K_UP]:
                    self.player.selectCostume(1)
                    self.vx=0
                    self.vy=-1
                elif keys[pygame.K_DOWN]:
                    self.player.selectCostume(3)
                    self.vx=0
                    self.vy=1
                else:
                    self.vx=0
                    self.vy=0

                if self.map[self.player.rect.top//GRIDSIZE+self.vy+self.mapOffsetY][self.player.rect.right//GRIDSIZE+self.vx-1+self.mapOffsetX]=="X":
                    self.vx=0
                    self.vy=0

            # vx=0
            # vy=0
            # if keys[pygame.K_LEFT]:
            #     vx=-3
            # if keys[pygame.K_RIGHT]:
            #     vx=3
            # if keys[pygame.K_UP]:
            #     vy=-3
            # if keys[pygame.K_DOWN]:
            #     vy=3
            # self.player.rect.left+=vx
            # self.player.rect.top+=vy

            # if vx>0 and self.player.rect.right>=GRIDSIZE*20:
            #     self.player.rect.right-=GRIDSIZE*20
            # if vx<0 and self.player.rect.left<0:
            #     self.player.rect.left+=GRIDSIZE*20


            # if vx>0:
            #     self.player.selectCostume(0)
            #     if self.map[int(self.player.rect.top/GRIDSIZE+0.1)][int(self.player.rect.right/GRIDSIZE)]=="X" or \
            #     self.map[int(self.player.rect.bottom/GRIDSIZE-0.1)][int(self.player.rect.right/GRIDSIZE)]=="X":
            #         self.player.rect.left=(self.player.rect.left//GRIDSIZE)*GRIDSIZE
            # if vx<0:
            #     self.player.selectCostume(2)
            #     if self.map[int(self.player.rect.top/GRIDSIZE+0.1)][int(self.player.rect.left/GRIDSIZE)]=="X" or \
            #     self.map[int(self.player.rect.bottom/GRIDSIZE-0.1)][int(self.player.rect.left/GRIDSIZE)]=="X":
            #         self.player.rect.left=(self.player.rect.left//GRIDSIZE+1)*GRIDSIZE
            # if vy>0:
            #     self.player.selectCostume(3)
            #     if self.map[int(self.player.rect.bottom/GRIDSIZE)][int(self.player.rect.left/GRIDSIZE+0.1)]=="X" or \
            #     self.map[int(self.player.rect.bottom/GRIDSIZE)][int(self.player.rect.right/GRIDSIZE-0.1)]=="X":
            #         self.player.rect.top=(self.player.rect.top//GRIDSIZE)*GRIDSIZE

            # if vy<0:
            #     self.player.selectCostume(1)
            #     if self.map[int(self.player.rect.top/GRIDSIZE)][int(self.player.rect.left/GRIDSIZE+0.1)]=="X" or \
            #     self.map[int(self.player.rect.top/GRIDSIZE)][int(self.player.rect.right/GRIDSIZE-0.1)]=="X":
            #         self.player.rect.top=(self.player.rect.top//GRIDSIZE+1)*GRIDSIZE
        return False


    def display(self,screen):
        #display background
        screen.fill((0, 0, 0))
        for y in range(12):
            s=self.map[y+self.mapOffsetY]
            for x in range(20):
                c=s[x+self.mapOffsetX]    
                if c=='X':
                    pygame.draw.rect(screen,(100,100,80),pygame.Rect(x*GRIDSIZE,y*GRIDSIZE,GRIDSIZE,GRIDSIZE))

        #display sprites
        self.allSprites.draw(screen)
        #display score and lives

        #display messages
        pass

quit = False
clock = pygame.time.Clock()
game=Game()

gameScreen=GameScreen(20*GRIDSIZE,12*GRIDSIZE)
display_info = pygame.display.Info()
gameScreen.resize(display_info.current_w, display_info.current_h)



while quit==False:
    clock.tick(160)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit=True
        if e.type == pygame.VIDEORESIZE:
            gameScreen.resize(e.w, e.h)

    keys = pygame.key.get_pressed()
    quit= quit or game.update(keys)

    # display the game
    game.display(gameScreen.screen)
    gameScreen.display(screen)