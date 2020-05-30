from enum import Enum
from collections import namedtuple

Command = namedtuple('Command', ['command', 'command_type'])


class SegmentType(Enum):
    CONSTANT = 'constant'
    LOCAL = 'local'
    ARGUMENT = 'argument'
    THIS = 'this'
    THAT = 'that'
    STATIC = 'static'
    POINTER = 'pointer'
    TEMP = 'temp'


class CommandType(Enum):
    ARITHMETIC = 1
    POP = 2
    PUSH = 3
    BRANCH = 4


class Commands(Enum):
    ADD = Command('add', CommandType.ARITHMETIC)
    SUB = Command('sub', CommandType.ARITHMETIC)
    NEG = Command('neg', CommandType.ARITHMETIC)
    EQ = Command('eq', CommandType.ARITHMETIC)
    GT = Command('gt', CommandType.ARITHMETIC)
    LT = Command('lt', CommandType.ARITHMETIC)
    AND = Command('and', CommandType.ARITHMETIC)
    OR = Command('or', CommandType.ARITHMETIC)
    NOT = Command('not', CommandType.ARITHMETIC)
    POP = Command('pop', CommandType.POP)
    PUSH = Command('push', CommandType.PUSH)
    LABEL = Command('label', CommandType.BRANCH)
    GOTO = Command('goto', CommandType.BRANCH)
    IF_GOTO = Command('if-goto', CommandType.BRANCH)

    @staticmethod
    def by_command(cmd):
        return next(filter(lambda x: x.value.command == cmd, Commands))


class VMCommand(object):
    def __init__(self, command_str):
        self._command_str = command_str

    @property
    def _command_op(self):
        return self._command_str.split()[0]

    @property
    def command_type(self):
        return Commands.by_command(self._command_op).value.command_type

    @property
    def command(self):
        return Commands.by_command(self._command_op)

    @property
    def arg1(self):
        return self._command_str.split()[1]

    @property
    def arg2(self):
        return self._command_str.split()[2]


def parse_code(input_code_file):
    for line in input_code_file:

        # skip emtpy lines and comments
        if len(line.split()) == 0 or line.split()[0] == '//':
            continue

        yield VMCommand(line)
