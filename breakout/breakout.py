import pygame
import math
import random

from enum import Enum
'''
V 1/ allow resize
V 2/ pause game on lost focus
V 3/ 4 lives + Display number of remaining lives
V 4/ ball paddle collision detect
V 5/ detect game over
V 6/ draw bricks
V 7/ display score
  8/ memorize High score
V 9/ detect brick collision
 10/ Special effects: multi ball, small paddle, large paddle, slow, fast, invert game,paddle gun
 11/ explosion en chaine
V12/ briques avec plusieurs vies
 13/ brique qui redonne des vies
 14/ le son
 15/ score :bonus de temps
V16/ levels definition
V17/ handle small side collisions

'''

LEVELS = [
    [
        [1, 1, 1, 1, 0, 1, 1, 1, ]
    ],
    [
        [1, 1, 1, 1, 0, 0, 1, 1, 1, ]
    ],
    [
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 2, 1, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 0, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 0, 3, 3, 3, 3],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 0, 3, 3, 3, 3],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
        [4, 0, 4, 4, 4, 4, 4, 4, 0, 4],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]


class GAME_DISPLAY:
    def __init__(self, gameWidth, gameHeight):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.font = pygame.font.Font(None, 100)
        self.fontGui = pygame.font.Font(None, 32)
        self.gameSurface = pygame.Surface((self.gameWidth, self.gameHeight))
        self.guiHeight = self.gameHeight/20
        self.guiSurface = pygame.Surface((self.gameWidth, self.guiHeight))

    def Resize(self, screen_width, screen_height):
        usedHeight = self.gameHeight+self.guiHeight
        margin = screen_width/40
        if (screen_width-margin*2) / self.gameWidth < (screen_height-margin*2)/usedHeight:
            self.scale = (screen_width-margin*2)/self.gameWidth
        else:
            self.scale = (screen_height-margin*2)/usedHeight

        self.topGuiMargin = (screen_height-usedHeight*self.scale)/2
        self.topGameMargin = self.topGuiMargin + \
            self.guiHeight*self.scale
        self.leftMargin = (screen_width-self.gameWidth*self.scale)/2

    def Clear(self):
        self.gameSurface.fill((255, 127, 255))
        self.guiSurface.fill((0, 0, 0))

    def DisplayMessage(self, line, color, text):
        text = self.font.render(text, True, color)
        textpos = text.get_rect(
            centerx=self.gameWidth / 2, centery=self.gameHeight/2+80*(line-1))
        self.gameSurface.blit(text, (textpos.left, textpos.bottom))

    def DiplayRefresh(self):
        screen.fill((0, 0, 255))
        screen.blit(pygame.transform.scale_by(self.guiSurface, self.scale),
                    (self.leftMargin, self.topGuiMargin))
        screen.blit(pygame.transform.scale_by(self.gameSurface, self.scale),
                    (self.leftMargin, self.topGameMargin))
        pygame.display.flip()

    def DisplayInfo(self, lives, level, score, hiscore):
        text = self.fontGui.render(
            f"Lives: {lives}        Level:{level}   ", False, (255, 255, 0))
        textRect = text.get_rect()
        textRect.centery = self.guiHeight/2
        textRect.left = 3
        self.guiSurface.blit(text, textRect)
        text = self.fontGui.render(
            f"Score:{score:04}          Hi-Score:{hiscore:04}", False, (255, 255, 0))
        textRect = text.get_rect()
        textRect.right = self.gameWidth-3
        textRect.centery = self.guiHeight/2
        self.guiSurface.blit(text, textRect)


class LAST_HIT(Enum):
    WALL = 1
    PADDLE = 2
    BRICK = 3
    TOP = 4


class BALL:
    def __init__(self, gameWidth, gameHeight):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.ball_radius = self.gameHeight/40
        self.lastHit = LAST_HIT.WALL

    def Reset(self, x, y):
        self.ball_x = x
        self.ball_y = y-self.ball_radius
        self.absSpeed = 10.8
        angle = random.randrange(30, 151)/180*math.pi
        self.speed_x = math.cos(angle)*self.absSpeed
        self.speed_y = -math.sin(angle)*self.absSpeed

    def Move(self):
        self.ball_x += self.speed_x
        self.ball_y += self.speed_y
        if self.ball_x-self.ball_radius <= 0:
            self.ball_x = self.ball_radius
            self.speed_x = -self.speed_x
            self.lastHit = LAST_HIT.WALL

        if self.ball_x+self.ball_radius >= self.gameWidth:
            self.ball_x = self.gameWidth-self.ball_radius
            self.speed_x = -self.speed_x
            self.lastHit = LAST_HIT.WALL

        if self.ball_y-self.ball_radius <= 0:
            self.ball_y = self.ball_radius
            self.speed_y = -self.speed_y
            self.lastHit = LAST_HIT.TOP

        # if self.ball_y+self.ball_radius >= self.gameHeight:
        #     self.ball_y = self.gameHeight-self.ball_radius
        #     self.speed_y = -self.speed_y

    def Draw(self, gameDisplay):
        pygame.draw.circle(gameDisplay, (255, 255, 255),
                           (self.ball_x, self.ball_y), self.ball_radius)

    def getBallBottom(self):
        return self.ball_y+self.ball_radius

    def getBallTop(self):
        return self.ball_y-self.ball_radius

    def getBallLeft(self):
        return self.ball_x-self.ball_radius

    def getBallRight(self):
        return self.ball_x+self.ball_radius

    def getballCenterX(self):
        return self.ball_x

    def getballCenterY(self):
        return self.ball_y

    def Rect(self):
        return pygame.Rect(self.ball_x-self.ball_radius, self.ball_y-self.ball_radius, self.ball_radius*2, self.ball_radius*2)


class BRICK:
    colors = [[50, 50, 50], [127, 0, 0], [
        192, 64, 0], [192, 192, 0], [0, 127, 0]]
    height = 30

    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        self.life = life
        self.width = 100
        self.surface = pygame.Surface((self.width, self.height))
        self.drawSurface(self.life)

    def drawSurface(self, life):
        margin = 4
        self.color = pygame.Color(BRICK.colors[life])
        self.surface.fill(self.color)
        pygame.draw.rect(self.surface, self.color+pygame.Color(50, 50, 50), (margin, margin,
                         self.width-2*margin, self.height-2*margin))

    def Draw(self, gameDisplay):
        gameDisplay.blit(self.surface, (self.x, self.y))

    def Hit(self):
        if self.life == 0:  # indestructible brick
            return False
        self.life -= 1
        if self.life == 0:
            return True  # brick destroyed
        else:
            self.drawSurface(self.life)
        return False

    def Rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class PADDLE:
    def __init__(self, gameWidth, gameHeight):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.gameWidth = gameWidth
        self.width = gameWidth/5
        self.height = gameHeight/10
        self.x = (self.gameWidth-self.width)/2
        self.speed = self.gameWidth/80
        self.paddleDirection = 0

    def Draw(self, gameDisplay):
        if self.paddleDirection < 0:
            pygame.draw.polygon(gameDisplay, (0, 0, 0),
                                ((self.x, self.gameHeight),
                                 (self.x+self.width, self.gameHeight),
                                 (self.x+self.width, self.gameHeight-self.height)
                                 ))
        elif self.paddleDirection > 0:
            pygame.draw.polygon(gameDisplay, (0, 0, 0),
                                ((self.x, self.gameHeight-self.height),
                                 (self.x, self.gameHeight),
                                 (self.x+self.width, self.gameHeight)
                                 ))
        else:
            pygame.draw.rect(gameDisplay,  (0, 0, 0), (self.x,
                                                       self.gameHeight-self.height/2, self.width, self.height/2))

    def moveLeft(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def moveRight(self):
        self.x += self.speed
        if self.x+self.width > self.gameWidth:
            self.x = self.gameWidth - self.width

    def getLeft(self):
        return self.x

    def getRight(self):
        return self.x+self.width

    def getTop(self):
        return self.gameHeight-self.height/2


class GAME:
    def __init__(self, width, height):
        self.hiScore = 0
        self.width = width
        self.height = height
        self.old_x = -1
        self.old_y = -1
        self.beep = pygame.mixer.Sound("ping.wav")

    def NewGame(self):
        self.paused = True
        self.gameOver = False
        self.ball = BALL(self.width, self.height)
        self.paddle = PADDLE(self.width, self.height)
        self.ball.Reset(
            (self.paddle.getLeft()+self.paddle.getRight())/2, self.paddle.getTop())

        self.bricks = []
        self.level = 1
        self.life = 5
        self.score = 0
        self.newWall(self.level)

    def newWall(self, level):
        levelindex = min(level, len(LEVELS))-1

        self.bricks.clear()  # remove old indestructible bricks
        self.indestructible = 0
        for line in range(len(LEVELS[levelindex])):
            offsetx = (1000-100*len(LEVELS[levelindex][line]))/2
            for i in range(len(LEVELS[levelindex][line])):
                brickType = LEVELS[levelindex][line][i]
                if brickType == 0:
                    self.indestructible += 1
                self.bricks.append(
                    BRICK(offsetx+i*100, 100+line*BRICK.height, brickType))

    def update(self):
        if not self.gameOver:
            if not self.paused:
                self.ball.Move()

                if self.ball.getBallBottom() > 600:  # TODO : replace by game height
                    self.life -= 1
                    if self.life == 0:
                        self.gameOver = True
                        if self.score > self.hiScore:
                            self.hiScore = self.score
                    else:
                        self.ball.Reset(
                            (self.paddle.getLeft()+self.paddle.getRight())/2, self.paddle.getTop())
                        self.paused = True
                if (self.ball.getBallBottom() >= self.paddle.getTop()) and (self.ball.getBallRight() > self.paddle.getLeft()) and (self.ball.getBallLeft() < self.paddle.getRight() and self.ball.lastHit != LAST_HIT.PADDLE):
                    old_angle = math.pi/2 - \
                        math.atan(self.ball.speed_x/self.ball.speed_y)
                    angle = (180+30*self.paddle.paddleDirection) / \
                        180*math.pi-old_angle

                    self.ball.speed_y = -self.ball.absSpeed*math.sin(angle)
                    if self.ball.speed_y > -1.5:
                        self.ball.speed_y = -1.5
                    self.ball.speed_x = -self.ball.absSpeed*math.cos(angle)
                    self.ball.lastHit = LAST_HIT.PADDLE
                    self.beep.play()
                if (self.ball.lastHit == LAST_HIT.PADDLE or self.ball.lastHit == LAST_HIT.TOP) and len(self.bricks) == self.indestructible:
                    self.level += 1
                    self.newWall(self.level)

                # brick collision
                ballrect = self.ball.Rect()
                for brick in self.bricks:
                    if pygame.Rect.colliderect(brick.Rect(), ballrect):
                        self.beep.play()
                        if not (self.ball.lastHit == LAST_HIT.BRICK and self.old_x == brick.x and self.old_y == brick.y):
                            if brick.Hit():
                                self.bricks.remove(brick)
                                self.score += 1

                            if (self.ball.speed_y < 0 and self.ball.getballCenterY()-self.ball.speed_y > brick.Rect().bottom) or  \
                                    (self.ball.speed_y > 0 and self.ball.getballCenterY()-self.ball.speed_y < brick.Rect().top):
                                self.ball.speed_y = -(self.ball.speed_y)
                            else:
                                self.ball.speed_x = -(self.ball.speed_x)
                            # exit the brick :we don't want multiple collisions inside the same brick
                            # while pygame.Rect.colliderect(brick.Rect(), self.ball.Rect()):
                            #     self.ball.Move()

                            self.old_x = brick.x
                            self.old_y = brick.y
                            self.ball.lastHit = LAST_HIT.BRICK
                            break

    def display(self, gameDisplay):
        gameDisplay.Clear()
        if self.gameOver:
            gameDisplay.DisplayMessage(1,
                                       (127, 0, 0), "GAME OVER")
            gameDisplay.DisplayMessage(2,
                                       (127, 0, 0), "Play again y/n")
        elif self.paused:
            gameDisplay.DisplayMessage(1, (0, 0, 0), "GAME PAUSED")
            gameDisplay.DisplayMessage(2,
                                       (0, 0, 0), "Press Space to play")
        self.ball.Draw(gameDisplay.gameSurface)
        self.paddle.Draw(gameDisplay.gameSurface)
        for brick in self.bricks:
            brick.Draw(gameDisplay.gameSurface)
        gameDisplay.DisplayInfo(self.life, self.level,
                                self.score, self.hiScore)
        gameDisplay.DiplayRefresh()


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400),  pygame.RESIZABLE)
clock = pygame.time.Clock()
inGame = True

gameDisplay = GAME_DISPLAY(1000, 600)
game = GAME(1000, 600)
game.NewGame()

display_info = pygame.display.Info()
gameDisplay.Resize(display_info.current_w, display_info.current_h)

while inGame:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inGame = False
        if event.type == pygame.VIDEORESIZE:
            gameDisplay.Resize(event.w, event.h)

    game.paddle.paddleDirection = 0
    keys = pygame.key.get_pressed()
    if game.gameOver == False and game.paused == False:
        if keys[pygame.K_LEFT]:
            game.paddle.moveLeft()
            game.paddle.paddleDirection = 1
        if keys[pygame.K_RIGHT]:
            game.paddle.moveRight()
            game.paddle.paddleDirection = -1

    if keys[pygame.K_SPACE]:
        game.paused = False

    if game.gameOver:
        if keys[pygame.K_y]:
            game.NewGame()
        elif keys[pygame.K_n]:
            inGame = False

    if not pygame.key.get_focused():
        game.paused = True

    game.update()
    game.display(gameDisplay)

pygame.quit()
