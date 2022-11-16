import math

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


class Matrix:

    def __init__(self, rows=None) -> None:
        self.rows = rows or []

    @property
    def width(self):
        if self.height == 0:
            return 0
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def point(self, x, y, b=1):
        if len(self.rows) <= y:
            for _ in range(y - len(self.rows) + 1):
                self.rows.append([])

        for row in self.rows:
            if len(row) <= x:
                row.extend([None] * (x - len(row) + 1))
        self.rows[y][x] = b
        return self

    def points(self, points, b=1):
        for x, y in points:
            self.point(x, y, b)
        return self

    def set(self, matrix, b=1):
        for y, row in enumerate(matrix):
            for x, pixel in enumerate(row):
                if pixel is True:
                    pixel = b
                if pixel is not None:
                    self.point(x, y, pixel)
        return self

    def over(self, sprite, x=0, y=0, b=None):
        new = self.copy()
        for _x, _y, _b in sprite:
            if _x + x < 0 or _y + y < 0:
                continue
            new.point(_x + x, _y + y, _b if b is None else b)
        return new

    def scale(self, by=1):
        new = self.__class__()
        multiples = [[]]
        for pool in [tuple(range(by))] * 2:
            multiples = [x+[y] for x in multiples for y in pool]
        for x, y, b in self:
            for _x, _y in multiples:
                new.point(x * by + _x, y * by + _y, b)
        return new

    def crop(self, right, down, left=0, up=0):
        new = self.__class__()
        for x, y, b in self:
            if x < left or x > right:
                continue
            if y < up or y > down:
                continue
            new.point(x, y, b)
        return new

    def copy(self, replace=None):
        new = self.__class__()
        for _x, _y, _b in self:
            if isinstance(replace, tuple):
                _b = replace[1] if _b == replace[0] else _b
            elif replace is not None:
                _b = replace
            new.point(_x, _y, _b)
        return new

    def __iter__(self):
        for y, row in enumerate(self.rows):
            for x, point in enumerate(row):
                if point is not None:
                    yield x, y, point


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
