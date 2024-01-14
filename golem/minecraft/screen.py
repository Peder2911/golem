import re
import time
import asyncio
import golem.minecraft.proto
import golem.screen
import golem.letters
import win32api
import pywinauto.mouse

class ScreenData():
    def __init__(self, window):
        self._window = window
        self._location_pattern = re.compile(r"XYZ: (-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+)")
        self._rotation_pattern = re.compile(r"Facing: [a-z]+ \(Towards [a-z]+ [XYZ]\) \((-?[0-9]+\.[0-9]+) / (-?[0-9]+\.[0-9]+)\)")

    def location(self) -> tuple[float,float,float]:
        location_line = golem.letters.read_line(self._window, 9)
        match = self._location_pattern.search(location_line)
        if match:
            x,y,z = match.groups()
            return float(x), float(y), float(z)
        else:
            raise ValueError(f"Failed to parse location line: \"{location_line}\"")

    def rotation(self) -> tuple[float,float]:
        rotation_line = golem.letters.read_line(self._window, 12)
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

    def _look(self,x:int, y:int):
        cx,cy = self._current_mouse()
        win32api.SetCursorPos((cx+x, cy+y))

    def look_left(self, amount: int)-> None:
        self._look(-amount,0)

    def look_right(self, duration: float)-> None:
        ...

    def look_up(self, duration: float)-> None:
        ...

    def look_down(self, duration: float)-> None:
        ...

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
