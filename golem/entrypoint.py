import asyncio
import logging
import time
import itertools
import asyncio
import golem.screen
import golem.letters
import golem.minecraft.screen
import golem.minecraft.proto
import golem.minecraft.minecraft

logging.basicConfig(level = logging.DEBUG)

async def circle(data: golem.minecraft.proto.MinecraftData,controller: golem.minecraft.proto.MinecraftController):
    for direction in itertools.cycle(["forwards", "left", "backwards", "right"]):
        coro = getattr(controller, direction)(.3)
        await asyncio.sleep(.1)
        controller.jump()
        await coro
        controller.say(str(data.location()))

async def _entrypoint(minecraft: golem.minecraft.minecraft.Minecraft):
    await minecraft.calibrate()
    for _ in range(1000):
        await minecraft.forwards(1)
        minecraft.look_up(90)
        await minecraft.right(1)
        minecraft.look_up(-90)
        await minecraft.backwards(1)
        minecraft.look_up(90)
        await minecraft.left(1)
        minecraft.look_up(-90)


def entrypoint():
    window = golem.screen.minecraft_window()
    window.type_keys("{VK_ESCAPE}")
    time.sleep(0.05)

    data = golem.minecraft.screen.ScreenData(window)
    controller = golem.minecraft.screen.ScreenController(window)
    minecraft = golem.minecraft.minecraft.Minecraft(data, controller)
    asyncio.run(_entrypoint(minecraft))
