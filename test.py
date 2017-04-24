#!/usr/bin/env python

import sqlite3
connection = sqlite3.connect("testdb.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE if exists Recipe")
cursor.execute("DROP TABLE if exists Ingredient")
cursor.execute("DROP TABLE if exists Measure")
cursor.execute("DROP TABLE if exists RecipeIngredient")

cursor.execute("""
CREATE TABLE Recipe (
id INTEGER PRIMARY KEY,
name VARCHAR(25),
description VARCHAR(50),
instructions VARCHAR(500));"""
)

cursor.execute("""
CREATE TABLE Ingredient (
id INTEGER PRIMARY KEY,
name VARCHAR(50));"""
)

cursor.execute("""
CREATE TABLE Measure (
id INTEGER PRIMARY KEY,
name VARCHAR(30));"""
)

cursor.execute("""
CREATE TABLE RecipeIngredient (
recipe_id INTEGER,
ingredient_id INTEGER,
measure_id INTEGER,
amount INTEGER,
CONSTRAINT fk_recipe FOREIGN KEY(recipe_id) REFERENCES Recipe(id),
CONSTRAINT fk_ingredient FOREIGN KEY(ingredient_id) REFERENCES Ingredient(id),
CONSTRAINT fk_measure FOREIGN KEY(measure_id) REFERENCES Measure(id));"""
)

measure_data = [ ('CUP'), ('TEASPOON'), ('TABLESPOON') ]

for p in measure_data:
    format_str = """INSERT INTO Measure (id, name)
    VALUES (NULL, "{name}");"""

    sql_command = format_str.format(name=p)
    cursor.execute(sql_command)


ingredient_data = [ ('egg'), ('salt'), ('sugar'), ('chocolate'), ('vanilla extract'), ('flour') ]

for p in ingredient_data:
    format_str = """INSERT INTO Ingredient (id, name)
    VALUES (NULL, "{name}");"""

    sql_command = format_str.format(name=p)
    cursor.execute(sql_command)


recipe_data = [ ('Boiled Egg', 'A single boiled egg', 'Add egg to cold water. Bring water to boil. Cook.'),
                    ('Chocolate Cake', 'Yummy cake', 'Add eggs, flour, chocolate to pan. Bake at 350 for 1 hour') ]

for p in recipe_data:
    format_str = """INSERT INTO Recipe (id, name, description, instructions)
    VALUES (NULL, "{name}", "{description}", "{instructions}");"""

    sql_command = format_str.format(name=p[0], description=p[1], instructions=p[2])
    cursor.execute(sql_command)


recipe_ingredient_data = [ (1, 1, 'NULL', 1), (2, 1, 'NULL', 3), (2, 2, 2, 1), (2, 3, 1, 2), (2, 4, 1, 1) ]

for p in recipe_ingredient_data:
    format_str = """INSERT INTO RecipeIngredient (recipe_id, ingredient_id, measure_id, amount)
    VALUES ({recipe_id}, {ingredient_id}, {measure_id}, {amount});"""

    sql_command = format_str.format(recipe_id=p[0], ingredient_id=p[1], measure_id=p[2], amount=p[3])
    cursor.execute(sql_command)


cursor.execute("""
SELECT r.name AS 'Recipe',
r.instructions,
ri.amount AS 'Amount',
mu.name AS 'Unit of Measure',
i.name AS 'Ingredient'
FROM Recipe r
JOIN RecipeIngredient ri on r.id = ri.recipe_id
JOIN Ingredient i on i.id = ri.ingredient_id
LEFT OUTER JOIN Measure mu on mu.id = measure_id"""
)
result = cursor.fetchall()
for r in result:
    print(r)

cursor.execute("SELECT * FROM Recipe")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

cursor.execute("SELECT * FROM Ingredient")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

cursor.execute("SELECT * FROM Measure")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

cursor.execute("SELECT * FROM RecipeIngredient")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)

connection.close()
