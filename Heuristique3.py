import Game,Remplissage_carrés


def default_values(values):
    valeur_par_defaut = {k: values[k] for i in range(18, len(Game.unitlist)) for k in Game.unitlist[i] if
                         len(values[k]) == 1}
    return valeur_par_defaut

#supprime digit de spot qui se trouve dans values
def erase(values,spot,digit):
    if len(values[spot])==2:
        print(spot, values[spot], "........................................")
        val = values[spot]
        val=val.replace(str(digit),'')
        values = Game.assign(values, spot,val)
        return values
        #values[spot]=values[spot].replace(str(digit),'')
    else:
        values[spot]=values[spot].replace(str(digit),'')
    return values


#supprime les elements digit des cases qui le contient soit dans la ligne ou la colonne
def delete_from_row_or_column(values,liste,digit,start,end):
    erased=False
    for i in range(start,end):
        if Game.unitlist[i].count(liste[0]) == 1 and  Game.unitlist[i].count(liste[1]) == 1:
            for j in range(0,len(Game.unitlist[i])):
                if Game.unitlist[i][j] not in liste:
                    if values[Game.unitlist[i][j]].count(str(digit))==1:
                        values=erase(values,Game.unitlist[i][j],digit)
                        erased=True #on a supprimmer une valeur d'une autre case

    if erased:

        valeur_par_defaut = default_values(values)
        print("called again")
        values = hidden_singles(values, valeur_par_defaut)
        values = locked_candidates(values, valeur_par_defaut)

    return values


    return
#verifie si les elements se trouvent dans la meme ligne ou la meme colonne
def check(values,liste,digit):
    print(digit,liste)
    l=sorted(liste,key=lambda x:int(x[1]))
    offset=0
    for i in range(0,len(l)-1):
      offset+=int(l[i+1][1]) - int(l[i][1])
    if (offset==6 and len(liste)==3)or (offset==3 and len(liste)==2):
        #les elements se trouvent sur la meme colonne
        col = [x[0] for x in l]
        values = delete_from_row_or_column(values, col, digit, 0, 9)
    elif (offset == 2 and len(liste)==3) or (offset==1 and len(liste)==2):
        #les elements se trouve,t sur la meme ligne
        lgn = [x[0] for x in l]
        values=delete_from_row_or_column(values,lgn,digit,9,18)
    else:
        return values

    return values

def locked_candidates(values,valeur_par_defaut):
    counter = 0
    numbers_found = []
    l=[]
    for square in range(18, len(Game.unitlist)):
        for s in range(0, len(Game.unitlist[square])):
            if Game.unitlist[square][s] not in valeur_par_defaut:
                for digit in values[Game.unitlist[square][s]]:
                    if int(numbers_found.count(digit)) == 0:
                        co=0
                        for w in range(0,len(Game.unitlist[square])):
                            temp= ((Game.unitlist[square][w],co+1) for ext in values[Game.unitlist[square][w]] if int(ext) == int(digit))
                            for t in temp:
                                if t:
                                    l.append(t)
                                    counter += 1
                            co+=1
                        counter -= 1  # parceque on a compter le meme chiffre de la meme case deux fois
                    if 0<counter <=2:
                        #on a trouver deux ou trois valeurs pareil
                        #on check si ces valeurs sont dans la meme lignes ou la meme colonne
                        values=check(values,l,int(digit))
                    if counter != 0:
                        numbers_found.append(digit)
                    counter = 0
                    l=[]

        numbers_found = []

    return values
def hidden_singles(values,valeur_par_defaut):


    counter = 0
    numbers_found=[]
    for square in range(18,len(Game.unitlist)):
        for s in range(0,len(Game.unitlist[square])):
            if Game.unitlist[square][s] not in valeur_par_defaut:
                for digit in values[Game.unitlist[square][s]]:
                    if   int(numbers_found.count(values[Game.unitlist[square][s]]))==0:
                        for w in Game.unitlist[square]:

                            counter+= sum(1 for ext in values[w] if int(ext) == int(digit))

                        counter-=1 #parceque on a compter le meme chiffre de la meme case deux fois

                    if counter==0:
                        #element unique dans une case
                        #eliminer toutes ces apparition dans les autres case qui lui sont paires

                        values=Game.assign(values,Game.unitlist[square][s],values[Game.unitlist[square][s]])

                    if counter!=0:
                        numbers_found.append(digit)
                    counter=0

        numbers_found=[]

    return values



def heuristique3(values):
    valeur_par_defaut= default_values(values)
    values=hidden_singles(values,valeur_par_defaut)
    values=locked_candidates(values,valeur_par_defaut)
    Game.display(values)
    print((Game.compteur_de_conflit(values)))
    # values=Game.assign(values,"A8",str(5))
    # Game.display(values)