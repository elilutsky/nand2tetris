from enum import Enum

from .tokenizer.tokens import *


class VMSegmentType(Enum):
    CONSTANT = 'constant'
    LOCAL = 'local'
    ARGUMENT = 'argument'
    THIS = 'this'
    THAT = 'that'
    STATIC = 'static'
    POINTER = 'pointer'
    TEMP = 'temp'


class VMArithmeticCommand(Enum):
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
    JackSymbol.MINUS.value: VMArithmeticCommand.NEG,
    JackSymbol.NOT.value: VMArithmeticCommand.NOT
}

JACK_BIN_OP_TO_VM_COMMAND_MAP = {
    JackSymbol.PLUS.value: VMArithmeticCommand.ADD,
    JackSymbol.MINUS.value: VMArithmeticCommand.SUB,
    JackSymbol.AND.value: VMArithmeticCommand.AND,
    JackSymbol.OR.value: VMArithmeticCommand.OR,
    JackSymbol.LOWER.value: VMArithmeticCommand.LT,
    JackSymbol.GREATER.value: VMArithmeticCommand.GT,
    JackSymbol.EQUAL.value: VMArithmeticCommand.EQ
}




