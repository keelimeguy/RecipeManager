#!/usr/bin/env python

import sqlite3
import argparse
import sys

from recipe_book import RecipeBook

def reset_database(database):
    book = RecipeBook(database)
    book.purge()
    book.make_tables()

    measure_data = [ ('CUP'), ('TEASPOON'), ('TABLESPOON') ]

    for p in measure_data:
        book.add_measure(p)

    ingredient_data = [ ('egg'), ('salt'), ('sugar'), ('chocolate'), ('vanilla extract'), ('flour') ]

    for p in ingredient_data:
        book.add_ingredient(p)

    recipe_data = [ ('Boiled Egg', 'A single boiled egg', 'Add egg to cold water. Bring water to boil. Cook.', 1, None),
                        ('Chocolate Cake', 'Yummy cake', 'Add eggs, flour, chocolate to pan. Bake at 350 for 1 hour', 8, None) ]

    for p in recipe_data:
        book.add_recipe(p[0], p[1], p[2], p[3], p[4])

    recipe_ingredient_data = [ (1, 1, None, 1), (2, 1, None, 3), (2, 2, 2, 1), (2, 3, 1, 2), (2, 4, 1, 1) ]

    for p in recipe_ingredient_data:
        book.add_recipe_ingredient(p[0], p[1], p[2], p[3])

    book.cursor.execute("""
    SELECT r.name AS 'Recipe',
    ri.amount AS 'Amount',
    mu.name AS 'Unit of Measure',
    i.name AS 'Ingredient'
    FROM Recipe r
    JOIN RecipeIngredient ri on r.id = ri.recipe_id
    JOIN Ingredient i on i.id = ri.ingredient_id
    LEFT OUTER JOIN Measure mu on mu.id = measure_id"""
    )

    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM Recipe")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM Ingredient")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM Measure")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM RecipeIngredient")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.save()
    book.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Example of interfacing with recipe_book.py')
    parser.add_argument('-r', '--reset', action="store_true",
                        help='Recreates a fresh database.')
    parser.add_argument('-d', '--database', default="testdb.db",
                        help='The database file you wish to use.')
    args = parser.parse_args()

    if args.reset:
        reset_database(args.database)
        print("\nDatabase has been reset: {}\n".format(args.database))
    book = RecipeBook(args.database)
    print(book)

    recipe = book.get(1)
    print(recipe)
    print

    recipe = book.get(2)
    print(recipe)
    print

    r_id = book.add("Ham Sandwich", "YUM! This is tasty!", "Put the ham between the slices of bread.", 1, None, [(1/8.0, "POUND", "Ham"), (2, "SLICES", "Bread")])
    recipe = book.get(r_id)
    print(recipe)
    print

    r_id = book.add("PB&J Sandwich", "A classic favorite!", "Spread the peanut butter and jelly between the slices of bread.", 1, "Peanut butter can get stuck on roof of mouth. Drink with milk.", [(2, "TABLESPOON", "Peanut Butter"), (2, "TABLESPOON", "Jelly"), (2, "SLICES", "Bread")])
    recipe = book.get(r_id)
    print(recipe)
    print

    book.cursor.execute("SELECT * FROM Recipe")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM Ingredient")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM Measure")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.cursor.execute("SELECT * FROM RecipeIngredient")
    print("fetchall:")
    result = book.cursor.fetchall()
    for r in result:
        print(r)

    book.close()
