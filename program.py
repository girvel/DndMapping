from tkinter import Tk, Canvas, NW, TclError

from PIL import ImageTk, Image

from angem.matrix import Matrix

from angem.vector2 import Vector2
from mapping.tile import tile_factory
from mapping.worldmap import WorldMap


def abs_mouse(root):
    return Vector2(
        root.winfo_pointerx() - root.winfo_rootx(),
        root.winfo_pointery() - root.winfo_rooty(),
    )


scaling = 4
tile_size = 16
tile_scaled_size = scaling * tile_size
world_map = WorldMap(Vector2(15, 10))
master_size = world_map.size * scaling * tile_size

if __name__ == '__main__':
    master = Tk()
    master.geometry(f"{master_size.x}x{master_size.y}")

    canvas = Canvas(master, width=master_size.x, height=master_size.y)
    canvas.pack()

    tile = tile_factory(scaling)

    stonewall = tile("Stone wall tile")

    cursor = stonewall.pil_image.copy()
    cursor.putalpha(192)
    cursor = ImageTk.PhotoImage(cursor)


    def lmb_pressed(event):
        world_map.put_tile(Vector2(event.x, event.y) // tile_scaled_size, stonewall)


    master.bind("<Button-1>", lmb_pressed)

    try:
        while True:
            canvas.delete("all")

            for v, img in world_map.displaying_field.enumerate():
                canvas.create_image(*(v * tile_scaled_size), anchor=NW, image=img)

            canvas.create_image(*(abs_mouse(master) // tile_scaled_size * tile_scaled_size), anchor=NW, image=cursor)

            master.update()
            master.update_idletasks()
    except TclError as err:
        if err.args[0] == 'can\'t invoke "update" command: application has been destroyed' and len(err.args) == 1:
            exit(0)
        raise err
    finally:
        result = Image.new("RGBA", tuple(master_size), color=(0, 0, 0, 0))

        for v, img in world_map.pil_enumerate():
            if img:
                result.paste(img, tuple(v * tile_scaled_size))

        result.save("result.png")
