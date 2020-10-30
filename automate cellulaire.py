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
#"source_nourriture": 0, #(rouge)
"source_eau": 0.6, #(bleu clair)
"habitation": 1 #(rose/mauve)
}
 
côté = 100 #taille de la carte
 
carte = np.array([[cell["ocean"] for a in range(côté)] for b in range(côté)],dtype=np.float64)#génération de la carte
 
intervale = 4#rayon dans lequel chaque cellule prendra en compte les autres
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
            cellule = ""
            entourage = carte[a+rayA:a+rayB,b+rayA:b+rayB]#on découpe du tableau entier l'entourage de notre cellule
            contexte = {}#on crée un dictionnaire qui va contenir chaque type et son nombre d'occurences
 
            for i in cell.keys():
                if carte[a,b] == cell[i]:#on sauvegarde le type de la cellule traitée
                    cellule = i
                contexte[i] = np.sum(entourage==cell[i])#on compte le nombre d'occurences de chaque type dans l'entourage de la cellule
            
            contexte[cellule] -= 1 #on enlève un au type de la cellule à traiter parce qu'elle a été comptée dans son propre entourage
 
            carte[a,b] = règle(cellule,contexte)#on applique la règle en fonction du type de la cellule et de son entourage
 
def île(taille, début):
    mid = int(taille/2)#on calcule le milieu de l'île (pour aller plus vite)
 
    for a in range(taille):#pour chaque "tranche" de la portion de carte:
        eq = math.sqrt((a-mid)**2)#on calcule la distance par rapport à la moitié
        inter = math.sqrt((mid**2)-(eq**2))#simple théorème de pythagore (on trace le cercle grâce à un triange rectangle dont l'hypothènuse est égale au rayon du cercle)
        for b in range(taille):#et pour chaque "case" dans cette tranche:
            if (b > mid-inter) and (b < mid+inter):#si la case est comprise dans le cercle:
                carte[début+a,début+b] = cell["terre"] #on la "colorie"
 
def règle(cellule,context):
    if (cellule == "habitation") and ((context["source_eau"] == 0) or not (context["habitation"] < 15)):
        return(cell["terre"])
    elif (cellule == "terre") and (context["habitation"] >= 1) and (rd.random() < 0.1):
        return(cell["habitation"])
    else:
        return(cell[cellule])
 
 
 
#====================execution du code============
 
#génération de l'île
taille_ile = 70
startpoint = (côté-taille_ile)//2
île(taille_ile,startpoint)
#création des ressources
gen_cell = {#définition des probabilitées
"source_eau": 0.005,
#"source_nourriture": 0.05,
"habitation": 0.01
}
for i in range(côté):
    for j in range(côté):
        if (np.sum(carte[i:i+4,j:j+4] == cell["terre"]) == 16) and (rd.random() < gen_cell["source_eau"]):
            carte[i:i+4,j:j+4] = np.array([cell["source_eau"] for z in range(16)], dtype=np.float64).reshape((4,4))
        if (carte[i,j] == cell["terre"]) and (rd.random() < gen_cell["habitation"]):
            carte[i,j] = cell["habitation"]
 
def afficher():
  rendu = gist_rainbow(carte)
  plt.imshow(rendu)
  plt.show()

def sauvegarder(nom):
  rendu = gist_rainbow(carte)
  plt.imsave(nom,rendu)

nb_digits = 3
def abs_frame(nb):
    a = len(str(nb))
    b = nb_digits-a
    c = ("0"*b)+str(nb)
    return(c)

for i in range(100):
    nom = f"frame {abs_frame(i+1)}.png"
    sauvegarder(nom)
    génération()