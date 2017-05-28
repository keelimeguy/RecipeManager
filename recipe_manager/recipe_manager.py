#!/usr/bin/env python

try:
    from Tkinter import *
    import tkFileDialog
except ImportError:
    from tkinter import *
from sys import platform as __platform__
import json
import os

if __debug__:
    print("debug")
    if __platform__ == "win32":
        print("windows")
    elif __platform__ == "darwin":
        print("mac")
    from data.recipe_book import RecipeBook
    from structure.modal_window import ModalWindow
    from recipe_view_window import RecipeViewWindow
    from recipe_list_window import RecipeListWindow
    from ingredient_list_window import IngredientListWindow
    from docs.documentation_window import DocumentationWindow
    from docs.about_window import AboutWindow
    from recipe_format_edit_window import RecipeFormatEditWindow
else:
    from recipe_manager.data.recipe_book import RecipeBook
    from recipe_manager.structure.modal_window import ModalWindow
    from recipe_manager.recipe_view_window import RecipeViewWindow
    from recipe_manager.recipe_list_window import RecipeListWindow
    from recipe_manager.ingredient_list_window import IngredientListWindow
    from recipe_manager.docs.documentation_window import DocumentationWindow
    from recipe_manager.docs.about_window import AboutWindow
    from recipe_manager.recipe_format_edit_window import RecipeFormatEditWindow

class RecipeManager():
    def __init__(self, root, database, preference_file):
        self.is_wind = (__platform__ == "win32")
        self.root = root
        self.root.title("Recipe Manager")
        self.root.geometry('500x500')
        self.preference_file = preference_file
        self.database = database

        self.menubar = Menu(self.root)

        self.fileoptions = { 'defaultextension':".db",
                            'filetypes':[('database files', '.db'), ('all files', '.*')],
                            'initialfile':self.database,
                            'parent':self.root,
                            'title':'Choose File' }

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Load", command=self.load_database)
        self.file_menu.add_command(label="Import", command=self.import_database)
        self.file_menu.add_command(label="Export", command=self.export_database)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.settings_menu = Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Edit Default Database", command=self.set_database_pref)
        self.settings_menu.add_command(label="Edit Listed Recipe Format", command=self.set_recipe_format)
        self.menubar.add_cascade(label="Preferences", menu=self.settings_menu)

        self.lists_menu = Menu(self.menubar, tearoff=0)
        self.lists_menu.add_command(label="Recipes", command=self.fresh_browse)
        self.lists_menu.add_command(label="Ingredients", command=self.list_ingredients)
        self.menubar.add_cascade(label="Lists", menu=self.lists_menu)

        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Documentation", command=self.docs)
        self.help_menu.add_command(label="About Recipe Manager", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menubar)

        self.my_gui = RecipeListWindow(self.root, self.database, self, self.preference_file)
        self.my_gui.focus()
        root.mainloop()

    def fresh_browse(self):
        self.my_gui.search = None
        self.browse()

    def browse(self):
        self.my_gui.destroy()
        search = self.my_gui.search
        self.my_gui = RecipeListWindow(self.root, self.database, self, self.preference_file, search)

    def list_ingredients(self):
        self.my_gui.destroy()
        self.my_gui = IngredientListWindow(self.root, self.database, self)

    def view_recipe(self, index):
        self.my_gui.destroy()
        id_list = self.my_gui.id_list
        search = self.my_gui.search
        self.my_gui = RecipeViewWindow(self.root, self.database, self, self.preference_file, index, id_list, search)

    def docs(self):
        DocumentationWindow(self.root, self)

    def about(self):
        w = AboutWindow(self.root)
        self.my_gui.wait_window(w.master)

    def set_recipe_format(self):
        w = RecipeFormatEditWindow(self.root, self, self.preference_file)
        self.my_gui.wait_window(w.master)
        self.my_gui.destroy()
        self.my_gui = RecipeListWindow(self.root, self.database, self, self.preference_file)

    def load_database(self):
        self.fileoptions['title'] = 'Load Database'
        filename = tkFileDialog.askopenfilename(**self.fileoptions)
        if filename:
            self.database = filename
        self.my_gui.destroy()
        self.my_gui = RecipeListWindow(self.root, self.database, self, self.preference_file)

    def import_database(self):
        self.fileoptions['title'] = 'Import Database'
        filename = tkFileDialog.askopenfilename(**self.fileoptions)
        if filename:
            self.combine_databases(source_file=filename, dest_file=self.database)
        self.my_gui.destroy()
        self.my_gui = RecipeListWindow(self.root, self.database, self, self.preference_file)

    def export_database(self):
        self.fileoptions['title'] = 'Export Database'
        filename = tkFileDialog.askopenfilename(**self.fileoptions)
        if filename:
            self.combine_databases(source_file=self.database, dest_file=filename)

    def combine_databases(self, source_file, dest_file):
        source = RecipeBook(source_file)
        dest = RecipeBook(dest_file)
        source.cursor.execute("""
            SELECT *
            FROM Recipe""")
        results = source.cursor.fetchall()
        if results:
            force = None
            for r in results:
                result = source.cursor.execute("""
                    SELECT ri.amount AS 'Amount',
                    mu.name AS 'Unit of Measure',
                    i.name AS 'Ingredient',
                    ri.order_num AS 'Order'
                    FROM Recipe r
                    JOIN RecipeIngredient ri on r.id = ri.recipe_id
                    JOIN Ingredient i on i.id = ri.ingredient_id
                    LEFT OUTER JOIN Measure mu on mu.id = measure_id
                    WHERE r.id = ?""", [r[0]])
                ingredients = []
                for i in sorted(result, key=lambda tup: tup[3]):
                    ingredients.append(i)

                dest.cursor.execute("""
                    SELECT *
                    FROM Recipe r
                    WHERE r.name = ?""", [r[1]])
                result = dest.cursor.fetchone()
                if result:
                    if force == None:
                        d = ModalWindow(self.my_gui, "Overwrite All", "Warning: Duplicate recipe names exist.\nDo you want to overwrite all duplicates?\n(Choosing 'No' will result in a prompt for each duplicate case)")
                        self.my_gui.wait_window(d.modalWindow)
                        force = (d.choice == 'Yes')
                    if not force:
                        d = ModalWindow(self.my_gui, "Overwrite Recipe", "Warning: Recipe name already exists.\nDo you want to overwrite {}?".format(r[1]))
                        self.my_gui.wait_window(d.modalWindow)
                        if d.choice == 'Yes':
                            dest.add(r[1], r[2], r[3], r[4], r[5], r[6], r[7], ingredients, True)
                    else:
                        dest.add(r[1], r[2], r[3], r[4], r[5], r[6], r[7], ingredients, force)
                else:
                    dest.add(r[1], r[2], r[3], r[4], r[5], r[6], r[7], ingredients, False)
        source.close()
        dest.renumber()
        dest.close(True)

    def set_database_pref(self):
        fileoptions = { 'defaultextension':".db",
                        'filetypes':[('database files', '.db'), ('all files', '.*')],
                        'initialfile':self.database,
                        'parent':self.root,
                        'title':'Choose Default Database' }
        filename = tkFileDialog.askopenfilename(**fileoptions)

        if filename:
            d = ModalWindow(self.my_gui, "Confirmation", "Warning: In the future, if the file at the given location cannot be found at startup\nthe program will automatically create the file at that position.\nIs this okay? Choosing 'No' cancels the change in preferences.")
            self.my_gui.wait_window(d.modalWindow)
            if d.choice == 'Yes':
                current_dir = os.getcwd()
                if not os.path.isfile(os.path.join(current_dir,self.preference_file)):
                    with open(os.path.join(current_dir,self.preference_file),"w") as f:
                        recipe_format = {"database":filename, "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
                        json.dump(recipe_format, f)
                else:
                    with open(os.path.join(current_dir,self.preference_file),"r") as f:
                        recipe_format = json.load(f)
                    with open(os.path.join(current_dir,self.preference_file),"w") as f:
                        recipe_format["database"] = filename
                        json.dump(recipe_format, f)

if __name__ == "__main__":
    preference_file = "recipe_manager_preferences.json"
    current_dir = os.getcwd()
    if not os.path.isfile(os.path.join(current_dir,preference_file)):
        if __platform__ == "win32":
            database = os.path.join(current_dir,"recipe_data.db")
        else:
            database = os.path.join(os.path.expanduser("~"),"Documents/recipe_data.db")
    else:
        with open(os.path.join(current_dir,preference_file),"r") as f:
            recipe_format = json.load(f)
            database = recipe_format["database"]

    book = RecipeBook(database)
    book.renumber()
    book.close(True)

    root = Tk()
    manager = RecipeManager(root, database, preference_file)
