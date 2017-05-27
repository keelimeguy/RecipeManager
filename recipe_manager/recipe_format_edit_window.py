try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import os
import json

from structure.insertion_listbox import InsertionListbox

class RecipeFormatEditWindow(object):

    def __init__(self, root, preference_file):
        self.root = root
        self.master = Toplevel(root)
        self.master.title("Edit Recipe Format")
        self.master.resizable(False, False)

        self.preference_file = preference_file

        # Setup the widgets in the window
        label = Label(self.master, text="Add entries to the right side then drag and drop them into the desired order.", justify=LEFT)
        label.grid(row = 0, column = 0, columnspan = 4, sticky=W)

        self.listbox = InsertionListbox(self.master, True)
        self.listbox.grid(row = 1, column = 0, columnspan = 4)

        self.done_button = Button(self.master, text="Done", command=self.format)
        self.done_button.grid(row=2, column=1, sticky=E)
        self.cancel_button = Button(self.master, text="Cancel", command=self.master.destroy)
        self.cancel_button.grid(row=2, column=2, sticky=W)

        self.master.grab_set()
        self.recipe_format = {}
        self.setup()

    def setup(self):
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
        for k, v in sorted(self.recipe_format.iteritems(), key=lambda (k,v): (v,k)):
            if not k in ["database"]:
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