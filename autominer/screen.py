import time

import numpy as np  # type: ignore
import pywinauto  # type: ignore
import pywinauto.findwindows  # type: ignore

import autominer.exceptions

ACTIVE_TEXT = 221


def minecraft_window():
    try:
        app = pywinauto.Application().connect(
            title_re="Minecraft 1.20.4", class_name="GLFW30"
        )
    except pywinauto.findwindows.ElementNotFoundError:
        raise autominer.exceptions.NotRunning()
    return app.top_window()


def grab_debug_text(window):
    window.type_keys("{VK_ESCAPE}")
    time.sleep(0.1)
    screenshot = np.array(window.capture_as_image())
    return (screenshot == ACTIVE_TEXT).all(axis=2)


def text_pixel_size(array):
    i = 0
    found = False
    for value in array.flatten():
        if value:
            found = True
            i += 1
        if found and not value:
            return i


def resample_debug_text(array):
    return array[45::5, 18::5]  # TODO compute these from screen size


def first_true_coord(array):
    for i, value in enumerate(array.flatten()):
        if value:
            row = i // array.shape[0]
            col = i % array.shape[0]
            return (row, col)
