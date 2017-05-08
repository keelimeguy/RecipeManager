import sqlite3

class RecipeBook:
    def __init__(self, database=None):
        if database == None:
            raise ValueError("Must specify database. None received.")
        self.database = database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.make_tables()

    def __str__(self):
        self.cursor.execute("""
        SELECT r.name AS 'Recipe',
        ri.amount AS 'Amount',
        mu.name AS 'Unit of Measure',
        i.name AS 'Ingredient'
        FROM Recipe r
        JOIN RecipeIngredient ri on r.id = ri.recipe_id
        JOIN Ingredient i on i.id = ri.ingredient_id
        LEFT OUTER JOIN Measure mu on mu.id = measure_id"""
        )

        result = self.cursor.fetchall()
        ret = ""
        for r in result:
            ret += str(r)
        return ret

    def __del__(self):
        self.close()

    def purge(self):
        self.cursor.execute("DROP TABLE IF EXISTS Recipe")
        self.cursor.execute("DROP TABLE IF EXISTS Ingredient")
        self.cursor.execute("DROP TABLE IF EXISTS Measure")
        self.cursor.execute("DROP TABLE IF EXISTS RecipeIngredient")
        self.close()
        self.__init__(self.database)

    def make_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recipe (
            id INTEGER PRIMARY KEY,
            name VARCHAR(25),
            description VARCHAR(50),
            instructions VARCHAR(500),
            yield Integer,
            notes VARCHAR(100),
            UNIQUE(name));"""
        )

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ingredient (
            id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            UNIQUE(name));"""
        )

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Measure (
            id INTEGER PRIMARY KEY,
            name VARCHAR(30),
            UNIQUE(name));"""
        )

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS RecipeIngredient (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            measure_id INTEGER,
            amount REAL,
            CONSTRAINT fk_recipe FOREIGN KEY(recipe_id) REFERENCES Recipe(id),
            CONSTRAINT fk_ingredient FOREIGN KEY(ingredient_id) REFERENCES Ingredient(id),
            CONSTRAINT fk_measure FOREIGN KEY(measure_id) REFERENCES Measure(id)
            UNIQUE(recipe_id, ingredient_id));"""
        )

    def add_measure(self, unit):
        if not unit:
            return None
        self.cursor.execute("""INSERT OR IGNORE INTO Measure (id, name) VALUES (NULL, ?)""", [unit])
        self.cursor.execute("""
            SELECT mu.id
            FROM Measure mu
            WHERE mu.name = ?""", [unit])
        return self.cursor.fetchone()[0]

    def add_ingredient(self, ingredient):
        self.cursor.execute("""INSERT OR IGNORE INTO Ingredient (id, name) VALUES (NULL, ?)""", [ingredient])
        self.cursor.execute("""
            SELECT i.id
            FROM Ingredient i
            WHERE i.name = ?""", [ingredient])
        return self.cursor.fetchone()[0]

    def add_recipe(self, name, description, instructions, amount_yield, notes):
        self.cursor.execute("""INSERT OR IGNORE INTO Recipe (id, name, description, instructions, yield, notes)
           VALUES (NULL, ?, ?, ?, ?, ?)""", (name, description, instructions, amount_yield, notes))
        self.cursor.execute("""
            SELECT r.id
            FROM Recipe r
            WHERE r.name = ?""", [name])
        return self.cursor.fetchone()[0]

    def add_recipe_ingredient(self, recipe_id, ingredient_id, measure_id, amount):
        self.cursor.execute("""INSERT OR IGNORE INTO RecipeIngredient (recipe_id, ingredient_id, measure_id, amount)
            VALUES (?, ?, ?, ?)""", (recipe_id, ingredient_id, measure_id, amount))

    def add(self, name, description, instructions, amount_yield, notes, ingredients):
        r_id = self.add_recipe(name, description, instructions, amount_yield, notes)
        for i in ingredients:
            i_id = self.add_ingredient(i[2])
            mu_id = self.add_measure(i[1])
            self.add_recipe_ingredient(r_id, i_id, mu_id, i[0])
        return r_id

    def get(self, recipe_id):
        result = self.cursor.execute("""
            SELECT ri.amount AS 'Amount',
            mu.name AS 'Unit of Measure',
            i.name AS 'Ingredient'
            FROM Recipe r
            JOIN RecipeIngredient ri on r.id = ri.recipe_id
            JOIN Ingredient i on i.id = ri.ingredient_id
            LEFT OUTER JOIN Measure mu on mu.id = measure_id
            WHERE r.id = ?""", [recipe_id])

        ingredients = []
        for r in result:
            ingredients.append(r)

        self.cursor.execute("""
            SELECT *
            FROM Recipe r
            WHERE r.id = ?""", [recipe_id])

        recipe = []
        recipe.append(self.cursor.fetchone())
        recipe.append(ingredients)

        return recipe

    def size(self):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM Recipe""")
        results = self.cursor.fetchall()
        return results[0][0]


    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
