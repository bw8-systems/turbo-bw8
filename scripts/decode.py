import enum


class Opcode(enum.Enum):
    System = enum.auto()
    AluBinary = enum.auto()
    AluUnary = enum.auto()
    AddImm = enum.auto()
    CmpImm = enum.auto()
    LoadImm = enum.auto()
    Call = enum.auto()
    Jump = enum.auto()
