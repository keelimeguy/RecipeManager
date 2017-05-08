#!/usr/bin/env python

import sqlite3
import argparse
import sys

from recipe_book import RecipeBook

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Example of interfacing with recipe_book.py')
    parser.add_argument('-r', '--reset', action="store_true",
                        help='Resets the database.')
    parser.add_argument('-d', '--database', default="testdb.db",
                        help='The database file you wish to use.')
    args = parser.parse_args()

    book = RecipeBook(args.database)
    if args.reset:
        book.purge()
        print("\nDatabase has been reset: {}\n".format(args.database))

    for i in range(1, book.size()+1):
        recipe = book.get(i)
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
