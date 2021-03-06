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
        self.cursor.execute("DROP TABLE IF EXISTS Recipe_")
        self.cursor.execute("DROP TABLE IF EXISTS Ingredient_")
        self.cursor.execute("DROP TABLE IF EXISTS Measure_")
        self.cursor.execute("DROP TABLE IF EXISTS RecipeIngredient_")
        self.cursor.execute("DROP TABLE IF EXISTS Recipe_clone")
        self.cursor.execute("DROP TABLE IF EXISTS Ingredient_clone")
        self.cursor.execute("DROP TABLE IF EXISTS Measure_clone")
        self.cursor.execute("DROP TABLE IF EXISTS RecipeIngredient_clone")
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
            prep_time REAL,
            cook_time REAL,
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
            order_num INTEGER,
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

    def add_recipe(self, name, description, instructions, amount_yield, notes, prep_time, cook_time):
        self.cursor.execute("""INSERT OR IGNORE INTO Recipe (id, name, description, instructions, yield, notes, prep_time, cook_time)
           VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", (name, description, instructions, amount_yield, notes, prep_time, cook_time))
        self.cursor.execute("""
            SELECT r.id
            FROM Recipe r
            WHERE r.name = ?""", [name])
        return self.cursor.fetchone()[0]

    def add_recipe_ingredient(self, recipe_id, ingredient_id, measure_id, amount, order_num):
        self.cursor.execute("""INSERT OR IGNORE INTO RecipeIngredient (recipe_id, ingredient_id, measure_id, amount, order_num)
            VALUES (?, ?, ?, ?, ?)""", (recipe_id, ingredient_id, measure_id, amount, order_num))

    def add(self, name, description, instructions, amount_yield, notes, prep_time, cook_time, ingredients, force=False, r_id=None):
        if force:
            if r_id == None:
                self.cursor.execute("""
                    SELECT r.id
                    FROM Recipe r
                    WHERE r.name = ?
                    """, [name])
                r_id = self.cursor.fetchone()
            if r_id != None:
                r_id = r_id[0]
                self.cursor.execute("""DELETE FROM Recipe WHERE name = ?""", [name])
                self.cursor.execute("""DELETE FROM RecipeIngredient WHERE recipe_id = ?""", [r_id])
        r_id = self.add_recipe(name, description, instructions, amount_yield, notes, prep_time, cook_time)
        order_num = None
        if ingredients is not None and len(ingredients)>0:
            if not len(ingredients[0])==4:
                order_num = 1
            for i in ingredients:
                i_id = self.add_ingredient(i[2])
                mu_id = self.add_measure(i[1])
                self.add_recipe_ingredient(r_id, i_id, mu_id, i[0], order_num if order_num else i[3])
                if order_num:
                    order_num+=1
        return r_id

    def get(self, recipe_id):
        result = self.cursor.execute("""
            SELECT ri.amount AS 'Amount',
            mu.name AS 'Unit of Measure',
            i.name AS 'Ingredient',
            ri.order_num AS 'Order'
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

    def delete(self, r_id):
        if r_id:
            self.cursor.execute("""DELETE FROM Recipe WHERE id = ?""", [r_id])
            self.cursor.execute("""DELETE FROM RecipeIngredient WHERE recipe_id = ?""", [r_id])
            self.save()

    def select_recipe(self, index, id_list=None):
        if id_list:
            r_id = [(i, None) for i in id_list]
        else:
            self.cursor.execute("""
                SELECT r.id
                FROM Recipe r
                """)
            r_id = self.cursor.fetchall()
            recipe = None
        if r_id:
            if len(r_id)>0:
                if index >= len(r_id):
                    index = 0
                elif index < 0:
                    index = len(r_id)-1
            if len(r_id)>index:
                r_id = r_id[index][0]
                recipe = self.get(r_id)
            else:
                r_id = None
        return recipe, r_id, index

    def select_index(self, recipe_id, id_list=None):
        if id_list:
            r_id = [(i, None) for i in id_list]
        else:
            self.cursor.execute("""
                SELECT r.id
                FROM Recipe r
                """)
            r_id = self.cursor.fetchall()
        if r_id:
            for i in range(len(r_id)):
                if r_id[i][0] == recipe_id:
                    return i
        return None

    def size(self):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM Recipe""")
        results = self.cursor.fetchall()
        return results[0][0]

    def renumber(self):
        self.cursor.execute("""
            SELECT i.id, (
                SELECT COUNT(*)
                FROM RecipeIngredient ri
                WHERE ri.ingredient_id = i.id
            )
            FROM Ingredient i""")
        results = self.cursor.fetchall()
        for r in results:
            if r[1]==0:
                self.cursor.execute("""DELETE FROM Ingredient WHERE id = ?""", [r[0]])

        self.cursor.execute("""
            SELECT mu.id, (
                SELECT COUNT(*)
                FROM RecipeIngredient ri
                WHERE ri.measure_id = mu.id
            )
            FROM Measure mu""")
        results = self.cursor.fetchall()
        for r in results:
            if r[1]==0:
                self.cursor.execute("""DELETE FROM Measure WHERE id = ?""", [r[0]])

        self.cursor.execute("""
            CREATE TABLE Recipe_ (
                id INTEGER PRIMARY KEY,
                name VARCHAR(25),
                description VARCHAR(50),
                instructions VARCHAR(500),
                yield Integer,
                notes VARCHAR(100),
                prep_time Integer,
                cook_time Integer,
                UNIQUE(name));"""
        )
        self.cursor.execute("""
            CREATE TABLE RecipeIngredient_ (
                recipe_id INTEGER,
                ingredient_id INTEGER,
                measure_id INTEGER,
                amount REAL,
                order_num INTEGER,
                CONSTRAINT fk_recipe FOREIGN KEY(recipe_id) REFERENCES Recipe(id),
                CONSTRAINT fk_ingredient FOREIGN KEY(ingredient_id) REFERENCES Ingredient(id),
                CONSTRAINT fk_measure FOREIGN KEY(measure_id) REFERENCES Measure(id)
                UNIQUE(recipe_id, ingredient_id));"""
        )
        self.cursor.execute("""
            CREATE TABLE Ingredient_ (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50),
                UNIQUE(name));"""
        )
        self.cursor.execute("""
            CREATE TABLE Measure_ (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                UNIQUE(name));"""
        )
        self.cursor.execute("""
            ALTER TABLE Recipe
                RENAME TO Recipe_clone""")
        self.cursor.execute("""
            ALTER TABLE Recipe_
                RENAME TO Recipe""")
        self.cursor.execute("""
            ALTER TABLE RecipeIngredient
                RENAME TO RecipeIngredient_clone""")
        self.cursor.execute("""
            ALTER TABLE RecipeIngredient_
                RENAME TO RecipeIngredient""")
        self.cursor.execute("""
            ALTER TABLE Ingredient
                RENAME TO Ingredient_clone""")
        self.cursor.execute("""
            ALTER TABLE Ingredient_
                RENAME TO Ingredient""")
        self.cursor.execute("""
            ALTER TABLE Measure
                RENAME TO Measure_clone""")
        self.cursor.execute("""
            ALTER TABLE Measure_
                RENAME TO Measure""")

        self.cursor.execute("""DELETE FROM RecipeIngredient WHERE 1=1""")

        self.cursor.execute("""
            SELECT *
            FROM Ingredient_clone""")
        results = self.cursor.fetchall()
        if results:
            for r in results:
                self.add_ingredient(r[1])
        self.cursor.execute("""
            SELECT *
            FROM Measure_clone""")
        results = self.cursor.fetchall()
        if results:
            for r in results:
                self.add_measure(r[1])

        self.cursor.execute("""
            SELECT *
            FROM Recipe_clone""")
        results = self.cursor.fetchall()
        if results:
            for r in results:
                result = self.cursor.execute("""
                    SELECT ri.amount AS 'Amount',
                    mu.name AS 'Unit of Measure',
                    i.name AS 'Ingredient',
                    ri.order_num AS 'Order'
                    FROM Recipe_clone r
                    JOIN RecipeIngredient_clone ri on r.id = ri.recipe_id
                    JOIN Ingredient_clone i on i.id = ri.ingredient_id
                    LEFT OUTER JOIN Measure_clone mu on mu.id = ri.measure_id
                    WHERE r.id = ?""", [r[0]])
                ingredients = []
                for i in result:
                    ingredients.append((i))
                self.add(r[1], r[2], r[3], r[4], r[5], r[6], r[7], ingredients, True)
        self.cursor.execute("DROP TABLE Recipe_clone")
        self.cursor.execute("DROP TABLE RecipeIngredient_clone")
        self.cursor.execute("DROP TABLE Ingredient_clone")
        self.cursor.execute("DROP TABLE Measure_clone")

    def save(self):
        self.connection.commit()

    def close(self, save=False):
        if save:
            self.save()
        self.connection.close()
