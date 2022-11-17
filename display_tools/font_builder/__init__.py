import pprint
import freetype
from display_tools.font import Font, Table, Matrix

class Builder(Font):

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?;:,.[]{}()@#$€£&+=-_*/\\|<>~^`"\'#%'

    def __init__(self, file, size, base=7, v_adjust=0) -> None:
        face = freetype.Face(file)
        face.set_pixel_sizes(0, size)
        super().__init__([
            base,
            dict(self.get_chars(face, v_adjust))
        ])

    def __repr__(self):
        return pprint.PrettyPrinter(indent=4, depth=3, width=2048, compact=True).pformat(self.data)

    @classmethod
    def get_chars(cls, face, v_adjust=0):
        for character in cls.chars:
            face.load_char(character, freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
            bitmap = face.glyph.bitmap
            sprite = cls.build_matrix(bitmap)
            table = Table.from_matrix(sprite, 6)
            yield character, (sprite.width, face.glyph.bitmap_top + v_adjust, *table.data)

    @staticmethod
    def build_matrix(bitmap):
        data = bytearray(bitmap.rows * bitmap.width)
        for y in range(bitmap.rows):
            for byte_index in range(bitmap.pitch):
                byte_value = bitmap.buffer[y * bitmap.pitch + byte_index]
                num_bits_done = byte_index * 8
                rowstart = y * bitmap.width + byte_index * 8
                for bit_index in range(min(8, bitmap.width - num_bits_done)):
                    bit = byte_value & (1 << (7 - bit_index))
                    data[rowstart + bit_index] = 1 if bit else 0
        matrix = Matrix()
        for y in range(bitmap.rows):
            for x in range(bitmap.width):
                if data[y * bitmap.width + x]:
                    matrix.point(x, y)
        return matrix
