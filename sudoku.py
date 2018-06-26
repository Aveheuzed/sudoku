#!/usr/bin/env python3
from matrix import Matrix
from itertools import chain, cycle
import copy


class Sudoku(Matrix):

    # 9 squares, 9 rows, 9 columns
    groups = [{(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)},
    {(3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2)},
    {(6, 0), (7, 0), (8, 0), (6, 1), (7, 1), (8, 1), (6, 2), (7, 2), (8, 2)},
    {(0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4), (0, 5), (1, 5), (2, 5)},
    {(3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5)},
    {(6, 3), (7, 3), (8, 3), (6, 4), (7, 4), (8, 4), (6, 5), (7, 5), (8, 5)},
    {(0, 6), (1, 6), (2, 6), (0, 7), (1, 7), (2, 7), (0, 8), (1, 8), (2, 8)},
    {(3, 6), (4, 6), (5, 6), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8), (5, 8)},
    {(6, 6), (7, 6), (8, 6), (6, 7), (7, 7), (8, 7), (6, 8), (7, 8), (8, 8)},

    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)},
    {(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)},
    {(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2)},
    {(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3)},
    {(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4)},
    {(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5)},
    {(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6)},
    {(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7)},
    {(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)},

    {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)},
    {(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)},
    {(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)},
    {(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)},
    {(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8)},
    {(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)},
    {(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8)},
    {(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)},
    {(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)}]

    def __init__(self, *args):
        super().__init__(9,9, *args)
        self.import_groups(__class__.groups)
        self._hiter = cycle(((x,y,l) for l in range(2,10) for x in range(9) for y in range(9)))
        # iterator for self.hypothesis

    solvers = property(lambda self:(self.try_fill, self.try_place, self.try_guess))
    finished = property(lambda self:all(len(cell)==1 for cell in self))
    error = property(lambda self:any(not len(cell) for cell in self))

    def __str__(self):
        rep = str()
        for row in self.values :
            for val in row :
                if len(val) > 1 :
                    rep += "-"
                elif len(val) == 1 :
                    rep += str(list(val)[0])
                else :
                    rep += "@"
            rep += "\n"
        return rep

    @staticmethod
    def extract_fixed_numbers(group):
        return filter(lambda x:len(x)==1, group)

    # solvers

    def try_fill(matrix, group) :
        """Supprime des possibilités de chaque case du groupe,
        en s'appuyant sur les cases déjà fixées"""
        for (x,y) in matrix.getgroup(group).keys():
            if len(matrix[x,y]) == 1 :
                continue
            gr = matrix.getgroup(group)
            del gr[x,y]
            for fn in matrix.extract_fixed_numbers(gr.values()) :
                matrix[x,y] -= fn
            if not len(matrix[x,y]) :
                raise RuntimeError

    def try_place(matrix, group):
        """Pour chaque chiffre qui reste à fixer dans le groupe, compte le nombre de
        cases candidates. Si une seule est trouvée, on peut fixer sa valeur."""
        to_place = set(range(1,10))
        for discard in matrix.extract_fixed_numbers(matrix.getgroup(group).values()):
            to_place -= discard
        for val in to_place :
            possible = [cell for cell,possible in matrix.getgroup(group).items() if val in possible]
            if len(possible) == 1 :
                matrix[possible[0]] = {val}


    def try_guess(matrix, group):
        """Si n nombres se retrouvent tous uniquement dans n cases, alors aucune autre
        possibilité pour ces cases"""
        grup  = matrix.getgroup(group)
        n_cell = {n:tuple(cell for cell, val in grup.items() if n in val) for n in range(1,10)} # number : cell that can carry it
        freqx = {freq:{n for n in n_cell.keys() if len(n_cell[n])==freq} for freq in range(1,10)} # frequency : number
        freqx = {key: value for key, value in freqx.items() if len(value)==key} # we look for numbers that are as numerous as the cells they may be in,
        for freq, numbers in freqx.items():
            cells = {n_cell[n] for n in numbers}
            if len(cells) == 1 : # that share all their cells,
                cells = list(cells)[0]
                for c in cells :
                    matrix[c] = numbers.copy()

    def hypothesis(matrix):
        """Try to make an hypothesis about a value in the sudoku.
        After solving, if it leads to impossible, then this hypothesis is wrong ;
        else, it's true, and self is updated"""
        if matrix.finished :
            return
        for x,y,l in matrix._hiter :
            if len(matrix[x,y]) == l :
                break

        values = matrix[x,y]
        cmatrix = Sudoku(*copy.deepcopy(matrix.values))
        cmatrix[x,y] = {list(values)[0]}
        tested = cmatrix[x,y]
        solve(cmatrix)
        if cmatrix.error :
            matrix[x,y] = values - tested
        elif cmatrix.finished :
            matrix[x,y] = cmatrix[x,y]

def fetch_from_stdin(grid):
    for r in range(9):
        row = list()
        for char in next(matval) :
            if char == "-" :
                row.append(set(range(1,10)))
            else :
                row.append({int(char)})
        grid.setrow(r,row)
    return grid

def solve(grid) :
    sum_len = sum(len(x) for x in grid)
    prev_sum_len = 9**3
    while not grid.finished or grid.error :
        while prev_sum_len > sum_len :
            for gr in range(len(grid.groups)) :
                for func in grid.solvers :
                    func(gr)
            sum_len, prev_sum_len = sum(len(x) for x in grid), sum_len
            if sum_len == 9**2 :
                break
        grid.hypothesis()

if __name__ == "__main__" :
    grid = Sudoku(dict(default=set()))
    matval = iter("""-5-81--7-
--8--3---
--1-4----
9--7--2--
43-----89
--6--2--1
----2-3--
---3--6--
-4--78-9-""".split("\n"))

    grid = fetch_from_stdin(grid)
    print(grid,end="\n\n")
    solve(grid)
    print(grid,end="\n\n")
