from dataclasses import dataclass
from enum import Enum


Bit = bool

class Byte:
    def __init__(self, bits: tuple[Bit, Bit, Bit, Bit, Bit, Bit, Bit, Bit]):
        ...


class Word:
    def __init__(self, bits: tuple[Byte, Byte]):
        self.bits = bits
