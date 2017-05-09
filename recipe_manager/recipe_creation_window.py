from Tkinter import *

from recipe_manager.recipe_book import RecipeBook
from recipe_manager.modal_window import ModalWindow

class RecipeCreationWindow(Frame):
    def __init__(self, master, database, root, recipe=None):
        Frame.__init__(self, master)
        self.root = root
        self.master.maxsize(409,344)
        self.master.title("Create Recipe")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.selected = False
        self.database = database
        self.final = None

        self.name_label = Label(self.master, text="Name:").grid(row=0, column=0, columnspan=2, sticky=E)
        self.name_text = Text(self.master, height=1, width=32)
        self.name_text.grid(row=0, column=2, columnspan=6, sticky=NSEW)
        self.name_text.bind('<Tab>', self.on_text_tab)
        self.name_text.bind('<Return>', self.on_text_tab)

        self.serv_label = Label(self.master, text="Serves:").grid(row=0, column=8, columnspan=2, sticky=E)
        self.serv_text = Text(self.master, undo=True, height=1, width=4)
        self.serv_text.grid(row=0, column=11, columnspan=2, sticky=NSEW)
        self.serv_text.bind('<Tab>', self.on_text_tab)
        self.serv_text.bind('<Return>', self.on_text_tab)

        self.desc_label = Label(self.master, text="Description:").grid(row=4, column=0, columnspan=2, sticky=E)
        self.desc_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.desc_scrollbar.grid(row=5, column=12, columnspan=1, sticky=W)
        self.desc_text = Text(self.master, undo=True, height=2, width=32)
        self.desc_text.grid(row=5, column=2, columnspan=10, sticky=NSEW)
        self.desc_text.bind('<Tab>', self.on_text_tab)
        self.desc_text.config(yscrollcommand=self.desc_scrollbar.set)
        self.desc_scrollbar.config(command=self.desc_text.yview)

        self.ingr_label = Label(self.master, text="Ingredients:").grid(row=6, column=0, columnspan=2, sticky=E)
        self.ingr_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.ingr_scrollbar.grid(row=7, column=12, columnspan=1, sticky=W)
        self.ingr_list = Listbox(self.master, height=4, width=32)
        self.ingr_list.grid(row=7, column=2, columnspan=10, sticky=NSEW)
        self.ingr_list.config(yscrollcommand=self.ingr_scrollbar.set)
        self.ingr_list.bind('<BackSpace>', self.rem_ingr)
        self.ingr_list.bind('<<ListboxSelect>>', self.on_select)
        self.ingr_scrollbar.config(command=self.ingr_list.yview)
        self.ingr_amount = Text(self.master, height=1, width=4)
        self.ingr_amount.insert(END, "<#>")
        self.ingr_amount.grid(row=8, column=2, sticky=E)
        self.ingr_amount.bind('<Tab>', self.on_text_tab)
        self.ingr_amount.bind('<Return>', self.on_text_tab)
        self.ingr_amount.bind("<FocusIn>", self.on_select)
        self.ingr_unit = Text(self.master, height=1, width=8)
        self.ingr_unit.insert(END, "<unit>")
        self.ingr_unit.grid(row=8, column=3, columnspan=2, sticky=EW)
        self.ingr_unit.bind('<Tab>', self.on_text_tab)
        self.ingr_unit.bind('<Return>', self.on_text_tab)
        self.ingr_unit.bind("<FocusIn>", self.on_select)
        self.ingr_text = Text(self.master, height=1, width=20)
        self.ingr_text.insert(END, "<name>")
        self.ingr_text.grid(row=8, column=5, columnspan=5, sticky=EW)
        self.ingr_text.bind('<Tab>', self.on_text_tab)
        self.ingr_text.bind('<Return>', self.on_text_tab)
        self.ingr_text.bind("<FocusIn>", self.on_select)
        self.ingr_add_button = Button(self.master, text="+", command=self.add_ingr).grid(row=8, column=11, sticky=EW)
        self.ingr_add_button = Button(self.master, text="-", command=self.rem_ingr).grid(row=8, column=12, sticky=EW)
        self.ingr_dict = {}

        self.inst_label = Label(self.master, text="Instructions:").grid(row=9, column=0, columnspan=2, sticky=E)
        self.inst_scrollbar = Scrollbar(self.master, orient=VERTICAL)
        self.inst_scrollbar.grid(row=10, column=12, columnspan=1, sticky=W)
        self.inst_text = Text(self.master, undo=True, height=4, width=32)
        self.inst_text.grid(row=10, column=2, columnspan=10, sticky=NSEW)
        self.inst_text.config(yscrollcommand=self.inst_scrollbar.set)
        self.inst_text.bind('<Tab>', self.on_text_tab)
        self.inst_scrollbar.config(command=self.inst_text.yview)

        Label(self.master, text="").grid(row=11, column=0)

        self.save_button = Button(self.master, text="Save", command=self.save_recipe)
        self.save_button.grid(row=12, column=2, columnspan=9, sticky=EW)
        self.back_button = Button(self.master, text="Back", command=self.master.destroy)
        self.back_button.grid(row=12, column=11, columnspan=2, sticky=EW)

        if recipe:
            self.name_text.insert(END, recipe[0][1])
            self.desc_text.insert(END, recipe[0][2])
            self.inst_text.insert(END, recipe[0][3])
            self.serv_text.insert(END, recipe[0][4])
            for i in recipe[1]:
                self.ingr_list.insert(END, i)
                self.ingr_dict[i[2]] = i[0]

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
        self.ingr_amount.config(bg="white")
        self.ingr_text.config(bg="white")

        try:
            amount = float(self.ingr_amount.get("1.0", END))
        except ValueError as e:
            self.ingr_amount.config(bg="red")
            return

        name = self.ingr_text.get("1.0", END).strip()
        if name in self.ingr_dict:
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
        try:
            servings = int(self.serv_text.get("1.0", END))
        except ValueError as e:
            self.serv_text.config(bg="red")
            self.serv_text.focus()
            return
        self.serv_text.config(bg="white")
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
            if d.choice == 'No':
                book.close()
                return
            force = True
        book.add(name, self.desc_text.get("1.0", END).strip(), self.inst_text.get("1.0", END).strip(),
            servings, None, [(ingr[0], ingr[1].strip(), ingr[2].strip()) for ingr in self.ingr_list.get(0, END)], force)
        book.save()
        book.close()
        self.master.destroy()
        self.final = name
