import numpy as np
import math

côté = 80 #taille de la carte

carte = np.zeros((côté,côté),dtype=np.uint8)#génération de la carte

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

types = [1,2,3,4]#liste des differents types de cellules (représentés par des chiffres)

def génération():
    for a in range(intervale,côté-intervale):
        for b in range(intervale,côté-intervale):
            entourage = carte[a+rayA:a+rayB,b+rayA:b+rayB]#on découpe du tableau entier l'entourage de notre cellule
            contexte = {}#on crée un dictionnaire qui va contenir chaque type et son nombre d'occurences

            for i in types:
                contexte[str(i)] = np.sum(entourage==i)#on compte le nombre d'occurences de chaque type dans l'entourage de la cellule
                #(ce bout de code a été totalement plagié: https://riptutorial.com/fr/python/example/29216/comptage-des-occurrences-dans-le-tableau-numpy )

            cellule = carte[a,b]#on relève le type de la cellule à traiter
            contexte[str(cellule)] -= 1 #on enlève un au type de la cellule à traiter parce qu'elle a été comptée dans son propre entourage

            carte[a,b] = règle(cellule,contexte)#on applique la règle en fonction du type de la cellule et de son entourage

def île(taille):
    base = np.zeros((taille,taille),dtype=np.uint8)#on crée une portion de carte qui contiendra l'île
    mid = int(taille/2)#on calcule le milieu de l'île (pour aller plus vite)

    for a in range(taille):#pour chaque "tranche" de la portion de carte:
        eq = math.sqrt((mid-i)**2)#on calcule la distance euclidienne avec la moitié
        inter = math.sqrt((mid**2)-(eq**2))#simple théorème de pythagore (on trace le cercle grâce à un triange rectangle dont l'hypothènuse est égale au rayon du cercle)
        for b in range(taille):#et pour chaque "case" dans cette tranche:
            if (b > mid-inter) and (b < mid+inter):#si la case est comprise dans le cercle:
                carte[a,b] == 1#on la "colorie"
    return(carte)

def règle(cell,context):
    pass