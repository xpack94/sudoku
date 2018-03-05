import Game
import random


def compteur_de_conflit(values):

    compteur=0
    for i in range(0,18):


        for j in range(0,len(Game.unitlist[i])):
            for k in range(j+1,len(Game.unitlist[i])):
                if values[Game.unitlist[i][j]] == values[Game.unitlist[i][k]] :
                    compteur+=1

    return compteur



def hill_climbing(values):



    #tout les nombre qui sont permis par carré
    nombre_permis=[1,2,3,4,5,6,7,8,9]
    nombre_permis_par_carre = nombre_permis.copy()

    #garder trace des nombre par defaut qui sont deja placé dans des cases
    #avec un dictionaire contenant tout les nom des case ayant une valeur par defaut
    valeur_par_defaut = {k: values[k]  for i in range(18,len(Game.unitlist)) for k in Game.unitlist[i]  if len(values[k]) == 1}



    for i in range(18,len(Game.unitlist)):
        inchangable_numbers = [values[k] for k in Game.unitlist[i] if len(values[k]) == 1]

        for l in inchangable_numbers:
            # suppresion de tout les nombre qui sont deja remplis dans des cases d'un carré
            nombre_permis_par_carre.remove(int(l))

        for u in Game.unitlist[i]:
            if len(values[u]) > 1:
                    #generation d'un nombre au hasard
                    r = random.randint(0, len(nombre_permis_par_carre)-1)
                    values[u]=str(nombre_permis_par_carre[r])
                    nombre_permis_par_carre.pop(r)

        nombre_permis_par_carre = nombre_permis.copy()





    Game.display(values)
    print(compteur_de_conflit(values))
    print(valeur_par_defaut)