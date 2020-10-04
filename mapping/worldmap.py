from PIL import ImageTk, Image
from angem.vector2 import Vector2

from angem.matrix import Matrix


class WorldMap:
    def __init__(self, size):
        self.size = size
        self.field = Matrix.filled(None, size.y, size.x)
        self.displaying_field = Matrix.filled(None, size.y, size.x)

    def get_pil_image(self, position):
        return self.field[position].pil_image if self.field[position] else None

    def get_tk_image(self, position):
        pi = self.get_pil_image(position)
        return ImageTk.PhotoImage(pi) if pi else None

    def put_tile(self, position, tile):
        self.field[position] = tile
        self.displaying_field[position] = self.get_tk_image(position)

    def pil_enumerate(self):
        for v, _ in self.field.enumerate():
            yield v, self.get_pil_image(v)
