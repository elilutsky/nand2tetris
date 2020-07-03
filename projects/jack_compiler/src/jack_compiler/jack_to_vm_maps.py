from enum import Enum

from .tokenizer.tokens import *


class SegmentType(Enum):
    CONSTANT = 'constant'
    LOCAL = 'local'
    ARGUMENT = 'argument'
    THIS = 'this'
    THAT = 'that'
    STATIC = 'static'
    POINTER = 'pointer'
    TEMP = 'temp'


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


JACK_UNARY_OP_TO_VM_COMMAND_MAP = {
    JackSymbol.MINUS: ArithmeticVMCommand.NEG,
    JackSymbol.NOT: ArithmeticVMCommand.NOT
}

JACK_BIN_OP_TO_VM_COMMAND_MAP = {
    JackSymbol.PLUS: ArithmeticVMCommand.ADD,
    JackSymbol.MINUS: ArithmeticVMCommand.SUB,
    JackSymbol.AND: ArithmeticVMCommand.AND,
    JackSymbol.OR: ArithmeticVMCommand.OR,
    JackSymbol.LOWER: ArithmeticVMCommand.LT,
    JackSymbol.GREATER: ArithmeticVMCommand.GT
}




