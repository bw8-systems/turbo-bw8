import enum
from dataclasses import dataclass

# inst[8] @ inst[14:9] @ inst[7:4] @ Bit(0)*4


# class Word:
#     def __init__(self, word: int):
#         split = list(bin(word)[2:])
#         while len(split) != 16:
#             split.insert(0, "0")

#         self.as_str =  "".join(split)

#     def __getitem__(self, index: int) -> int


class MemoryWriteMode(enum.Enum):
    Disabled = enum.auto()
    Word = enum.auto()
    Byte = enum.auto()


class WritebackMode(enum.Enum):
    Disabled = enum.auto()
    AluResult = enum.auto()
    MemoryResult = enum.auto()


class AluOperation(enum.Enum):
    Nop = 0  # TODO: Keep?
    Lhs = 1
    Add = 2
    Addc = 3
    Sub = 4
    Subb = 5
    And = 6
    Or = 7
    Xor = 8
    Shl = 9
    Lsr = 10
    Asr = 11


class JumpCondition(enum.Enum):
    Always = enum.auto()
    Never = enum.auto()
    Equal = enum.auto()
    NotEqual = enum.auto()
    LessThan = enum.auto()
    GreaterEqual = enum.auto()
    SignedLessThan = enum.auto()
    SignedGreaterEqual = enum.auto()


@dataclass
class ControlWord:
    MemoryReadEnable: bool  # 1
    MemoryWriteEnable: MemoryWriteMode  # 2
    WritebackEnable: WritebackMode  # 2
    AluOperation: AluOperation  # 4
    Immediate: int  # 3
    JumpCondition: JumpCondition  # 3


def decode_lui(inst: str) -> ControlWord:
    inst[8] @ inst[14:9] @ inst[7:4] @ Bit(0) * 4

    return ControlWord(
        MemoryReadEnable=False,
        MemoryWriteEnable=False,
        WritebackEnable=WritebackMode.AluResult,
        AluOperation=AluOperation.Nop,  # TODO
        ImmediateMode=ImmediateMode.Lui,
        JumpCondition=JumpCondition.Never,
    )


def decode_mem8(inst: str) -> ControlWord:
    ...


def decode_mem16(inst: str) -> ControlWord:
    ...


def decode_alu2(inst: str) -> ControlWord:
    ...


def decode_alu1_imm_wide(inst: str) -> ControlWord:
    ...


def decode_branch(inst: str) -> ControlWord:
    ...


def decode_alu1_imm(inst: str) -> ControlWord:
    ...


def decode_stz(inst: str) -> ControlWord:
    ...


def decode_alu1(inst: str) -> ControlWord:
    ...


def decode_interrupt(inst: str) -> ControlWord:
    ...


def decode_zero_op(inst: str) -> ControlWord:
    ...


def instructions():
    for val in range(2**16):
        split = list(bin(val)[2:])
        while len(split) != 16:
            split.insert(0, "0")
        yield "".join(split)


control_words = list[ControlWord]()

for inst in instructions():
    if inst.startswith("0"):
        control_words.append(decode_lui(inst))
    if inst.startswith("10"):
        control_words.append(decode_mem8(inst))
    if inst.startswith("110"):
        control_words.append(decode_mem16(inst))
    if inst.startswith("1110"):
        control_words.append(decode_alu2(inst))
    if inst.startswith("11110"):
        control_words.append(decode_alu1_imm_wide(inst))
    if inst.startswith("111110"):
        control_words.append(decode_branch(inst))
    if inst.startswith("1111110"):
        control_words.append(decode_alu1_imm(inst))
    if inst.startswith("11111110"):
        control_words.append(decode_stz(inst))
    if inst.startswith("111111110"):
        control_words.append(decode_alu1(inst))
    if inst.startswith("1111111110"):
        control_words.append(decode_interrupt(inst))
    if inst.startswith("1111111111"):
        control_words.append(decode_zero_op(inst))

print(len(control_words) / 1024)
