import logging
import re
import time
import asyncio
import golem.minecraft.proto
import golem.screen
import golem.letters
import win32api
import pywinauto.mouse

logger = logging.getLogger(__name__)

class ScreenData():
    def __init__(self, window):
        self._window = window
        self._location_pattern = re.compile(r"XYZ: (-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+)")
        self._rotation_pattern = re.compile(r"Facing: [a-z]+ \(Towards [a-z]+ [XYZ]\) \((-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+)\)")

    def location(self) -> tuple[float,float,float]:
        logger.debug(f"Reading position")
        location_line = golem.letters.read_line(self._window, 9)
        logger.debug(f"Read \"{location_line}\"")
        match = self._location_pattern.search(location_line)
        if match:
            x,y,z = match.groups()
            return float(x), float(y), float(z)
        else:
            raise ValueError(f"Failed to parse location line: \"{location_line}\"")

    def rotation(self) -> tuple[float,float]:
        logger.debug(f"Reading rotation")
        rotation_line = golem.letters.read_line(self._window, 12)
        logger.debug(f"Read \"{rotation_line}\"")
        match = self._rotation_pattern.search(rotation_line)
        if match:
            x,y = match.groups()
            return float(x), float(y)
        else:
            raise ValueError(f"Failed to parse rotation line: \"{rotation_line}\"")
        return .0, .0

class ScreenController():
    def __init__(self, window):
        self._window = window 

    async def left(self, duration: float) -> None:
        self._window.type_keys("{a down}")
        await asyncio.sleep(duration)
        self._window.type_keys("{a up}")

    async def right(self, duration: float) -> None:
        self._window.type_keys("{d down}")
        await asyncio.sleep(duration)
        self._window.type_keys("{d up}")

    async def forwards(self, duration: float) -> None:
        self._window.type_keys("{w down}")
        await asyncio.sleep(duration)
        self._window.type_keys("{w up}")

    async def backwards(self, duration: float) -> None:
        self._window.type_keys("{s down}")
        await asyncio.sleep(duration)
        self._window.type_keys("{s up}")

    def _current_mouse(self) -> tuple[int,int]:
        return win32api.GetCursorPos()

    def _look(self,x:float, y:float):
        logger.debug(f"Look: {x},{y}")
        cx,cy = self._current_mouse()
        win32api.SetCursorPos((int(cx+x), int(cy+y)))
        time.sleep(.1)

    def look_left(self, duration: float)-> None:
        self._look(-duration,0)

    def look_right(self, duration: float)-> None:
        self._look(duration,0)

    def look_up(self, duration: float)-> None:
        self._look(0,-duration)

    def look_down(self, duration: float)-> None:
        self._look(0,duration)

    def jump(self) -> None:
        self._window.type_keys("{SPACE down}")
        time.sleep(.1)
        self._window.type_keys("{SPACE up}")

    def say(self, message: str):
        self._window.type_keys("{t down}")
        time.sleep(.1)
        self._window.type_keys("{t up}")
        self._window.type_keys(message)
        self._window.type_keys("{ENTER}")
