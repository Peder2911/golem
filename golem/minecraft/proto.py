
import typing

class MinecraftData(typing.Protocol):
    def location(self) -> tuple[float,float,float]:
        ...

    def rotation(self) -> tuple[float,float]:
        ...

class MinecraftController(typing.Protocol):
    async def left(self, duration: float) -> None:
        ...

    async def right(self, duration: float) -> None:
        ...

    async def forwards(self, duration: float) -> None:
        ...

    async def backwards(self, duration: float) -> None:
        ...

    def look_left(self, duration: float)-> None:
        ...

    def look_right(self, duration: float)-> None:
        ...

    def look_up(self, duration: float)-> None:
        ...

    def look_down(self, duration: float)-> None:
        ...

    def jump(self) -> None:
        ...

    def say(self, message: str):
        ...
