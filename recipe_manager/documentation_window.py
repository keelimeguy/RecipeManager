try:
    from Tkinter import *
except ImportError:
    from tkinter import *

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
        return """    After start up you will be in the list view. Here you can create recipes and search through the
    saved recipes. A normal search will search through the name and notes sections of a recipe. You can also sort
    entries by clicking the column headers.

    To start a search, press the enter key after typing or press the search button. An empty search returns all recipes.
    Examples:
        "toast"
        "vegan"
        "ingr:turnip"
        "prep<10"
        "cook=10"
        "serves>=5"
    Notice that you can also search according to the values in the following fields:
    - Yield (using "serve", "serves", "yield", or "yields")
    - Prep Time (using "prep" or "prep_time")
    - Cook Time (using "cook" or "cook_time")
    - Ingredients (using "ingr" or "ingredient" followed by ':' and the desired search text)

    You can search multiple terms using "|" (OR), "&" (AND), and "~" (NOT).
    Examples:
        "vegan&~breakfast"   - will search all recipes with the word 'vegan' but without the word 'breakfast'
        "toast|prep=0"   - will search all recipes that either contain the word 'toast' or have 0 prep time
        "ingr:salt&~ingr:pepper"   - will search all recipes with 'salt' in their ingredient list but not 'pepper'
    This functionality is made user friendly in the advanced search window, described below.

    The button labeled '..' (next to the search button) will open the advanced search window. Here you can enter your
    search terms in the logical fields separated by ', ' (a simple space without a comma will work as well). Search
    terms follow the same rules as the normal search box, that is, you can still enter terms like "yield<=2".

    Click on a recipe in the list to view its details. Press the left or right arrow buttons at the top of this recipe
    view mode to cycle through the recipes from the most recent search. You can also edit recipes from this view by
    pressing the "Edit Recipe" button. Note that when editing or creating a recipe, the order of the ingredients in the
    ingredient list box corresponds to the order they appear in the recipe view window. To add an ingredient, fill in
    the amount, unit, and name fields then press the "+" button. Selecting an ingredient in the list and pressing "-"
    will remove that ingredient.

    You may manage separate recipe books in different database (.db) files. You can load a recipe book under the "File"
    option in the menu bar. You can also import or export all recipes in the current recipe book into other existing
    recipe books. You can change the default recipe book (which opens at startup) under the "Preferences" menu option.
    From this preferences menu you can also adjust the format of recipes in the list view, choosing what fields are shown    \n    and in what order.

    Please let me know your suggestions and feedback.

    Enjoy!""".format(version)
