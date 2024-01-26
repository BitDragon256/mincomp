import amulet
from amulet.api.block import Block


def edit_block():
    # load the level
    level = amulet.load_level("Z:/Programm/MultiMC/instances/1.20.1/.minecraft/saves/Testing Redstone")

    # pick a game version that we want to work with.
    # see the next page to see what versions are available.
    game_version = ("java", (1, 20, 1))  # the version that we want the block data in.

    # get a block
    block, block_entity = level.get_version_block(
        0,  # x location
        70,  # y location
        0,  # z location
        "minecraft:overworld",  # dimension
        game_version,
    )

    if isinstance(block, Block):
        # Check that what we have is actually a block.
        # There are some edge cases such as item frames where the returned value might not be a Block.
        print(block)
        # Block(minecraft:air)

    # set a block
    # define a block in the format of the version we want to work with.
    block = Block("minecraft", "stone")
    level.set_version_block(
        0,  # x location
        70,  # y location
        0,  # z location
        "minecraft:overworld",  # dimension
        game_version,
        block,
    )

    # save the changes to the world
    level.save()

    # close the world
    level.close()


def complex_set_block():
    import amulet
    from amulet.api.block import Block
    from amulet.utils.world_utils import block_coords_to_chunk_coords
    from amulet_nbt import StringTag, IntTag

    # load the level
    level = amulet.load_level("Z:/Programm/MultiMC/instances/1.20.1/.minecraft/saves/Testing Redstone")

    # let's set the block at 15, 70, 17 and 15, 72, 17 to be green glazed
    # terracotta using the Java and Bedrock formats respectively.

    # Note that the format you define the block in does not need to match the world you are writing the block to.
    # The translator will handle block translating it to the correct format.

    # First we need to define the Block object for each of the formats.
    # The translator holds a specification for each block for each version which the UI is built off.
    # You can also look at the Minecraft wiki to find the blockstate format.
    java_block = Block(
        "minecraft", "green_glazed_terracotta", {"facing": StringTag("south")}
    )
    bedrock_block = Block(
        "minecraft", "green_glazed_terracotta", {"facing_direction": IntTag(3)}
    )

    # Then we can translate the block to the universal format.
    (
        universal_block_1,
        universal_block_entity_1,
        universal_extra_1,
    ) = level.translation_manager.get_version("java", (1, 16, 5)).block.to_universal(
        java_block
        # if your block has a block entity you can give it as a second input here.
    )
    # Block(universal_minecraft:glazed_terracotta[color="green",facing="south"]), None, False

    # Use the translator to convert the block to the universal format.
    (
        universal_block_2,
        universal_block_entity_2,
        universal_extra_2,
    ) = level.translation_manager.get_version("bedrock", (1, 16, 210)).block.to_universal(
        bedrock_block
        # if your block has a block entity you can give it as a second input here.
    )
    # Block(universal_minecraft:glazed_terracotta[color="green",facing="south"]), None, False

    # The boolean output at the end can for the most part be ignored but lets explain the use of it.
    # There are certain cases that require more than just the block state to fully define the block.
    # If the translator is not able to fully define the translation it will return that value as True.
    # The calling code can then give it more data to fully define the translation.

    # Blocks with a block entity is a simple example.
    # Doing the translation without the block entity will use the default NBT data and return the value as True.
    # The calling code can then call the translator again with the block entity.

    # Another example is multi-block structures such as doors in older versions of the game.
    # Doors used to split the state data over the bottom and top block.
    # The translator has the ability to reach back into the world to inspect neighbour blocks to get this extra data.
    # This is done through a callback function given to the translator.

    # Now we now have the universal block state converted from both Bedrock and Java. Lets set the data in the level.

    # First we need to register the Block objects with the block palette to get the runtime block id.
    block_id_1 = level.block_palette.get_add_block(universal_block_1)
    block_id_2 = level.block_palette.get_add_block(universal_block_2)
    # In this case the two translations gave the same universal block object so the block ids are the same.

    # This code was documented in the previous example so I won't do it again.
    x, z = 15, 17
    cx, cz = block_coords_to_chunk_coords(x, z)
    chunk = level.get_chunk(cx, cz, "minecraft:overworld")
    offset_x, offset_z = x - 16 * cx, z - 16 * cz

    # set the blocks into the world.
    chunk.blocks[offset_x, 70, offset_z] = block_id_1
    chunk.blocks[offset_x, 72, offset_z] = block_id_2

    # Set the block entities.
    for block_entity, location in (
            (universal_block_entity_1, (15, 70, 17)),
            (universal_block_entity_2, (15, 72, 17)),
    ):
        if block_entity is not None:
            # if there is a block entity to go along with the block we just set,
            # add it to the chunks block entities.
            chunk.block_entities[location] = block_entity
        elif location in chunk.block_entities:
            # if there is no new block entity and there was one present from the previous block, remove it.
            del chunk.block_entities[location]

    # we have changed the chunk data, so we need to set this value otherwise it won't get saved.
    chunk.changed = True

    # save and close the world
    level.save()
    level.close()
