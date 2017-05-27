# -*- coding: utf-8 -*-
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

if __debug__:
    from data.recipe_book import RecipeBook
else:
    from recipe_manager.data.recipe_book import RecipeBook
from structure.modal_window import ModalWindow
from structure.drag_drop_listbox import DragDropListbox

class RecipeCreationWindow(Frame):
    def __init__(self, master, database, root, recipe=None):
        Frame.__init__(self, master)
        self.root = root
        self.master.maxsize(419,438)
        self.master.title("Create Recipe")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.selected = False
        self.database = database
        self.old_id = None
        self.final = None

        self.name_label = Label(self.master, text="Name:").grid(row=0, column=0, columnspan=2, sticky=E)
        self.name_text = Text(self.master, height=1, width=32)
        self.name_text.grid(row=0, column=2, columnspan=7, sticky=NSEW)
        self.name_text.bind('<Tab>', self.on_text_tab)
        self.name_text.bind('<Return>', self.on_text_tab)

        self.serv_label = Label(self.master, text="Serves:").grid(row=0, column=9, sticky=E)
        self.serv_text = Text(self.master, undo=True, height=1, width=4)
        self.serv_text.grid(row=0, column=11, columnspan=2, sticky=NSEW)
        self.serv_text.bind('<Tab>', self.on_text_tab)
        self.serv_text.bind('<Return>', self.on_text_tab)

        self.prep_label = Label(self.master, text="Prep Time:").grid(row=1, column=2, sticky=E)
        self.prep_text = Text(self.master, undo=True, height=1, width=4)
        self.prep_text.grid(row=1, column=3, sticky=NSEW)
        self.prep_text.bind('<Tab>', self.on_text_tab)
        self.prep_text.bind('<Return>', self.on_text_tab)
        self.prep_unit_label = Label(self.master, text="min.").grid(row=1, column=4, sticky=E)

        Label(self.master, text="").grid(row=1, column=5, sticky=EW)

        self.cook_label = Label(self.master, text="Cook Time:").grid(row=1, column=6, sticky=E)
        self.cook_text = Text(self.master, undo=True, height=1, width=4)
        self.cook_text.grid(row=1, column=7, sticky=NSEW)
        self.cook_text.bind('<Tab>', self.on_text_tab)
        self.cook_text.bind('<Return>', self.on_text_tab)
        self.cook_unit_label = Label(self.master, text="min.").grid(row=1, column=8, sticky=E)

        self.desc_label = Label(self.master, text="Description:").grid(row=5, column=0, columnspan=2, sticky=E)
        self.desc_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.desc_scrollbar.grid(row=6, column=12, columnspan=1, sticky=W)
        self.desc_text = Text(self.master, undo=True, height=2, width=32)
        self.desc_text.grid(row=6, column=2, columnspan=10, sticky=NSEW)
        self.desc_text.bind('<Tab>', self.on_text_tab)
        self.desc_text.config(yscrollcommand=self.desc_scrollbar.set)
        self.desc_scrollbar.config(command=self.desc_text.yview)

        self.ingr_label = Label(self.master, text="Ingredients:").grid(row=7, column=0, columnspan=2, sticky=E)
        self.ingr_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.ingr_scrollbar.grid(row=8, column=12, columnspan=1, sticky=W)
        self.ingr_list = DragDropListbox(self.master, fix_first=False, height=4, width=32)
        self.ingr_list.grid(row=8, column=2, columnspan=10, sticky=NSEW)
        self.ingr_list.config(yscrollcommand=self.ingr_scrollbar.set)
        self.ingr_list.bind('<BackSpace>', self.rem_ingr)
        self.ingr_list.bind('<<ListboxSelect>>', self.on_select)
        self.ingr_list.bind("<MouseWheel>", self.on_mousewheel)
        self.ingr_scrollbar.config(command=self.ingr_list.yview)
        self.ingr_amount = Text(self.master, height=1, width=4)
        self.ingr_amount.insert(END, "<#>")
        self.ingr_amount.grid(row=9, column=2, sticky=E)
        self.ingr_amount.bind('<Tab>', self.on_text_tab)
        self.ingr_amount.bind('<Return>', self.on_text_tab)
        self.ingr_amount.bind("<FocusIn>", self.on_select)
        self.ingr_unit = Text(self.master, height=1, width=8)
        self.ingr_unit.insert(END, "<unit>")
        self.ingr_unit.grid(row=9, column=3, columnspan=2, sticky=EW)
        self.ingr_unit.bind('<Tab>', self.on_text_tab)
        self.ingr_unit.bind('<Return>', self.on_text_tab)
        self.ingr_unit.bind("<FocusIn>", self.on_select)
        self.ingr_text = Text(self.master, height=1, width=20)
        self.ingr_text.insert(END, "<name>")
        self.ingr_text.grid(row=9, column=5, columnspan=5, sticky=EW)
        self.ingr_text.bind('<Tab>', self.on_text_tab)
        self.ingr_text.bind('<Return>', self.on_text_tab)
        self.ingr_text.bind("<FocusIn>", self.on_select)
        self.ingr_add_button = Button(self.master, text="+", command=self.add_ingr).grid(row=9, column=11, sticky=EW)
        self.ingr_add_button = Button(self.master, text="-", command=self.rem_ingr).grid(row=9, column=12, sticky=EW)
        self.ingr_dict = {}

        self.inst_label = Label(self.master, text="Instructions:").grid(row=10, column=0, columnspan=2, sticky=E)
        self.inst_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.inst_scrollbar.grid(row=11, column=12, columnspan=1, sticky=W)
        self.inst_text = Text(self.master, undo=True, height=4, width=32)
        self.inst_text.grid(row=11, column=2, columnspan=10, sticky=NSEW)
        self.inst_text.config(yscrollcommand=self.inst_scrollbar.set)
        self.inst_text.bind('<Tab>', self.on_text_tab)
        self.inst_scrollbar.config(command=self.inst_text.yview)

        self.note_label = Label(self.master, text="Notes:").grid(row=12, column=0, columnspan=2, sticky=E)
        self.note_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.note_scrollbar.grid(row=13, column=12, columnspan=1, sticky=W)
        self.note_text = Text(self.master, undo=True, height=3, width=32)
        self.note_text.grid(row=13, column=2, columnspan=10, sticky=NSEW)
        self.note_text.config(yscrollcommand=self.note_scrollbar.set)
        self.note_text.bind('<Tab>', self.on_text_tab)
        self.note_scrollbar.config(command=self.note_text.yview)

        Label(self.master, text="").grid(row=14, column=0)

        self.save_button = Button(self.master, text="Save", command=self.save_recipe)
        self.save_button.grid(row=15, column=2, columnspan=9, sticky=EW)
        self.back_button = Button(self.master, text="Back", command=self.master.destroy)
        self.back_button.grid(row=15, column=11, columnspan=2, sticky=EW)

        if recipe:
            self.name_text.insert(END, recipe[0][1])
            self.desc_text.insert(END, recipe[0][2])
            self.inst_text.insert(END, recipe[0][3])
            self.serv_text.insert(END, recipe[0][4])
            self.note_text.insert(END, recipe[0][5] if recipe[0][5]!=None else "")
            self.prep_text.insert(END, recipe[0][6])
            self.cook_text.insert(END, recipe[0][7])
            for i in sorted(recipe[1], key=lambda tup: tup[3]):
                self.ingr_list.insert(END, (i[0], i[1] if i[1]!=None else "", i[2]))
                self.ingr_dict[i[2]] = i[0]

    def on_mousewheel(self, event):
        self.ingr_list.yview_scroll(-1*(event.delta/120), "units") # Windows
        # self.recipe_list.yview_scroll(-1*(event.delta), "units") # OS X

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

    def on_select(self, event):
        if event.widget == self.ingr_amount or event.widget == self.ingr_unit or event.widget == self.ingr_text:
            if self.ingr_amount.get("1.0", END).strip() == "<#>":
                self.ingr_amount.delete("1.0", END)
            if self.ingr_unit.get("1.0", END).strip() == "<unit>":
                self.ingr_unit.delete("1.0", END)
            if self.ingr_text.get("1.0", END).strip() == "<name>":
                self.ingr_text.delete("1.0", END)
        elif event.widget == self.ingr_list:
            if len(self.ingr_amount.get("1.0", END).strip()) == 0 and len(self.ingr_unit.get("1.0", END).strip()) == 0 and len(self.ingr_text.get("1.0", END).strip()) == 0 and len(self.ingr_list.curselection())>0 or self.selected:
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
        self.name_text.config(bg="white")
        self.serv_text.config(bg="white")
        self.prep_text.config(bg="white")
        self.cook_text.config(bg="white")
        self.ingr_amount.config(bg="white")
        self.ingr_text.config(bg="white")
        try:
            str_amount = self.ingr_amount.get("1.0", END).strip()
            if str_amount == "-":
                str_amount = "0"
            else:
                for frac in [(.5, " 1/2"), (.25, " 1/4"), (.125, " 1/8"), (.333, " 1/3"), (.75, " 3/4"), (.0625, " 1/16"), (.666, " 2/3")]:
                    if frac[1] in str_amount:
                        str_amount = str_amount.replace(frac[1], str(frac[0])[1:]).replace(" ","")
                        break
                    if str_amount[:(len(frac[1])-1)] == frac[1].strip() and len(str_amount) == (len(frac[1])-1):
                        str_amount = str_amount.replace(frac[1].strip(), str(frac[0])).strip()
                        break
            amount = float(str_amount)
        except ValueError as e:
            self.ingr_amount.config(bg="red")
            return

        name = self.ingr_text.get("1.0", END).strip()
        if name in self.ingr_dict or len(name)==0:
            self.ingr_text.config(bg="red")
            self.ingr_text.focus()
            return

        self.ingr_dict[name] = amount
        self.ingr_list.insert(END, (amount, self.ingr_unit.get("1.0", END).strip(), name))
        self.ingr_text.delete("1.0", END)
        self.ingr_amount.delete("1.0", END)
        self.ingr_unit.delete("1.0", END)

    def rem_ingr(self, event=None):
        sel = self.ingr_list.curselection()
        for i in sel:
            del self.ingr_dict[self.ingr_list.get(i)[2]]
            self.ingr_list.delete(i)

    def save_recipe(self):
        self.name_text.config(bg="white")
        self.serv_text.config(bg="white")
        self.prep_text.config(bg="white")
        self.cook_text.config(bg="white")
        self.ingr_amount.config(bg="white")
        self.ingr_text.config(bg="white")
        if len(self.name_text.get("1.0", END).strip())==0:
            self.name_text.config(bg="red")
            self.name_text.focus()
            return
        servings = self.serv_text.get("1.0", END)
        if servings.strip() == "-":
            servings = "0"
        try:
            servings = int(servings)
            if servings < 0:
                raise ValueError()
        except ValueError as e:
            self.serv_text.config(bg="red")
            self.serv_text.focus()
            return
        try:
            prep = float(self.prep_text.get("1.0", END))
            if prep < 0:
                raise ValueError()
        except ValueError as e:
            self.prep_text.config(bg="red")
            self.prep_text.focus()
            return
        try:
            cook = float(self.cook_text.get("1.0", END))
            if cook < 0:
                raise ValueError()
        except ValueError as e:
            self.cook_text.config(bg="red")
            self.cook_text.focus()
            return
        force = False
        book = RecipeBook(self.database)
        name = self.name_text.get("1.0", END).strip()
        book.cursor.execute("""
            SELECT *
            FROM Recipe r
            WHERE r.name = ?""", [name])
        result = book.cursor.fetchone()
        if result:
            d = ModalWindow(self, "Overwrite Recipe", "Warning: Recipe name already exists.\nDo you want to overwrite?")
            self.wait_window(d.modalWindow)
            if d.choice == 'Yes':
                force = True
                self.old_id = result[0]
            else:
                book.close()
                return
        book.add(name, self.desc_text.get("1.0", END).strip(), self.inst_text.get("1.0", END).strip().replace('^o', u'°'),
            servings, self.note_text.get("1.0", END).strip(), prep, cook, [(ingr[0], ingr[1].strip(), ingr[2].strip()) for ingr in self.ingr_list.get(0, END)], force)
        book.close(True)
        self.master.destroy()
        self.final = name
