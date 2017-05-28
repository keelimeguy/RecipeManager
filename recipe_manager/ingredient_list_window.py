try:
    from Tkinter import *
except ImportError:
    from tkinter import *
from TkTreectrl import *
import os
import json

if __debug__:
    from data.recipe_book import RecipeBook
else:
    from recipe_manager.data.recipe_book import RecipeBook
from structure.color_scheme import *
from search_window import SearchWindow

class IngredientListWindow(Frame):
    def __init__(self, root, database, manager, search=None):
        Frame.__init__(self, root)
        self.root = root
        self.header = Frame(root, bg=BG_COLOR)
        self.header.pack(fill=BOTH)
        self.window = Frame(root, bg=BG_COLOR)
        self.window.pack(fill=BOTH, expand=YES)
        self.footer = Frame(root, bg=BG_COLOR)
        self.footer.pack(fill=BOTH)

        self.search_button = Button(self.header, text="..", command=self.adv_search)
        self.search_button.pack(side=RIGHT)
        self.search_button = Button(self.header, text="Search", command=self.search_ingredient)
        self.search_button.pack(side=RIGHT)

        self.search_text = Text(self.header, width=16, height=1)
        self.search_text.bind('<Return>', self.search_ingredient)
        self.search_text.pack(side=RIGHT, fill=X, expand=YES)
        Label(self.header, text="", width=1, bg=BG_COLOR).pack(side=RIGHT)

        self.manager = manager
        self.database = database

        self.ingredient_list = MultiListbox(self.window, command=self.on_select, height=400, width=400, headerfont=("Times", 11, "bold"))
        self.ingredient_list.bind("<Button-1>", self.sort_column_sngl)
        self.ingredient_list.bind("<Double-1>", self.sort_column_dbl)
        self.ingredient_list.pack(fill=BOTH, expand=YES, side=LEFT)
        self.vsb = Scrollbar(self.window, orient="vertical", command=self.ingredient_list.yview)
        self.ingredient_list.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.footer, orient="horizontal", command=self.ingredient_list.xview)
        self.ingredient_list.configure(xscrollcommand=self.hsb.set)
        self.ingredient_list.bind("<MouseWheel>", self.on_mousewheel)

        self.vsb.pack(fill=BOTH, side=LEFT)
        self.hsb.pack(fill=BOTH)

        self.id_list = []
        self.orig_index_list = []
        self.id_dict = {}
        self.orig_index_dict = {}
        self.search = search
        if search!=None:
            self.search_text.insert("1.0", search)
            self.search_ingredient()
        else:
            self.populate()

    def on_mousewheel(self, event):
        self.ingredient_list.yview_scroll(-1*(event.delta/120), "units") # Windows
        # self.ingredient_list.yview_scroll(-1*(event.delta), "units") # OS X

    def on_select(self, event):
        if event>=0:
            self.search = "!ingr:{}".format(self.ingredient_list.get(event)[0][0])
            self.manager.browse()

    def sort_column_dbl(self, event):
        self.sort_column_sngl(event, True)

    def sort_column_sngl(self, event, dbl=False):
        region = self.ingredient_list.identify(event.x, event.y)
        if region:
            if region[0]!='header':
                if dbl and region[1]>0:
                    self.on_select(self.orig_index_list.index(region[1]-1))
                return
            region_r = self.ingredient_list.identify(event.x+5, event.y)
            if region_r and region_r[1]==region[1] or not region_r:
                region_l = self.ingredient_list.identify(event.x-5, event.y)
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
        self.ingredient_list.sort(column=col, mode=('dictionary', self.sort_dict[col]))
        for i in range(size):
            self.id_list.append(self.id_dict[self.ingredient_list.get(i)[0][0]])
            self.orig_index_list.append(self.orig_index_dict[self.ingredient_list.get(i)[0][0]])

    def destroy(self):
        self.header.destroy()
        self.window.destroy()
        self.footer.destroy()

    def populate(self, search=None):
        self.ingredient_list.delete(0, END)
        book = RecipeBook(self.database)
        columns = ["Ingredient", "Recipe Occurrences"]
        self.ingredient_list.config(columns=columns)
        self.sort_dict = []
        for col in range(len(columns)):
            self.sort_dict.append('decreasing')
        self.ingredient_list.column_config(0, width=180)

        search_format = " WHERE {}".format(search) if search!=None else ""
        book.cursor.execute("""
            SELECT i.id, i.name, (
                SELECT COUNT(*)
                FROM RecipeIngredient ri
                WHERE ri.ingredient_id = i.id
            )
            FROM Ingredient i{}""".format(search_format))
        results = book.cursor.fetchall()

        self.id_list = []
        self.orig_index_list = []
        self.id_dict = {}
        self.orig_index_dict = {}
        index = 0
        for r in results:
            if r[2]==0:
                book.cursor.execute("""DELETE FROM Ingredient WHERE id = ?""", [r[0]])
            else:
                self.id_list.append(r[0])
                self.orig_index_dict[r[1]] = index
                self.orig_index_list.append(index)
                self.id_dict[r[1]] = r[0]
                r = r[1:]
                r_str = r[0]
                if len(r)>1:
                    for i in range(len(r)-1):
                        r_str+=(u"; {}".format(r[i+1]))
                item = self.ingredient_list.insert(END, *(r))
                index+=1
        self.ingredient_list.yview(MOVETO, 0)
        book.close(True)

    def adv_search(self, event=None):
        w = SearchWindow(Toplevel(self), self.root, "Ingredient", "ingredients")
        w.master.focus()
        self.wait_window(w.master)
        if w.final != None:
            self.search_text.delete("1.0", END)
            self.search_text.insert("1.0", w.final)
            self.search_ingredient()

    def search_ingredient(self, event=None):
        search = self.search_text.get("1.0", END).strip()
        self.search = search
        search_key = None
        sort_by = None
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

                for cond in ["ingr:", "ingredient:"]:
                    if cond in search:
                        ingr_cond = cond
                        break
                if ingr_cond:
                    search = search.split(ingr_cond)[1]
                like_term = ("NOT LIKE" if negate else "LIKE")
                key = "i.name {} \'%{}%\'".format(like_term, search)
                search_key = (joiner.join([search_key, key]) if search_key else key)
                joiner = " AND "
        self.populate(search_key)
        return "break"
