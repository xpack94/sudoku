import Game
import random
import itertools
import Remplissage_carrés





def combinison_possible(values,default_values,conflit_actuel):


    list_de_candidats=[]
    comb=[]
    for i in range(18, len(Game.unitlist)):

        comb.append(itertools.combinations(Game.unitlist[i],r=2))

    for c in comb:
        for f in c :
            #on verifie que les cases a swaper ne sont pas des cases contenant des valeurs par defaut
            if f[0]  not in default_values and  f[1] not in default_values :
                values=Game.swap(values,f[0],f[1])
                #tester si le swap reduit les conflits
                conflits=Game.compteur_de_conflit(values)
                if  conflits<conflit_actuel :
                    #on mets le tuple qui diminue les nombre de conflits dans la liste des candidats
                    list_de_candidats.append((f,conflits))
                #on re-swap de nouveau
                values=Game.swap(values,f[0],f[1])

    if len(list_de_candidats)==0:
        #aucun swap ne permet de deminuer les conflits
        #on arrete (maximum local trouvé )
        return values

    #maintetant qu'on a la liste de tout les candidats possible
    #on choisit celui qui diminu les conflit le plus
    meilleur= min(list_de_candidats , key=lambda x:x[1])
    values=Game.swap(values,meilleur[0][0],meilleur[0][1])
    values= combinison_possible(values,default_values,meilleur[1])
    return values


def hill_climbing(values,valeur_par_defaut):


    #values,valeur_par_defaut=Remplissage_carrés.remplissage(values)
    Game.display(values)
    conflit = Game.compteur_de_conflit(values)
    print("nombre de conflit avant ",conflit)
    values=combinison_possible(values,valeur_par_defaut,conflit)
    Game.display(values)
    print("nombre de conflit apres ",Game.compteur_de_conflit(values))


