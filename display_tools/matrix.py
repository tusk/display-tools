
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