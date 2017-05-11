#!/usr/bin/env python

from Tkinter import *
import argparse

from recipe_book import RecipeBook
from recipe_view_window import RecipeViewWindow
from recipe_list_window import RecipeListWindow
# from recipe_manager.recipe_book import RecipeBook
# from recipe_manager.recipe_view_window import RecipeViewWindow
# from recipe_manager.recipe_list_window import RecipeListWindow

class RecipeManager():
    def __init__(self, root, database):
        self.root = root
        self.root.title("Recipe Manager")

        self.database = database
        self.my_gui = RecipeListWindow(self.root, self.database, self)
        root.mainloop()

    def browse(self):
        self.my_gui.destroy()
        search = self.my_gui.search
        self.my_gui = RecipeListWindow(self.root, self.database, self, search)

    def view_recipe(self, index):
        self.my_gui.destroy()
        self.my_gui.destroy()
        self.my_gui.destroy()
        id_list = self.my_gui.id_list
        search = self.my_gui.search
        self.my_gui = RecipeViewWindow(self.root, self.database, self, index, id_list, search)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the recipe manager GUI.')
    parser.add_argument('-d', '--database', default="recipe_data.db",
                        help='The database file you wish to use.')
    args = parser.parse_args()

    book = RecipeBook(args.database)
    book.renumber()
    book.close()

    root = Tk()
    manager = RecipeManager(root, args.database)
