from tkinter import Tk, Canvas, NW, TclError

from PIL import ImageTk, Image

from angem.matrix import Matrix

from angem.vector2 import Vector2


def abs_mouse(root):
    return Vector2(
        root.winfo_pointerx() - root.winfo_rootx(),
        root.winfo_pointery() - root.winfo_rooty(),
    )


size = Vector2(15, 10)
scaling = 4
tile_size = 16
tile_scaled_size = scaling * tile_size
master_size = size * scaling * tile_size
field = Matrix.filled(None, size.y, size.x)
displaying_field = Matrix.filled(None, size.y, size.x)

if __name__ == '__main__':
    master = Tk()
    master.geometry(f"{master_size.x}x{master_size.y}")

    canvas = Canvas(master, width=master_size.x, height=master_size.y)
    canvas.pack()

    source = Image.open('assets/sprites/Stone wall tile.png')
    source = source.resize(tuple(Vector2(*source.size) * scaling), Image.NEAREST)
    displaying_field[1, 2] = ImageTk.PhotoImage(source)
    field[1, 2] = source

    cursor = source.copy()
    cursor.putalpha(192)
    cursor = ImageTk.PhotoImage(cursor)


    def lmb_pressed(event):
        v = Vector2(event.x, event.y) // tile_scaled_size
        displaying_field[v] = ImageTk.PhotoImage(source)
        field[v] = source


    master.bind("<Button-1>", lmb_pressed)

    try:
        while True:
            canvas.delete("all")

            for v, img in displaying_field.enumerate():
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

        for v, img in field.enumerate():
            if img:
                result.paste(img, tuple(v * tile_scaled_size))

        result.save("result.png")
