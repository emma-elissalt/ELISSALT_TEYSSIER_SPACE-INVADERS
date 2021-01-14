# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : aliens

Créée le 07/01/2021

@author: Emma et Timothée
"""

class CObjetGraphique:
    def __init__(self,pXCentre, pYCentre, pLargeur, pHauteur):
        #tous les objets graphiques possèdent les propriétés suivantes
        # Centre de l'objet
        self.__xCentre = pXCentre
        self.__yCentre = pYCentre
        # Hauteur et Largeur de l'objet
        self.__largeur = pLargeur
        self.__hauteur = pHauteur
        # Identifiant unique dans le canevas
        self.__nomTag = ""
    
    #Permet de modifier le nom du tag = identifiant unique dans le canevas
    def setTag(self, pNomTag):
        self.__nomTag = pNomTag
    def getTag(self):
        return self.__nomTag

    def getXCentre(self):
        return self.__xCentre
    def getYCentre(self):
        return self.__yCentre
    
    #Renvoie les points extremes de la boite entourant l'objet
    def xMin(self):
        return self.__xCentre - self.__largeur // 2
    def xMax(self):
        return self.__xCentre + self.__largeur // 2
    def yMin(self):
        return self.__yCentre - self.__hauteur // 2
    def yMax(self):
        return self.__yCentre + self.__hauteur // 2
    

    #teste si il y a collision entre cet objet(self) et un autre objet graphique
    def collision(self, pObjet):
        if pObjet.xMax()>self.xMin() and pObjet.xMin()<self.xMax():
            if pObjet.yMax()>self.yMin() and pObjet.yMin()<self.yMax():
                return True
        return False
        
    #déplace l'objet dans le canevas d'une valeur pDX et pDY
    def deplacer(self, pCanevas, pDX, pDY):
        self.__xCentre+=pDX
        self.__yCentre+=pDY
        pCanevas.move(self.__nomTag, pDX, pDY)
        
    #Efface l'objet du canevas     
    def efface(self, pCanevas):
        pCanevas.delete(self.__nomTag)
        