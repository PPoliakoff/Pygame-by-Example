import pygame
pygame.font.init()

pygame.init()
screen = pygame.display.set_mode((800, 400))
petit_text = pygame.font.SysFont("Arial", 40)

score = 0
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

    i = petit_text.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(i, (0, 0))

    if perdu == True:
        i = petit_text.render('PERDU! Rejouer? o/n', True, (0, 0, 0))
        screen.blit(i, (220, 120))

    if perdu == False:
        perdu = b.colliderect(pygame.Rect(xp-40, yp-40, 80, 80))
        pygame.draw.circle(screen, (255, 128, 0), (xp, yp), 40)
    pygame.display.flip()

    clock.tick(150)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and yp == 320:
            vp = -8
        if perdu:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_n:
                quit = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_o:
                score = 0
                yp = 320
                vp = 0
                xb = 1000
                sb = 60
                perdu = False

    yp += vp
    if yp < 320:
        vp += 0.1
    else:
        vp = 0
        yp = 320

    xb -= 2
    if xb < -sb:
        xb = 800
        if perdu == False:
            sb += 5
            score += 1
