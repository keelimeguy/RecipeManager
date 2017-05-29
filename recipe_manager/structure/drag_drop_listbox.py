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
        self.selection_clear(0, "end")
        if self.fix_first and self.curIndex == 0:
            return
        i = self.nearest(event.y)
        if self.fix_first and i == 0:
            i = 1
        if i < self.curIndex:
            while i < self.curIndex:
                x = self.get(self.curIndex)
                self.delete(self.curIndex)
                self.curIndex-=1
                self.insert(self.curIndex, x)
                self.activate(self.curIndex)
        elif i > self.curIndex:
            while i > self.curIndex:
                x = self.get(self.curIndex)
                self.delete(self.curIndex)
                self.curIndex+=1
                self.insert(self.curIndex, x)
                self.activate(self.curIndex)
        self.selection_set(self.curIndex)
