from collections import namedtuple

from PIL import Image
from angem.vector2 import Vector2


def tile_factory(scaling):
    def ctor(*args, **kwargs):
        return Tile(*args, scaling=scaling, **kwargs)
    return ctor


class Tile:
    def __init__(self, name, scaling=1):
        self.pil_image = Image.open(f"assets/sprites/{name}.png")
        self.pil_image = self.pil_image.resize(tuple(Vector2(*self.pil_image.size) * scaling), Image.NEAREST)
