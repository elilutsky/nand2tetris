from enum import Enum


class SegmentType(Enum):
    CONSTANT = 'constant'
    LOCAL = 'local'
    ARGUMENT = 'argument'
    THIS = 'this'
    THAT = 'that'
    STATIC = 'static'
    POINTER = 'pointer'
    TEMP = 'temp'


class SymbolKind(Enum):
    FIELD = 'field kind'
    STATIC = 'static kind'
    ARGUMENT = 'argument kind'
    LOCAL = 'local kind'


class ArithmeticVMCommand(Enum):
    ADD = 'add'
    SUB = 'sub'
    NEG = 'neg'
    EQ = 'eq'
    GT = 'gt'
    LT = 'lt'
    AND = 'and'
    OR = 'or'
    NOT = 'not'


SYMBOL_KIND_TO_SEGMENT_MAP = {
    SymbolKind.FIELD: SegmentType.THIS,
    SymbolKind.STATIC: SegmentType.STATIC,
    SymbolKind.ARGUMENT: SegmentType.ARGUMENT,
    SymbolKind.LOCAL: SegmentType.LOCAL
}

JACK_BIN_OP_TO_VM_COMMAND_MAP = {

}




