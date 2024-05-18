from itertools import product
from typing import Callable


class DiagonalMatrix:
    length = 16

    def __init__(self, matrix: list[list[bool]] | None = None):
        if matrix:
            self._matrix = matrix
        else:
            self._matrix = [[False,]*self.length for _ in range(self.length)]
        if len(self._matrix) != 16:
            raise ValueError("Count of rows in matrix must be 16")
        if len(self._matrix[0]) != 16:
            raise ValueError("Count of columns in matrix must be 16")

    def get_address_column(self, item: int):
        if item not in range(16):
            raise KeyError()
        return list(row[(self.length - item + i - 1) % self.length] for i, row in enumerate(self._matrix))

    def set_address_column(self, item: int, value: list[bool]):
        if len(value) != self.length:
            raise ValueError()
        for i, row in enumerate(self._matrix):
            row[(self.length - item + i - 1) % self.length] = value[i]

    def get_word(self, item: int):
        if item not in range(16):
            raise KeyError()
        return list(self[(i + item) % self.length, item] for i in range(self.length))

    def set_word(self, item: int, value: list[bool]):
        if len(value) != self.length:
            raise ValueError()
        for i in range(self.length):
            self[(i + item) % self.length, item] = value[i]

    def apply_function_on_columns(
            self,
            func: Callable[[bool, bool], bool],
            item1: int,
            item2: int,
            item3: int
    ):
        column1 = self.get_address_column(item1)
        column2 = self.get_address_column(item2)
        column3 = [func(i, j) for i, j in zip(column1, column2)]
        self.set_address_column(item3, column3)

    def sum_fields(self, v: (bool, bool, bool)):
        for i in range(self.length):
            word = self.get_word(i)
            if not all(map(lambda x: x[0] == x[1], zip(word, v))):
                continue
            flag = False
            for j in reversed(range(4)):
                word[j+12] = flag != (word[j+3] != word[j+7])
                flag = ((word[j+3] and word[j+7]) or
                        (word[j+3] and flag) or
                        (word[j+7] and flag))
            word[11] = flag
            self.set_word(i, word)

    def compare(self, value: list[bool]):
        if len(value) != self.length:
            raise ValueError()
        g = False
        l = False
        answer = []
        for j in range(self.length):
            for bit in self.get_word(j):
                g = (old_g := g) and (not value and bit and l)
                l = l and (value and not bit and not old_g)
            match g, l:
                case False, False:
                    answer.append(0)
                case True, False:
                    answer.append(1)
                case False, True:
                    answer.append(-1)
                case _:
                    raise ArithmeticError()
        return answer

    def find_words_in_range(
            self,
            top: list[bool],
            bottom: list[bool]
    ):
        flags = [True] * self.length
        for i, r in enumerate(self.compare(top)):
            flags[i] = flags[i] and r != 1
        for i, r in enumerate(self.compare(bottom)):
            flags[i] = flags[i] and r != -1
        return flags

    def __getitem__(self, item: (int, int)):
        return self._matrix[item[0]][item[1]]

    def __setitem__(self, item: (int, int), value: bool):
        self._matrix[item[0]][item[1]] = value
