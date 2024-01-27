import xml.etree.ElementTree as ET
from enum import Enum

import amulet
from amulet.api.block import Block

from gate import MinecraftGateBlueprint


CIRCUIT_TAG = "circuit"
GATE_TAG = "comp"
WIRE_TAG = "wire"


class GateDirection(Enum):
    NONE = -1,
    UP = 0,
    DOWN = 1,
    RIGHT = 2,
    LEFT = 3


NOT = "NOT Gate"
AND = "AND Gate"
OR = "OR Gate"
NAND = "NAND Gate"
NOR = "NOR Gate"
XOR = "XOR Gate"


class LogicGate:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.position = (0, 0)
        self.out = []
        self.direction = GateDirection.NONE


minecraft_gate_blueprints = {
    AND: MinecraftGateBlueprint([(0, 1), (0, -1)], [(1, 0)])
}


class MinecraftGate:
    def __init__(self, gate_type, position):
        self.gate_type = gate_type
        self.position = position
        self.direction = GateDirection.RIGHT


# parses the given circuit file and returns a tuple (gates, wires) with the gates and wires in it as xml tree elements
def read_circuit_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    circuit = filter(lambda x: x.tag == CIRCUIT_TAG, root)
    gates = list(filter(lambda part: part.attrib["name"] == GATE_TAG, circuit))
    wires = list(filter(lambda part: part.attrib["name"] == WIRE_TAG, circuit))
    return gates, wires

