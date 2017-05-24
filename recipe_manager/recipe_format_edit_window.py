from Tkinter import *
import os
import json

from drag_drop_listbox import DragDropListbox

class RecipeFormatEditWindow(object):

    def __init__(self, root, preference_file):
        self.root = root
        self.master = Toplevel(root)
        self.master.title("Edit Recipe Format")
        self.master.resizable(False, False)

        self.preference_file = preference_file

        # Setup the widgets in the window
        label = Label(self.master, text="Add desired entries to the right side and drag and drop them into the desired order.", justify=LEFT)
        label.grid(row = 0, column = 0, columnspan = 4, sticky=W)

        self.listbox_unused = Listbox(self.master)
        self.listbox_unused.grid(row = 1, column = 0, rowspan=6, sticky=EW)

        self.add_button = Button(self.master, text=">", command=self.add)
        self.add_button.grid(row=3, column=1, columnspan=2, sticky=S)
        self.remove_button = Button(self.master, text="<", command=self.remove)
        self.remove_button.grid(row=4, column=1, columnspan=2, sticky=N)

        self.listbox = DragDropListbox(self.master, True)
        self.listbox.grid(row = 1, column = 3, rowspan=6, sticky=EW)

        self.done_button = Button(self.master, text="Done", command=self.format)
        self.done_button.grid(row=7, column=1, sticky=E)
        self.cancel_button = Button(self.master, text="Cancel", command=self.master.destroy)
        self.cancel_button.grid(row=7, column=2, sticky=W)

        self.master.grab_set()
        self.recipe_format = {}
        self.setup()

    def setup(self):
        current_dir = os.getcwd()
        if not os.path.isfile(os.path.join(current_dir,self.preference_file)):
            with open(os.path.join(current_dir,self.preference_file),"w") as f:
                self.recipe_format = {"database":"recipe_data.db", "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4}
                json.dump(self.recipe_format, f)
        else:
            with open(os.path.join(current_dir,self.preference_file),"r") as f:
                    self.recipe_format = json.load(f)
                    if self.recipe_format["name"]!=1:
                        raise ValueError("Key \"name\" must have value \"1\" in {}".format(self.preference_file))
        for k, v in sorted(self.recipe_format.iteritems(), key=lambda (k,v): (v,k)):
            if v > 0:
                self.listbox.insert(END, k.replace(' ', '').replace('_', ' ').title())
            else if not k in ["database"]:
                self.listbox_unused.insert(END, k.replace(' ', '').replace('_', ' ').title())

    def add(self):
        pass

    def remove(self):
        pass

    def format(self):
        for i in range(self.listbox.size()):
            self.recipe_format[self.listbox.get(i).replace(' ', '_').lower()] = i
            self.listbox.delete(i)
        while self.listbox_unused.size()>0:
            self.recipe_format[self.listbox_unused.get(0).replace(' ', '_').lower()] = 0
            self.listbox.delete(0)

        if self.recipe_format["name"]!=1:
            raise ValueError("Key \"name\" must have value \"1\" in {}".format(self.preference_file))

        current_dir = os.getcwd()
        with open(os.path.join(current_dir,self.preference_file),"w") as f:
            json.dump(self.recipe_format, f)
