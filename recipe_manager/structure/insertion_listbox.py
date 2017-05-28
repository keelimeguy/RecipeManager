try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from drag_drop_listbox import DragDropListbox
from color_scheme import *

class InsertionListbox(DragDropListbox):
    def __init__(self, master, fix_first=False, reorder=True, **kw):
        self.master = Frame(master, bg=BG_COLOR)
        self.listbox_unused = Listbox(self.master)
        self.listbox_unused.grid(row = 1, column = 0, rowspan=6, sticky=EW)

        self.add_button = Button(self.master, text=">", command=self.add, highlightbackground=BG_COLOR)
        self.add_button.grid(row=3, column=1, columnspan=2, sticky=NS)
        self.remove_button = Button(self.master, text="<", command=self.remove, highlightbackground=BG_COLOR)
        self.remove_button.grid(row=4, column=1, columnspan=2, sticky=NS)

        if reorder:
            DragDropListbox.__init__(self, self.master, fix_first, **kw)
        else:
            Listbox.__init__(self, self.master, kw)
        Listbox.grid(self, row = 1, column = 3, rowspan=6, sticky=EW)

    def grid(self, **kw):
        self.master.grid(kw)

    def pack(self, **kw):
        self.master.pack(kw)

    def add(self):
        for i in self.listbox_unused.curselection():
            self.insert(END, self.listbox_unused.get(i))
            self.listbox_unused.delete(i)

    def remove(self):
        for i in self.curselection():
            if i is not 0:
                self.listbox_unused.insert(END, self.get(i))
                self.delete(i)

    def size_unused(self):
        return self.listbox_unused.size()

    def get_unused(self, first, last=None):
        return self.listbox_unused.get(first, last)

    def insert_unused(self, index, *elements):
        return self.listbox_unused.insert(index, *elements)
