from enum import Enum
from collections import namedtuple

Command = namedtuple('Command', ['command', 'command_type'])


class SegmentType(Enum):
    CONSTANT = 'constant'


class CommandType(Enum):
    ARITHMETIC = 1
    POP = 2
    PUSH = 3


class Commands(Enum):
    ADD = Command('add', CommandType.ARITHMETIC)
    SUB = Command('sub', CommandType.ARITHMETIC)
    NEG = Command('neg', CommandType.ARITHMETIC)
    EQ = Command('eg', CommandType.ARITHMETIC)
    GT = Command('gt', CommandType.ARITHMETIC)
    AND = Command('and', CommandType.ARITHMETIC)
    OR = Command('or', CommandType.ARITHMETIC)
    NOT = Command('not', CommandType.ARITHMETIC)
    POP = Command('pop', CommandType.POP)
    PUSH = Command('push', CommandType.PUSH)

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


def filter_irrelevant_lines(code):
    return filter(None, filter(lambda x: not x.startswith('//'), code))


def parse_code(code):
    for line in filter_irrelevant_lines(code.splitlines()):
        yield VMCommand(line)
