#!/usr/bin/env python3

class Matrix :

    def __init__(self, x, y, *args):
        """args may be :
- a dict of the form : {(x,y) : value} with x,y integers
It may contain a 'default' key.
- y iterables of length x"""
        self.width = x
        self.height = y
        assert len(args) in (1,y)
        self.groups = list()
        if len(args) == y :
            self.values = [list(arg) for arg in args]
        elif len(args) == 1 and isinstance(args[0], dict):
            args = args[0]
            self.values = [[args.get("default"),]*x for _ in range(y)]
            for k,v in args.items() :
                if k == "default" :
                    continue
                self.values[k[1]][k[0]] = v

    def makegroup(self, *cells):
        """Defines a group, and returns its identifier (small integer)
This group can be used later as an alias in __get|setitem__"""
        self.groups.append(set(cells))
        return len(self.groups) - 1

    def import_groups(self, groups):
        self.groups = groups

    def export_groups(self):
        return self.groups

    def __getitem__(self, xy):
        """gives access to A SINGLE cell"""
        if isinstance(xy, slice) :
            return self.values[xy.stop][xy.start]
        else : # then, it's a tuple
            x,y = xy
            return self.values[y][x]

    def __setitem__(self, xy, value):
        if isinstance(xy, slice) :
            self.values[x.stop][x.start] = value
        else : # then, it's a tuple
            x,y = xy
            self.values[y][x] = value

    def getrow(self, row):
        return self.values[row]

    def setrow(self, row, val):
        self.values[row] = val

    def getcol(self, col):
        return [row[col] for row in self.values]

    def setcol(self, col, val):
        for row, v in zip(self.value,col) :
            row[col] = v

    def getgroup(self, group):
        """Return a dict {(x,y):value}"""
        return {(x,y):self[x:y] for x,y in self.groups[group]}

    def setgroup(self, group, value):
        """Gives all the cells in <group> the value <value>"""
        for x,y in self.groups[group]:
            self[x,y] = value

    def findgroup(self, x, y) :
        """Yields the id of all the groups that contain (x,y)"""
        xy = (x,y)
        for i,group in enumerate(self.groups) :
            if xy in group :
                yield i

    def __iter__(self):
        for row in self.values :
            yield from row
