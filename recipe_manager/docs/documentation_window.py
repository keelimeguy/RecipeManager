try:
    from Tkinter import *
except ImportError:
    from tkinter import *

import os
from ..structure.color_scheme import *

class DocumentationWindow(object):

    def __init__(self, root, manager):
        self.options = [("Recipes", "recipes.txt"), ("Lists", "lists.txt"),
                        ("Searching", "search.txt"), ("Databases", "databases.txt")]

        self.root = root
        self.manager = manager
        self.master = Toplevel(root)
        self.master.title("Documentation")
        self.master.resizable(False, False)
        self.master.config(bg=BG_COLOR)

        self.canvas = Canvas(self.master, borderwidth=0, width=640, height=560, bg=BG_COLOR)
        wrap_width = 640
        self.vsb = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.master, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.canvas_width = self.canvas.winfo_reqwidth() - 4
        self.canvas_height = self.canvas.winfo_reqheight() - 4

        self.frame = Frame(self.canvas, bg=BG_COLOR, width=self.canvas_width, height=self.canvas_height)
        self.frame_id = self.canvas.create_window((4,4), window=self.frame, anchor=N+W,
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        self.options_listbox = Listbox(self.master)
        self.options_listbox.bind('<<ListboxSelect>>', self.on_select)

        for option in self.options:
            self.options_listbox.insert(END, option[0])

        self.options_listbox.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, sticky=NSEW)
        self.canvas.grid(row = 0, column = 2, columnspan = 10, sticky=NSEW)
        self.vsb.grid(row = 0, column = 12, sticky=NS)
        self.hsb.grid(row = 1, column = 2, columnspan = 11, sticky=EW)

        self.description_frame = Frame(self.frame, bg=BG_COLOR)
        self.description_frame.grid(row = 0, column = 0, sticky=NSEW)

        self.doc_title = Label(self.description_frame, text="<Title>", font=("Times", 12, "bold"), bg=BG_COLOR)
        self.doc_title.grid(row = 0, column = 0, columnspan = 2, padx = 2, pady = 2)

        self.doc_desc = Label(self.description_frame, text="<Description>", justify=LEFT, wraplength=wrap_width, bg=BG_COLOR)
        self.doc_desc.grid(row = 1, column = 0, columnspan = 2, sticky=W)
        self.setup(self.options[0])

        self.master.focus()

    def on_select(self, event):
        entry = self.options[int(self.options_listbox.curselection()[0])]
        self.setup(entry)

    def _bound_to_mousewheel(self, event):
        self.master.bind_all("<MouseWheel>", self.on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.master.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        if self.manager.is_wind:
            self.canvas.yview_scroll(-1*(event.delta/120), "units")
        else:
            self.canvas.yview_scroll(-1*(event.delta), "units")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def setup(self, option):
        self.doc_title.config(text=option[0])
        data = "ERROR: Docs for {} not found.".format(option[0])

        if __debug__:
            current_dir = os.getcwd()
            docs_dir = os.path.join(os.path.join(current_dir, "recipe_manager"), "docs")
            if os.path.isfile(os.path.join(docs_dir, option[1])):
                with open(os.path.join(docs_dir, option[1]), 'r') as myfile:
                    data = myfile.read()
        else:
            path = os.path.join(sys._MEIPASS, "docs")
            if os.path.isfile(os.path.join(path, option[1])):
                with open(os.path.join(path, option[1]), 'r') as myfile:
                    data = myfile.read()

        self.doc_desc.config(text=data)
