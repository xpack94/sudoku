import Game
import random



''''fonction qui remplis tout les cases avec des chiffre au hasard en tenant compte des
    contraintes dans le meme carré'''

def remplissage(values):



    #tout les nombre qui sont permis par carré
    nombre_permis=[1,2,3,4,5,6,7,8,9]
    nombre_permis_par_carre = nombre_permis.copy()

    #garder trace des nombres par defaut qui sont deja placé dans des cases
    #avec un dictionaire contenant tout les nom des cases ayant une valeur par defaut
    valeur_par_defaut = {k: values[k]  for i in range(18,len(Game.unitlist)) for k in Game.unitlist[i]  if len(values[k]) == 1}


    #les carrés commence a l'indice 18
    for i in range(18,len(Game.unitlist)):
        inchangable_numbers = [values[k] for k in Game.unitlist[i] if len(values[k]) == 1]

        for l in inchangable_numbers:
            # suppresion de tout les nombre qui sont deja remplis dans des cases d'un carré
            #pour ne pas generer le meme nombre dans un meme carré
            nombre_permis_par_carre.remove(int(l))

        for u in Game.unitlist[i]:
            if len(values[u]) > 1:
                    #generation d'un nombre au hasard
                    r = random.randint(0, len(nombre_permis_par_carre)-1)
                    values[u]=str(nombre_permis_par_carre[r])
                    nombre_permis_par_carre.pop(r)

        nombre_permis_par_carre = nombre_permis.copy()


    ''''jusque ici tout les carrés sont remplis avec des valeur tel que
        aucune il y'a pas de conflit dans le meme carré
        mais il y'a des conflits dans les lignes et colonnes et donc
        on appelle l'algorithme de hill climbing pour essayer de minimiser le nombre
        de conflits total le plus que possible'''''

    return values,valeur_par_defaut

