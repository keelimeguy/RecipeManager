#!/usr/bin/env python

import unittest
import os

from recipe_manager.recipe_book import RecipeBook

def table_info(book, table):
    book.cursor.execute("""
        PRAGMA table_info({})
        """.format(table))
    return book.cursor.fetchall()

class RecipeBookTestCase(unittest.TestCase):
    def setUp(self):
        self.database = "recipe_book_test_case_REMOVEME.db"

    def test_fresh_book(self):
        book = RecipeBook(self.database)
        self.assertEqual(str(book), "")
        self.assertEqual(table_info(book, "Recipe"),
            [(0, u'id', u'INTEGER', 0, None, 1),
            (1, u'name', u'VARCHAR(25)', 0, None, 0),
            (2, u'description', u'VARCHAR(50)', 0, None, 0),
            (3, u'instructions', u'VARCHAR(500)', 0, None, 0),
            (4, u'yield', u'Integer', 0, None, 0),
            (5, u'notes', u'VARCHAR(100)', 0, None, 0)])
        self.assertEqual(table_info(book, "Ingredient"),
            [(0, u'id', u'INTEGER', 0, None, 1),
            (1, u'name', u'VARCHAR(50)', 0, None, 0)])
        self.assertEqual(table_info(book, "Measure"),
            [(0, u'id', u'INTEGER', 0, None, 1),
            (1, u'name', u'VARCHAR(30)', 0, None, 0)])
        self.assertEqual(table_info(book, "RecipeIngredient"),
            [(0, u'recipe_id', u'INTEGER', 0, None, 0),
            (1, u'ingredient_id', u'INTEGER', 0, None, 0),
            (2, u'measure_id', u'INTEGER', 0, None, 0),
            (3, u'amount', u'REAL', 0, None, 0)])
        book.close()

    def test_add(self):
        book = RecipeBook(self.database)
        self.assertEqual(str(book), "")
        r_id = book.add("Test Name", "Test Description", "Test Instructions", 15, "Test Notes",
            [(1, "Test Unit 1", "Test Ingredient 1"), (2, "Test Unit 2", "Test Ingredient 2")])
        self.assertEqual(book.get(r_id),
            [(1, u'Test Name', u'Test Description', u'Test Instructions', 15, u'Test Notes'),
            [(1.0, u'Test Unit 1', u'Test Ingredient 1'), (2.0, u'Test Unit 2', u'Test Ingredient 2')]])
        book.close()

    def test_size(self):
        book = RecipeBook(self.database)
        self.assertEqual(str(book), "")
        self.assertEqual(book.size(), 0)
        r_id = book.add("Test Name", "Test Description", "Test Instructions", 15,
            "Test Notes", [(1, "Test Unit 1", "Test Ingredient 1")])
        self.assertEqual(book.size(), 1)
        r_id = book.add("Test Name 2", "Test Description", "Test Instructions", 15,
            "Test Notes", [(1, "Test Unit 2", "Test Ingredient 2")])
        self.assertEqual(book.size(), 2)
        book.purge()
        self.assertEqual(book.size(), 0)
        book.close()

    def test_save(self):
        book = RecipeBook(self.database)
        self.assertEqual(str(book), "")
        r_id = book.add("Test Name", "Test Description", "Test Instructions", 15,
            "Test Notes", [(1, "Test Unit 1", "Test Ingredient 1")])
        self.assertEqual(str(book),
            "(u'Test Name', 1.0, u'Test Unit 1', u'Test Ingredient 1')")
        book.save()
        book.close()
        book = RecipeBook(self.database)
        self.assertEqual(str(book),
            "(u'Test Name', 1.0, u'Test Unit 1', u'Test Ingredient 1')")
        book.close()

    def test_purge(self):
        book = RecipeBook(self.database)
        self.assertEqual(str(book), "")
        r_id = book.add("Test Name", "Test Description", "Test Instructions", 15,
            "Test Notes", [(1, "Test Unit 1", "Test Ingredient 1")])
        self.assertEqual(str(book),
            "(u'Test Name', 1.0, u'Test Unit 1', u'Test Ingredient 1')")
        book.purge()
        self.assertEqual(str(book), "")
        book.close()

    def tearDown(self):
        try:
            os.remove(self.database)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
