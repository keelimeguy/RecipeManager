try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import os
import json

from .structure.color_scheme import *
from .structure.insertion_listbox import InsertionListbox

class RecipeFormatEditWindow(object):

    def __init__(self, root, manager, preference_file):
        self.root = root
        self.manager = manager
        self.master = Toplevel(root)
        self.master.title("Edit Recipe Format")
        self.master.resizable(False, False)
        self.master.config(bg=BG_COLOR)

        self.preference_file = preference_file

        # Setup the widgets in the window
        label = Label(self.master, text="Add entries to the right side then drag and drop them into the desired order.", justify=LEFT, bg=BG_COLOR)
        label.grid(row = 0, column = 0, columnspan = 4, sticky=W)

        self.listbox = InsertionListbox(self.master, True)
        self.listbox.grid(row = 1, column = 0, columnspan = 4)

        self.done_button = Button(self.master, text="Done", command=self.format, highlightbackground=BG_COLOR)
        self.done_button.grid(row=2, column=1, sticky=E)
        self.cancel_button = Button(self.master, text="Cancel", command=self.master.destroy, highlightbackground=BG_COLOR)
        self.cancel_button.grid(row=2, column=2, sticky=W)

        self.master.grab_set()
        self.recipe_format = {}
        self.setup()

    def setup(self):
        current_dir = os.getcwd()
        if not os.path.isfile(os.path.join(current_dir,self.preference_file)):
            if self.manager.is_wind:
                self.recipe_format = {"database":os.path.join(current_dir,"recipe_data.db"), "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
            else:
                self.recipe_format = {"database":os.path.join(os.path.expanduser("~"),"Documents/recipe_data.db"), "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
            with open(os.path.join(current_dir,self.preference_file),"r") as f:
                json.dump(self.recipe_format, f)
        else:
            with open(os.path.join(current_dir,self.preference_file),"r") as f:
                    self.recipe_format = json.load(f)
                    if self.recipe_format["name"]!=1:
                        raise ValueError("Key \"name\" must have value \"1\" in {}".format(self.preference_file))
        for k, v in sorted(self.recipe_format.items(), key=lambda x: (0,x[0]) if (isinstance(x[1], list) or isinstance(x[1], str)) else (x[1],x[0])):
            if not k in ["database", "tips_index", "seed", "show_tips"]:
                if v > 0:
                    self.listbox.insert(END, k.replace(' ', '').replace('_', ' ').title())
                else:
                    self.listbox.insert_unused(END, k.replace(' ', '').replace('_', ' ').title())

    def format(self):
        for i in range(self.listbox.size()):
            self.recipe_format[self.listbox.get(i).replace(' ', '_').lower()] = i+1
        for i in range(self.listbox.size_unused()):
            self.recipe_format[self.listbox.get_unused(i).replace(' ', '_').lower()] = 0

        current_dir = os.getcwd()
        with open(os.path.join(current_dir,self.preference_file),"w") as f:
            json.dump(self.recipe_format, f)

        self.master.destroy()