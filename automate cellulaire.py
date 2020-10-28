import numpy as np
import math
import random as rd
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap


gist_rainbow = cm.get_cmap(name="gist_rainbow")#création d'une colormap pour faciliter le rendu

#types de cellules / leur couleur (cmap = gist_rainbow) :
cell = {
"ocean": 96/129, #(bleu foncé)
"terre": 0.4, #(vert)
"source_nourriture": 0, #(rouge)
"source_eau": 0.6, #(bleu clair)
"habitation": 1 #(rose/mauve)
}

côté = 80 #taille de la carte

carte = np.array([[cell["ocean"] for a in range(côté)] for b in range(côté)],dtype=np.float64)#génération de la carte

intervale = 2#rayon dans lequel chaque cellule prendra en compte les autres
"""
en l'occurence:
# # # # #
# # # # #
# # O # #
# # # # #
# # # # #
"""

rayA = -intervale#on crée une variable pour la borne basse, pour gagner du temps
rayB = intervale+1#même principe, mais on ajoute 1 parce que la borne haute est exclue

def génération():
    for a in range(intervale,côté-intervale):
        for b in range(intervale,côté-intervale):
            entourage = carte[a+rayA:a+rayB,b+rayA:b+rayB]#on découpe du tableau entier l'entourage de notre cellule
            print(entourage.size)
            contexte = {}#on crée un dictionnaire qui va contenir chaque type et son nombre d'occurences

            for i in cell.keys():
                contexte[i] = np.sum(entourage==cell[i])#on compte le nombre d'occurences de chaque type dans l'entourage de la cellule

            cellule = carte[a,b]#on relève le type de la cellule à traiter
            contexte[str(cellule)] -= 1 #on enlève un au type de la cellule à traiter parce qu'elle a été comptée dans son propre entourage

            carte[a,b] = règle(cellule,contexte)#on applique la règle en fonction du type de la cellule et de son entourage

def île(taille):
    base = np.array([[cell["ocean"] for a in range(taille)] for b in range(taille)],dtype=np.float64)#on crée une portion de carte qui contiendra l'île
    mid = int(taille/2)#on calcule le milieu de l'île (pour aller plus vite)

    for a in range(taille):#pour chaque "tranche" de la portion de carte:
        eq = math.sqrt((a-mid)**2)#on calcule la distance par rapport à la moitié
        inter = math.sqrt((mid**2)-(eq**2))#simple théorème de pythagore (on trace le cercle grâce à un triange rectangle dont l'hypothènuse est égale au rayon du cercle)
        for b in range(taille):#et pour chaque "case" dans cette tranche:
            if (b > mid-inter) and (b < mid+inter):#si la case est comprise dans le cercle:
                base[a,b] == cell["terre"] #on la "colorie"
    return(base)

def règle(cell,context):
    pass



#====================execution du code============

#génération de l'île
taille_ile = 30
ile = île(taille_ile)
#implémentation de l'île sur la carte
startpoint = 20
endpoint = startpoint+taille_ile
carte[startpoint:endpoint,startpoint:endpoint] = ile
#création des ressources
gen_cell = {#définition des probabilitées
"source_eau": 0.05,
"source_nourriture": 0.05,
"habitation": 0.01
}
for i in range(côté):
    for j in range(côté):
        for k in gen_cell.keys():
            if (carte[i,i] == cell["terre"]) and (rd.random() > gen_cell[k]):
                carte[i,j] = float(k)

carte *= 255
print(carte)
plt.imshow(carte,cmap=gist_rainbow)
plt.show()