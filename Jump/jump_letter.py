import random
import pygame.font
import pygame
pygame.init()

font = pygame.font.SysFont("Arial", 80)
lettres = "abcdefghijklmnopqurstuvwxyz"
lettre = random.choice(lettres)

screen = pygame.display.set_mode((800, 400))
xp = 70
yp = 320
vp = 0
xb = 750
yb = 300
sb = 60
perdu = False
clock = pygame.time.Clock()
quit = False
while quit == False:
    b = pygame.Rect(xb, yb, sb, 60)
    screen.fill((0, 128, 128))
    pygame.draw.rect(screen, (64, 64, 0), pygame.Rect(0, 360, 800, 400))
    pygame.draw.rect(screen, (0, 0, 255), b)
    if perdu == False:
        perdu = b.colliderect(pygame.Rect(xp-40, yp-40, 80, 80))
        pygame.draw.circle(screen, (255, 128, 0), (xp, yp), 40)

        i = font.render(lettre, True, (0, 0, 0))
        screen.blit(i, (xp-15, yp-55))

    pygame.display.flip()

    clock.tick(150)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True
        if e.type == pygame.KEYDOWN and e.unicode == lettre and yp == 320:
            lettre = random.choice(lettres)
            vp = -8

    yp += vp
    if yp < 320:
        vp += 0.1
    else:
        vp = 0
        yp = 320

    xb -= 2
    if xb < -sb:
        xb = 800
        sb += 5
