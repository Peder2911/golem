
import datetime
import logging
import numpy as np
from PIL import Image as img
from collections import defaultdict
import golem.screen

logger = logging.getLogger(__name__)

_POSITIONS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-:$#\"!'/?%^()@.,;_[]"
_LETTER_HEIGHT = 7
_LETTER_WIDTH = 5
_SPRITE_HEIGHT = 9
_SPRITE_WIDTH = 9
letters = (np.array(img.open("letters.png")) == 255).all(axis = 2)

# TODO handle variable width letters

def raw_letter(l):
    i = _POSITIONS.index(l)
    row = i // _SPRITE_HEIGHT
    col = i % _SPRITE_WIDTH
    ulx = (row * _LETTER_HEIGHT) + (row)
    uly = (col * _LETTER_WIDTH)  + (col)
    return letters[ulx:ulx+_LETTER_HEIGHT+1, uly:uly+_LETTER_WIDTH]

def mask(letter_array):
    return letter_array.any(axis=0).nonzero()[0]


masks = {l:mask(np.invert(raw_letter(l))) for l in _POSITIONS}

def letter(l):
    return raw_letter(l)[:, masks[l]]

def ocr(array):
    chartried = 0
    for l in _POSITIONS:
        letter_array = letter(l)
        check_array = array[:letter_array.shape[0], :letter_array.shape[1]]
        if np.array_equal(letter_array, check_array):
            return l, letter_array.shape[1]
        chartried += 1
    return None,0

def read_line(window, linenumber: int = 0):
    text = golem.screen.grab_debug_text(window)
    resampled = golem.screen.resample_debug_text(text)[9*linenumber:,:]

    message = ""
    letter = ""
    offset = 0

    now = datetime.datetime.now()
    while letter != None:
        letter,read = ocr(resampled[:,offset:])
        if letter is None:
            offset += 4
            letter,read = ocr(resampled[:,offset:])
            if letter is not None:
                letter = " "+letter
        offset += read+1
        if letter is not None:
            message += letter
    logger.debug(f"Read line (spent {datetime.datetime.now()-now})")
    return message


