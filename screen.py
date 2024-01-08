
import time
import pywinauto # type: ignore
import numpy as np # type: ignore

ACTIVE_TEXT=221

def minecraft_window():
    app = pywinauto.Application().connect(title_re = "Minecraft 1.20.4", class_name = "GLFW30")
    return app.top_window()

def debug_text_array(window):
    window.type_keys("{VK_ESCAPE}")
    time.sleep(1)
    return np.array(window.capture_as_image())[:,:,1] == ACTIVE_TEXT

def text_pixel_size(array):
    i = 0
    found = False
    for value in array.flatten():
        if value:
            print("found")
            found = True
            i += 1
        if found and not value:
            return i

def first_true_coord(array):
    for i,value in enumerate(array.flatten()):
        if value:
            row = i // array.shape[0]
            col = i % array.shape[0]
            print(i)
            return (row,col)
