try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from structure.color_scheme import *

class SearchWindow(Frame):
    def __init__(self, master, root, type=None, objects="objects"):
        Frame.__init__(self, master)
        self.root = root
        self.master.title("Search{}".format(" "+type if type else ""))
        self.master.resizable(False, False)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grab_set()
        self.master.config(bg=BG_COLOR)

        self.final = None

        self.name_label = Label(self.master, text="Find {} with..".format(objects), bg=BG_COLOR).grid(row=0, column=0, columnspan=2, sticky=E)

        self.all_label = Label(self.master, text="All of these terms:", bg=BG_COLOR).grid(row=1, column=0, columnspan=2, sticky=E)
        self.all_text = Text(self.master, undo=True, height=1, width=32)
        self.all_text.grid(row=1, column=3, columnspan=3, sticky=EW)
        self.all_text.bind('<Tab>', self.on_text_tab)
        self.all_text.bind('<Return>', self.search)

        self.any_label = Label(self.master, text="Any of these terms:", bg=BG_COLOR).grid(row=2, column=0, columnspan=2, sticky=E)
        self.any_text = Text(self.master, undo=True, height=1, width=32)
        self.any_text.grid(row=2, column=3, columnspan=3, sticky=EW)
        self.any_text.bind('<Tab>', self.on_text_tab)
        self.any_text.bind('<Return>', self.search)

        self.none_label = Label(self.master, text="None of these terms:", bg=BG_COLOR).grid(row=3, column=0, columnspan=2, sticky=E)
        self.none_text = Text(self.master, undo=True, height=1, width=32)
        self.none_text.grid(row=3, column=3, columnspan=3, sticky=EW)
        self.none_text.bind('<Tab>', self.on_text_tab)
        self.none_text.bind('<Return>', self.search)

        Label(self.master, text="", bg=BG_COLOR).grid(row=4, column=6)

        self.save_button = Button(self.master, text="Search", command=self.search)
        self.save_button.grid(row=5, column=4, sticky=EW)

        self.save_button = Button(self.master, text="Cancel", command=self.master.destroy)
        self.save_button.grid(row=5, column=5, sticky=EW)

    def _focusNext(self, widget):
        '''Return the next widget in tab order'''
        widget = self.root.call('tk_focusNext', widget._w)
        if not widget: return None
        return self.nametowidget(widget.string)

    def on_text_tab(self, event):
        '''Move focus to next widget'''
        widget = event.widget
        next = self._focusNext(widget)
        next.focus()
        return "break"

    def search(self, event=None):
        and_terms = None
        for term in self.all_text.get("1.0", END).strip().replace(", ", " ").split(" "):
            term = term.strip() if term else None
            if term and len(term)>0:
                and_terms = ("&".join([and_terms, term]) if and_terms else term)
        for term in self.none_text.get("1.0", END).strip().replace(", ", " ").split(" "):
            term = term.strip() if term else None
            if term and len(term)>0:
                and_terms = ("&~".join([and_terms, term]) if and_terms else "~{}".format(term))
        for term in self.any_text.get("1.0", END).strip().replace(", ", " ").split(" "):
            term = term.strip() if term else None
            if term and len(term)>0:
                term = "{}&{}".format(term, and_terms) if and_terms else term
                self.final = ("|".join([self.final, term]) if self.final else term)
        if not self.final:
            self.final = and_terms if and_terms else ""
        self.master.destroy()
