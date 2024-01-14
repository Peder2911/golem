import golem.minecraft.proto

class Minecraft:
    def __init__(self, data: golem.minecraft.proto.MinecraftData, controller: golem.minecraft.proto.MinecraftController):
        self._data = data
        self._controller = controller
