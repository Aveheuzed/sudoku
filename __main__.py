#!/usr/bin/env python3
import tkinter as tk
import string
from itertools import chain

from sudoku import Sudoku, solve as compute


"""GUI layer for sudoku.py"""


class SudokuLayer(tk.Widget):

    def __init__(self, master, sudoku):
        self.master = master
        self.sudoku = sudoku
        self.swidgets = dict()
        prv = None
        for x in range(11):
            if x in (3,7) :
                continue
            for y in range(11):
                if y in (3,7) :
                    continue
                e = tk.Entry(self.master,width=2, borderwidth=0)
                e.grid(row=x,column=y)
                self.swidgets[(x,y)] = e
                if prv is not None :
                    vcmd = (self.master.register(self._vcmd_factory(prv, e)), "%S")
                    prv.configure(validate="key", validatecommand=vcmd)
                prv = e

        self.master.grid_rowconfigure(3,weight=1, minsize=10)
        self.master.grid_rowconfigure(7,weight=1, minsize=10)
        self.master.grid_columnconfigure(3,weight=1, minsize=10)
        self.master.grid_columnconfigure(7,weight=1, minsize=10)


        self.mainbutton = tk.Button(self.master, text="go !", command=self.solve)
        self.mainbutton.grid(row=11, column=5, columnspan=2)

        self.swidgets = {self._get_sudoku_coords(x,y):w for (x,y),w in self.swidgets.items()}

    @staticmethod
    def _vcmd_factory(owner, jumpto):
        # owner being bound
        # jumps to widget if char convenient
        def f(text):
            owner.delete("0", "end")
            if text in string.digits[1:] :
                jumpto.focus()
                return True
            elif text in string.whitespace :
                jumpto.focus()
            else :
                owner.bell()    
            return False
        return f

    @staticmethod
    def _get_sudoku_coords(x,y):
        if x >=7 :
            x -= 2
        elif x >= 3 :
            x -= 1
        if y >=7 :
            y -= 2
        elif y >= 3 :
            y -= 1
        return (x,y)
    
    def solve(self):
        for x in range(9):
            for y in range(9):
                val = self.swidgets[(x,y)].get().strip()
                if val :
                    self.sudoku[x,y] = {int(val)}
                    self.swidgets[(x,y)]["bg"] = "light grey"
                else :
                    self.sudoku[x,y] = set(range(1,10))

        print(self.sudoku)
        #### there it is !!!!     ###
        compute(self.sudoku)

        for x in range(9):
            for y in range(9):
                val = str(list(self.sudoku[(x,y)])[0])
                self.swidgets[(x,y)].delete(0,"end")
                self.swidgets[(x,y)].insert(0,val)
            


if __name__ == "__main__" :
    main = tk.Tk()
    main.resizable(False,False)
    s = Sudoku(dict(default=None))
    sw = SudokuLayer(main, s)
