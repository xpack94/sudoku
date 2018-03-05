import Game
import random
import itertools

def compteur_de_conflit(values):

    compteur=0
    for i in range(0,18):


        for j in range(0,len(Game.unitlist[i])):
            for k in range(j+1,len(Game.unitlist[i])):
                if values[Game.unitlist[i][j]] == values[Game.unitlist[i][k]] :
                    compteur+=1

    return compteur



def combinison_possible(values,default_values,conflit_actuel):


    list_de_candidats=[]
    comb=[]
    for i in range(18, len(Game.unitlist)):

        comb.append(itertools.combinations(Game.unitlist[i],r=2))

    for c in comb:
        for f in c :
            #on verifie que les cases a swaper ne sont pas des cases contenant des valeurs par defaut
            if f[0]  not in default_values and  f[1] not in default_values :
                values=swap(values,f[0],f[1])
                #tester si le swap reduit les conflits
                conflits=compteur_de_conflit(values)
                if  conflits<conflit_actuel :
                    #on mets le tuple qui diminue les nombre de conflits dans la liste des candidats
                    list_de_candidats.append((f,conflits))
                #on re-swap de nouveau
                values=swap(values,f[0],f[1])

    if len(list_de_candidats)==0:
        #aucun swap ne permet de deminuer les conflits
        #on arrete (maximum local trouvé )
        return values

    #maintetant qu'on a la liste de tout les candidats possible
    #on choisit celui qui diminu les conflit le plus
    meilleur= min(list_de_candidats , key=lambda x:x[1])
    values=swap(values,meilleur[0][0],meilleur[0][1])
    values= combinison_possible(values,default_values,meilleur[1])
    return values

#fonction qui swap deux valeurs dans deux case du meme carré
def swap(values,first,second):
    temp = values[first]
    values[first] = values[second]
    values[second] = temp
    return values

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
    conflit = compteur_de_conflit(values)
    print("nombre de conflit avant ",conflit)
    values=combinison_possible(values,valeur_par_defaut,conflit)
    Game.display(values)
    print("nombre de conflit apres ",compteur_de_conflit(values))


