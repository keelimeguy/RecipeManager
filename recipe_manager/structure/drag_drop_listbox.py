try:
    from Tkinter import *
except ImportError:
    from tkinter import *

class DragDropListbox(Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, fix_first=False, **kw):
        kw['selectmode'] = SINGLE
        Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.fix_first = fix_first
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if self.fix_first and (i == 0 or self.curIndex == 0):
            return
        if i < self.curIndex:
            while i < self.curIndex:
                x = self.get(i)
                self.delete(i)
                i+=1
                self.insert(i, x)
            self.curIndex = i-1
        elif i > self.curIndex:
            while i > self.curIndex:
                x = self.get(i)
                self.delete(i)
                i-=1
                self.insert(i, x)
            self.curIndex = i+1
