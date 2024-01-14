import time
import itertools
import asyncio
import golem.screen
import golem.letters
import golem.minecraft.screen
import golem.minecraft.proto

async def circle(data: golem.minecraft.proto.MinecraftData,controller: golem.minecraft.proto.MinecraftController):
    for direction in itertools.cycle(["forwards", "left", "backwards", "right"]):
        coro = getattr(controller, direction)(.3)
        await asyncio.sleep(.1)
        controller.jump()
        await coro
        #print(data.location())
        #print(data.rotation())
        controller.say(str(data.location()))

def entrypoint():
    window = golem.screen.minecraft_window()
    window.type_keys("{VK_ESCAPE}")
    time.sleep(0.05)

    data = golem.minecraft.screen.ScreenData(window)
    controller = golem.minecraft.screen.ScreenController(window)
    while True:
        controller.look_left(8)
        if int(data.rotation()[0]) == 90:
            break

    
