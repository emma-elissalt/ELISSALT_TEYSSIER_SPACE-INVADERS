# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : tir (du vaisseau)

Créée le 30/12/2020

@author: Emma et Timothée
"""

from ClasseObjetGraphique import CObjetGraphique

class CBlocIlot(CObjetGraphique):
    def __init__(self, pXCentre, pYCentre, pLigne):
        CObjetGraphique.__init__(self,  pXCentre+6, pYCentre+6, 10, 10)
        self.ligne = pLigne

    def dessin(self, pCanevas):
        self.setTag(pCanevas.create_rectangle(self.xMin(), self.yMin(), self.xMax(), self.yMax(),fill='gray', outline=""))

class CIlot:
    def __init__(self):
        self.blocs = []

    def dessin(self, pCanevas, pX0, pY0):
        y=5    
        for x in range(0,2):            
            self.blocs.append(CBlocIlot(pX0 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        for x in range(0,2):            
            self.blocs.append(CBlocIlot(pX0 + 8*10 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        y=4
        for x in range(0,10):            
            self.blocs.append(CBlocIlot(pX0 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        y=3
        for x in range(0,10):            
            self.blocs.append(CBlocIlot(pX0 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        y=2
        for x in range(0,10):            
            self.blocs.append(CBlocIlot(pX0 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        y=1    
        for x in range(0,8):            
            self.blocs.append(CBlocIlot(pX0 + 1*10 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
        y=0
        for x in range(0,6):            
            self.blocs.append(CBlocIlot(pX0 + 2*10 + x*10,pY0 + y*10,y))
            self.blocs[-1].dessin(pCanevas)
                

    def collision(self, pCanevas, pObjet):
        #Vérifie si une collision existe dans ce cas supprime le bloc en question
        for bloc in self.blocs:
            if bloc.collision(pObjet):
                #efface du canevas
                bloc.efface(pCanevas)
                #destruction du bloc
                del self.blocs[self.blocs.index(bloc)]
                #renvoie qu'une collision a eu lieu
                return True                
        #Si on arrive là c'est qu'aucune collision a eu lieu
        return False

    #Efface tous les blocs qui ont YMin < pY
    def efface(self, pCanevas, pY):
        for bloc in self.blocs:
            if bloc.yMin()<pY:
                #efface du canevas
                bloc.efface(pCanevas)
                #destruction du bloc
                del self.blocs[self.blocs.index(bloc)]

class CRangIlot:
    def __init__(self):
        self.ilots = []

    def dessin(self, pCanevas, pX0, pY0):
        self.ilots.append(CIlot())
        self.ilots[0].dessin(pCanevas,pX0, pY0)
        self.ilots.append(CIlot())
        self.ilots[1].dessin(pCanevas, pX0+12*18, pY0)
        self.ilots.append(CIlot())
        self.ilots[2].dessin(pCanevas, pX0+24*18, pY0)
    
    def collision(self, pCanevas, pObjet):
        #Vérifie si une collision existe dans ce cas supprime le bloc en question
        for ilot in self.ilots:
            if ilot.collision(pCanevas, pObjet):
                #renvoie qu'une collision a eu lieu
                return True                
        #Si on arrive là c'est qu'aucune collision a eu lieu
        return False
   
    def detruireLigne(self, pCanevas, pIndiceLigne):
        for ilot in self.ilots:
            ilot.detruireLigne(pCanevas, pIndiceLigne)
     
    #Efface tous les blocs qui ont YMin < pY
    def efface(self, pCanevas, pY):
        for ilot in self.ilots:
            ilot.efface(pCanevas, pY)
