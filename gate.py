import amulet
from amulet.api.block import Block


class BlockArray:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.data = [[[Block("universal_minecraft", "air") for z in range(sz)] for y in range(sy)] for x in range(sx)]

    def __getitem__(self, key):
        x, y, z = key
        self.check_bounds(key)
        return self.data[x][y][z]

    def __setitem__(self, key, value):
        x, y, z = key
        self.check_bounds(key)
        self.data[x][y][z] = value

    def __repr__(self):
        s = ""
        sx, sy, sz = self.size
        for y in range(sy):
            s += "["
            for z in range(sz):
                s += "["
                for x in range(sx):
                    s += f"{self[x, y, z]}"
                    if x != sx - 1:
                        s += ", "
                s += "]"
                if z != sz - 1:
                    s += ",\n"
            s += "]"
            if y != sy - 1:
                s += ",\n\n"

        return s

    def check_bounds(self, key):
        for i in range(3):
            if key[i] < 0 or key[i] >= self.size[i]:
                raise Exception(f"index {key} is out of bounds for array of size {self.size}")


class MinecraftGateBlueprint:
    def __init__(self, inport_positions, outport_positions, bounding_box, blocks):
        self.inport_positions = inport_positions
        self.outport_positions = outport_positions
        self.bounding_box = bounding_box
        self.blocks = blocks

    def __repr__(self):
        return f"Gate: Bounding: {self.bounding_box}, In: {self.inport_positions}, Out: {self.outport_positions}"
