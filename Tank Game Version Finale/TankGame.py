import pygame
from pygame.locals import *
import random
import time


def writeScorefile():

    haveOne = False
    try:                                
        open('Score.txt', 'r')
        haveOne = True
    finally:
        if not haveOne:               
        
            scores = open('Score.txt', 'w')
            scores.write('1,0' + '\n')
            scores.write('2,0' + '\n')
            scores.close()
            scoredata = {}
            
def player_classes(option,player):
 #change les classes de chars pour chaque joueur en fonction de sa sélection
    
    #paramètre : joueur1 ou 2, l'option qu'il a choisie
    #vérifie quelle classe l'utilisateur a choisie, ajoute des attributs en conséquence
    
    if option == 0: #tank 1 a une vitesse de tir plus rapide et se déplace plus vite, mais a moins de hp
        player.cooldown = 10
        player.health = 3
        player.speed = 5
        player.pics = ver1
        player.image = ver1[0]

    elif option == 1: #tire plus lentement, se déplace plus lentement, mais a plus de PV
        player.cooldown = 30
        player.health = 5
        player.speed = 3
        player.pics = ver2
        player.image = ver2[0]

def movement(player):
    #cette fonction est pour le mouvement, fonctionne avec les deux joueurs
     
    
     #param joueur : joueur1 ou joueur2,
     #return: rien, mais déplace les sprites du joueur sur la carte en mouvement:
     #en fonction des touches définies pour le mouvement sur le sprite du joueur, si
     #l'une de ces touches est enfoncée, la gauche ou le haut de l'objet sprite est incrémenté à
     #la vitesse spécifiée, en fonction de leur classe tank. La direction du joueur est définie en fonction de la touche enfoncée,
     #et l'image du sprite change pour correspondre au mouvement.

     # Détection de collision:
     #si le sprite entre en collision avec quoi que ce soit dans le groupe de sprites "joueurs" ou l'une des tuiles murales sur la carte,
     #selon la direction du sprite à ce moment, la position de sa valeur gauche ou haute est décrémentée de sa
     # valeur de vitesse, ce qui fait que le char reste en place lorsqu'il entre en collision avec un autre joueur ou les murs.
    
    key = pygame.key.get_pressed()
    #c'est pour que le sprite continue de bouger lorsque l'utilisateur tient la touche


    if key[player.keys[0]]:
        player.rect.left -= player.speed
        player.direction = 'left'
        player.image = player.pics[3]

    elif key[player.keys[1]]:
        player.rect.left += player.speed
        player.direction = 'right'
        player.image = player.pics[2]

    elif key[player.keys[2]]:
        player.rect.top -= player.speed
        player.direction = 'up'
        player.image = player.pics[0]

    elif key[player.keys[3]]:
        player.rect.top += player.speed
        player.direction = 'down'
        player.image = player.pics[1]


    if len(pygame.sprite.spritecollide(player,players,False))> 1 or pygame.sprite.spritecollide(player,walls,False):
    #puisque le "joueur" lui-même fait partie du groupe de sprites des joueurs, nous vérifions si la longueur de la collision est
     #supérieur à 1, ce qui signifie qu'il est entré en collision avec l'autre joueur. La liste des collisions renverra -1 si elle
     #n'a rien, donc si la valeur renvoyée n'est pas -1, il a touché une tuile murale.

        if player.direction == 'left':
            player.rect.left += player.speed
        if player.direction == 'right':
            player.rect.left -= player.speed
        if player.direction == 'up':
            player.rect.top += player.speed
        if player.direction == 'down':
            player.rect.top -= player.speed

def drawPlayerHealth(player):
    #met à jour et dessine la santé du joueur en mode bataille
    
    #paramètre : quel joueur, 1&2
    #retour : rien, mais mise à jour des images de santé varibales et blit
    #en utilisant une boucle for dans la plage de santé du joueur, pour chaque point de santé, un cœur sera dessiné.
    # la position des cœurs change selon le joueur,
    # si c'est player1, des coeurs seront dessinés en bas à gauche de l'écran
    # si c'est player2, des coeurs seront dessinés en bas à droite de l'écran
    
    healthimage = pygame.image.load('health2.png')
    
    p1healthpos = [60, 500]                                 #Position initiale de santé/barre cardiaque du joueur 1
    p1title = my_font4.render('P1', True, (255,0,0))
    p2healthpos = [520,500]
    p2title = my_font4.render('P2', True, (0,0,255))        #Position initiale des barres de santé/cœurs du joueur 2
    
    screen.blit(p1title, (35, 500))
    screen.blit(p2title, (495, 500))
    for c in range(player.health):
        if player == player1:
            screen.blit(healthimage,p1healthpos)
            p1healthpos[0] += 15
        else:
            screen.blit(healthimage, p2healthpos)
            p2healthpos[0] += 14
            
            
def bullet(player):
   #fonction qui génère un sprite de balle, définit la taille, la couleur et la position des balles
    
    #parametre player : joueur 1 ou 2
    #return : rien, mais le sprite de balle sera généré
    #la fonction sera déclenchée par les joueurs appuyant sur leur touche de tir
    #si c'est le cas, une balle sera créée, sa position est orientée loin de la position du joueur

    
    bullet = pygame.sprite.Sprite()

    bullet.image = pygame.Surface((10,10))
    bullet.image.fill((0,0,0))
    bullet.rect = pygame.Rect(bullet.image.get_rect())
    bullet.direction = player.direction

  
    if bullet.direction == 'up':                                                
        bullet.rect.x, bullet.rect.y = player.rect.x + 5, player.rect.y - 15    
        #les positions des balles doivent faire face à la direction dans laquelle le joueur fait face
        #il faut qu'il y ait de la distance entre eux
    elif bullet.direction == 'down':
        bullet.rect.x, bullet.rect.y = player.rect.x + 5, player.rect.y + 24
    elif bullet.direction == 'left':
        bullet.rect.x, bullet.rect.y = player.rect.x - 15, player.rect.y + 5
    elif bullet.direction == 'right':
        bullet.rect.x, bullet.rect.y = player.rect.x + 24, player.rect.y + 5

    bulletgroup.add(bullet)

def bullet_update():
    #met à jour la position de la balle
   
    #return Aucun, mais la position des balles sera modifiée
    #mettre à jour les balles à chaque cycle, changer les x, y des balles pour animer le mouvement
 
    for bullet in bulletgroup:
        if bullet.direction == 'left':
            bullet.rect.x -= 6
        elif bullet.direction == 'right':
            bullet.rect.x += 6
        elif bullet.direction == 'up':
            bullet.rect.y -= 6
        elif bullet.direction == 'down':
            bullet.rect.y += 6

def readMap():
    #une fonction qui transforme les fichiers CSV en listes itérables afin que les tuiles puissent être ajoutées en fonction des informations
    # stockées dans les fichiers txt.
    # Chaque tuile est un sprite dans le groupe des murs
    #paramètres : aucun
    # retour : Aucun, cependant, un groupe de sprites r généré
    # choisit au hasard une carte à lire, coupe chaque ligne dans le fichier cvs, chaque point séparé signifie qu'une tuile doit être
    # établi. Donne au carreau une image et rect, ajoute le carreau au groupe
    
    Map = open(random.choice(maps), 'r')
    
    x = 0
    y = 0
    
    for l in Map:
        builtup = l.split(',')
        builtup[-1] = builtup[-1].strip('\n')
        for D in builtup:
            if D == '.':
                tile = pygame.sprite.Sprite()
                tile.image = tiles
                tile.rect = pygame.Rect(x, y, 11, 11)       
                walls.add(tile)                     #pour chaque ligne du fichier correspond à une colonne de la carte
                y += 11                               #la valeur des coordonnées y augmente de 11 car la taille de l'image est de 11 sur 11
            else:
                y += 11
        x += 11                               #ajouter 11 à x pour commencer sur la colonne suivante
        y = 0
           
    Map.close()
   
def gameMenu(thisStage):
    
    
    #paramètres : variable thisStage, si elle est vraie, la fonction s'exécute, sinon la fonction ne sera pas déclenchée
     
    
    global run, selecting, battling, end     
                                                                                                                
    pygame.mixer.music.load(musicList[0])    
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    Title = my_font.render('TankG', True, (175,44,33))
    Start_label = my_font2.render('Start Game', True, (212,212,212))
    Exit_label = my_font2.render('Exit Game', True, (212,212,212))
    
    Srect = Rect(210,280, 421, 339)         #rects ici est utilisé pour voir si les coordonnées de la souris sont dedans
    Erect = Rect(245, 340, 380, 430)
        
    while thisStage:
            
            x, y = pygame.mouse.get_pos()
            Opt = 0                                             #Opt signifie options, cette variable lisse le rendu et le suivi des événements
            
            if Srect[0] < x <Srect[2] and Srect[1] < y < Srect[3]:
                my_font2.set_underline(True)
                Start_label = my_font2.render('Start Game', True, (212,212,212))
                
                screen.blit(Start_label, (210,280))
                pygame.display.flip()

                Opt = 1                                                          #si la souris est sur les titres 
                                                                                 #souligner les titres, (un effet cool)
            elif Erect[0] < x < Erect[2] and Erect[1] < y < Erect[3]:           

                my_font2.set_underline(True)
                Exit_label = my_font2.render('Exit Game', True, (212,212,212))
        
                screen.blit(Exit_label, (220, 340))
                pygame.display.flip()
                
                Opt = 2
                
            my_font2.set_underline(False)
            Start_label = my_font2.render('Start Game', True, (212,212,212))
            Exit_label = my_font2.render('Exit Game', True, (212,212,212))

            screen.blit(screenPIC, (0,0))
            screen.blit(Title, (175,100))
            screen.blit(Start_label, (210,280))                 
            screen.blit(Exit_label, (220, 340))
            pygame.display.flip()
            
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.mixer.music.stop()
                    run = False
                    starting = False
                    selecting = False
                    battling = False
                    end = False
                    thisStage = False
                    
                elif ev.type == MOUSEBUTTONDOWN:
                    if Opt == 1:
                        pygame.mixer.music.stop()
                        starting = False
                        thisStage = False
                    elif Opt == 2:
                        pygame.mixer.music.stop()
                        run = False
                        starting = False
                        selecting = False
                        battling = False
                        end = False
                        thisStage = False

def selectionScreen(thisStage):
    #affiche le menu de sélection
    global run, selecting, battling, end                      
    pygame.mixer.music.load(musicList[1])    
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    Opt1 = 0
    Opt2 = 0                                   #Opt1 pour les options du joueur 1, Opt2 pour les options du joueur 2
    
    instructionP1 = pygame.image.load('instruction2.png')           #pics avec les commandes du joueur, aidez les utilisateurs à apprendre les commandes de leurs chars
    instructionP2 = pygame.image.load('instruction1.png')
    
    Title = my_font3.render('Choisissez votre tank ', True, (212,250,242))
    p1Title = my_font4.render('P1', True, (212,212,212))
    p2Title = my_font4.render('P2', True, (212,212,212))
    
    instruction = my_font4.render('Utilisez vos commandes gauche et droite pour chosir votre TANK', True, (175,44,33))
    instruction2 = my_font4.render('Appuyer sur entrer pour lancer la partie', True, (175,44,33))

    options = [imageUp_v1,imageUp_v2]                 #options réelles et leurs statistiques, cela aide le rendu lorsque l'utilisateur change de tank
    stats = {0:['3', '5', '3'], 1:['5','3','1']}
    
    DisplaySurf = pygame.Surface((100,100))
    DisplaySurf.fill((255,255,255))                 # surface blanche, crée un contraste entre les réservoirs et l'arrière-plan, facile pour l'utilisateur de voir les différences de tanks
    DisplaySurf2 = pygame.Surface((100,100))
    DisplaySurf2.fill((255,255,255))
    
    while thisStage:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.mixer.music.stop()
                run = False
                selecting = False
                battling = False
                end = False
                thisStage = False
            elif ev.type == KEYDOWN:
                if ev.key == K_RETURN:
                    pygame.mixer.music.stop()
                    readMap()
                    player_classes(Opt1, player1)
                    player_classes(Opt2, player2)
                    selecting = False
                    thisStage = False
                elif ev.key == K_a: 
                    if Opt1 == 0:
                        Opt1 = 1                                  
                    else:
                        Opt1 -= 1
                elif ev.key == K_d:
                    if Opt1 == 1:
                        Opt1 = 0
                    else:
                        Opt1 += 1
                elif ev.key == K_LEFT:
                    if Opt2 == 0:
                        Opt2 = 1
                    else:
                        Opt2 -= 1
                elif ev.key == K_RIGHT:
                    if Opt2 == 1:
                        Opt2 = 0
                    else:
                        Opt2 += 1
                        
        p1statsHealth = my_font5.render('Vie: ' + stats[Opt1][0], True, (212,212,212))
        p1statsSpeed = my_font5.render('Vitesse: ' + stats[Opt1][1],True, (212,212,212))
        p1statsReload = my_font5.render('Recharge: ' + stats[Opt1][2], True, (212,212,212))   #ces rendus doivent être dans la boucle car lorsque les utilisateurs changent
        p2statsHealth = my_font5.render('Vie: ' + stats[Opt2][0], True, (212,212,212))   #entre les tanks, les informations statistiques doivent être mises à jour
        p2statsSpeed = my_font5.render('Vitesse: ' + stats[Opt2][1],True, (212,212,212))
        p2statsReload = my_font5.render('Recharge: ' + stats[Opt2][2], True, (212,212,212))
        
        screen.blit(screenPIC, (0,0))
        screen.blit(Title, (50, 34))
        screen.blit(p1Title, (160, 170))
        screen.blit(p2Title, (420, 170))
        screen.blit(p1statsHealth, (40,240))
        screen.blit(p1statsSpeed, (40,260))
        screen.blit(p1statsReload, (40,280))
        screen.blit(p2statsHealth, (500,240))
        screen.blit(p2statsSpeed, (500,260))
        screen.blit(p2statsReload, (500,280))
        screen.blit(DisplaySurf, (120, 200))
        screen.blit(DisplaySurf2, (380, 200))
        screen.blit(options[Opt1], (158, 238))
        screen.blit(options[Opt2], (418, 238))
        screen.blit(instructionP1, (70, 300))
        screen.blit(instructionP2, (330, 290))
        screen.blit(instruction, (70, 480))
        screen.blit(instruction2, (170, 500))
        pygame.display.flip()
    
def battleScreen(thisStage):
    
    
    #paramètres : thisStage, doit être True pour exécuter la fonction,
    # retour : Aucun, anime l'interaction du jeu
    
    global run, end        
    pygame.mixer.music.load(musicList[2])    
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    timer = 0
    timer2 = 0
    
    while thisStage:
        fps = clock.tick(30)        
        timer += 1
        timer2 += 1
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.mixer.music.stop()
                run = False
                battling = False
                thisStage = False
                end = False
                
        movement(player1)               # régit le mouvement du joueur, ainsi que la collision les uns avec les autres et les murs
        movement(player2) 
        bullet_update()
        key = pygame.key.get_pressed()

        if key[player1.keys[4]]:
            if timer >= player1.cooldown:
                shoot.play()
                bullet(player1)
                timer = 0

        if key[player2.keys[4]]:
            if timer2 >= player2.cooldown:
                shoot.play()
                bullet(player2)
                timer2 = 0
                
        for bullets in bulletgroup:
            if pygame.sprite.collide_rect(bullets,player1):
                bulletgroup.remove(bullets)
                player1.health -= 1
                explode.play()
                screen.blit(explosion, player1.rect)
                pygame.display.flip()
                time.sleep(1)
                player1.rect.center = spawnpoints[random.randint(0,2)]
                
            if pygame.sprite.collide_rect(bullets,player2):
                bulletgroup.remove(bullets)
                player2.health -= 1
                explode.play()
                screen.blit(explosion, player2.rect)
                pygame.display.flip()
                time.sleep(1)
                player2.rect.center = spawnpoints[random.randint(0,2)]
            if pygame.sprite.spritecollide(bullets,walls,False):
                explode.play()
                bulletgroup.remove(bullets)
            if len(pygame.sprite.spritecollide(bullets,bulletgroup, False))>1:
                pygame.sprite.spritecollide(bullets,bulletgroup, True)


        screen.blit(background, (0,0))
        walls.draw(screen)
        players.draw(screen)
        bulletgroup.draw(screen)
        drawPlayerHealth(player1)
        drawPlayerHealth(player2)
        pygame.display.flip()
        pygame.display.update()
        
        if player1.health == 0 or player2.health == 0:
            pygame.mixer.music.stop()
            battling = False
            thisStage = False
            endScreen(end)

            
def endScreen(thisStage):
    #détermine le gagnant, calcule les scores, affiche l'écran de fin .
    '''
    parameters: thisStage, needs to be true to execute this function
    returns: None
    '''
    global run, starting, selecting

    pygame.mixer.music.load(musicList[3])    
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    bulletgroup.empty()     #supprimer toute
    walls.empty()           #supprimer les tuiles car la carte sera redessinée

    scores = open('Score.txt', 'r')
    for l in scores:
        dataFields = l.split(',')
        dataFields[-1] = dataFields[-1].strip('\n')
        scoredata[dataFields[0]] = int(dataFields[1])               #lire le fichier cvs du score, mettre à jour les données du score
    scores.close()
    
    winner = max(player1.health,player2.health)     #utiliser la santé restante pour déterminer le gagnant
    
    if winner == player1.health:
            WinnerTitle =  my_font2.render('PLAYER 1 WINS', True, (212,212,212))
            scoredata['1'] +=1                                                      #celui qui gagne gagne 1 point
    else:
            WinnerTitle = my_font2.render('PLAYER 2 WINS', True, (212,212,212))
            scoredata['2'] +=1

    scores = open('Score.txt', 'w')
    scores.write('1,' + str(scoredata['1']) + '\n')         #enregistrer la victoire
    scores.write('2,' + str(scoredata['2']) + '\n')
    scores.close()
            
    Title = my_font3.render('Fin de Partie ', True, (255,0,0))
    scoreTitle = my_font2.render('Score', True, (212,212,212))
    instruction = my_font4.render('', True, (175,44,33))
    instruction2 = my_font4.render('Appuyez sur Entrée pour retournez au MENU', True, (175,44,33))

    while thisStage:
        p1Scores = my_font2.render('Player 1:  ' +str(scoredata['1']), True, (212,212,212))
        p2Scores = my_font2.render('Player 2:  '+ str(scoredata['2']), True, (212,212,212))

        screen.blit(screenPIC, (0,0))
        screen.blit(Title, (120,50))
        screen.blit(WinnerTitle, (165,200))
        screen.blit(scoreTitle, (245,280))
        screen.blit(p1Scores, (60,340))
        screen.blit(p2Scores, (350,340))
        screen.blit(instruction, (230, 480))
        screen.blit(instruction2, (170,500))
        pygame.display.flip()
        
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.mixer.music.stop()
                run = False
                end = False
                thisStage = False
            elif ev.type == KEYDOWN:
                if ev.key == K_RETURN:
                    pygame.mixer.music.stop()
                    thisStage = False
                elif ev.key == K_r:
                    scoredata['1'] = 0        #réinitialiser les scores 
                    scoredata['2'] = 0

    scores = open('Score.txt', 'w')
    scores.write('1,' + str(scoredata['1']) + '\n')
    scores.write('2,' + str(scoredata['2']) + '\n')         #enregistrement final 
    scores.close()
        
    starting = True
    selecting = True
    
pygame.init()
pygame.mixer.init(44100, -16, 2, 2048)
clock = pygame.time.Clock()

colours = pygame.color.THECOLORS
my_font = pygame.font.SysFont('impact', 120)
my_font2 = pygame.font.SysFont('moolboran', 66)
my_font3 = pygame.font.SysFont('andalus', 72)      #configuration des polices
my_font4 = pygame.font.SysFont('candara', 20)
my_font5 = pygame.font.SysFont('arial', 16)

size = (605, 540)
screen = pygame.display.set_mode(size)
screenPIC = pygame.image.load('menu.png')
pygame.display.set_caption("TankGame by Rayan & Alex")              #configuration de l'écran
background = pygame.Surface(size)
background = background.convert()
background.fill(colours['grey'])

explode = pygame.mixer.Sound('explosion.ogg')
shoot = pygame.mixer.Sound('fire.ogg')          #effets sonores et musique
musicList = ['menuSong.ogg','selectSong.ogg','battleSong.ogg','endSong.ogg']

maps = ['map1.txt', 'map2.txt', 'map3.txt']
tiles = pygame.image.load('tile.png')

explosion = pygame.image.load('maybe.png')
imageUp_v1 = pygame.image.load('ver1 up.png')
imageDown_v1 = pygame.image.load('ver1 down.png')
imageRight_v1 = pygame.image.load('ver1 right.png')     #charger des images pour les tanks
imageLeft_v1 = pygame.image.load('ver1 left.png')

imageUp_v2 = pygame.image.load('ver2 up.png')
imageDown_v2 = pygame.image.load('ver2 down.png')
imageRight_v2 = pygame.image.load('ver2 right.png')
imageLeft_v2 = pygame.image.load('ver2 left.png')

ver1 = [imageUp_v1,imageDown_v1,imageRight_v1,imageLeft_v1]
ver2 = [imageUp_v2,imageDown_v2,imageRight_v2,imageLeft_v2]
spawnpoints = [(30,30),(40,390),(560,130),(560,390)]                

#pygame.sprite est très utile pour organiser et stocker des informations
players = pygame.sprite.Group()

player1 = pygame.sprite.Sprite()
player1.rect = pygame.Rect((20, 20),(24,24))                        #rect est utilisé pour la détection de collision
player1.direction = 'up'                                            #la position de départ est en haut
player1.keys = (K_a, K_d, K_w, K_s,K_1)                             #stocke les clés nécessaires à l'utilisation
player2 = pygame.sprite.Sprite()
player2.rect = pygame.Rect((560, 390), (24,24))
player2.direction = 'up'
player2.keys = (K_LEFT, K_RIGHT, K_UP, K_DOWN,K_m)

players.add(player1)
players.add(player2)

bulletgroup = pygame.sprite.Group()
walls = pygame.sprite.Group()                     

            
run = True
starting = True                     #variables de contrôle pour les fonctions et les boucles
selecting = True
battling = True
end = True


writeScorefile()
scoredata = {}

while run:
    fps = clock.tick(30)

    gameMenu(starting)
    selectionScreen(selecting)
    battleScreen(battling)
    
   

pygame.display.quit()
quit()

