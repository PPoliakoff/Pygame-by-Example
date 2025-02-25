import pygame
import random

def pomme():
    global pomme_x,pomme_y
    pomme_ok=False
    while pomme_ok==False:
        pomme_x=random.randrange(0,n_cases)
        pomme_y=random.randrange(0,n_cases)
        if (pomme_x,pomme_y)not in snake:
            pomme_ok =True


def nouvelle_partie():
    global snake,tete_x,tete_y,speed_x,speed_y,longueur_serpent,etat,vitesse_jeu
    snake=[]
    tete_x=random.randrange(0,n_cases)
    tete_y=random.randrange(0,n_cases)
    speed_x=0
    speed_y=0
    pomme()
    longueur_serpent=10
    etat="joue"
    vitesse_jeu=10

def affiche_Perdu(surface):
    font=pygame.font.Font(None,100)
    text=font.render("Perdu",True,COULEUR_TEXTE)
    pos_text= text.get_rect(center=(largeur_fenetre//2,hauteur_fenetre//3))
    surface.blit(text,pos_text)
    text=font.render("Rejouer? o/n",True,COULEUR_TEXTE)
    pos_text= text.get_rect(center=(largeur_fenetre//2,2*hauteur_fenetre//3))
    surface.blit(text,pos_text)


COULEUR_FOND=(0,255,255)
COULEUR_POMME=(255,0,0)
COULEUR_SERPENT=(0,0,0)
COULEUR_TETE=(0,255,0)
COULEUR_BORD=(0,0,127)
COULEUR_TEXTE=(255,0,0)

pygame.init()
fenetre=pygame.display.set_mode((0,0))

largeur_fenetre=fenetre.get_width()
hauteur_fenetre=fenetre.get_height()

n_cases=50
taille_case=int(min(largeur_fenetre/(n_cases+1),hauteur_fenetre/(n_cases+1)))
marge_x=(largeur_fenetre-n_cases*taille_case)//2
marge_y=(hauteur_fenetre-n_cases*taille_case)//2

nouvelle_partie()

clock=pygame.time.Clock()
while etat!="terminé":
    clock.tick(vitesse_jeu)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            etat="terminé"

    keys=pygame.key.get_pressed()
    if speed_y==0:
        if keys[pygame.K_UP]:
            speed_x=0
            speed_y=-1
        if keys[pygame.K_DOWN]:
            speed_x=0
            speed_y=1
    if speed_x==0:
        if keys[pygame.K_LEFT]:
            speed_x=-1
            speed_y=0
        if keys[pygame.K_RIGHT]:
            speed_x=1
            speed_y=0

    if etat=="joue":
        tete_y+=speed_y
        tete_x+=speed_x

        if tete_x<0:
            tete_x=n_cases-1
        elif tete_x>=n_cases:
            tete_x=0

        if tete_y<0:
            tete_y=n_cases-1
        elif tete_y>=n_cases:
            tete_y=0

        if speed_x!=0 or speed_y!=0:
            if(tete_x,tete_y)in snake:
                etat="perdu"
            snake.append((tete_x,tete_y))
            if len(snake)>longueur_serpent:
                del snake[0]

        if tete_x==pomme_x and tete_y==pomme_y:
            pomme()
            longueur_serpent+=10
            vitesse_jeu+=1
    else:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_y] or keys[pygame.K_o] :
            nouvelle_partie()
        elif keys[pygame.K_n]:
            etat="terminé"

    fenetre.fill(COULEUR_FOND)
    pygame.draw.rect(fenetre,COULEUR_BORD, (marge_x-2,marge_y-2,n_cases*taille_case+4,n_cases*taille_case+4),2)
    for c in snake:
        pygame.draw.rect(fenetre,COULEUR_SERPENT,(marge_x+c[0]*taille_case,marge_y+c[1]*taille_case,taille_case,taille_case))
    pygame.draw.rect(fenetre,COULEUR_TETE,(marge_x+tete_x*taille_case,marge_y+tete_y*taille_case,taille_case,taille_case))

    pygame.draw.circle(fenetre,COULEUR_POMME,(marge_x+taille_case//2+pomme_x*taille_case,marge_y+taille_case//2+pomme_y*taille_case),taille_case//2)
    if etat=="perdu":
        affiche_Perdu(fenetre)
    pygame.display.flip()
pygame.quit()    