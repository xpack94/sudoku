
import HillClimbing
import Recuit_simulé
import sys
import Remplissage_carrés
import Heuristique2
import Heuristique1
import Heuristique2
## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}



def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)
comptage = 0
noeud_explores=0
################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


################ Constraint Propagation ################


#assigne une valeur d a une case
#elimine cette valeur du square de cette case
# def assign_square(values, s, d):
#
#     square = {j: values[s] for j in units[s][-1]}
#     eliminate_from_square(values,square,s,d)
#     values[s]=d
#     return values
#
#
# #elimine la valeur d de toutes les cases de square
# def eliminate_from_square(values,square,s,d):
#     print(square,s,d)
#     for i in square:
#         if d in values[i]:
#             values[i]=values[i].replace(d,'')




def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""

    global comptage
    comptage+=1
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False





def eliminate(values, s, d):

    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, '')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    print(values)
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        p=[''.join(values[r + c].center(width) + ('|' if c in '36' else '')) for c in cols]
        for pl in p:
            print(pl,end='')
        print()
        if r in 'CF': print(line)
    print()


################ Search ################

def solve(grid): return search(parse_grid(grid))


def search(values):
    result=False
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)


    return some(search(assign(values.copy(), s, d))
                for d in values[s] )




################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


# def from_file(filename, sep='\n'):
#     "Parse a file into a list of strings, separated by sep."
#     return file(filename).read().strip().split(sep)
#

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq


def compteur_de_conflit(values):

    compteur=0
    for i in range(0,18):


        for j in range(0,len(unitlist[i])):
            for k in range(j+1,len(unitlist[i])):
                if values[unitlist[i][j]] == values[unitlist[i][k]] :
                    compteur+=1

    return compteur


def score(values):

    return sum([-1 for u in range(0,18)  for l in unitlist[u] if len(values[l]) ==1])

#fonction qui swap deux valeurs dans deux case du meme carré
#si l'argument increment est a inc alors on increment le nombre de noeuds total visité
#si il est a dec alors on decremente
def swap(values,first,second,increment=False):

    if increment == "inc":
        increment_nodes()
    elif increment=="dec":
        decrement_nodes()
    temp = values[first]
    values[first] = values[second]
    values[second] = temp
    return values

def decrement_nodes():
    global noeud_explores
    noeud_explores=noeud_explores-1
    return noeud_explores

def increment_nodes():
    global noeud_explores
    noeud_explores=noeud_explores+1
    return noeud_explores

def renitialize():
    global comptage
    comptage=0

def renitialize_nodes():
    global noeud_explores
    noeud_explores=0
    return noeud_explores

################ System test ################

import time, random


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    results_by_algorithm=[]

    def time_solve(grid):
        values, valeur_par_defaut = Remplissage_carrés.remplissage(parse_grid(grid))
        #faire des copy et utiliser chaque copie dans un algorithme
        v1 = values.copy()
        v2 = values.copy()
        v3 = values.copy()
        global comptage,noeud_explores
        start_algorithms=time.clock()
        start = time.clock()
        brute_force = solve(grid)
        t = time.clock() - start
        results_by_algorithm.append(("brute_force",t,compteur_de_conflit(brute_force),comptage))
        start = time.clock()
        hill,nodes = HillClimbing.hill_climbing(v1,valeur_par_defaut)
        t = time.clock() - start
        results_by_algorithm.append(("hill_climbing", t, compteur_de_conflit(hill),nodes))
        #v=values.copy()
        start = time.clock()
        h1,nodes_explored = Heuristique1.heuristique(v2, valeur_par_defaut)
        t = time.clock() - start
        results_by_algorithm.append(("heuristique1", t, compteur_de_conflit(hill), nodes_explored))
        #v = values.copy()
        start = time.clock()
        recuit,nodes = Recuit_simulé.recuit_simule(v3, valeur_par_defaut)
        t = time.clock() - start
        results_by_algorithm.append(("recuit_simule", t, compteur_de_conflit(recuit),nodes))
        #v = values.copy()
        renitialize()
        start = time.clock()
        h3 = Heuristique2.heuristique2(parse_grid(grid))
        t = time.clock() - start
        results_by_algorithm.append(("heuristique2", t, compteur_de_conflit(h3),comptage))
        global_time=time.clock()-start_algorithms
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print
            '(%.2f seconds)\n' % t
        return (t, solved(values),results_by_algorithm,global_time)



    times, results,algo ,global_time= zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        # print(
        # "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
        #     sum(results), N, name, sum(times) / N, N / sum(times), max(times)))

        brute_force_t=0
        hill_climbing_t=0
        h1_t,h3_t,recuit_t=0,0,0
        brute_force_c,hill_c,h1_c,h3_c,recuit_c=0,0,0,0,0
        brute_count,hill_count,h1_count,recuit_count,h3_count=0,0,0,0,0
        brute_force_comp,hill_comp,h1_comp,h3_comp,recuit_comp=0,0,0,0,0
        #faire les statistiques

        for c in results_by_algorithm:
                if c[0]=="brute_force":
                 brute_force_t+=c[1]
                 brute_force_c+=c[2]
                 brute_count+=1
                 brute_force_comp+=c[3]
                elif c[0]=="hill_climbing":
                    hill_climbing_t+=c[1]
                    if c[2]==0:
                        hill_count+=1
                    hill_c+=c[2]
                    hill_comp+=c[3]
                elif c[0]=="heuristique1":
                    h1_t+=c[1]
                    if c[2]==0:
                        h1_count+=1
                    h1_c+=c[2]
                    h1_comp+=c[3]
                elif c[0]=="recuit_simule":
                    recuit_t+=c[1]
                    if c[2]==0:
                        recuit_count+=1
                    recuit_c+=c[2]
                    recuit_comp+=c[3]
                else:
                    h3_t+=c[1]
                    if c[2]==0:
                        h3_count += 1
                    h3_c+=c[2]
                    h3_comp+=c[3]

        print("brute force solved", brute_count, "of", N, "avreage time", brute_force_t / N,"secs","avreage conflicts",brute_force_c,
              "avreage explored nodes",brute_force_comp/N)
        print("hill climbing solved", hill_count , "of", N, "avreage time", hill_climbing_t / N,"secs",
                      "avreage conflitcs", hill_c / N,"avreage explored nodes",hill_comp/N)
        print("heuristique1 solved", h1_count , "of", N, "avreage time", h1_t / N,"secs", "avreage conflitcs",
                      h1_c / N,"avreage explored nodes",h1_comp/N)
        print("recuit simule solved", recuit_count, "of", N, "avreage time", recuit_t / N,"secs",
                      "avreage conflits", recuit_c / N,"avreage explored Nodes",recuit_comp/N)
        print("heuristique2 solved", h3_count, "of", N, "avreage time", h3_t / N, "secs","avreage conflitcs",
                      h3_c / N,"avreage explored nodes",h3_comp/N)

        print("global time taken  ",sum(global_time),"secs","avreage time taken",sum(global_time)/N,"secs")




def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."

    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    return random_puzzle(N)  ## Give up and make a new puzzle


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)

if __name__ == '__main__':
    test()
    # solve_all(from_file("easy50.txt", '========'), "easy", None)
    # solve_all(from_file("top95.txt"), "hard", None)
    # solve_all(from_file("hardest.txt"), "hardest", None)
    # solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    grid1 = '200060000007004086000001300000000040090000000480000710900078000000050002020600501'
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    grid3= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    grid4='406010000020000100500207000600001800000030509080000300030060210000000050000350408'
    grid5='039010000000073080708000105005000008001900000360000000024000009000080320000001800'
    grid6="900250000030649000000003020000000800500070410691020000008100000040000070075000080"
    #print("avant la resolution")
    #display(parse_grid(grid1))
    solve_all(from_file("100config.txt"),"easy",None)
    #values,valeur_par_defaut=Remplissage_carrés.remplissage(parse_grid(grid3))
    #v=values.copy()
    #print(compteur_de_nombre(v))
    # renitialize()
    # v1,nodeuds=HillClimbing.hill_climbing(values,valeur_par_defaut)
    # print(nodeuds)
    # v2,nodeuds=Heuristique1.heuristique(values,valeur_par_defaut)
    # display(v1)
    #print(nodeuds)
    #v2, nodeuds = HillClimbing.hill_climbing(v, valeur_par_defaut)
    #print(nodeuds)
    # print(comptage)
    # v=Recuit_simulé.recuit_simule(v,valeur_par_defaut)
    #display(v)
    # print("conflits apres",compteur_de_conflit(v))
    #Heuristique.heuristique(v,valeur_par_defaut)
    #Heuristique2.apply_heuristique(parse_grid(grid1))
    #print(comptage)

    #Heuristique3.heuristique3(parse_grid("039010000000073080708000105005000008001900000360000000024000009000080320000001800"))
    #display(solve(grid6))

    ## References used:
    ## http://www.scanraid.com/BasicStrategies.htm
    ## http://www.sudokudragon.com/sudokustrategy.htm
    ## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
    ## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/