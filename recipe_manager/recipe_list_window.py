try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from TkTreectrl import *
import os
import json

if __debug__:
    from data.recipe_book import RecipeBook
    from recipe_creation_window import RecipeCreationWindow
else:
    from recipe_manager.data.recipe_book import RecipeBook
    from recipe_manager.recipe_creation_window import RecipeCreationWindow
from search_window import SearchWindow

class RecipeListWindow(Frame):
    def __init__(self, root, database, manager, preference_file, search=None):
        Frame.__init__(self, root)
        self.root = root
        self.header = Frame(root)
        self.header.pack(fill=BOTH)
        self.window = Frame(root)
        self.window.pack(fill=BOTH, expand=YES)
        self.footer = Frame(root)
        self.footer.pack(fill=BOTH)
        self.preference_file = preference_file

        self.button_create = Button(self.header, text="New Recipe", command=self.create_recipe)
        self.button_create.pack(side=LEFT)
        Label(self.header, text="", width=10).pack(side=LEFT)
        self.search_text = Text(self.header, width=16, height=1)
        self.search_text.bind('<Return>', self.search_recipe)
        self.search_text.pack(side=LEFT, fill=X, expand=YES)
        self.search_button = Button(self.header, text="Search", command=self.search_recipe)
        self.search_button.pack(side=LEFT)

        self.search_button = Button(self.header, text="..", command=self.adv_search)
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
        self.recipe_list.bind("<MouseWheel>", self.on_mousewheel)

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
            region_r = self.recipe_list.identify(event.x+5, event.y)
            if region_r and region_r[1]==region[1] or not region_r:
                region_l = self.recipe_list.identify(event.x-5, event.y)
                if region_l and region_l[1]==region[1] or not region_l:
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
        if not os.path.isfile(os.path.join(current_dir,self.preference_file)):
            with open(os.path.join(current_dir,self.preference_file),"w") as f:
                self.recipe_format = {"database":os.path.join(current_dir,"recipe_data.db"), "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
                json.dump(self.recipe_format, f)
        else:
            with open(os.path.join(current_dir,self.preference_file),"r") as f:
                self.recipe_format = json.load(f)
                if self.recipe_format["name"]!=1:
                    raise ValueError("Key \"name\" must have value \"1\" in {}".format(self.preference_file))
        del self.recipe_format["database"]

    def populate(self, search=None, grouped=True):
        self.load_json()
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
        if grouped:
            book.cursor.execute("""
                SELECT r.id,{}
                FROM Recipe r
                LEFT JOIN (SELECT ri.recipe_id as recipe_id, GROUP_CONCAT(ing.name) as name
                    FROM RecipeIngredient ri
                    JOIN Ingredient ing on ing.id = ri.ingredient_id
                    GROUP BY ri.recipe_id) i on i.recipe_id = r.id{}
                GROUP BY r.id""".format(str_format, search_format))
        else:
            book.cursor.execute("""
                SELECT r.id,{}
                FROM Recipe r
                LEFT JOIN (SELECT ri.recipe_id as recipe_id, ing.name as name
                    FROM RecipeIngredient ri
                    JOIN Ingredient ing on ing.id = ri.ingredient_id) i on i.recipe_id = r.id{}
                GROUP BY r.id""".format(str_format, search_format))
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
            r = [r[i] for i in range(1, len(r))]
            cook_index = self.recipe_format["cook_time"]
            prep_index = self.recipe_format["prep_time"]
            serve_index = self.recipe_format["yield"]
            for i in range(len(r)):
                if cook_index > 0 and i==cook_index-1 or prep_index > 0 and i==prep_index-1:
                    r[i] = "{} min.".format(r[i])
                if serve_index > 0 and i==serve_index-1 and r[i] == 0:
                    r[i] = "-"
            r_str = r[0]
            if len(r)>1:
                for i in range(len(r)-1):
                    r_str+=(u"; {}".format(r[i+1]))
            item = self.recipe_list.insert(END, *(r))
            index+=1
        self.recipe_list.yview(MOVETO, 0)

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

    def adv_search(self, event=None):
        w = SearchWindow(Toplevel(self), self.root, "Recipe", "recipes")
        w.master.focus()
        self.wait_window(w.master)
        if w.final != None:
            self.search_text.delete("1.0", END)
            self.search_text.insert("1.0", w.final)
            self.search_recipe()

    def search_recipe(self, event=None):
        search = self.search_text.get("1.0", END).strip()
        self.search = search
        search_key = None
        sort_by = None
        perfect = False
        for search_or in self.search.split("|"):
            # OR-ed terms
            joiner = " OR "
            for search in search_or.split("&"):
                # AND-ed terms
                if not search or search.strip() == "":
                    break
                search = search.strip()
                if search[0] == "~" and len(search)>1:
                    search = search[1:]
                    negate = True
                else:
                    negate = False
                searched = False
                ingr_cond = None

                for cond in ["!ingr:", "!ingredient:"]:
                    if cond in search:
                        searched = True
                        ingr_cond = cond
                        ingr_search = search.split(ingr_cond)[1]
                        if self.search_text.get("1.0", END).strip() == cond+ingr_search:
                            perfect = True
                            ingr_search = ("{} \'{}\'".format("=", ingr_search) if ingr_search else None)
                            break
                if not ingr_cond:
                    for cond in ["ingr:", "ingredient:"]:
                        if cond in search:
                            ingr_cond = cond
                            ingr_search = search.split(ingr_cond)[1]
                            ingr_like = "NOT LIKE" if negate else "LIKE"
                            ingr_search = ("{} \'%{}%\'".format(ingr_like, ingr_search) if ingr_search else None)
                            ingr_cond = None
                            searched = True
                            break
                if perfect or searched and not ingr_cond:
                    key = ("i.name {}".format(ingr_search) if ingr_search else None)
                    if key:
                        search_key = (joiner.join([search_key, key]) if search_key else key)
                        joiner = " AND "
                    searched = True
                else:
                    for val in ["prep", "prep_time", "cook", "cook_time", "serve", "serves", "yield", "yields"]:
                        if val in search:
                            for cond in ["=", ">=", "<=", ">", "<"]:
                                if val+cond in search:
                                    if val == "prep":
                                        val = "prep_time"
                                    elif val == "cook":
                                        val = "cook_time"
                                    search = search.split(cond)[1]
                                    key = ("r.{} {} {}".format(val if val in ["prep_time", "cook_time"] else "yield", cond, search) if search else None)
                                    if key:
                                        if negate:
                                            key = "NOT ({})".format(key)
                                        search_key = (joiner.join([search_key, key]) if search_key else key)
                                        joiner = " AND "
                                    sort_by = val
                                    searched = True
                if not searched or searched and ingr_cond and not perfect:
                    like_term = ("NOT LIKE" if negate else "LIKE")
                    key = "(r.name {} \'%{}%\' {} r.notes {} \'%{}%\')".format(
                        like_term, search,
                        "AND" if negate else "OR",
                        like_term, search)
                    search_key = (joiner.join([search_key, key]) if search_key else key)
                    joiner = " AND "
        self.populate(search_key, not perfect)
        if sort_by:
            col = self.recipe_format[sort_by if sort_by in ["prep_time", "cook_time"] else "yield"]-1
            if col >= 0:
                self.sort_column(col)
        return "break"
