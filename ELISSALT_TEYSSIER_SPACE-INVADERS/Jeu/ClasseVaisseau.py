# -*- coding: utf-8 -*-
"""
Projet : Space invaders
Classe : vaisseau

Créée le 21/12/2020

@author: Emma et Timothée
"""
from ClasseObjetGraphique import CObjetGraphique

class CVaisseau(CObjetGraphique):
        
    def dessin(self, pCanevas, pImage):
        self.setTag('Vaisseau')
        pCanevas.create_image(self.getXCentre(), self.getYCentre(), image=pImage ,tags=self.getTag())
    
