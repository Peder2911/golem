
import numpy as np
from PIL import Image as img

_POSITIONS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:$#'!\"/?%()@"
_LETTER_HEIGHT = 7
_LETTER_WIDTH = 5
_SPRITE_HEIGHT = 9
_SPRITE_WIDTH = 9
letters = (np.array(img.open("letters.png")) == 255).all(axis = 2)

# TODO handle variable width letters

def letter(l):
    i = _POSITIONS.index(l)
    row = i // _SPRITE_HEIGHT
    col = i % _SPRITE_WIDTH
    ulx = (row * _LETTER_HEIGHT) + (row)
    uly = (col * _LETTER_WIDTH)  + (col)
    return letters[ulx:ulx+_LETTER_HEIGHT, uly:uly+_LETTER_WIDTH]

def ocr(array):
    for l in _POSITIONS:
        if np.array_equal(letter(l), array):
            return l
