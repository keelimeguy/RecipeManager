from Tkinter import *

version = '0.4.3'

class AboutWindow(object):

    def __init__(self, root):
        self.root = root
        self.master = Toplevel(root)
        self.master.title("About")
        self.master.resizable(False, False)

        # Setup the widgets in the window
        label = Label(self.master, text=self.get_text(), justify=LEFT)
        label.grid(row = 1, column = 0, columnspan = 2, sticky=W)

        self.master.grab_set()

    def get_text(self):
        return """    ------------Recipe Manager------------

    Simply manage your personal recipes.

    version: {}
    author:  Keelin Wheeler
    website: https://github.com/keelimeguy    """.format(version)
