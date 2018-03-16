import Game,Remplissage_carrés



def hidden_singles(values):
    counter = 0
    numbers_found=[]
    for square in range(18,len(Game.unitlist)):
        for s in range(0,len(Game.unitlist[square])):
            for digit in values[Game.unitlist[square][s]]:
                if   int(numbers_found.count(values[Game.unitlist[square][s]]))==0:
                    for w in Game.unitlist[square]:
                        if values[w] ==digit:
                            counter+=1
                    counter-=1 #parceque on a compter le meme chiffre de la meme case deux fois
                if counter==0:
                    #element unique dans une case
                    #eliminer toutes ces apparition dans les autres case qui lui sont paires
                    values=Game.assign(values,Game.unitlist[square][s],values[Game.unitlist[square][s]])
                    print("found",Game.unitlist[square][s])
                if counter!=0:
                    numbers_found.append(digit)
                counter=0

        numbers_found=[]

    return values



def heuristique3(values):
    values=hidden_singles(values)
    Game.display(values)