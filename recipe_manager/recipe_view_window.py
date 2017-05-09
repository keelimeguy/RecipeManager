from Tkinter import *

from recipe_book import RecipeBook
from recipe_creation_window import RecipeCreationWindow
from modal_window import ModalWindow

class RecipeViewWindow(Frame):
    def __init__(self, root, database, manager, index=0, id_list=None, search=None):
        Frame.__init__(self, root)
        self.manager = manager
        self.window = Frame(root)
        self.window.grid(row=0, column=0)
        self.root = root
        self.canvas = Canvas(self.window, borderwidth=0, background="#ffffff", width=400, height=560)
        self.frame = Frame(self.canvas, background="#ffffff")
        self.vsb = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.window, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.button_left = Button(self.window, text="<", command=self.shift_left)
        self.button_right = Button(self.window, text=">", command=self.shift_right)
        self.button_left.grid(row=0, column=0, sticky=W)
        self.button_right.grid(row=0, column=11, sticky=E)

        self.button_edit = Button(self.window, text="Remove Recipe", command=self.remove_recipe)
        self.button_edit.grid(row=0, column=3, sticky=EW)

        self.button_edit = Button(self.window, text="Edit Recipe", command=self.edit_recipe)
        self.button_edit.grid(row=0, column=4, sticky=EW)

        self.button_browse = Button(self.window, text="Back to Browse", command=self.browse_recipe)
        self.button_browse.grid(row=0, column=5, sticky=EW)

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
        self.serv_label.grid(row=1, column=0, sticky=W)
        self.prep_label = Label(self.frame, text="Prep Time", bg="white", font=("Times", 10, ""))
        self.prep_label.grid(row=1, column=1, sticky=W)
        self.cook_label = Label(self.frame, text="Cook Time", bg="white", font=("Times", 10, ""))
        self.cook_label.grid(row=1, column=2, sticky=W)
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
        self.blank_label_3 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_3.grid(row=row+3, column=1, sticky=W)
        self.note_label_title = Label(self.frame, text="Notes", bg="white", font=("Times", 12, "bold"))
        self.note_label_title.grid(row=row+4, column=0, columnspan=3, sticky=W)
        self.note_label = Label(self.frame, text="Note", bg="white", font=("Times", 10, ""))
        self.note_label.grid(row=row+5, column=0, columnspan=3, sticky=W)

        self.index = index
        self.id_list = id_list
        self.search = search
        self.populate()

    def populate(self):
        book = RecipeBook(self.database)
        recipe, r_id, self.index = book.select_recipe(self.index, self.id_list)
        book.close()

        name = recipe[0][1] if r_id else "<Name>"
        description = recipe[0][2] if r_id else "<Description>"
        directions = recipe[0][3] if r_id else "<Directions>"
        servings = recipe[0][4] if r_id else "<Servings>"
        notes = recipe[0][5] if r_id else "<Notes>"
        prep_time = recipe[0][6] if r_id else "<Prep Time>"
        cook_time = recipe[0][7] if r_id else "<Cook Time>"
        ingredients = []
        if r_id:
            for i in recipe[1]:
                ingredients.append(i)
        else:
            ingredients.append(("<Amount>", "<Unit>", "<Ingredient>"))

        self.name_label.config(text=name)
        self.serv_label.config(text="Serves {}    ".format(servings))
        self.prep_label.config(text="    Prep: {} min.    ".format(prep_time))
        self.cook_label.config(text="    Cook: {} min.".format(cook_time))
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
        self.blank_label_3.destroy()
        self.blank_label_3 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_3.grid(row=row+3, column=1, sticky=W)
        self.note_label_title.destroy()
        self.note_label_title = Label(self.frame, text="Notes", bg="white", font=("Times", 12, "bold"))
        self.note_label_title.grid(row=row+4, column=0, columnspan=3, sticky=W)
        self.note_label.destroy()
        self.note_label = Label(self.frame, text=notes, bg="white", font=("Times", 10, ""))
        self.note_label.grid(row=row+5, column=0, columnspan=3, sticky=W)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def shift_left(self):
        self.index-=1
        self.populate()

    def shift_right(self):
        self.index+=1
        self.populate()

    def edit_recipe(self):
        book = RecipeBook(self.database)
        recipe, r_id, self.index = book.select_recipe(self.index, self.id_list)
        book.close()
        old_id = r_id
        w = RecipeCreationWindow(Toplevel(self), self.database, self.root, recipe)
        self.wait_window(w)
        if w.final != None:
            book = RecipeBook(self.database)
            book.cursor.execute("""
                SELECT r.id
                FROM Recipe r
                WHERE r.name = ?
                """, [w.final])
            r_id = book.cursor.fetchone()[0]
            self.id_list = [r_id if x==old_id else x for x in self.id_list]
            next_index = book.select_index(r_id, self.id_list)
            book.close()
            self.index =  next_index if next_index else self.index
            self.populate()

    def browse_recipe(self):
        self.manager.browse()

    def remove_recipe(self):
        d = ModalWindow(self, "Delete Recipe", "Do you want to delete the current recipe?")
        self.wait_window(d.modalWindow)
        if d.choice == 'No':
            return
        book = RecipeBook(self.database)
        book.delete(book.select_recipe(self.index, self.id_list)[1])
        book.close()
        self.id_list.remove(self.id_list[self.index])
        self.populate()
