try:
    from Tkinter import *
except ImportError:
    from tkinter import *

from color_scheme import *

class ModalWindow(object):

    def __init__(self, root, title, text):
        self.choice = None

        # Setup the window
        self.modalWindow = Toplevel(root)
        self.modalWindow.title(title)
        self.modalWindow.resizable(False, False)
        self.modalWindow.config(bg=BG_COLOR)

        # Setup the widgets in the window
        label = Label(self.modalWindow, text = text, font = '-size 10')
        label.grid(row = 0, column = 0, columnspan = 2, padx = 2, pady = 2)

        but = Button(self.modalWindow, text = 'Yes', command = self.choiceYes)
        but.grid(row = 1, column = 0, sticky = 'nsew', padx = 2, pady = 5)

        but = Button(self.modalWindow, text = 'No', command = self.choiceNo)
        but.grid(row = 1, column = 1, sticky = 'nsew', padx = 2, pady = 5)

        self.modalWindow.rowconfigure(1, minsize = 40)
        self.modalWindow.grab_set()

    def choiceYes(self):
        self.choice = 'Yes'
        self.modalWindow.destroy()

    def choiceNo(self):
        self.choice = 'No'
        self.modalWindow.destroy()
