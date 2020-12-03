# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:09:29 2020

@author: jujug
"""
from math import inf as infinity
import random as rd

#on defini les valeur des joueurs
IA = 1
Adversaire = 2

#affiche le morpion en remplacant les chiffres par des signes
def Affichage(Morpion):
    for i in range(len(Morpion)):
        for j in range(len(Morpion[i])):
            if Morpion[i][j] == 1:
                print("O", '|',end=' ') 
            elif Morpion[i][j] == 2:
                print("X", '|',end=' ') 
            else:
                print(" ", '|',end=' ') 
        print()
    return Morpion

#Creation du morpion "vide" => rempli de 0
def CreationMorpion():
    tab = []
    taille = input('Quelle taille de matrice souhaitez-vous?')
    for i in range(int(taille)):
        tab2 =[]
        for j in range(int(taille)):
            tab2.append(0)
        tab.append(tab2)      
    return tab

#Trouve toutes les cases possibles => cases vides
def Possibilites(matrice):
    possibilites = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if (matrice[i][j] == 0):
                possibilites.append([i,j])
    return possibilites    


def MinMax (matrice, profondeur, joueur):

    if (joueur == IA):
        meilleur = [-1, -1, -infinity]
    else:
        meilleur = [-1, -1, +infinity]
        
    #cas ou la partie est finie   
    if (profondeur == 0 or Fin(matrice)):
        score = ScoreMinMax(matrice)
        return [-1, -1, score]
    
    #cas ou la partie n'est pas finie, on parcourt toutes les cases possibles
    for case in Possibilites(matrice):
        x, y = case[0], case[1]
        matrice[x][y] = joueur
        
        if (joueur == IA):
            score = MinMax(matrice, profondeur - 1, Adversaire)
        else:
            score = MinMax(matrice, profondeur - 1, IA)
    
        matrice[x][y] = 0
        score[0], score[1] = x, y

        if (joueur == IA):
            if score[2] > meilleur[2]:
                meilleur = score  #  fonction max_value
        else:
            if (score[2] < meilleur[2]):
                meilleur = score  # fonction min_value
    return meilleur

def Modification (matrice, x, y, joueur):
    matrice[x][y] = joueur
    return matrice
  
def TourIA(matrice):
    profondeur = len(Possibilites(matrice))
    
    if (profondeur == 0 or Fin(matrice)):
        return matrice

    # Si l'IA commence, position au hasard
    if (profondeur == 9):              
        x = rd.randint(0,2)
        y = rd.randint(0,2)  
    #sinon appel a MinMax
    else:                       
        case = MinMax(matrice, profondeur, IA)
        x, y = case[0], case[1]

    matrice = Modification(matrice, x, y, IA)
    Affichage(matrice)
    return matrice 
    
def TourAdversaire(matrice):
    #Le joueur "humain" joue

    if (Fin(matrice)):
        return matrice
    
    caseChoisie = False
    while caseChoisie == False:   
        Ligne = input('Quelle ligne voulez-vous modifier?')
        reponseLigne = int(Ligne)-1
        Colonne = input('Quelle colonne voulez-vous modifier?')
        reponseColonne = int(Colonne)-1
        if (reponseColonne<len(matrice) and reponseLigne<len(matrice)): 
            if (matrice[reponseLigne][reponseColonne]== 0):
                matrice[reponseLigne][reponseColonne] = Adversaire
                caseChoisie = True
            else:
                print('La case est déjà remplie, choississez une autre case')
                caseChoisie = False
        else:
            print("La case n'existe pas , choississez une autre case")
            caseChoisie = False
        
    return (matrice)

#Permet de savoir si la partie est finie  
def Gagnant (matrice):
    
    tailleMat = len(matrice)
    fin = False
    
    #test lignes   
    for l in matrice:
        compteurL = 0
        for c in range(len(l)-1):
            if (l[c]!=l[c+1]):
                break
            elif (l[c]==l[c+1] and l[c]!=0):
                compteurL = compteurL+1
            if (compteurL == tailleMat-1):
                fin = True
                return (fin, l[0])
            
    #test colonnes     
    for c in range(tailleMat) :
        compteurC = 0
        for l in range (tailleMat-1):
            if (matrice [l][c] != matrice[l+1][c]) :
                break
            elif (matrice [l][c] == matrice[l+1][c]and matrice [l][c]!=0) :
                compteurC = compteurC+1
            if (compteurC == tailleMat-1):
                fin = True
                return (fin,matrice[l][c] )
        
    #test diagonales 
    compteurA = 0
    for d in range (tailleMat -1):      
        if (matrice[d][d] != matrice[d+1][d+1]):
            break
        elif (matrice[d][d] == matrice[d+1][d+1] and matrice [d][d]!=0):
            compteurA = compteurA +1
        if (compteurA == tailleMat-1):
            fin = True
            return (fin, matrice[0][0])
    compteurB = 0
    for d in range(tailleMat-1): 
        if (matrice[d][tailleMat-d-1]!=matrice[d+1][tailleMat-d-2]):
            break
        elif (matrice[d][tailleMat-d-1]==matrice[d+1][tailleMat-d-2] and matrice [d][tailleMat-d-1]!=0):
            compteurB = compteurB +1
        if (compteurB == tailleMat-1):
            fin = True
            return (fin, matrice[0][tailleMat-1])
        
    #test si la matrice est pleine
    compteurN = 0
    for i in range(tailleMat):
        for j in range(tailleMat) :
            if (matrice[i][j] != 0):
                compteurN= compteurN+1
    if (compteurN == tailleMat*tailleMat and fin == False):
        fin = True
        return (fin, "nul")        
    
    #si la partie n'est pas finie
    if (fin == False):
        return (fin, -1)

#Donne le resultat de la partie
def ScoreMinMax (matrice):
    
    finJeu, gagnant = Gagnant(matrice)
    if (finJeu == True):
        if gagnant == IA:
            return  1
        elif gagnant == Adversaire:
            return  -1
        elif gagnant == "nul":
            return  0
    
def ScoreFinal (matrice):
    
    finJeu, gagnant = Gagnant(matrice)
    if (finJeu == True):
        if gagnant == Adversaire:
            print ("Le gagnant est le joueur 1 (vous)")
            return  -1
        elif gagnant == IA:
            print ("Le gagnant est le joueur 2 (IA)")
            return  1
        elif gagnant == "nul":
            print ("Match nul")
            return  0
    elif (finJeu == False):
        return  5
    
def Fin(matrice):
    finJeu, gagnant = Gagnant(matrice)
    if finJeu == True:
        return True
    else:
        return False

def Tour(matrice, joueur):
    if(joueur == IA):
        print("C'est à l'IA de jouer")
        matrice = TourIA(matrice)     

    else:
        print("C'est à vous de jouer:")
        matrice = TourAdversaire(matrice) 
        Affichage(matrice)

    
def Morpion():
    debut= ' '
    while (debut != 'oui' and debut != 'non'):
        debut = (input('Veux-tu jouer en 1er ? (oui/non):  ')).lower()
        
    Morpion=Affichage(CreationMorpion())
    
    if debut == 'oui':
        joueur = Adversaire
        joueur2 = IA
    else :
        joueur = IA
        joueur2 = Adversaire
    print (Fin(Morpion))
    while (not Fin(Morpion)):
        Tour(Morpion, joueur)
        joueur, joueur2 = joueur2, joueur
        ScoreFinal(Morpion)
        
        

Morpion()

    