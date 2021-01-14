# -*- coding: utf-8 -*-
"""
Cette page correspond au porgramme du jeu space invaders, avec l'interface graphique Tkinter

Créée le 17/12/20

@author: Emma et Timothée
"""

#On utilise tkinter
from tkinter import Tk, Button, Canvas, Label, Menu, PhotoImage, FLAT
#On importe nos classes
from ClasseVaisseau import CVaisseau
from ClasseAliens import CTableauAlien
from ClasseTir import CTir
from ClasseIlot import CRangIlot
from ClasseBonus import CBonus
#On importe random pour les probabilités de tir et de passage
from random import random

#partie du code gérant les interractions avec l'utilisateur et les affichages

def deplacerDroite(event):
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #déplacement autorisé si pas sur le bord droit
    depX = deplacementVaisseau
    if vaisseau.xMax()+deplacementVaisseau > 612:
        depX = 612 - vaisseau.xMax()
    vaisseau.deplacer(zoneDessin, depX, 0)

def deplacerGauche(event):
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #déplacement autorisé si pas sur le bord gauche
    depX = -deplacementVaisseau
    if vaisseau.xMin()-deplacementVaisseau< 0 :
        depX = -vaisseau.xMin()
    vaisseau.deplacer(zoneDessin,depX,0)

def tirer(event):
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #tir du vaisseau
    global nombreTir, objetTir
    if nombreTir>=maxTir:
        return
    nombreTir+=1
    #Ajoute un nouvel objet Tir
    objetTir.append(CTir((vaisseau.xMax()+vaisseau.xMin())//2,vaisseau.yMin()-9))
    objetTir[-1].dessinTirVaisseau(zoneDessin)
    #Si la liste contient plus d'un tir alors pas la peine d'appeler la fonction de déplacement
    if len(objetTir)==1:
       zoneDessin.after(vitesseTir , deplacerTirVaisseau)
 
#Pour mettre le jeu sur pause sans quitter la partie
def pause(event):
    global pause
    if not(pause):
        pause=True
        #les fonctions vont automatiquement s'arrêter car elles testent la variable pause
        zoneDessin.after(1000)
    else:    
        pause=False
        #redémarre toute les fonctions : Tir vaisseau et alien, deplacement bonus et alien
        if len(objetTir)>0:
            zoneDessin.after(vitesseTir, deplacerTirVaisseau)
        if len(tirsAlien)>0:
            zoneDessin.after(vitesseTir, deplacerTirAlien)
        fenetre.after(vitesseBonus, deplacerBonus)         
        fenetre.after(vitesseAlien, deplacerAlien) 
        
#Cheat code pour gagner des vies supplémentaires      
def cheatVie(event):
    global nombreVies  
    nombreVies += 10
    labelVie['text'] = "VIE(S) : " + str(nombreVies)

def cheatTir(event):
    global maxTir
    maxTir += 3
        
#Indique au joueur le niveau de la partie 
def affichageLegende(pLegende):
    global tagLegende
    tagLegende = zoneDessin.create_text(306 , hauteurZoneDessin // 2 , text = pLegende, fill = "black", font=('Fixedsys',40))
    fenetre.after(2000, detruireLegende) #Attends 2 secondes avant d'effacer le message

def detruireLegende():
    zoneDessin.delete(tagLegende)
 
#affiche les points gagné apres avoir tué un alien et indique au joeur son score total
def afficherScore(donnee,x,y):
    global scores
    scores.append(zoneDessin.create_text(x,y,font=('Fixedsys',8),text=str(donnee)+' pts',fill='yellow'))
    fenetre.after(1500,EffacerScore)

def EffacerScore():
    global scores
    i=0
    while i<len(scores):
        zoneDessin.delete(scores[i])
        i+=1
    scores=[]

#Affichage du scénario
def aPropos():
    zoneDessin.delete('all')
    zoneDessin.create_image(308,hauteurZoneDessin // 2, image=imgGalaxie)
    zoneDessin.create_text(306,50,text = "Dans une autre galaxie, PROXIDIA,", fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,100,text ="l'empreur Balrog en soif de pouvoir," , fill = "yellow", font=('Fixedsys',20)) 
    zoneDessin.create_text(306,150,text ="envoya ses fidèles serviteurs :" , fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,200,text ="le dieu du tonnerre PIKACHU et" , fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,250,text ="le maître de la force BEBE YODA" , fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,300,text ="ces derniers ayant failli," , fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,350,text ="L'empreur est venu vous défier..." , fill = "yellow", font=('Fixedsys',20))
    zoneDessin.create_text(306,400,text ="Arriverez-vous à sauver la galaxie?" , fill = "yellow", font=('Fixedsys',20))

#Fin de la partie du code gérant les interractions avec l'utilisateur et les affichages

#Partie du code gérant les niveaux

#construction de la fenetre pour le niveau 1 du jeu
def afficherNiveau1():
    #RAZ de la partie
    global nombreVies, scores, score, tagImage, niveau
    global nombreTir, maxTir, objetTir
    global vitesseAlien, tirsAlien, tableauAlien
    global vaisseau, rangIlot
    global etatEnnemiBonus
    niveau=1
    zoneDessin.delete("all")
    scores=[]
    nombreVies = 3
    labelVie['text'] = "VIE(S) : " + str(nombreVies)
    score = 0
    labelScore['text'] = "Score : " + str(score)
    #Dessin du fond
    tagImage = zoneDessin.create_image(308, hauteurZoneDessin // 2, image=tempImage1)
    maxTir=3
    vitesseAlien = 750
    #Initialisation du vaisseau
    vaisseau = CVaisseau(22, hauteurZoneDessin-24,45,45)
    vaisseau.dessin(zoneDessin,imageVaisseau)
    #Initialisation du rang1 des aliens
    tableauAlien = CTableauAlien(deplacementAlien)
    tableauAlien.dessin(zoneDessin, 30, 30, 75, 65, imageAlien1, imageAlien2, imageAlien3)
    #Initialiser les ilots
    rangIlot = CRangIlot()
    rangIlot.dessin(zoneDessin,2*18, hauteurZoneDessin - 7*18)
    #Tir des aliens
    tirsAlien = []
    #Tirs du vaisseau
    nombreTir = 0
    objetTir = []
    #Ennemi bonus
    etatEnnemiBonus = False
    affichageLegende("LEVEL 1")
    
#Construction du niveau 2    
def afficherNiveau2():
    global niveau   
    global maxTir, nombreTir, objetTir
    global vitesseAlien, tirsAlien, tableauAlien
    global etatEnnemiBonus
    #On ne touche pas aux ilots
    #On ne touche pas au score, ni au nombre de vie
    #On ne touche pas au vaisseau
    #Paramètre propre a ce niveau
    niveau=2
    zoneDessin.itemconfigure(tagImage, image=tempImage2)     #On change le fond !
    maxTir=2
    vitesseAlien = 650
    #Efface les tirs de vaisseaux en cours
    nombreTir = 0
    for tir in objetTir:
        tir.efface(zoneDessin)
    objetTir = []
    #Initialisation du rang1 des aliens
    tableauAlien = CTableauAlien(deplacementAlien)
    tableauAlien.dessin(zoneDessin, 30, 30, 75, 65, imageAlien1, imageAlien2, imageAlien3)
    #Efface les tirs des aliens
    for tir in tirsAlien:
        tir.efface(zoneDessin)
    tirsAlien = []
    affichageLegende("LEVEL 2")

#Construction du niveau 3
def afficherNiveau3():
    global niveau   
    global maxTir, nombreTir, objetTir
    global vitesseAlien, tirsAlien, tableauAlien
    global etatEnnemiBonus
    #On ne touche pas aux ilots
    #On ne touche pas au score, ni au nombre de vie
    #On ne touche pas au vaisseau
    #Paramètre propre a ce niveau
    niveau=3
    zoneDessin.itemconfigure(tagImage, image=tempImage3)     #On change le fond !
    maxTir=1
    vitesseAlien = 500
    #Efface les tirs de vaisseaux en cours
    nombreTir = 0
    for tir in objetTir:
        tir.efface(zoneDessin)
    objetTir = []
    #Initialisation du rang1 des aliens
    tableauAlien = CTableauAlien(deplacementAlien)
    tableauAlien.dessin(zoneDessin, 30, 30, 75, 65, imageAlien1, imageAlien2, imageAlien3)
    #Efface les tirs des aliens
    for tir in tirsAlien:
        tir.efface(zoneDessin)
    tirsAlien = []
    affichageLegende("LEVEL 3")    
    
#Fonction qui lance le jeu sur le niveau 1
def nouvellePartie():
    global fin, pause
    if not(fin):
        return
    fin = False
    pause = False
    afficherNiveau1()
    #Initier le déplacement
    deplacerAlien()

#Fin de la partie du code gérant les niveaux

#Partie du code gérant la fin du jeu

#Fonction qui créée l'affichage du game over
def gameOver():
    global fin
    #Arrête toutes les fonctions
    fin=True
    #Efface le canevas
    zoneDessin.delete("all")
    #Affiche GAME OVER
    zoneDessin.create_image(308, hauteurZoneDessin // 2, image=imgGameOver)
    zoneDessin.create_text(306 , hauteurZoneDessin // 2 , text = "GAME OVER", fill = "red", font=('Fixedsys',40))

#Fonction qui créée l'affichage du victory
def victory():
    global fin, zoneDessin
    #Arrête toutes les fonctions
    fin=True
    #Efface le canevas
    zoneDessin.delete("all")
    #Affiche VICTORY
    zoneDessin.create_image(308, hauteurZoneDessin // 2, image=imgVictory)
    zoneDessin.create_text(306 , hauteurZoneDessin // 2 , text = "VICTORY", fill = "yellow", font=('Fixedsys',40))
   
def fermerProprement():
    global fenetre
    fenetre.destroy()

#Fin de la partie fin du jeu

#Partie du code gérant les tirs

def detruireTirVaisseau(tir):
    global nombreTir, objetTir, zoneDessin
    #Efface le tir du canevas
    tir.efface(zoneDessin)
    #détruit le tir dans la liste des tirs
    del objetTir[objetTir.index(tir)]
    #mise à jour du nombre de tir en cours
    nombreTir-=1
   
def detruireTirAlien(tir):
    global tirsAlien
    #Efface le tir du canevas
    tir.efface(zoneDessin)
    #détruit le tir dans la liste des tirs aliens
    del tirsAlien[tirsAlien.index(tir)]
    
    
def deplacerTirVaisseau():
    #Si partie finie alors ne fait rien
    global score, etatEnnemiBonus, vitesseAlien
      #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #déplace tous les tirs d'une case vers le haut
    #Attention parcours des tirs de la fin vers le début car destruction possible des éléments
    for i in range(len(objetTir)-1,-1,-1):
        tir = objetTir[i]
        tir.deplacer(zoneDessin,0,-deplacementTir)
        #vérifie que :
        # collision avec les ilots
        if rangIlot.collision(zoneDessin, tir):
            detruireTirVaisseau(tir)
        elif tir.yMin()<=0: # le tir ne sort pas du haut de l'écran
            detruireTirVaisseau(tir)
        elif tableauAlien.collision(zoneDessin, tir): # le tir vient de rencontrer un alien
            #Un alien a été détruit
            afficherScore(10,tir.xMin(),tir.yMin())
            score += 10
            labelScore['text'] = "Score : " + str(score)
            detruireTirVaisseau(tir)
            #Augmente la vitesse des aliens
            vitesseAlien-=25
            if tableauAlien.nombreAliens()==0:
                if niveau==1:
                    afficherNiveau2()
                elif niveau==2:
                    afficherNiveau3()
                else:
                    victory()
        elif etatEnnemiBonus: #si il y a un ennemi bonus
            if ennemiBonus.collision(tir):
                #ennemi bonus détruit
                etatEnnemiBonus=False
                ennemiBonus.efface(zoneDessin)
                afficherScore(150,tir.xMin(),tir.yMin())
                detruireTirVaisseau(tir)
                score += 150
                labelScore['text'] = "Score : " + str(score)
    #ne déplace les tirs que si il y a des tirs !
    if len(objetTir)>0:
        zoneDessin.after(vitesseTir, deplacerTirVaisseau)

def deplacerTirAlien():
    global nombreVies, vaisseau, fin
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #déplace tous les tirs alien d'une case vers le bas
    #Attention parcours des tirs de la fin vers le début car destruction possible des éléments
    for i in range(len(tirsAlien)-1,-1,-1):
        tir = tirsAlien[i]
        tir.deplacer(zoneDessin,0,deplacementTir)
        #vérifie que :
        if tir.yMax()>=hauteurZoneDessin: # le tir ne sort pas du bas de l'écran
            detruireTirAlien(tir)
        elif rangIlot.collision(zoneDessin, tir): # collision avec les ilots
            detruireTirAlien(tir)
        elif vaisseau.collision(tir): # collision avec le vaisseau
            detruireTirAlien(tir)
            #Perds une vie
            nombreVies-=1
            labelVie['text'] = "VIE(S) : " + str(nombreVies)
            vaisseau.efface(zoneDessin)
            vaisseau = CVaisseau(22, hauteurZoneDessin-24,45,45)
            vaisseau.dessin(zoneDessin,imageVaisseau)
            if nombreVies==0:
               gameOver()
    #ne déplace les tirs que si il y a des tirs !
    if len(tirsAlien)>0:
        zoneDessin.after(vitesseTir, deplacerTirAlien)
    
#Fin de la partie du code gérant les tirs

#Partie du code gérant le déplacement des éléments

def deplacerBonus():
    global etatEnnemiBonus
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    if not(etatEnnemiBonus):
        return
    ennemiBonus.deplacer(zoneDessin, sensBonus*deplacementBonus, 0)
    if ennemiBonus.xMin()<0:
        #efface le vaisseau bonus
        ennemiBonus.efface(zoneDessin)
        etatEnnemiBonus=False
    elif ennemiBonus.xMax()>612:
        #efface le vaisseau bonus
        ennemiBonus.efface(zoneDessin)
        etatEnnemiBonus=False
    else:
        #La fonction se rappelle pour simuler un déplacement
        fenetre.after(vitesseBonus, deplacerBonus)         
    
def deplacerAlien():
    global tirsAlien
    global etatEnnemiBonus, ennemiBonus, sensBonus
    #Si partie finie ou en pause alors ne fait rien
    if fin or pause:
        return
    #Si pas ennemi bonus, je teste si j'en crée un
    if not(etatEnnemiBonus):
        if random()<=probabiliteEnnemiBonus:
            #Choisit le bord d'apparition de la soucoupe bonus à droite ou à gauche
            if random()<=0.5: # Une chance sur deux pour bord droit ou gauche
                debut = 612-26
                sensBonus = -1
            else:
                debut = 26
                sensBonus = +1
            ennemiBonus = CBonus(debut, hauteurZoneDessin-8*18-10, 55, 20)
            ennemiBonus.dessin(zoneDessin, imageSoucoupe)
            etatEnnemiBonus=True
            deplacerBonus()
    #Création du tir des aliens
    if random()<=probabiliteTirAlien:
        x0,y0 = tableauAlien.positionTir()
        if x0>=0: #tir valide
            #ajoute le tir alien
            tirsAlien.append(CTir(x0,y0+9))
            #dessine le tir alien
            tirsAlien[-1].dessinTirAlien(zoneDessin)
            #deplacer alien
            if len(tirsAlien)==1:
                deplacerTirAlien()
    #Je déplace l'Alien vers la droite ou vers la gauche
    tableauAlien.deplacer(zoneDessin, 0, 612)
    #Quand les aliens sont à la même hauteur que les ilots détruire ligne par ligne
    positionY = tableauAlien.getYMax()
    rangIlot.efface(zoneDessin, positionY)
    if positionY>hauteurZoneDessin-45:
        gameOver()
    else: 
        #La fonction se rappelle sans fin toutes les vitesseAlien ms pour déplacer l'alien
        fenetre.after(vitesseAlien, deplacerAlien)  

#Fin de la partie du code gérant le déplacement des éléments
    
#Création de la fenêtre du jeu
fenetre = Tk()
#On lui ajoute un titre
fenetre.title('SPACE INVADERS : Emma ELISSALT et Timothée TEYSSIER')

#Création des labels ; parent=fenetre, Police de caractère=Fixedsys pour faire vintage, text=Valeur par défaut
labelScore = Label(fenetre,font=('Fixedsys',12),text="SCORE : ")
labelVie = Label(fenetre,font=('Fixedsys',12), text="VIE(S) : 3")

#Placement des labels sur la grille de la fenêtre : 
#  sticky définit comment positionner le controle dans la cellule : w=WEST(à gauche donc), E=EAST (à droite donc)
labelScore.grid(row=0,column=0,sticky='w')
labelVie.grid(row=0,column=1,sticky='e')

#Création du canevas : width=Largeur, height=Hauteur, bg=BackGround(couleur de fond)
hauteurZoneDessin = 486
zoneDessin = Canvas(fenetre,width=612,height=hauteurZoneDessin,bg='black',relief=FLAT)
# Placement du canevas : columnspan et rowspan permettent de faire tenir le canevas sur plusieurs cellules
zoneDessin.grid(row=1,column=0,columnspan=2,rowspan=4)

#Partie pour mettre les images de fond sur le canevas
tempImage = PhotoImage(file='donuts.gif')
tempImage1 = PhotoImage(file='pika.gif')
tempImage2 = PhotoImage(file='yoda.gif')
tempImage3 = PhotoImage(file='balrog.gif')
imgVictory=PhotoImage(file='bisounours.gif')
imgGameOver= PhotoImage(file='mario.gif')
imgGalaxie= PhotoImage(file='galaxie.gif')
#images des aliens, du bonus et du vaisseau
imageAlien1 = PhotoImage(file='alien1.png')
imageAlien2 = PhotoImage(file='alien2.png')
imageAlien3 = PhotoImage(file='alien3.png')
imageSoucoupe = PhotoImage(file='soucoupe.png')
imageVaisseau = PhotoImage(file='vaisseau.png')

#on initialise l'affichage d'entrée pour l'image
zoneDessin.create_image(308, hauteurZoneDessin // 2, image=tempImage)

#Fin partie image sur canevas

#Création des boutons : on garde la même police.
boutonDemarrer = Button(fenetre,text="Nouvelle partie",font=('Fixedsys',12), command=nouvellePartie)
boutonQuitter = Button(fenetre,text="Quitter",font=('Fixedsys',12), command=fermerProprement)
#Placement des boutons : padx permet de laisser une marge à droite et à gauche des boutons
boutonDemarrer.grid(row=2,column=2,padx=5)
boutonQuitter.grid(row=4,column=2,padx=5)

#Menu principal sous forme de barre
#Création de la barre de menu
menuPrincipal = Menu(fenetre)
#"Placement" du menu dans la fenêtre de l'application
fenetre['menu'] = menuPrincipal
#Création d'un menu dans le menu principal
menuAction = Menu(menuPrincipal)
#Création d'un "nom" dans le menu principal pour ouvrir menuAction
menuPrincipal.add_cascade(label="Actions", menu=menuAction)
#Ajoute des items au menu Action
menuAction.add_command(label="Nouvelle partie", command=nouvellePartie)
menuAction.add_command(label="Quitter", command=fermerProprement)
menuAction.add_command(label="A propos...", command=aPropos)

#Création du lien avec les touches du clavier
zoneDessin.bind_all("<Right>", deplacerDroite)
zoneDessin.bind_all("<Left>", deplacerGauche)
zoneDessin.bind_all("<space>", tirer)
zoneDessin.bind_all("p", pause) #touche pour mettre en pause le jeu
zoneDessin.bind_all("v",cheatVie) #cheat code
zoneDessin.bind_all("t",cheatTir) #cheat code

#Valeur par défauts
vitesseAlien = 700 #Déplacement tous les 700ms
deplacementAlien = 18 #Par déplacement les aliens bougent de 9 pixels
probabiliteTirAlien = 0.4

vitesseTir = 150 #Même vitesse pour les tirs aliens et les tirs vaisseaux
deplacementTir = 18 #Par déplacement les tirs bougent de 9 pixels en Y

deplacementVaisseau = 18 #Par deplacement nombre de pixel en X

probabiliteEnnemiBonus = 0.2
vitesseBonus = 100
deplacementBonus = 18 #Par deplacement nombre de pixel en X

maxTir=3 
nombreTir = 0
objetTir = []
fin = True
 
#Affichage du texte du début 
zoneDessin.create_text(306, 100, text = "SPACE INVADERS", fill = "purple", font=('Fixedsys',40))
zoneDessin.create_text(306, 350, text = "Emma ELISSALT", fill = "black", font=('Fixedsys',32))
zoneDessin.create_text(306, 400, text = "Timothée TEYSSIER", fill = "black", font=('Fixedsys',32))

#Démarrage du jeu
fenetre.mainloop()

