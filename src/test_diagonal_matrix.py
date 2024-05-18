import unittest
from itertools import product
from typing import Callable
from src.diagonal_matrix import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = DiagonalMatrix()

    def test_init(self):
        self.assertEqual(len(self.matrix._matrix), 16)
        self.assertEqual(len(self.matrix._matrix[0]), 16)

        with self.assertRaises(ValueError):
            DiagonalMatrix([[False] * 15 for _ in range(16)])

        with self.assertRaises(ValueError):
            DiagonalMatrix([[False] * 16 for _ in range(15)])

    def test_get_set_address_column(self):
        for i in range(16):
            column = self.matrix.get_address_column(i)
            self.assertEqual(len(column), 16)

        with self.assertRaises(KeyError):
            self.matrix.get_address_column(16)

        value = [False] * 16
        self.matrix.set_address_column(0, value)
        self.assertEqual(self.matrix.get_address_column(0), list(value))

        with self.assertRaises(ValueError):
            self.matrix.set_address_column(0, [False] * 15)

    def test_get_set_word(self):
        for i in range(16):
            word = self.matrix.get_word(i)
            self.assertEqual(len(word), 16)

        with self.assertRaises(KeyError):
            self.matrix.get_word(16)

        value = [False] * 16
        self.matrix.set_word(0, value)
        self.assertEqual(self.matrix.get_word(0), list(value))

        with self.assertRaises(ValueError):
            self.matrix.set_word(0, [False] * 15)

    def test_apply_function_on_columns(self):
        def func(a, b):
            return a or b

        self.matrix.apply_function_on_columns(func, 0, 1, 2)
        column0 = self.matrix.get_address_column(0)
        column1 = self.matrix.get_address_column(1)
        column2 = self.matrix.get_address_column(2)

        for i in range(16):
            self.assertEqual(column2[i], func(column0[i], column1[i]))

    def test_sum_fields(self):
        self.matrix.set_word(0, [False, True, True] + [True] * 4 +[False, False, False, True] + [False] * 5)
        self.matrix.sum_fields((False, True, True))
        self.assertEqual(
            [False, True, True, True, True, True, True, False,
             False, False, True, True, False, False, False, False],
            self.matrix.get_word(0)
        )

    def test_compare(self):
        value = [False] * 16
        self.assertEqual(self.matrix.compare(value), [0] * 16)

        with self.assertRaises(ValueError):
            self.matrix.compare([False] * 15)

    def test_find_words_in_range(self):
        for i in range(self.matrix.length):
            self.matrix[i, 5] = True
        top = [True] * 16
        bottom = [False] * 16
        self.assertEqual(self.matrix.find_words_in_range(top, bottom), [True] * 16)

    def test_getitem_setitem(self):
        for i, j in product(range(16), range(16)):
            self.matrix[(i, j)] = True
            self.assertTrue(self.matrix[(i, j)])


if __name__ == '__main__':
    unittest.main()
