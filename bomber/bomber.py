import pygame
import pygame.midi
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((710, 499))
font = pygame.font.SysFont("Courier", 30, bold=True, )
pygame.midi.init()
midi = pygame.midi.Output(0)
# midi.set_instrument(19)
# midi.set_instrument(103)
# midi.set_instrument(5)
midi.set_instrument(27)


space = [
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
]


ship = [
    "        ",
    "XXXX    ",
    "XXXX    ",
    "    XXXX",
    "    XXXX",
    "XXXX    ",
    "XXXX    ",
    "        ",
]

bomb = [
    "        ",
    "   XX   ",
    "  X  X  ",
    " X    X ",
    "X      X",
    " X    X ",
    "  X  X  ",
    "   XX   ",
]
explosion = [
    "X XX X X",
    "xx  XX X",
    "  X  X  ",
    " XXXX X ",
    "XXX X X ",
    "X XXX XX",
    "X X  X  ",
    "X  XX XX",
]
building = [
    "    XXXX",
    "    XXXX",
    "    XXXX",
    "    XXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
    "XXXXXXXX",
]

old_sound = 0


def sound(f):
    global old_sound
    old_sound = f
    midi.note_on(old_sound, 127)


def sound_off():
    midi.note_off(old_sound, 127)


def PrepareImage(mat, color1, color2):
    image = pygame.Surface((16, 16))
    image.fill(color2)
    for y in range(8):
        for x in range(8):
            if mat[y][x] != ' ':
                pygame.draw.rect(image, color1, (x*2, y*2, 2, 2))
    return image


chars = []
chars.append(PrepareImage(space, (0, 0, 255), (0, 0, 0)))
chars.append(PrepareImage(ship, (127, 127, 0), (0, 0, 255)))
chars.append(PrepareImage(bomb, (0, 0, 0), (0, 0, 255)))
chars.append(PrepareImage(explosion, (127, 127, 127), (0, 0, 255)))
chars.append(PrepareImage(explosion, (0, 0, 0), (255, 0, 0)))
chars.append(PrepareImage(building, (0, 0, 0), (0, 0, 255)))
chars.append(PrepareImage(building, (0, 0, 0), (0, 255, 0)))
chars.append(PrepareImage(building, (0, 0, 0), (0, 255, 255)))
chars.append(PrepareImage(building, (0, 0, 0), (255, 0, 0)))
chars.append(PrepareImage(building, (0, 0, 0), (255, 0, 255)))
chars.append(PrepareImage(building, (0, 0, 0), (255, 255, 0)))
chars.append(PrepareImage(building, (0, 0, 0), (255, 255, 255)))

map = []
for y in range(24):
    map.append([])
    for x in range(40):
        map[y].append(0)

for x in range(40):
    for y in range(24-random.randint(0, 15), 24):
        map[y][x] = random.randint(5, 11)

a = 0
b = -1
px = 0
py = 0
score = 0
quit = False
lives = 1
clock = pygame.time.Clock()
while not quit:
    clock.tick(10)
    sound_off()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit = True

    if lives > 0:
        map[py][px] = 0
        px += 1
        if px == 40:
            px = 0
            py += 1
        if map[py][px] != 0:
            map[py][px] = 4
            lives = 0
        else:
            map[py][px] = 1

        if b > -1:
            map[b][a] = 0
            if b >= 23:
                map[23][a] = 3
                b = -1
                score += 5
            else:
                b += 1
                if map[b][a] >= 5:
                    sound(b*2)
                    score += 10
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            b = py+1
            a = px
        elif b > 0:
            map[b][a] = 2

    if lives > 0:
        screen.fill((0, 0, 0))
    else:
        screen.fill((127, 0, 0))
        if lives > -15:
            lives -= 1
            midi.set_instrument(118)
            sound(random.randrange(0, 10))

    text = font.render(
        f"   PYBOMBER 2025      Score: {score:06} ", True, (0, 0, 127), (0, 255, 255))
    screen.blit(text, (32, 35))
    for y in range(24):
        for x in range(40):
            screen.blit(chars[map[y][x]], (35+x*16, 70+y*16))

    pygame.display.flip()
