import enum
from dataclasses import dataclass


class Register(enum.IntEnum):
    R0 = 0
    R1 = enum.auto()
    R2 = enum.auto()
    R3 = enum.auto()
    R4 = enum.auto()
    R5 = enum.auto()
    R6 = enum.auto()
    R7 = enum.auto()
    R8 = enum.auto()
    R9 = enum.auto()
    R10 = enum.auto()
    R11 = enum.auto()
    R12 = enum.auto()
    R13 = enum.auto()
    R14 = enum.auto()
    R15 = enum.auto()

    LinkRegister = R15


class ImmediateFormat(enum.IntEnum):
    Lui = 0
    Mem = enum.auto()
    Jmp = enum.auto()
    Alu = enum.auto()
    JmpR = enum.auto()
    Stz = enum.auto()


class MemoryMode(enum.IntEnum):
    Disabled = 0
    ReadWord = enum.auto()
    ReadByte = enum.auto()
    WriteWord = enum.auto()
    WriteByte = enum.auto()


class MemoryOperationFormat(enum.Enum):
    Word = enum.auto()
    Byte = enum.auto()


class WritebackMode(enum.IntEnum):
    Disabled = 0
    AluResult = enum.auto()
    MemoryResult = enum.auto()


class AluFunction(enum.IntEnum):
    Nop = 0  # TODO: Keep?
    Lhs = enum.auto()
    Rhs = enum.auto()  # TODO: Both??
    Add = enum.auto()
    Addc = enum.auto()
    Sub = enum.auto()
    Subb = enum.auto()
    And = enum.auto()
    Or = enum.auto()
    Xor = enum.auto()
    Shl = enum.auto()
    Lsr = enum.auto()
    Asr = enum.auto()
    Swap = enum.auto()
    Sxt = enum.auto()


class JumpCondition(enum.IntEnum):
    Always = 0
    Never = enum.auto()
    Equal = enum.auto()
    NotEqual = enum.auto()
    LessThan = enum.auto()
    GreaterEqual = enum.auto()
    SignedLessThan = enum.auto()
    SignedGreaterEqual = enum.auto()


class LeftSelect(enum.IntEnum):
    SourceRegister = 0
    ProgramCounter = enum.auto()


class RightSelect(enum.IntEnum):
    DestinationRegister = 0
    Immediate = enum.auto()


@dataclass
class ControlWord:
    left_select: LeftSelect = LeftSelect(0)
    right_select: RightSelect = RightSelect(0)
    memory_mode: MemoryMode = MemoryMode(0)
    writeback_mode: WritebackMode = WritebackMode(0)
    alu_function: AluFunction = AluFunction(0)
    immediate_format: ImmediateFormat = ImmediateFormat(0)
    jump_condition: JumpCondition = JumpCondition(0)
    source_register: Register = Register(0)
    destination_register: Register = Register(0)


class BitString:
    def __init__(self, value: int, width: int = 16):
        self.width = width
        self.value = value

    def __str__(self) -> str:
        return bin(self.value)

    def is_clear(self, index: int) -> bool:
        assert index < self.width
        masked = self.value & (1 << index)
        return masked == 0

    def is_set(self, index: int) -> bool:
        return not self.is_clear(index)

    def field(self, *, width: int, offset: int) -> "BitString":
        return BitString(
            (self.value & ((2**width - 1) << offset)) >> offset, width=width
        )

    def into[T](self, transform: type[T]) -> T:
        return transform(self.value)


NOP = ControlWord(
    left_select=LeftSelect.SourceRegister,
    right_select=RightSelect.DestinationRegister,
    memory_mode=MemoryMode.Disabled,
    writeback_mode=WritebackMode.Disabled,
    alu_function=AluFunction.Nop,
    immediate_format=ImmediateFormat.Alu,
    jump_condition=JumpCondition.Never,
    destination_register=Register.R0,
    source_register=Register.R0,
)

INSTRUCTION_WIDTH = 16


def source_register(inst: BitString) -> Register:
    return inst.field(width=4, offset=4).into(Register)


def destination_register(inst: BitString) -> Register:
    return inst.field(width=4, offset=0).into(Register)


def lui(inst: BitString) -> ...:
    return ControlWord(
        immediate_format=ImmediateFormat.Lui,
        destination_register=inst.field(width=4, offset=0).into(Register),
    )


def mem(inst: BitString, format: MemoryOperationFormat) -> ControlWord:
    if format is MemoryOperationFormat.Word:
        read = MemoryMode.ReadWord
        write = MemoryMode.WriteWord
    else:
        read = MemoryMode.ReadByte
        write = MemoryMode.WriteByte

    is_load = inst.is_clear(13)
    dest = destination_register(inst)
    source = source_register(inst)

    return ControlWord(
        immediate_format=ImmediateFormat.Mem,
        left_select=LeftSelect.SourceRegister,
        right_select=RightSelect.DestinationRegister,
        alu_function=AluFunction.Add,
        destination_register=dest,
        source_register=source,
        memory_mode=read if is_load else write,
        writeback_mode=(
            WritebackMode.MemoryResult if is_load else WritebackMode.Disabled
        ),
    )


def alu2(inst: BitString) -> ControlWord:
    dest = destination_register(inst)
    source = source_register(inst)

    left_select = LeftSelect.SourceRegister
    right_select = RightSelect.DestinationRegister

    match inst.field(width=4, offset=8).into(int):
        case 0b0000:
            func = AluFunction.Lhs
        case 0b0001:
            func = AluFunction.Add
        case 0b0010:
            func = AluFunction.Addc
        case 0b0011:
            func = AluFunction.Sub
        case 0b0100:
            func = AluFunction.Subb
        case 0b0101:
            func = AluFunction.And
        case 0b0110:
            func = AluFunction.Or
        case 0b0111:
            func = AluFunction.Xor
        case 0b1000:
            func = AluFunction.Shl
        case 0b1001:
            func = AluFunction.Lsr
        case 0b1010:
            func = AluFunction.Asr
        case 0b1011:
            func = AluFunction.Sub
        case 0b1100:
            func = (
                AluFunction.Lhs
            )  # TODO: 0b1100 represents mv vec, gpr and mv gpr, vec. For now, this is just a normal mv gpr
        case 0b1101:
            # TODO: Handle immediate mode functions
            func = AluFunction.Shl
        case 0b1110:
            # TODO: Handle immediate mode functions
            func = AluFunction.Lsr
        case 0b1111:
            # TODO: Handle immediate mode functions
            func = AluFunction.Asr
        case _:
            assert False

    return ControlWord(
        immediate_format=ImmediateFormat.Alu,
        alu_function=func,
        left_select=left_select,
        right_select=right_select,
        destination_register=dest,
        source_register=source,
        memory_mode=MemoryMode.Disabled,
        writeback_mode=WritebackMode.AluResult,
    )


def op11(inst: BitString) -> ControlWord:
    dest = destination_register(inst)
    source = source_register(inst)

    match inst.field(width=2, offset=9).into(int):
        case 0b00:
            # This is lli
            return ControlWord(
                left_select=LeftSelect.SourceRegister,
                right_select=RightSelect.Immediate,
                immediate_format=ImmediateFormat.Alu,
                memory_mode=MemoryMode.Disabled,
                writeback_mode=WritebackMode.AluResult,
                jump_condition=JumpCondition.Never,
                destination_register=dest,
                source_register=source,
                alu_function=AluFunction.Rhs,
            )
        case 0b01:  # addi
            return ControlWord(
                left_select=LeftSelect.SourceRegister,
                right_select=RightSelect.Immediate,
                immediate_format=ImmediateFormat.Alu,
                memory_mode=MemoryMode.Disabled,
                writeback_mode=WritebackMode.AluResult,
                jump_condition=JumpCondition.Never,
                destination_register=dest,
                source_register=source,
                alu_function=AluFunction.Add,
            )
        case 0b10:  # cmpi
            return ControlWord(
                left_select=LeftSelect.SourceRegister,
                right_select=RightSelect.Immediate,
                immediate_format=ImmediateFormat.Alu,
                memory_mode=MemoryMode.Disabled,
                writeback_mode=WritebackMode.Disabled,
                jump_condition=JumpCondition.Never,
                destination_register=dest,
                source_register=source,
                alu_function=AluFunction.Sub,
            )
        case 0b11:
            if inst.is_clear(3):  # j
                return ControlWord(
                    left_select=LeftSelect.SourceRegister,
                    right_select=RightSelect.Immediate,
                    immediate_format=ImmediateFormat.Jmp,
                    memory_mode=MemoryMode.Disabled,
                    writeback_mode=WritebackMode.Disabled,
                    jump_condition=JumpCondition.Always,
                    destination_register=dest,
                    source_register=source,
                    alu_function=AluFunction.Add,
                )
            else:  # jal
                return ControlWord(
                    left_select=LeftSelect.SourceRegister,
                    right_select=RightSelect.Immediate,
                    immediate_format=ImmediateFormat.Jmp,
                    memory_mode=MemoryMode.Disabled,
                    writeback_mode=WritebackMode.AluResult,
                    jump_condition=JumpCondition.Always,
                    destination_register=Register.LinkRegister,
                    source_register=source,
                    alu_function=AluFunction.Add,
                )
        case _:
            assert False


def branch(inst: BitString) -> ControlWord:
    if inst.is_clear(9):
        # TODO: This is mv mmu, gpr or mv gpr, mmu
        return NOP

    match inst.field(width=3, offset=0).into(int):
        case 0b000:
            condition = JumpCondition.Always
        case 0b001:
            condition = JumpCondition.Always
        case 0b010:
            condition = JumpCondition.Equal
        case 0b011:
            condition = JumpCondition.NotEqual
        case 0b100:
            condition = JumpCondition.LessThan
        case 0b101:
            condition = JumpCondition.GreaterEqual
        case 0b110:
            condition = JumpCondition.SignedLessThan
        case 0b111:
            condition = JumpCondition.SignedGreaterEqual
        case _:
            assert False

    return ControlWord(
        left_select=LeftSelect.ProgramCounter,
        right_select=RightSelect.Immediate,
        memory_mode=MemoryMode.Disabled,
        writeback_mode=WritebackMode.Disabled,  # TODO: enable for JAL / JALR
        alu_function=AluFunction.Add,
        immediate_format=ImmediateFormat.JmpR,
        jump_condition=condition,
        destination_register=Register.LinkRegister,
        source_register=Register.R0,
    )


def bitwise_imm(inst: BitString) -> ControlWord:
    function = AluFunction.And if inst.is_clear(8) else AluFunction.Or

    return ControlWord(
        alu_function=function,
    )


def stz(inst: BitString) -> ControlWord:
    return ControlWord(
        left_select=LeftSelect.SourceRegister,
        right_select=RightSelect.DestinationRegister,
        immediate_format=ImmediateFormat.Stz,
        memory_mode=MemoryMode.WriteWord,
        writeback_mode=WritebackMode.Disabled,
        alu_function=AluFunction.Nop,
        jump_condition=JumpCondition.Never,
        destination_register=Register.R0,
        source_register=source_register(inst),
    )


def alu1(inst: BitString) -> ControlWord:
    dest = destination_register(inst)
    source = source_register(inst)

    match inst.field(width=3, offset=4).into(int):
        case 0b000:  # not
            function = (
                AluFunction.Or
            )  # TODO! Need NOT as a function, or need to be able to produce xor -1
        case 0b001:  # apc
            function = AluFunction.Add
        case 0b010:  # neg
            function = AluFunction.Sub  # TODO: Probably not right just guessing rn
        case 0b011:  # negb
            function = AluFunction.Subb  # TODO: probably not right just guessing rn
        case 0b100:  # swap
            function = AluFunction.Swap
        case 0b101:  # sxt
            function = AluFunction.Sxt
        case 0b110:  # unused
            return NOP
        case 0b111:  # unused
            return NOP
        case _:
            assert False

    return ControlWord(
        left_select=LeftSelect.SourceRegister,
        right_select=RightSelect.DestinationRegister,
        memory_mode=MemoryMode.Disabled,
        writeback_mode=WritebackMode.AluResult,
        alu_function=function,  # TODO
        immediate_format=ImmediateFormat.Alu,
        jump_condition=JumpCondition.Never,
        destination_register=dest,
        source_register=source,
    )


def spr(_inst: BitString) -> ControlWord:
    return NOP


def op5(_inst: BitString) -> ControlWord:
    return NOP


def env(_inst: BitString) -> ControlWord:
    return NOP


def interrupt(_inst: BitString) -> ControlWord:
    return NOP


def zero(_inst: BitString) -> ControlWord:
    return NOP


def decode_instruction(instruction: int) -> ControlWord:
    bits = BitString(instruction)
    if bits.is_clear(15):
        return lui(bits)
    if bits.is_clear(14):
        return mem(bits, MemoryOperationFormat.Byte)
    if bits.is_clear(13):
        return mem(bits, MemoryOperationFormat.Word)
    if bits.is_clear(12):
        return alu2(bits)
    if bits.is_clear(11):
        return op11(bits)
    if bits.is_clear(10):
        return branch(bits)
    if bits.is_clear(9):
        return bitwise_imm(bits)
    if bits.is_clear(8):
        return stz(bits)
    if bits.is_clear(7):
        return alu1(bits)
    if bits.is_clear(6):
        return spr(bits)
    if bits.is_clear(5):
        return op5(bits)
    if bits.is_clear(4):
        return env(bits)
    if bits.is_clear(3):
        return interrupt(bits)
    else:
        return zero(bits)


control_words = list[ControlWord]()
for instruction in range(2**INSTRUCTION_WIDTH):
    word = decode_instruction(instruction)
    control_words.append(word)


with open("decoder.bin", "wb") as f:
    for word in control_words:
        binary = (
            word.left_select
            | (word.right_select << 1)
            | (word.memory_mode << 2)
            | (word.writeback_mode << 5)
            | (word.alu_function << 7)
            | (word.immediate_format << 11)
            | (word.jump_condition << 14)
            | (word.source_register << 17)
            | (word.destination_register << 21)
        )
        f.write(binary.to_bytes(4, byteorder="little"))
