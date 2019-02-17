#!/usr/bin/env python

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

import random
import json
import sys
import os

from ..structure.color_scheme import *

class TipWindow(object):
    def __init__(self, root, preference_file):

        self.master = Toplevel(root)
        self.master.title("Tips")
        self.master.resizable(False, False)
        self.master.config(bg=BG_COLOR)

        self.preference_file = preference_file

        self.label = Label(self.master, text = self.next_tip(), font = '-size 10', bg=BG_COLOR, wraplength=280)
        self.label.grid(row = 0, column = 0, columnspan = 2, padx = 2, pady = 2)

        but = Button(self.master, text = 'Another Tip', command = self.another, highlightbackground=BG_COLOR)
        but.grid(row = 1, column = 0, sticky = 'nsew', padx = 2, pady = 5)

        but = Button(self.master, text = 'Continue', command = self.master.destroy, highlightbackground=BG_COLOR)
        but.grid(row = 1, column = 1, sticky = 'nsew', padx = 2, pady = 5)

        self.master.rowconfigure(1, minsize = 40)
        self.master.attributes("-topmost", True)
        self.master.grab_set()

    def another(self):
        self.label.config(text=self.next_tip())

    def next_tip(self):
        current_dir = os.getcwd()
        lines = []


        if not os.path.isfile(os.path.join(current_dir,self.preference_file)):
            with open(os.path.join(current_dir,self.preference_file),"w") as f:
                recipe_format = {"database":filename, "name": 1, "description": 0, "instructions": 0, "yield": 2, "notes": 5, "prep_time": 3, "cook_time": 4, "tips_index": (0,0)}
                json.dump(recipe_format, f)
                tips_index = [0,0]
                seed = random.randint(0,sys.maxsize)
        else:
            with open(os.path.join(current_dir,self.preference_file),"r") as f:
                recipe_format = json.load(f)
                tips_index = recipe_format.get("tips_index", None)
                seed = recipe_format.get("seed", None)
            if tips_index == None:
                tips_index = [0,0]
            if seed == None:
                seed = random.randint(0,sys.maxsize)


        if __debug__:
            docs_dir = os.path.join(os.path.join(current_dir, "recipe_manager"), "docs")
            if os.path.isfile(os.path.join(docs_dir, "tips.txt")):
                with open(os.path.join(docs_dir, "tips.txt"), 'r') as f:
                    for line in f:
                        if len(line.strip())>0:
                            if "---" in line:
                                next_line = list(i.strip() for i in line.split("---"))
                            else:
                                next_line = [line.strip()]
                            lines.append(next_line)
        else:
            # path = os.path.join(sys._MEIPASS, "docs")
            path = os.path.join(os.getcwd(), "text")
            if os.path.isfile(os.path.join(path, "tips.txt")):
                with open(os.path.join(path, "tips.txt"), 'r') as f:
                    for line in f:
                        if len(line.strip())>0:
                            if "---" in line:
                                next_line = list(i.strip() for i in line.split("---"))
                            else:
                                next_line = [line.strip()]
                            lines.append(next_line)

        random.Random(seed).shuffle(lines)

        if tips_index[0]>=len(lines):
            tips_index[0] = len(lines)-1
        cur_line = lines[tips_index[0]]
        if tips_index[1]>=len(cur_line):
            tips_index[1] = len(cur_line)-1
        cur_tip = cur_line[tips_index[1]]
        if len(cur_line)-1 > tips_index[1]:
            tips_index = [tips_index[0], tips_index[1]+1]
        elif len(lines)-1 > tips_index[0]:
            tips_index = [tips_index[0]+1, 0]
        else:
            tips_index = [0, 0]
            seed+=1

        with open(os.path.join(current_dir,self.preference_file),"w") as f:
            recipe_format["tips_index"] = tips_index
            recipe_format["seed"] = seed
            json.dump(recipe_format, f)

        return cur_tip if cur_tip!=None else "Tips can be shown at startup. Cool huh?"
