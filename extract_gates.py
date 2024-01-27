import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag, IntTag

import world

chunks_to_check = [(-1, 1)]
overworld = "minecraft:overworld"
start_block = Block(
    "minecraft", "blue_concrete"
)
universal_start_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("blue")
    }
)
end_block = Block(
    "minecraft", "red_concrete"
)
universal_end_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("red")
    }
)

start_level = 42
end_level = 100
chunk_width = 16


def get_start_end(level):
    starts, ends = [], []
    for chunk_coords in chunks_to_check:
        chunk = level.get_chunk(*chunk_coords, overworld)
        for y in range(start_level, end_level):
            for x in range(chunk_width):
                for z in range(chunk_width):
                    block = chunk.block_palette[chunk.blocks[x, y, z]]
                    loc = (x + chunk_coords[0], y, z + chunk_coords[1])
                    if block == universal_start_block:
                        starts.append(loc)
                    elif block == universal_end_block:
                        ends.append(loc)
    return starts, ends


def extract():
    level = amulet.load_level(world.world_path())
    starts, ends = get_start_end(level)
