from Tkinter import *

version = '0.4.1'

class DocumentationWindow(object):

    def __init__(self, root):
        self.root = root
        self.master = Toplevel(root)
        self.master.title("Documentation")
        self.master.resizable(False, False)

        # Setup the widgets in the window
        label = Label(self.master, text="Using Recipe Manager")
        label.grid(row = 0, column = 0, columnspan = 2, padx = 2, pady = 2)

        label2 = Label(self.master, text=self.get_text(), justify=LEFT)
        label2.grid(row = 1, column = 0, columnspan = 2, sticky=W)

        self.master.grab_set()

    def get_text(self):
        return """    After start up you will be in the list view. Here you can search through the saved recipes. A normal search will
    search through the name and notes sections of a recipe. You can also sort entries by clicking the column headers.

    To start a search, press the enter key after typing or press the search button. An empty search returns all recipes.
    Examples:
        "toast"
        "vegan"
        "prep<10"
        "cook=10"
        "serves>=5"
    Notice that you can also search according to the values in the "prep, "cook", and "serves" fields.

    You can search multiple terms using "|" (OR), "&" (AND), and "~" (NOT).
    Examples:
        "vegan&~breakfast"   - will search all recipes with the word 'vegan' but without the word 'breakfast'
        "toast|prep=0"   - will search all recipes that either contain the word 'toast' or have 0 prep time
    This functionality is made user friendly in the advanced search window.

    The button labeled '..' next to the search button will open the advanced search window. Here you can enter your
    search terms in the logical fields separated by ', ' (a simple space without a comma will work as well). Search
    terms follow the same rules as the normal search box, that is, you can still enter terms like "serves<=2".

    Click on a recipe in the list to view its details. Press the left or right arrow buttons at the top of this recipe
    view mode to cycle through the recipes from the most recent search. You can also edit recipes in this view.

    You may manage separate recipe books in different database (.db) files. You can load a recipe book under the "File"
    option in the menu bar. You can also import or export all recipes in the current recipe book into other existing
    recipe books. You can change the default recipe book (which opens at startup) under the "Preferences" menu option.    \n
    All else should be easy to pick up. Let me know your suggestions/feedback.

    Enjoy!""".format(version)
