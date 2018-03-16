import Game
import Remplissage_carrés, Recuit_simulé
def apply_heuristique(values):
    #generer 50 sudoku candidats et appliqué le recuit simulé pour chaqu'un
    #prendre celui avec le moins de conflits
    conflits_actuels=1000 # un nombre maximal de conflit qu'on essaye de minimiser
    v=values.copy()
    for i in range(0,5):
        values1,valeur_par_defaut=Remplissage_carrés.remplissage(v)
        values1=Recuit_simulé.recuit_simule(values1,valeur_par_defaut)
        conflits= Game.compteur_de_conflit(values1)
        if conflits<conflits_actuels:
            conflits_actuels=conflits
            print("conflits act",conflits_actuels)
        if conflits_actuels==0:
            return values1
        v=values.copy()

    return values1
def heuristique1(values):
   values=apply_heuristique(values)
   print("le nombre de conflit apres",Game.compteur_de_conflit(values))
   Game.display(values)