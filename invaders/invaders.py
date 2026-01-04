import pygame
import random
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((30,20))
        pygame.draw.polygon(self.image,(0,127,0),((0,19),(15,0),(29,19)))
        self.rect=self.image.get_rect(center=(400,560))
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Bombe(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((15,15))
        pygame.draw.circle(self.image,(255,0,0),(8,8),7)
        self.rect=self.image.get_rect(center=(x,y))
    def update(self):
        self.rect.y+=3
        if self.rect.y>600:
            self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((8,16))
        self.image.fill((255,255,0))
        self.rect=self.image.get_rect(center=(x,y))
    def update(self):
        self.rect.y-=3
        if self.rect.top<0:
            self.kill()

class Ennemi(pygame.sprite.Sprite):
    vitesse=2
    vitesseY=0
    cogneMur=False
    def __init__(self,x,y,color):
        super().__init__()
        self.image=pygame.Surface((40,40))
        self.image.fill(color)
        self.rect=self.image.get_rect(center=(x,y))
    def update(self):
        self.rect.x+=Ennemi.vitesse
        self.rect.y+=Ennemi.vitesseY
        if self.rect.left<=0 or self.rect.right>=800:
            Ennemi.cogneMur=True
        if random.randrange(5 *(10+len(bombes)))==0:
            bombes.add(Bombe(self.rect.x+20,self.rect.y+38))
    def rebond():
        if Ennemi.cogneMur:
            Ennemi.vitesse*=-1
            Ennemi.cogneMur=False
            Ennemi.vitesseY=10
        else:
            Ennemi.vitesseY=0

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Invaders")

ennemis=pygame.sprite.Group()
bombes=pygame.sprite.Group()
missiles=pygame.sprite.Group()
player=Player()
ennemiColor=[(255,0,0),(127,127,0),(127,0,127),(64,128,64)]

clock = pygame.time.Clock()
exit = False
while not exit:
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit=True
        if event.type== pygame.KEYDOWN and event.key==pygame.K_SPACE and len(missiles)<5:
            missiles.add(Missile(player.rect.centerx-4,player.rect.top+4))

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.rect.x>0:
        player.rect.x-=5
    elif keys[pygame.K_RIGHT] and player.rect.right<800:
        player.rect.x+=5
    if len(ennemis)==0:
        for i in range(8):
            for j in range(4):
                ennemis.add(Ennemi(120+i*70,70+j*70,ennemiColor[j]))
    ennemis.update()
    bombes.update()
    missiles.update()
    Ennemi.rebond()
    if len(pygame.sprite.spritecollide(player,bombes,False))>0:
        exit=True
    pygame.sprite.groupcollide(missiles,bombes,True,True)
    pygame.sprite.groupcollide(missiles,ennemis,True,True)
    screen.fill((0, 0,0))
    ennemis.draw(screen)
    bombes.draw(screen) 
    missiles.draw(screen)
    player.draw(screen)
    pygame.display.flip()
