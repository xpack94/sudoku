import HillClimbing
import Recuit_simulé
import sys
import Remplissage_carrés
import Heuristique2
import Heuristique1
import Heuristique3
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
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)

    # for d in values[s]:
    #     #incrementer le compteur a chaque tour de boucle
    #     #car a chaque tour on assign un chiffre a une case
    #     compteur=comptage_tentative(compteur)
    #     result,compteur=search(assign(values.copy(), s, d),compteur)
    #     if result:
    #         #le jeux a été resolu
    #         break


    #return result,compteur
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
def swap(values,first,second):
    temp = values[first]
    values[first] = values[second]
    values[second] = temp
    return values



################ System test ################

import time, random


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print
            '(%.2f seconds)\n' % t
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print(
        "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


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
    print("avant la resolution")
    display(parse_grid(grid4))

    #display(solve(grid2))

    #values,valeur_par_defaut=Remplissage_carrés.remplissage(parse_grid(grid1))
    #v=values.copy()
    #print(compteur_de_nombre(v))
    #v1=HillClimbing.hill_climbing(values,valeur_par_defaut)
    # v=Recuit_simulé.recuit_simule(v,valeur_par_defaut)
    #display(v)
    # print("conflits apres",compteur_de_conflit(v))
    #Heuristique.heuristique(v,valeur_par_defaut)
    #Heuristique2.apply_heuristique(parse_grid(grid1))
    #print(comptage)
    Heuristique3.heuristique3(parse_grid(grid4))

    #solve(parse_grid(grid2))

    ## References used:
    ## http://www.scanraid.com/BasicStrategies.htm
    ## http://www.sudokudragon.com/sudokustrategy.htm
    ## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
    ## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/