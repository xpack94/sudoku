import random
import Remplissage_carrés
import Game
import itertools
import sys
import math



def probability(p):
   return p>random.uniform(0.0, 1.0)

def cooling(t):
    if t < 0.001:
        return 0
    else:
        return 0.99 * t


def trouver_candidat(temp,values, default_values,conflit_actuel):



    comb=[]
    for i in range(18, len(Game.unitlist)):

        comb.append(list(itertools.combinations(Game.unitlist[i],r=2)))

    #suppression des valeur par defaut de la liste des combinaison possible
    #car ces valeur ne peuvent pas etre changer
    for c in comb:
       l=0
       while(l <len(c)):
            if c[l][0] in default_values or c[l][1] in default_values:
                c.remove (c[l])
                l-=1

            l+=1

    comb = [x for c in comb for x in c]
    for t in range(sys.maxsize):

            if temp == 0 or conflit_actuel==0:
             return values






            rand = random.randint(0, len(comb) - 1)
            #random_enfant = randint(0,len(comb[rand])-1)
            enfant_potentiel =comb[rand]
            values=Game.swap(values,enfant_potentiel[0],enfant_potentiel[1])
            #tester si le swap reduit les conflits
            conflits=Game.compteur_de_conflit(values)
            #print("swaped ", enfant_potentiel ,"conflit ",conflits ,"conf actuel ", conflit_actuel)
            diff_conflit= float(conflit_actuel-conflits)

            if  diff_conflit>0 or probability(math.exp(diff_conflit/temp)):

                conflit_actuel=conflits
                temp = cooling(temp)


                #tester si on peut mettre le swap comme candidat
                # if  diff_conflit>0 or probability (math.exp(diff_conflit/temp)) :
                #         #values = trouver_candidat(temp, values, default_values,conflits)
                #         conflit_actuel=conflits

            else:
                values = Game.swap(values, enfant_potentiel[0], enfant_potentiel[1])




        #values = trouver_candidat(temp, values, default_values, conflit_actuel)
        #maintetant qu'on a la liste de tout les candidats possible
        #on choisit celui qui diminu les conflit le plus

    return values






def recuit_simule(values,valeur_par_defaut):
    Temperature = 3.5 #par defaut
    #values,valeur_par_defaut =Remplissage_carrés.remplissage(values)
    Game.display(values)
    conflit=Game.compteur_de_conflit(values)
    print("nombre de conflit avant ", conflit)
    values= trouver_candidat(Temperature,values,valeur_par_defaut,conflit)
    print("nombre de conflit apres ", Game.compteur_de_conflit(values))
    Game.display(values)
    return values

