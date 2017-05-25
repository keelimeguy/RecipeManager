try:
    from Tkinter import *
except ImportError:
    from tkinter import *

if __debug__:
    from recipe_book import RecipeBook
    from modal_window import ModalWindow
else:
    from recipe_manager.recipe_book import RecipeBook
    from recipe_manager.modal_window import ModalWindow
from recipe_creation_window import RecipeCreationWindow

class RecipeViewWindow(Frame):
    def __init__(self, root, database, manager, preferences, index=0, id_list=None, search=None):
        Frame.__init__(self, root)
        self.manager = manager
        self.root = root
        self.header = Frame(root)
        self.under_header = Frame(root)
        self.window = Frame(self.under_header)
        self.footer = Frame(self.under_header)
        self.header.pack(fill=BOTH)
        self.under_header.pack(fill=BOTH, expand=YES)
        self.footer.pack(fill=BOTH, side=BOTTOM)
        self.window.pack(fill=BOTH, expand=YES, side=BOTTOM)
        self.root.bind("<Left>", self.shift_left)
        self.root.bind("<Right>", self.shift_right)
        self.root.bind("<Up>", self.shift_up)
        self.root.bind("<Down>", self.shift_down)
        self.preferences = preferences

        self.first=True
        self.destroyed=False

        self.canvas = Canvas(self.window, borderwidth=0, background="#ffffff", width=450, height=560)
        self.vsb = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.hsb = Scrollbar(self.footer, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.header.grid_rowconfigure(0, weight=1)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_rowconfigure(5, weight=1)
        self.header.grid_columnconfigure(5, weight=1)

        self.button_left = Button(self.header, text="<", command=self.shift_left)
        self.button_right = Button(self.header, text=">", command=self.shift_right)
        self.button_left.grid(row=0, column=0, sticky=W)
        self.button_right.grid(row=0, column=5, sticky=E)
        self.button_remove = Button(self.header, text="Remove Recipe", command=self.remove_recipe)
        self.button_remove.grid(row=0, column=1, sticky=E)
        self.button_edit = Button(self.header, text="Edit Recipe", command=self.edit_recipe)
        self.button_edit.grid(row=0, column=2, sticky=EW)
        self.button_edit = Button(self.header, text="Refresh", command=self.populate)
        self.button_edit.grid(row=0, column=3, sticky=EW)
        self.button_browse = Button(self.header, text="Back to Browse", command=self.browse_recipe)
        self.button_browse.grid(row=0, column=4, sticky=W)

        self.database = database

        self.vsb.pack(fill=BOTH, side=RIGHT)
        self.canvas.pack(fill=BOTH, expand=YES, side=RIGHT)
        self.hsb.pack(fill=BOTH)

        self.canvas_width = self.canvas.winfo_reqwidth() - 4
        self.canvas_height = self.canvas.winfo_reqheight() - 4

        self.frame = Frame(self.canvas, background="#ffffff", width=self.canvas_width, height=self.canvas_height)
        self.frame_id = self.canvas.create_window((4,4), window=self.frame, anchor=N+W,
                                  tags="self.frame")

        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)

        self.name_label = Label(self.frame, text="Name", bg="white", font=("Times", 18, "bold"), wraplength=self.canvas_width)
        self.name_label.grid(row=0, column=0, columnspan=6, sticky=W)
        self.serv_label = Label(self.frame, text="Servings", bg="white", font=("Times", 10, ""), justify=LEFT)
        self.serv_label.grid(row=1, column=0, sticky=W)
        self.prep_label = Label(self.frame, text="Prep Time", bg="white", font=("Times", 10, ""), justify=LEFT)
        self.prep_label.grid(row=1, column=1, sticky=W)
        self.cook_label = Label(self.frame, text="Cook Time", bg="white", font=("Times", 10, ""), justify=LEFT)
        self.cook_label.grid(row=1, column=2, sticky=W)
        self.desc_label = Label(self.frame, text="Description", bg="white", font=("Times", 12, "italic"), justify=LEFT, wraplength=self.canvas_width)
        self.desc_label.grid(row=2, column=0, columnspan=6, sticky=W)
        self.blank_label_1 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_1.grid(row=3, column=1, sticky=W)
        self.ingr_label_title = Label(self.frame, text="Ingredients", bg="white", font=("Times", 12, "bold"))
        self.ingr_label_title.grid(row=4, column=0, columnspan=3, sticky=W)
        self.ingr_label_list = []
        row = 5
        self.ingr_label_list.append((Label(self.frame, text="Amount", bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=40),
            Label(self.frame, text="Unit", bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width*3/8),
            Label(self.frame, text="Ingredient", bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width*3/8)))
        self.ingr_label_list[0][0].grid(row=row, column=0, sticky=W+N)
        self.ingr_label_list[0][1].grid(row=row, column=1, sticky=W+N)
        self.ingr_label_list[0][2].grid(row=row, column=2, columnspan=2, sticky=W+N)
        row+=1
        self.blank_label_2 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_2.grid(row=row, column=1, sticky=W)
        self.dir_label_title = Label(self.frame, text="Directions", bg="white", font=("Times", 12, "bold"))
        self.dir_label_title.grid(row=row+1, column=0, columnspan=3, sticky=W)
        self.dir_label = Label(self.frame, text="Direction", bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width)
        self.dir_label.grid(row=row+2, column=0, columnspan=3, sticky=W)
        self.blank_label_3 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_3.grid(row=row+3, column=1, sticky=W)
        self.note_label_title = Label(self.frame, text="Notes", bg="white", font=("Times", 12, "bold"))
        self.note_label_title.grid(row=row+4, column=0, columnspan=3, sticky=W)
        self.note_label = Label(self.frame, text="Note", bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width)
        self.note_label.grid(row=row+5, column=0, columnspan=3, sticky=W)

        self.index = index
        self.id_list = id_list
        self.search = search
        self.populate()

    def _bound_to_mousewheel(self, event):
        self.bind_all("<MouseWheel>", self.on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units") # Windows
        # self.canvas.yview_scroll(-1*(event.delta), "units") # OS X

    def destroy(self):
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.header.destroy()
        self.under_header.destroy()
        self.window.destroy()
        self.footer.destroy()
        self.destroyed = True

    def populate(self):
        self.canvas.yview(MOVETO, 0)
        self.canvas.xview(MOVETO, 0)
        book = RecipeBook(self.database)
        recipe, r_id, self.index = book.select_recipe(self.index, self.id_list)
        book.close()
        name = recipe[0][1] if r_id and recipe[0] else "<Name>"
        description = recipe[0][2] if r_id and recipe[0] else "<Description>"
        directions = recipe[0][3] if r_id and recipe[0] else "<Directions>"
        servings = recipe[0][4] if r_id and recipe[0] else "<Servings>"
        notes = recipe[0][5] if r_id and recipe[0] else "<Notes>"
        prep_time = recipe[0][6] if r_id and recipe[0] else "<Prep Time>"
        cook_time = recipe[0][7] if r_id and recipe[0] else "<Cook Time>"
        ingredients = []
        if r_id and recipe:
            for i in sorted(recipe[1], key=lambda tup: tup[3]):
                ingredients.append(i)
        else:
            ingredients.append(("<Amount>", "<Unit>", "<Ingredient>", "<Order>"))

        self.name_label.destroy()
        self.name_label = Label(self.frame, text=name, bg="white", font=("Times", 18, "bold"), wraplength=self.canvas_width)
        self.name_label.grid(row=0, column=0, columnspan=6, sticky=W)
        self.serv_label.config(text="Serves {}    ".format(servings))
        self.prep_label.config(text="    Prep: {} min.    ".format(prep_time))
        self.cook_label.config(text="    Cook: {} min.".format(cook_time))
        self.desc_label.destroy()
        self.desc_label = Label(self.frame, text=description, bg="white", font=("Times", 12, "italic"), justify=LEFT, wraplength=self.canvas_width)
        self.desc_label.grid(row=2, column=0, columnspan=6, sticky=W)
        for i in self.ingr_label_list:
            i[0].destroy()
            i[1].destroy()
            i[2].destroy()
        row = 5
        self.ingr_label_list = []
        for i in ingredients:
            self.ingr_label_list.append((Label(self.frame, text=i[0], bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=40),
                Label(self.frame, text=i[1], bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width*3/8),
                Label(self.frame, text=i[2], bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width*3/8)))
            self.ingr_label_list[row-5][0].grid(row=row, column=0, sticky=W+N)
            self.ingr_label_list[row-5][1].grid(row=row, column=1, sticky=W+N)
            self.ingr_label_list[row-5][2].grid(row=row, column=2, columnspan=2, sticky=W+N)
            row+=1
        self.blank_label_2.destroy()
        self.blank_label_2 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_2.grid(row=row, column=1, sticky=W)
        self.dir_label_title.destroy()
        self.dir_label_title = Label(self.frame, text="Directions", bg="white", font=("Times", 12, "bold"))
        self.dir_label_title.grid(row=row+1, column=0, columnspan=3, sticky=W)
        self.dir_label.destroy()
        self.dir_label = Label(self.frame, text=directions, bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width)
        self.dir_label.grid(row=row+2, column=0, columnspan=3, sticky=W)
        self.blank_label_3.destroy()
        self.blank_label_3 = Label(self.frame, text="", bg="white", height=1)
        self.blank_label_3.grid(row=row+3, column=1, sticky=W)
        self.note_label_title.destroy()
        self.note_label_title = Label(self.frame, text="Notes", bg="white", font=("Times", 12, "bold"))
        self.note_label_title.grid(row=row+4, column=0, columnspan=3, sticky=W)
        self.note_label.destroy()
        self.note_label = Label(self.frame, text=notes, bg="white", font=("Times", 10, ""), justify=LEFT, wraplength=self.canvas_width)
        self.note_label.grid(row=row+5, column=0, columnspan=3, sticky=W)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def onCanvasConfigure(self, event):
        self.canvas_width = event.width-4
        self.canvas_height = event.height-4
        self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
        if self.first:
            self.populate()
            self.first=False

    def shift_left(self, event=None):
        self.index-=1
        self.populate()

    def shift_right(self, event=None):
        self.index+=1
        self.populate()

    def shift_up(self, event=None):
        shift_delta = 1
        self.canvas.yview_scroll(-1*(shift_delta), "units") # Windows
        # self.canvas.yview_scroll(-1*(shift_delta*120), "units") # OS X

    def shift_down(self, event=None):
        shift_delta = 1
        self.canvas.yview_scroll(shift_delta, "units") # Windows
        # self.canvas.yview_scroll(shift_delta*120, "units") # OS X

    def edit_recipe(self):
        book = RecipeBook(self.database)
        recipe, r_id, self.index = book.select_recipe(self.index, self.id_list)
        book.close()
        w = RecipeCreationWindow(Toplevel(self), self.database, self.root, recipe)
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
        if old_id in self.id_list:
            self.id_list = [r_id if x==old_id else x for x in self.id_list]
        else:
            self.id_list.append(r_id)
        book = RecipeBook(self.database)
        next_index = book.select_index(r_id, self.id_list)
        self.index =  next_index if next_index else self.index
        self.populate()

    def browse_recipe(self):
        self.manager.browse()

    def remove_recipe(self):
        book = RecipeBook(self.database)
        recipe, r_id, index = book.select_recipe(self.index, self.id_list)
        d = ModalWindow(self, "Delete Recipe", "Are you sure you want to delete {}?".format(recipe[0][1]))
        d.modalWindow.focus()
        self.wait_window(d.modalWindow)
        if d.choice == 'Yes':
            book.delete(r_id)
            book.close()
            self.id_list.remove(r_id)
            self.populate()
        else:
            book.close()
