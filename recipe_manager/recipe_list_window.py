import os
import json
from Tkinter import *

from recipe_book import RecipeBook
from recipe_creation_window import RecipeCreationWindow

class RecipeListWindow(Frame):
    def __init__(self, root, database, manager, search=None):
        Frame.__init__(self, root)
        self.root = root
        self.window = Frame(root)
        self.window.grid(row=0, column=0)
        self.canvas = Canvas(self.window, borderwidth=0, background="#ffffff", width=400, height=560)
        self.frame = Frame(self.canvas, background="#ffffff")

        self.button_create = Button(self.window, text="New Recipe", command=self.create_recipe)
        self.button_create.grid(row=0, column=1, sticky=W)

        self.search_text = Text(self.window, width=32, height=1)
        self.search_text.grid(row=0, column=8, sticky=W)
        self.search_text.bind('<Return>', self.search_recipe)
        self.search_button = Button(self.window, text="Search", command=self.search_recipe)
        self.search_button.grid(row=0, column=9, sticky=W)

        self.manager = manager
        self.database = database

        self.canvas.grid(row=1, column=0, columnspan=10, sticky=NSEW)
        self.frame_id = self.canvas.create_window((4,4), window=self.frame, anchor=N+W,
                                  tags="self.frame")

        self.recipe_list = Listbox(self.frame, width=65, height=34)
        self.recipe_list.pack(side=LEFT)
        self.recipe_list.bind('<<ListboxSelect>>', self.on_select)
        self.vsb = Scrollbar(self.window, orient="vertical", command=self.recipe_list.yview)
        self.recipe_list.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.window, orient="horizontal", command=self.recipe_list.xview)
        self.recipe_list.configure(xscrollcommand=self.hsb.set)

        self.vsb.grid(row=1, column=11, sticky=NSEW)
        self.hsb.grid(row=2, column=0, columnspan=10, sticky=NSEW)

        self.id_list = []
        self.search = search
        self.load_json()
        if search!=None:
            self.search_text.insert("1.0", search)
            self.search_recipe()
        else:
            self.populate()

    def load_json(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir,"recipe_format.json"),"r") as f:
            self.recipe_format = json.load(f)

    def populate(self, search=None):
        self.recipe_list.delete(0, END)
        book = RecipeBook(self.database)
        formatting = []
        for k, v in sorted(self.recipe_format.iteritems(), key=lambda (k,v): (v,k)):
            if v > 0:
                formatting.append("r."+k.replace(' ', ''))
        str_format = ','.join(formatting)
        search_format = " WHERE {}".format(search) if search!=None else ""
        book.cursor.execute("""
            SELECT r.id,{}
            FROM Recipe r{}""".format(str_format, search_format))
        results = book.cursor.fetchall()
        self.id_list = []
        for r in results:
            self.id_list.append(r[0])
            r = r[1:]
            serv_index = self.recipe_format["yield"]
            if serv_index > 0:
                r = [(r[i] if i!=serv_index-1 else "Serves {}".format(r[i])) for i in range(len(r))]
            prep_index = self.recipe_format["prep_time"]
            if prep_index > 0:
                r = [(r[i] if i!=prep_index-1 else "Prep: {} min.".format(r[i])) for i in range(len(r))]
            cook_index = self.recipe_format["cook_time"]
            if cook_index > 0:
                r = [(r[i] if i!=cook_index-1 else "Cook: {} min.".format(r[i])) for i in range(len(r))]
            r = [(r[i].encode("utf-8")) for i in range(len(r))]
            self.recipe_list.insert(END, r)

    def on_select(self, event):
        self.manager.view_recipe(int(event.widget.curselection()[0]))

    def create_recipe(self):
        recipe = None
        w = RecipeCreationWindow(Toplevel(self), self.database, self.root, recipe)
        self.wait_window(w)
        self.populate()

    def search_recipe(self, event=None):
        search = self.search_text.get("1.0", END).strip()
        for cond in ["=", ">=", "<=", ">", "<"]:
            for val in ["prep", "cook"]:
                if val+cond in search:
                    self.search = search
                    search = search.split(cond)[1]
                    self.populate(("r.{}_time {} {}".format(val, cond, search)) if search else None)
                    return "break"
        self.search = search
        self.populate("r.name LIKE \'%"+search+"%\' OR r.notes LIKE \'%"+search+"%\'")
        return "break"
