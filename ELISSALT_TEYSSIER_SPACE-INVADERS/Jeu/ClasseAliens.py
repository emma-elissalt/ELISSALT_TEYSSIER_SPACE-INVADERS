# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : aliens

Créée le 21/12/2020

@author: Emma et Timothée
"""

from random import randrange
from ClasseObjetGraphique import CObjetGraphique

#un alien peut avoir 3 représentations graphiques
class CAliens(CObjetGraphique):
    #Ajoute à la classe de base la notion de type d'alien (1, 2 ou 3)
    def __init__(self, pXCentre, pYCentre, pTypeAlien):
        self.__typeAlien = pTypeAlien
        if pTypeAlien==1: 
            CObjetGraphique.__init__(self,  pXCentre, pYCentre, 55, 40)
        if pTypeAlien==2: 
            CObjetGraphique.__init__(self,  pXCentre, pYCentre, 45, 45)
        if pTypeAlien==3: 
            CObjetGraphique.__init__(self,  pXCentre, pYCentre, 45, 45)

    #Renvoie les coordonnées du haut d'un tir alien : centré en X et Y = YMax de l'alien
    def positionTir(self):
        return (self.xMax()+self.xMin())/2, self.yMax()

    def dessin(self, pCanevas, pImage, pNumero):
        self.setTag('Alien' + str(pNumero))
        pCanevas.create_image(self.getXCentre(), self.getYCentre(), image=pImage ,tags=self.getTag())
 
class CRangAlien:
    def __init__(self, pTypeAlien, pNombreMax):
        self.__aliens =[]
        self.__typeAlien = pTypeAlien
        self.__nombreMax = pNombreMax
        
    def dessin(self, pCanevas, pImage, pCentreX, pCentreY, pDeltaX):
        for i in range(self.__nombreMax):
            #Ajout d'un nouvel alien à la liste
            self.__aliens.append(CAliens(pCentreX + i * pDeltaX, pCentreY, self.__typeAlien))
            #Dessin de l'alien
            self.__aliens[i].dessin(pCanevas, pImage, self.__typeAlien*10 + i)

    #Le déplacement d'une rangée revient à déplacer chacun des aliens de la rangée
    def deplacer(self, pCanevas, pDX, pDY):
        for alien in self.__aliens:
            alien.deplacer(pCanevas, pDX, pDY)
            
    #Teste si un alien arrive sur le bord de l'écran
    #  pDirection vaut 1 si on se déplace vers la droite
    #  pDirection vaut -1 si on se déplace vers la gauche
    #  Renvoie VRAI sinon renvoie FAUX    
    def alienSurBordEcran(self, pBordGauche, pBordDroit, pFuturDeplacementEnX):
        for alien in self.__aliens:
            if alien.xMax()+pFuturDeplacementEnX>=pBordDroit:
                return True #je sors dés que j'ai trouvé un alien sur un bord
            elif alien.xMin()+pFuturDeplacementEnX<=pBordGauche:
                return True #je sors dés que j'ai trouvé un alien sur un bord        
        return False 
            
    #Teste si une collision existe entre les aliens et un objet graphique
    #si OUI renvoie VRAI et efface du canevas l'alien
    #sinon renvoie FAUX
    def collision(self, pCanevas, pObjet):
        #Parcours les aliens de la rangée pour tester la collision
        for alien in self.__aliens:
            if alien.collision(pObjet):
                #efface du canevas l'alien et l'objet
                alien.efface(pCanevas)
                #enleve l'alien de la rangée
                del self.__aliens[self.__aliens.index(alien)]
                #renvoie qu'une collision a eu lieu
                return True                
        #Si on arrive là c'est qu'aucune collision a eu lieu
        return False

    #Gestion du tir des aliens
    #La rangée doit tirer, cherche le point de départ du tir
    def positionTir(self):
        #Attention l'alien a pu être détruit entre temps et donc ne plus avoir de rangée
        if len(self.__aliens)!=0:
            indiceAlien = randrange(0,len(self.__aliens),1)
            return self.__aliens[indiceAlien].positionTir()
        return -1, -1 #renvoie des coordonnées en dehors de l'écran

    def nombreAliens(self):
        return len(self.__aliens)
    
    def getYMax(self):
        if len(self.__aliens)!=0:
            return self.__aliens[0].yMax()
        return 0 #si pas d'alien sur la ligne

class CTableauAlien:
    def __init__(self, pVitesse):
        self.__rangees=[]
        self.__direction=1 #Gestion du sens de déplacement des aliens +1 vers la droite -1 vers la gauche
        self.__vitesse = pVitesse
        
    def dessin(self, pCanevas, pXCentrePremierAlien, pYCentrePremierAlien, pDeltaX, pDeltaY, pImage1, pImage2, pImage3):
        #Ajout des 3 rangées au tableau
        self.__rangees.append(CRangAlien(1, 6)) #Création d'une rangée de 6 aliens de type 1
        self.__rangees.append(CRangAlien(2, 6)) #Création d'une rangée de 6 aliens de type 2
        self.__rangees.append(CRangAlien(3, 6)) #Création d'une rangée de 6 aliens de type 3
        #Dessin des rangées dans le canevas
        self.__rangees[0].dessin(pCanevas, pImage1, pXCentrePremierAlien, pYCentrePremierAlien, pDeltaX)
        self.__rangees[1].dessin(pCanevas, pImage2, pXCentrePremierAlien, pYCentrePremierAlien+pDeltaY, pDeltaX)
        self.__rangees[2].dessin(pCanevas, pImage3, pXCentrePremierAlien, pYCentrePremierAlien+2*pDeltaY, pDeltaX)
        
    def deplacer(self, pCanevas, pBordGauche, pBordDroit):
        #Déplacement du tableau, vérifie q'une des rangées n'est pas sur un bord
        #si oui alors inverse la direction de déplacement
        #sinon déplacement par défaut
        dX = self.__vitesse*self.__direction
        dY = 0
        inverserDirection = False
        for rangee in self.__rangees:
            if rangee.alienSurBordEcran(pBordGauche, pBordDroit, dX):
                inverserDirection = True
                break #je sors dés que j'ai trouvé un alien sur un bord
        if inverserDirection:
            self.__direction = -1 * self.__direction
            dX = 0
            dY = self.__vitesse
        for rangee in self.__rangees:
            rangee.deplacer(pCanevas, dX, dY)
            
    def collision(self, pCanevas, pObjet):
        #Vérifie si une collision existe dans ce cas efface les 2 objets
        for rangee in self.__rangees:
            if rangee.collision(pCanevas, pObjet):
                #Si la rangée ne possède plus d'alien alors suppression de la rangée dans la liste
                if len(self.__rangees)==0:
                    del self.__rangees[self.__rangees.index(rangee)]
                #renvoie qu'une collision a eu lieu
                return True                
        #Si on arrive là c'est qu'aucune collision a eu lieu
        return False
    
    def getYMax(self):
        yMax = 0
        for rangee in self.__rangees:
            if rangee.getYMax()>yMax:
                yMax = rangee.getYMax()
        return yMax  

    def positionTir(self):
        indiceRangee = randrange(0,len(self.__rangees),1)
        return self.__rangees[indiceRangee].positionTir()
                
    def nombreAliens(self):
        nombre=0
        for rangee in self.__rangees:
            nombre = nombre + rangee.nombreAliens()
        return nombre
             