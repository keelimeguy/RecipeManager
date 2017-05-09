#!/usr/bin/env python

from Tkinter import *
import argparse

from recipe_creation_window import RecipeCreationWindow
from recipe_book import RecipeBook

class RecipeManagerWindow(Frame):
    def __init__(self, root, database):
        Frame.__init__(self, root)
        self.root = root
        self.root.title("Recipe Manager")
        self.root.maxsize(423,607)
        self.canvas = Canvas(root, borderwidth=0, background="#ffffff", width=400, height=560)
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.button_left = Button(root, text="<", command=self.shift_left)
        self.button_right = Button(root, text=">", command=self.shift_right)
        self.button_left.grid(row=0, column=0, sticky=W)
        self.button_right.grid(row=0, column=11, sticky=E)

        self.button_edit = Button(root, text="Edit Recipe", command=self.edit_recipe)
        self.button_edit.grid(row=0, column=4, sticky=EW)

        self.button_create = Button(root, text="New Recipe", command=self.create_recipe)
        self.button_create.grid(row=0, column=5, sticky=EW)

        self.database = database

        self.vsb.grid(row=1, column=11, sticky=NSEW)
        self.hsb.grid(row=2, column=0, columnspan=10, sticky=NSEW)
        self.canvas.grid(row=1, column=0, columnspan=10, sticky=NSEW)
        self.frame_id = self.canvas.create_window((4,4), window=self.frame, anchor=N+W,
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.name_label = Label(self.frame, text="Name", bg="white", font=("Times", 18, "bold"))
        self.name_label.grid(row=0, column=0, columnspan=6, sticky=W)
        self.serv_label = Label(self.frame, text="Servings", bg="white", font=("Times", 10, ""))
        self.serv_label.grid(row=1, column=0, columnspan=6, sticky=W)
        self.desc_label = Label(self.frame, text="Description", bg="white", font=("Times", 12, "italic"))
        self.desc_label.grid(row=2, column=0, columnspan=6, sticky=W)
        self.blank_label_1 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_1.grid(row=3, column=1, sticky=W)
        self.ingr_label_title = Label(self.frame, text="Ingredients", bg="white", font=("Times", 12, "bold"))
        self.ingr_label_title.grid(row=4, column=0, columnspan=3, sticky=W)
        self.ingr_label_list = []
        row = 5
        self.ingr_label_list.append((Label(self.frame, text="Amount", bg="white", font=("Times", 10, "")),
            Label(self.frame, text="Unit", bg="white", font=("Times", 10, "")),
            Label(self.frame, text="Ingredient", bg="white", font=("Times", 10, ""))))
        self.ingr_label_list[0][0].grid(row=row, column=0, sticky=W)
        self.ingr_label_list[0][1].grid(row=row, column=1, sticky=W)
        self.ingr_label_list[0][2].grid(row=row, column=2, columnspan=2, sticky=W)
        row+=1
        self.blank_label_2 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_2.grid(row=row, column=1, sticky=W)
        self.dir_label_title = Label(self.frame, text="Directions", bg="white", font=("Times", 12, "bold"))
        self.dir_label_title.grid(row=row+1, column=0, columnspan=3, sticky=W)
        self.dir_label = Label(self.frame, text="Direction", bg="white", font=("Times", 10, ""))
        self.dir_label.grid(row=row+2, column=0, columnspan=3, sticky=W)

        self.index = 0
        self.populate()

    def select_recipe(self, index):
        book = RecipeBook(self.database)
        book.cursor.execute("""
            SELECT r.id
            FROM Recipe r
            """)
        r_id = book.cursor.fetchall()
        if r_id:
            if len(r_id)>0:
                if index >= len(r_id):
                    index = 0
                elif index < 0:
                    index = len(r_id)-1
            if len(r_id)>index:
                r_id = r_id[index][0]
                recipe = book.get(r_id)
            else:
                r_id = None
        book.close()
        return recipe, r_id, index

    def select_index(self, recipe_id):
        book = RecipeBook(self.database)
        book.cursor.execute("""
            SELECT r.id
            FROM Recipe r
            """)
        r_id = book.cursor.fetchall()
        if r_id:
            for i in range(len(r_id)):
                print(r_id[i], recipe_id)
                if r_id[i][0] == recipe_id:
                    return i
        return None

    def populate(self):
        recipe, r_id, self.index = self.select_recipe(self.index)

        name = recipe[0][1] if r_id else "<Name>"
        description = recipe[0][2] if r_id else "<Description>"
        directions = recipe[0][3] if r_id else "<Directions>"
        servings = recipe[0][4] if r_id else "<Servings>"
        ingredients = []
        if r_id:
            for i in recipe[1]:
                ingredients.append(i)
        else:
            ingredients.append(("<Amount>", "<Unit>", "<Ingredient>"))

        self.name_label.config(text=name)
        self.serv_label.config(text="Serves {}".format(servings))
        self.desc_label.config(text=description)
        for i in self.ingr_label_list:
            i[0].destroy()
            i[1].destroy()
            i[2].destroy()
        row = 5
        self.ingr_label_list = []
        for i in ingredients:
            self.ingr_label_list.append((Label(self.frame, text=i[0], bg="white", font=("Times", 10, "")),
                Label(self.frame, text=i[1], bg="white", font=("Times", 10, "")),
                Label(self.frame, text=i[2], bg="white", font=("Times", 10, ""))))
            self.ingr_label_list[row-5][0].grid(row=row, column=0, sticky=W)
            self.ingr_label_list[row-5][1].grid(row=row, column=1, sticky=W)
            self.ingr_label_list[row-5][2].grid(row=row, column=2, columnspan=2, sticky=W)
            row+=1
        self.blank_label_2.destroy()
        self.blank_label_2 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_2.grid(row=row, column=1, sticky=W)
        self.dir_label_title.destroy()
        self.dir_label_title = Label(self.frame, text="Directions", bg="white", font=("Times", 12, "bold"))
        self.dir_label_title.grid(row=row+1, column=0, columnspan=3, sticky=W)
        self.dir_label.destroy()
        self.dir_label = Label(self.frame, text=directions, bg="white", font=("Times", 10, ""), justify=LEFT)
        self.dir_label.grid(row=row+2, column=0, columnspan=3, sticky=W)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def shift_left(self):
        self.index+=1
        self.populate()

    def shift_right(self):
        self.index-=1
        self.populate()

    def edit_recipe(self, start_new=False):
        if start_new:
            recipe = None
        else:
            recipe, r_id, self.index = self.select_recipe(self.index)
        w = RecipeCreationWindow(Toplevel(self), self.database, self.root, recipe)
        self.wait_window(w)
        if w.final:
            book = RecipeBook(self.database)
            book.cursor.execute("""
                SELECT r.id
                FROM Recipe r
                WHERE r.name = ?
                """, [w.final])
            r_id = book.cursor.fetchone()[0]
            book.close()
            next_index = self.select_index(r_id)
            print(next_index)
            self.index =  next_index if next_index else self.index
            self.populate()

    def create_recipe(self):
        self.edit_recipe(True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run the recipe manager GUI.')
    parser.add_argument('-d', '--database', default="recipe_data.db",
                        help='The database file you wish to use.')
    args = parser.parse_args()
    root = Tk()
    my_gui = RecipeManagerWindow(root, args.database)
    root.mainloop()
