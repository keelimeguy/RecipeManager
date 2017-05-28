try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from ..structure.color_scheme import *

version = '0.6.5'

class AboutWindow(object):

    def __init__(self, root):
        self.root = root
        self.master = Toplevel(root)
        self.master.title("About")
        self.master.resizable(False, False)
        self.master.config(bg=BG_COLOR)

        # Setup the widgets in the window
        label = Label(self.master, text=self.get_text(), justify=LEFT, bg=BG_COLOR)
        label.grid(row = 1, column = 0, columnspan = 2, sticky=W)

        self.master.grab_set()

    def get_text(self):
        return """    ------------Recipe Manager------------

    Simply manage your personal recipes.

    version: {}
    author:  Keelin Wheeler
    website: https://github.com/keelimeguy    """.format(version)
