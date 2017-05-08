#!/usr/bin/env python

from Tkinter import *

from recipe_book import RecipeBook

class CreateRecipeView(Frame):
    def __init__(self, master):
        self.master = master
        master.maxsize(375,323)
        master.title("Create Recipe")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.selected = False

        self.name_label = Label(master, text="Name:").grid(row=0, column=0, columnspan=2, sticky=E)
        self.name_text = Text(master, height=1, width=32)
        self.name_text.grid(row=0, column=2, columnspan=9, sticky=NSEW)
        self.name_text.bind('<Tab>', self.on_text_tab)
        self.name_text.bind('<Return>', self.on_text_tab)

        self.desc_label = Label(master, text="Description:").grid(row=2, column=0, columnspan=2, sticky=E)
        self.desc_scrollbar = Scrollbar(master, orient=VERTICAL)
        self.desc_scrollbar.grid(row=3, column=11, columnspan=1, sticky=W)
        self.desc_text = Text(master, undo=True, height=2, width=32)
        self.desc_text.grid(row=3, column=2, columnspan=9, sticky=NSEW)
        self.desc_text.bind('<Tab>', self.on_text_tab)
        self.desc_text.config(yscrollcommand=self.desc_scrollbar.set)
        self.desc_scrollbar.config(command=self.desc_text.yview)

        self.ingr_label = Label(master, text="Ingredients:").grid(row=4, column=0, columnspan=2, sticky=E)
        self.ingr_scrollbar = Scrollbar(master, orient=VERTICAL)
        self.ingr_scrollbar.grid(row=5, column=11, columnspan=1, sticky=W)
        self.ingr_list = Listbox(master, height=4, width=32)
        self.ingr_list.grid(row=5, column=2, columnspan=9, sticky=NSEW)
        self.ingr_list.config(yscrollcommand=self.ingr_scrollbar.set)
        self.ingr_list.bind('<BackSpace>', self.rem_ingr)
        self.ingr_list.bind('<<ListboxSelect>>', self.on_select)
        self.ingr_scrollbar.config(command=self.ingr_list.yview)
        self.ingr_amount = Text(master, height=1, width=4)
        self.ingr_amount.grid(row=6, column=2, sticky=E)
        self.ingr_amount.bind('<Tab>', self.on_text_tab)
        self.ingr_amount.bind('<Return>', self.on_text_tab)
        self.ingr_unit = Text(master, height=1, width=8)
        self.ingr_unit.grid(row=6, column=3, columnspan=2, sticky=EW)
        self.ingr_unit.bind('<Tab>', self.on_text_tab)
        self.ingr_unit.bind('<Return>', self.on_text_tab)
        self.ingr_text = Text(master, height=1, width=20)
        self.ingr_text.grid(row=6, column=5, columnspan=5, sticky=EW)
        self.ingr_text.bind('<Tab>', self.on_text_tab)
        self.ingr_text.bind('<Return>', self.on_text_tab)
        self.ingr_add_button = Button(master, text="+", command=self.add_ingr).grid(row=6, column=11, sticky=EW)
        self.ingr_add_button = Button(master, text="-", command=self.rem_ingr).grid(row=6, column=12, sticky=EW)

        self.inst_label = Label(master, text="Instructions:").grid(row=7, column=0, columnspan=2, sticky=E)
        self.inst_scrollbar = Scrollbar(master, orient=VERTICAL)
        self.inst_scrollbar.grid(row=8, column=11, columnspan=1, sticky=W)
        self.inst_text = Text(master, undo=True, height=4, width=32)
        self.inst_text.grid(row=8, column=2, columnspan=9, sticky=NSEW)
        self.inst_text.config(yscrollcommand=self.inst_scrollbar.set)
        self.inst_text.bind('<Tab>', self.on_text_tab)
        self.inst_scrollbar.config(command=self.inst_text.yview)

        self.save_button = Button(master, text="Save", command=self.save_recipe)
        self.save_button.grid(row=9, column=2, columnspan=9, sticky=EW)
        self.back_button = Button(master, text="Back", command=master.quit)
        self.back_button.grid(row=9, column=11, columnspan=2, sticky=EW)

    def _focusNext(self, widget):
        '''Return the next widget in tab order'''
        widget = self.master.call('tk_focusNext', widget._w)
        if not widget: return None
        return self.nametowidget(widget.string)

    def on_text_tab(self, event):
        '''Move focus to next widget'''
        widget = event.widget
        next = self._focusNext(widget)
        next.focus()
        return "break"

    def on_select(self, event):
        if len(self.ingr_amount.get("1.0", END).strip()) == 0 and len(self.ingr_unit.get("1.0", END).strip()) == 0 and len(self.ingr_text.get("1.0", END).strip()) == 0 or self.selected:
            self.selected = True
            entry = self.ingr_list.get(self.ingr_list.curselection()[0])
            self.ingr_text.delete("1.0", END)
            self.ingr_amount.delete("1.0", END)
            self.ingr_unit.delete("1.0", END)
            self.ingr_amount.insert(END, str(entry[0]))
            self.ingr_unit.insert(END, entry[1])
            self.ingr_text.insert(END, entry[2])
        return "break"

    def add_ingr(self):
        self.selected = False
        self.ingr_amount.focus()
        try:
            amount = float(self.ingr_amount.get("1.0", END))
        except ValueError as e:
            print(e)
            self.ingr_amount.config(bg="red")
            return
        self.ingr_amount.config(bg="white")
        self.ingr_list.insert(END, (amount, self.ingr_unit.get("1.0", END), self.ingr_text.get("1.0", END)))
        self.ingr_text.delete("1.0", END)
        self.ingr_amount.delete("1.0", END)
        self.ingr_unit.delete("1.0", END)

    def rem_ingr(self, event=None):
        sel = self.ingr_list.curselection()
        for i in sel:
            self.ingr_list.delete(i)

    def save_recipe(self):
        pass


root = Tk()
my_gui = CreateRecipeView(root)
root.mainloop()
