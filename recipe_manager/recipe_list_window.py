import os
import json
from Tkinter import *
from TkTreectrl import *

from recipe_book import RecipeBook
from recipe_creation_window import RecipeCreationWindow
# from recipe_manager.recipe_book import RecipeBook
# from recipe_manager.recipe_creation_window import RecipeCreationWindow

class RecipeListWindow(Frame):

    def FrameWidth(self, event):
        self.canvas.itemconfig(self.frame, width=event.width, height=event.height)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, root, database, manager, search=None):
        Frame.__init__(self, root)
        self.root = root
        self.header = Frame(root)
        self.header.pack(fill=BOTH)
        self.window = Frame(root)
        self.window.pack(fill=BOTH, expand=YES)
        self.footer = Frame(root)
        self.footer.pack(fill=BOTH)
        self.root.bind_all("<MouseWheel>", self.on_mousewheel)

        self.button_create = Button(self.header, text="New Recipe", command=self.create_recipe)
        self.button_create.pack(side=LEFT)
        Label(self.header, text="", width=10).pack(side=LEFT)
        self.search_text = Text(self.header, width=16, height=1)
        self.search_text.bind('<Return>', self.search_recipe)
        self.search_text.pack(side=LEFT, fill=X, expand=YES)
        self.search_button = Button(self.header, text="Search", command=self.search_recipe)
        self.search_button.pack(side=LEFT)

        self.manager = manager
        self.database = database

        self.recipe_list = MultiListbox(self.window, command=self.on_select, headerfont=("Times", 11, "bold"))
        self.recipe_list.bind("<Button-1>", self.sort_column_sngl)
        self.recipe_list.bind("<Double-1>", self.sort_column_dbl)
        self.recipe_list.pack(fill=BOTH, expand=YES, side=LEFT)
        self.vsb = Scrollbar(self.window, orient="vertical", command=self.recipe_list.yview)
        self.recipe_list.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.footer, orient="horizontal", command=self.recipe_list.xview)
        self.recipe_list.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(fill=BOTH, side=LEFT)
        self.hsb.pack(fill=BOTH)

        self.id_list = []
        self.orig_index_list = []
        self.id_dict = {}
        self.orig_index_dict = {}
        self.search = search
        self.load_json()
        if search!=None:
            self.search_text.insert("1.0", search)
            self.search_recipe()
        else:
            self.populate()

    def on_mousewheel(self, event):
        self.recipe_list.yview_scroll(-1*(event.delta/120), "units") # Windows
        # self.recipe_list.yview_scroll(-1*(event.delta), "units") # OS X

    def on_select(self, event):
        if event>=0:
            self.manager.view_recipe(event)

    def sort_column_dbl(self, event):
        self.sort_column_sngl(event, True)

    def sort_column_sngl(self, event, dbl=False):
        region = self.recipe_list.identify(event.x, event.y)
        if region:
            if region[0]!='header':
                if dbl and region[1]>0:
                    self.on_select(self.orig_index_list.index(region[1]-1))
                return
            self.sort_column(region[1])

    def sort_column(self, col):
        size = len(self.id_list)
        self.id_list = []
        self.orig_index_list = []
        if self.sort_dict[col] == 'increasing':
            self.sort_dict[col] = 'decreasing'
        else:
            self.sort_dict[col] = 'increasing'
        self.recipe_list.sort(column=col, mode=('dictionary', self.sort_dict[col]))
        for i in range(size):
            self.id_list.append(self.id_dict[self.recipe_list.get(i)[0][0]])
            self.orig_index_list.append(self.orig_index_dict[self.recipe_list.get(i)[0][0]])

    def destroy(self):
        self.header.destroy()
        self.window.destroy()
        self.footer.destroy()

    def load_json(self):
        current_dir = os.getcwd()
        if not os.path.isfile(os.path.join(current_dir,"recipe_format.json")):
            with open(os.path.join(current_dir,"recipe_format.json"),"w") as f:
                self.recipe_format = {"name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
                json.dump(self.recipe_format, f)
        else:
            with open(os.path.join(current_dir,"recipe_format.json"),"r") as f:
                self.recipe_format = json.load(f)
                if self.recipe_format["name"]!=1:
                    raise ValueError("Key \"name\" must hav value \"1\" in recipe_format.json")

    def populate(self, search=None):
        self.recipe_list.delete(0, END)
        book = RecipeBook(self.database)
        formatting = []
        columns = []
        for k, v in sorted(self.recipe_format.iteritems(), key=lambda (k,v): (v,k)):
            if v > 0:
                formatting.append("r."+k.replace(' ', ''))
                columns.append(k.replace(' ', '').replace('_', ' ').title())
        self.recipe_list.config(columns=columns)
        self.sort_dict = []
        for col in range(len(columns)):
            self.sort_dict.append('decreasing')
        self.recipe_list.column_config(0, width=180)
        str_format = ','.join(formatting)
        search_format = " WHERE {}".format(search) if search!=None else ""
        book.cursor.execute("""
            SELECT r.id,{}
            FROM Recipe r{}""".format(str_format, search_format))
        results = book.cursor.fetchall()
        self.id_list = []
        self.orig_index_list = []
        self.id_dict = {}
        self.orig_index_dict = {}
        index = 0
        for r in results:
            self.id_list.append(r[0])
            self.orig_index_dict[r[1]] = index
            self.orig_index_list.append(index)
            self.id_dict[r[1]] = r[0]
            r = r[1:]
            prep_index = self.recipe_format["prep_time"]
            if prep_index > 0:
                r = [(r[i] if i!=prep_index-1 else "{} min.".format(r[i])) for i in range(len(r))]
            cook_index = self.recipe_format["cook_time"]
            if cook_index > 0:
                r = [(r[i] if i!=cook_index-1 else "{} min.".format(r[i])) for i in range(len(r))]
            r_str = r[0]
            if len(r)>1:
                for i in range(len(r)-1):
                    r_str+=("; {}".format(r[i+1]))
            item = self.recipe_list.insert(END, *(r))
            index+=1

    def create_recipe(self):
        w = RecipeCreationWindow(Toplevel(self), self.database, self.root, None)
        w.master.focus()
        self.wait_window(w.master)
        if w.final != None:
            old_id = w.old_id
            book = RecipeBook(self.database)
            book.cursor.execute("""
                SELECT r.id
                FROM Recipe r
                WHERE r.name = ?
                """, [w.final])
            r_id = book.cursor.fetchone()[0]
            book.close()
            self.manager.my_gui.repopulate(old_id, r_id)

    def repopulate(self, old_id, r_id):
        self.search = None
        self.search_text.delete("1.0", END)
        self.populate()

    def search_recipe(self, event=None):
        search = self.search_text.get("1.0", END).strip()
        for cond in ["=", ">=", "<=", ">", "<"]:
            for val in ["prep", "cook", "serves"]:
                if val+cond in search:
                    self.search = search
                    search = search.split(cond)[1]
                    self.populate(("r.{} {} {}".format(val+"_time" if val!="serves" else "yield", cond, search)) if search else None)
                    self.sort_column(self.recipe_format[val+"_time" if val!="serves" else "yield"]-1)
                    return "break"
        self.search = search
        self.populate("r.name LIKE \'%"+search+"%\' OR r.notes LIKE \'%"+search+"%\'")
        return "break"
