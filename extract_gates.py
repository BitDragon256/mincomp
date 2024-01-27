import amulet
from amulet.api.block import Block
from amulet.utils.world_utils import block_coords_to_chunk_coords
from amulet_nbt import StringTag, IntTag

import numpy as np

import world
from gate import MinecraftGateBlueprint, BlockArray

chunks_to_check = [(-1, 1)]
overworld = "minecraft:overworld"
universal_start_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("blue")
    }
)
universal_end_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("red")
    }
)
universal_inport_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("white")
    }
)
universal_outport_block = Block(
    "universal_minecraft",
    "concrete",
    {
        "color": StringTag("orange")
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
                    loc = (x + chunk_coords[0] * chunk_width, y, z + chunk_coords[1] * chunk_width)
                    if block == universal_start_block:
                        starts.append(loc)
                    elif block == universal_end_block:
                        ends.append(loc)
    return starts, ends


def manhattan_distance(start, end):
    dist = 0
    for d in range(3):
        dd = end[d] - start[d]
        if dd <= 0:
            return -1
        dist += dd
    return dist


def merge_start_end(starts, ends):
    boundings = []
    for start in starts:
        min_end = ends[0]
        min_dist = 1000000
        for end in ends:
            dist = manhattan_distance(start, end)
            if min_dist > dist > 0:
                min_end = end
                min_dist = dist
        boundings.append((start, min_end))
    return boundings


def to_chunk(level, x, z):
    cx, cz = block_coords_to_chunk_coords(x, z)
    ox, oz = x - cx * chunk_width, z - cz * chunk_width
    return (cx, cz), (ox, oz)


def get_gates(level, boundings):
    gates = []
    for bounding in boundings:
        inports, outports = [], []

        start, end = bounding
        blocks = BlockArray(
            end[0] - start[0] + 1,
            end[1] - start[1] + 1,
            end[2] - start[2] + 1
        )
        for x in range(start[0], end[0] + 1):
            for z in range(start[2], end[2] + 1):
                (cx, cz), (ox, oz) = to_chunk(level, x, z)
                chunk = level.get_chunk(cx, cz, overworld)
                for y in range(start[1], end[1] + 1):
                    block = chunk.block_palette[chunk.blocks[ox, y, oz]]
                    blocks[x - start[0], y - start[1], z - start[2]] = block
                    loc = (x, y, z)
                    if block == universal_inport_block:
                        inports.append(loc)
                    elif block == universal_outport_block:
                        outports.append(loc)

        (cx, cy, cz) = bounding[0]  # center
        for inport in inports:
            x, y, z = inport
            inport = (x - cx, y - cy, z - cz)
        for outport in outports:
            x, y, z = outport
            outport = (x - cx, y - cy, z - cz)

        gates.append(MinecraftGateBlueprint(
            inports,
            outports,
            bounding,
            blocks
        ))
    return gates


def extract():
    level = amulet.load_level(world.world_path())
    starts, ends = get_start_end(level)
    boundings = merge_start_end(starts, ends)
    gates = get_gates(level, boundings)