# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : tir (du vaisseau)

Créée le 31/12/2020

@author: Emma et Timothée
"""

from ClasseObjetGraphique import CObjetGraphique

class CTir(CObjetGraphique):
    def __init__(self, pXCentre, pYCentre):
        CObjetGraphique.__init__(self,  pXCentre, pYCentre, 6, 18)
        
    def dessinTirVaisseau(self, pCanevas):
        self.setTag(pCanevas.create_rectangle(self.xMin(), self.yMin(), self.xMax(), self.yMax(),fill='green'))

    def dessinTirAlien(self, pCanevas):
        self.setTag(pCanevas.create_rectangle(self.xMin(), self.yMin(), self.xMax(), self.yMax(),fill='orange'))

