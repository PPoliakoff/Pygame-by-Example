# RetroCentipede

import pygame
import pygame.midi
import random

pygame.init()
pygame.font.init()
pygame.midi.init()
midi = pygame.midi.Output(0)

font = pygame.font.SysFont("Courier", 32, bold=True, )
screen = pygame.display.set_mode((1024, 768))

# define characters
Empty = []

Mushroom = [
    "   XX   ",
    "  XXXX  ",
    " XXXXXX ",
    "XXXXXXXX",
    "XXXXXXXX",
    " X XX X ",
    "   XX   ",
    "   XX   "
]

Mushroom2 = [
    "   XX   ",
    "  XXXX  ",
    " XXXXXX ",
    "X   XXXX",
    "     XXX",
    "    X X ",
    "        ",
    "        "
]
Centipede = [
    "  XXXX  ",
    " XXXXXX ",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    " XXXXXX ",
    "  X  X  ",
    "  X  X  ",
]

Centipede2 = [
    "  XXXX  ",
    " XXXXXX ",
    "X  XX  X",
    "X  XX  X",
    "XXXXXXXX",
    " XXXXXX ",
    "  X  X  ",
    "  X  X  ",
]

Spider = [
    "  XXXX  ",
    "  XXXX  ",
    "XXXXXXXX",
    "X XXXX X",
    "X X  X X",
    "X X  X X",
    "X X  X X",
    "  X  X  ",
]

Gun = [
    "",
    "   XX",
    "   XX",
    "  XXXX  ",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
]

Missile = [
    "",
    "",
    "",
    "   XX",
    "   XX",
    "   XX",
    "   XX",
    "",
    "",
]


def sound(f, i):
    midi.set_instrument(i)
    old_sound.append(f)
    midi.note_on(f, 127)


def sound_off():
    for f in old_sound:
        midi.note_off(f, 127)
    old_sound.clear()


def PrepareImage(mat, color1, color2):
    image = pygame.Surface((32, 32), flags=pygame.SRCALPHA)
    image.fill(color2)
    for y in range(min(8, len(mat))):
        for x in range(min(8, len(mat[y]))):
            if mat[y][x] != ' ':
                pygame.draw.rect(image, color1, (x*4, y*4, 4, 4))
    return image


def resetMap():
    global my, sy, px, py
    for y in range(len(map)):
        for x in range(len(map[y])):
            if y > 0 and y < 17 and random.randrange(10) == 0:
                map[y][x] = 1
            else:
                map[y][x] = 0
    # diplay remaining lives
    for i in range(lives):
        map[23][12+i*2] = 6  # gun
    NewCentipede()
    my = -1  # cancel missile
    sy = -1
    px = 16
    py = 21
    map[py][px] = 6  # initial gun


def NewCentipede():
    centipede.clear()
    for i in range(6):
        if i < 5:
            centipede.append([i, 0, 1, 3])
        else:
            centipede.append([i, 0, 1, 4])
        map[0][i] = centipede[i][3]


def impact(mx, my):
    if map[my][mx] == 1:
        map[my][mx] = 2
        sound(55, 27)
        return 5
    elif map[my][mx] == 2:
        map[my][mx] = 0
        sound(55, 27)
        return 5
    elif map[my][mx] == 3:  # centipede body
        map[my][mx] = 1
        sound(67, 27)
        return 100
    elif map[my][mx] > 3:  # spider or centiped head
        map[my][mx] = 0
        sound(81, 27)
        return 250
    print(map[my][mx])  # this should never happen


Chars = []
centipede = []
Chars.append(PrepareImage(Empty, (0, 0, 0), (0, 0, 0, 0)))
Chars.append(PrepareImage(Mushroom, (0, 255, 0), (0, 0, 0, 0)))
Chars.append(PrepareImage(Mushroom2, (0, 255, 0), (0, 0, 0, 0)))
Chars.append(PrepareImage(Centipede, (255, 0, 0), (0, 0, 0, 0)))
Chars.append(PrepareImage(Centipede2, (255, 0, 0), (0, 0, 0, 0)))
Chars.append(PrepareImage(Spider, (0, 0, 255), (0, 0, 0, 0)))
Chars.append(PrepareImage(Gun, (255, 0, 255), (0, 0, 0, 0)))
Chars.append(PrepareImage(Missile, (255, 255, 0), (0, 0, 0, 0)))
map = []
for y in range(24):
    map.append([])
    for x in range(32):
        map[y].append(0)


def newGame():
    global gameOver, lives, score
    gameOver = False
    lives = 3
    score = 0
    resetMap()


quit = False
clock = pygame.time.Clock()
sx = 0
sdy = 1
sdx = 1
count = 0
explosion = 0
old_sound = []
hiscore = 0
newGame()
while not quit:
    clock.tick(30)
    sound_off()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True
    keys = pygame.key.get_pressed()
    if gameOver:
        if keys[pygame.K_y]:
            newGame()
        elif keys[pygame.K_n]:
            quit = True

    if not gameOver and explosion == 0:
        if map[py][px] != 6:  # gun hits something
            explosion = 50

        map[py][px] = 0

        if px > 0 and keys[pygame.K_LEFT]:
            px -= 1
        if px < 31 and keys[pygame.K_RIGHT]:
            px += 1
        if py > 18 and keys[pygame.K_UP]:
            py -= 1
        if py < 22 and keys[pygame.K_DOWN]:
            py += 1

        if map[py][px] > 2:  # gun hits something
            explosion = 50

        map[py][px] = 6  # gun

        if my < 0:
            if keys[pygame.K_SPACE]:
                mx = px
                my = py-1
        else:
            if map[my][mx] != 7:  # missile
                score += impact(mx, my)
                my = -1
            map[my][mx] = 0
            my -= 1
        if my >= 0:
            if map[my][mx] == 0:
                map[my][mx] = 7  # missile
            else:
                score += impact(mx, my)
                my = -1

        if count < 2:
            count += 1
        else:
            count = 0
            if sy < 0:
                if random.randrange(30) == 0:
                    # new spider
                    sy = 22-random.randrange(4)
                    if px > 15:
                        sx = 0
                        sdx = 1
                    else:
                        sx = 31
                        sdx = -1
                    sdy = -1
                    map[sy][sx] = 5  # spider

            else:
                # move spider
                if map[sy][sx] != 5:
                    sy = -1  # dead spyder
                else:
                    if random.randrange(60) == 0 and sy != 22:
                        map[sy][sx] = 1
                    else:
                        map[sy][sx] = 0

                    sx += sdx
                    sy += sdy
                    if sy == 22 or sy == 18:
                        sdy = -sdy
                    if sx == 32 or sx == -1:
                        sy = -1
                    else:
                        map[sy][sx] = 5  # spider

            # move centipede
            for i in range(len(centipede)):
                e = centipede[i]
                if map[e[1]][e[0]] == e[3]:
                    map[e[1]][e[0]] = 0
                else:
                    if i > 0:
                        centipede[i-1][3] = 4
                    e[1] = -1
            found = False
            for e in centipede:
                if e[1] >= 0:
                    found = True
                    e[0] += e[2]

                    if e[0] > 31 or e[0] < 0 or map[e[1]][e[0]] == 1 or map[e[1]][e[0]] == 2:
                        e[2] = -e[2]
                        e[1] += 1
                        e[0] += e[2]
                    if e[1] > 22:
                        e[1] = 0
                    map[e[1]][e[0]] = e[3]
            if not found:
                NewCentipede()
    if explosion > 0:
        explosion -= 1
        sound(random.randrange(0, 10), 118)
        screen.fill(
            (random.randrange(60), random.randrange(60), random.randrange(60)))
        if explosion == 0:
            lives -= 1
            if lives < 0:
                gameOver = True
                if score > hiscore:
                    hiscore = score
            else:
                resetMap()
    else:
        screen.fill((0, 0, 0))

    # display the game
    for y in range(len(map)):
        for x in range(len(map[y])):
            screen.blit(Chars[map[y][x]], (x*32, y*32))
    text = font.render(
        f"Score: {score:08} ", True, (0, 127, 255), (0, 0, 0))
    screen.blit(text, (0, 732))
    text = font.render(
        f"Hi Score: {hiscore:08} ", True, (0, 127, 255), (0, 0, 0))
    screen.blit(text, (660, 732))
    if gameOver:
        text = font.render(
            "GAME OVER", True, (255, 0, 0), (0, 0, 0, 0))
        screen.blit(text, (420, 350))
        text = font.render(
            "Play again Y/N", True, (255, 0, 0), (0, 0, 0, 0))
        screen.blit(text, (380, 380))
    pygame.display.flip()
