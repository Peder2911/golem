
import numpy as np
from PIL import Image as img
from collections import defaultdict

_POSITIONS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:$#'!\"/?%&()@"
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
    return letters[ulx:ulx+_LETTER_HEIGHT, uly:uly+_LETTER_WIDTH]

def mask(letter_array):
    return letter_array.any(axis=0).nonzero()[0]


masks = {l:mask(np.invert(raw_letter(l))) for l in _POSITIONS}

def letter(l):
    return raw_letter(l)[:, masks[l]]

def ocr(array):
    for l in _POSITIONS:
        letter_array = letter(l)
        check_array = array[:letter_array.shape[0], :letter_array.shape[1]]
        if np.array_equal(letter_array, check_array):
            return l, letter_array.shape[1]
    return None,0
