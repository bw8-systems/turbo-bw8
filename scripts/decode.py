from enum import Enum, auto
from dataclasses import dataclass

INSTRUCTION_WIDTH = 16


class Register(Enum):
    R0 = auto()
    R1 = auto()
    R2 = auto()
    R3 = auto()
    R4 = auto()
    R5 = auto()
    R6 = auto()
    R7 = auto()
    R8 = auto()
    R9 = auto()
    R10 = auto()
    R11 = auto()
    R12 = auto()
    R13 = auto()
    R14 = auto()
    R15 = auto()


class AluOp(Enum):
    ...


@dataclass
class ControlWord:
    register_a: Register
    register_b: Register
    register_c: Register

    alu_function: AluOp


class Opcode(Enum):
    Memory = auto()


def decode_memory():
    ...


for instruction in range(2**INSTRUCTION_WIDTH):
    if instruction & 0b1 == 0:
        decode_memory()

"""
Destinations - All in Register File
a0
a1
a2
a3
lr
io

----
cs
ds
kcs
kds
ilr


MOV16 -> Register File <-> Register File
Sources:
a0, a1, a2, a3, lr
"""
