import math
from display_tools.matrix import Matrix

class Font:

    def __init__(self, data) -> None:
        self.data = data

    def char(self, char):
        base, chars = self.data
        width, top, *parts = chars.get(char, (2, 0))
        return width, base - top, parts

    def matrix(self, char):
        width, top, data = self.char(char)
        table = Table(data, math.ceil(width / 6), 6)
        matrix = Matrix()
        matrix.set(table.as_matrix())
        return matrix, top

    def render(self, text, b=None, hspace=1, vspace=4):
        base, _ = self.data
        matrix = Matrix()
        x = 0
        y = 0
        for char in text:
            if char == '\n':
                x = 0
                y += base + vspace
                continue
            char_matrix, top = self.matrix(char)
            matrix = matrix.over(char_matrix, x, top + y, b=b)
            x += char_matrix.width or 2
            x += hspace
        return matrix


class Table:

    def __init__(self, data, steps, bits=8) -> None:
        self.steps = steps
        self.data = data
        self.bits = bits

    def as_matrix(self):
        matrix = []
        for x, y in self.points():
            if len(matrix) <= y:
                for _ in range(y - len(matrix) + 1):
                    matrix.append([])
            for row in matrix:
                if len(row) <= x:
                    row.extend([None] * (x - len(row) + 1))
            matrix[y][x] = 1
        return matrix

    def points(self):
        y = 0
        for i, step in enumerate(self.data):
            x_step = i % self.steps
            for x in range(self.bits):
                if 2**x & step:
                    yield x + (x_step * self.bits), y
            if x_step + 1 == self.steps:
                y += 1

    @classmethod
    def from_matrix(cls, matrix, bits=8):
        values = []
        width = None
        steps = 0
        for row in matrix.rows:
            if width is None:
                width = len(row)
                steps = math.ceil(width / bits)
            vals = [0] * steps
            for i, pixel in enumerate(row):
                if pixel is not None:
                    step = math.floor(i / bits)
                    vals[step] += 2**(i % bits)
            values.extend(vals)
        return cls(tuple(values), steps, bits)
