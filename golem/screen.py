import datetime
import logging
import time

import datetime
from PIL import Image as img
import numpy as np  # type: ignore
import pywinauto  # type: ignore
import pywinauto.findwindows  # type: ignore

import golem.exceptions

ACTIVE_TEXT = 221


logger = logging.getLogger(__name__)

def minecraft_window():
    try:
        app = pywinauto.Application().connect(
            title_re="Minecraft 1.20.4", class_name="GLFW30"
        )
    except pywinauto.findwindows.ElementNotFoundError:
        raise golem.exceptions.NotRunning()
    return app.top_window()


def grab_debug_text(window):
    now = datetime.datetime.now()
    screenshot = np.zeros(0) 
    while not screenshot.any():
        screenshot = (np.array(window.capture_as_image()) == ACTIVE_TEXT).all(axis=2)
    logger.debug(f"Took a screenshot (spent {datetime.datetime.now()-now})")
    return screenshot


def text_pixel_size(array):
    i = 0
    found = False
    for value in array.flatten():
        if value:
            found = True
            i += 1
        if found and not value:
            return i

def figure_out_pixel_size(array) -> int:
    seen = False
    i = 0
    for v in array.flatten():
        seen |= v
        if seen:
            i +=1
        if seen and not v:
            break
    return i - 1

def resample_debug_text(array):
    logger.debug(f"Resampling debug text")
    pixel_size = figure_out_pixel_size(array)
    if pixel_size == -1:
        img.fromarray(array).save("testing/weird.png")
    return np.invert(array[45::pixel_size, 18::pixel_size][2:,1:])  # TODO compute these from screen size


def first_true_coord(array):
    for i, value in enumerate(array.flatten()):
        if value:
            row = i // array.shape[0]
            col = i % array.shape[0]
            return (row, col)
