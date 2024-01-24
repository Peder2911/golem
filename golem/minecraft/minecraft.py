import asyncio
import logging
import golem.minecraft.proto

CALIB_LEN = 2
MOVEMENT_BUFFER_TIME = .5 

logger = logging.getLogger(__name__)

class Minecraft:
    def __init__(self, data: golem.minecraft.proto.MinecraftData, controller: golem.minecraft.proto.MinecraftController):
        self._data = data
        self._controller = controller

        self._xd = .0
        self._yd = .0
        self._md = .0

    def _calibrate_rotation(self):
        x_1,y_1=self._data.rotation()
        self._controller.look_left(CALIB_LEN)
        self._controller.look_up(CALIB_LEN)
        x_2,y_2=self._data.rotation()
        self._xd = abs(x_2 - x_1) / CALIB_LEN
        self._yd = abs(y_2 - y_1) / CALIB_LEN
        logger.debug(f"Calibrated: {self._xd}, {self._yd}")


    async def calibrate(self):
        while not self._aligned:
            self._calibrate_rotation()
            self.align()

        _,_,z_1 = self._data.location()
        await self._controller.forwards(CALIB_LEN/2)
        await asyncio.sleep(MOVEMENT_BUFFER_TIME)
        _,_,z_2 = self._data.location()
        self._md = (z_2 - z_1)*2
        await self._controller.backwards(CALIB_LEN/2)
        await asyncio.sleep(MOVEMENT_BUFFER_TIME)


    def align(self):
        x,y = self._data.rotation()
        self.look_left(x)
        self.look_up(y)
    
    @property
    def _aligned(self):
        x,y = self._data.rotation()
        return abs(x) < 0.2 and abs(y) < 0.2

    async def left(self, units):
        if self._md:
            await self._controller.left(units / self._md)
            await asyncio.sleep(MOVEMENT_BUFFER_TIME)

    async def right(self, units):
        if self._md:
            await self._controller.right(units / self._md)
            await asyncio.sleep(MOVEMENT_BUFFER_TIME)

    async def forwards(self, units):
        if self._md:
            await self._controller.forwards(units / self._md)
            await asyncio.sleep(MOVEMENT_BUFFER_TIME)

    async def backwards(self, units):
        if self._md:
            await self._controller.backwards(units / self._md)
            await asyncio.sleep(MOVEMENT_BUFFER_TIME)
    
    def look_left(self, degrees):
        if self._xd:
            self._controller.look_left(degrees / self._xd)
    
    def look_up(self, degrees):
        if self._yd:
            self._controller.look_up(degrees / self._yd)
