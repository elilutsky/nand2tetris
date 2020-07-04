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


def translate_jack_op_token_to_vm_command(op_token):
    return JACK_BIN_OP_TO_VM_COMMAND_MAP[op_token.value]


def translate_jack_unary_op_token_to_vm_command(op_token):
    return JACK_UNARY_OP_TO_VM_COMMAND_MAP[op_token.value]


JACK_UNARY_OP_TO_VM_COMMAND_MAP = {
    JackSymbol.MINUS.value: ArithmeticVMCommand.NEG,
    JackSymbol.NOT.value: ArithmeticVMCommand.NOT
}

JACK_BIN_OP_TO_VM_COMMAND_MAP = {
    JackSymbol.PLUS.value: ArithmeticVMCommand.ADD,
    JackSymbol.MINUS.value: ArithmeticVMCommand.SUB,
    JackSymbol.AND.value: ArithmeticVMCommand.AND,
    JackSymbol.OR.value: ArithmeticVMCommand.OR,
    JackSymbol.LOWER.value: ArithmeticVMCommand.LT,
    JackSymbol.GREATER.value: ArithmeticVMCommand.GT,
    JackSymbol.EQUAL.value: ArithmeticVMCommand.EQ
}




