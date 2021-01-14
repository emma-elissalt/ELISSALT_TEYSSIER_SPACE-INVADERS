# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : ennemi bonus

Créée le 07/01/21

@author: Emma et Timothée
"""

from ClasseObjetGraphique import CObjetGraphique

class CBonus(CObjetGraphique):
        
    def dessin(self, pCanevas, pImage):
       self.setTag("bonus")
       pCanevas.create_image(self.getXCentre(), self.getYCentre(), image=pImage ,tags=self.getTag())
   