from .consts import *


def create_instruction(cmd, symbol_table):
    for instruction_type in Instruction.__subclasses__():
        if instruction_type.is_of_type(cmd):
            return instruction_type(cmd, symbol_table)
    return Instruction(cmd, symbol_table)


class Instruction(object):
    def __init__(self, cmd, symbol_table):
        self.cmd = cmd
        self.symbol_table = symbol_table

    @staticmethod
    def is_of_type(cmd):
        """
        Returns True if the given `cmd` is of the instruction type.
        """
        raise NotImplementedError()

    def to_binary(self):
        raise NotImplementedError()


class LabelInstruction(Instruction):
    LABEL_REGEX = re.compile('\((?P<label_name>.+)\)')

    @staticmethod
    def is_of_type(cmd):
        return bool(LabelInstruction.LABEL_REGEX.match(cmd))

    def to_binary(self):
        raise Exception('Label instructions do not convert to binary')

    @property
    def variable_name(self):
        return LabelInstruction.LABEL_REGEX.match(self.cmd)['label_name']


class AInstruction(Instruction):
    A_REGEX = re.compile('@(?P<value>[^@]+)')
    A_INSTRUCTION_MAX_LITERAL_SIZE = 32767

    def __init__(self, cmd, symbol_table):
        super().__init__(cmd, symbol_table)

    @staticmethod
    def is_of_type(cmd):
        return bool(AInstruction.A_REGEX.match(cmd))

    def to_binary(self):
        if int(self.get_value()) > AInstruction.A_INSTRUCTION_MAX_LITERAL_SIZE:
            raise Exception('A instruction max literal size exceeded')
        return '0' + f'{int(self.get_value()):b}'.zfill(15)

    def get_value(self):
        value = AInstruction.A_REGEX.match(self.cmd)['value']
        if not value.isdecimal():
            if value not in self.symbol_table:
                self.symbol_table.add_variable(value)
            value = self.symbol_table[value]
        return value


def parse_instruction(line, symbol_table):
    """
    Parses the given assembly line into a machine binary instruction. The returned string is a 16-bit machine binary.
    """
    parsed = lexer.parse(line)
    return parse_c_instruction(parsed)


def parse_c_instruction(parsed):
    comp = parse_comp_part(parsed)
    if any(parsed.find_data('jump')):
        jump_part = parse_jump_instruction(parsed)
        result = comp + '000' + jump_part
    else:
        assign_part = parse_assign_instruction(parsed)
        result = comp + assign_part + '000'

    return '111' + result


def parse_jump_instruction(parsed):
    jmp = next(parsed.find_data('jump'))
    return JMP_TO_BINARY[jmp.children[0].value]


def parse_assign_instruction(parsed):
    dest = next(parsed.find_data('dest'))
    return ('1' if any(dest.scan_values(lambda x: x == 'A')) else '0') + \
           ('1' if any(dest.scan_values(lambda x: x == 'D')) else '0') + \
           ('1' if any(dest.scan_values(lambda x: x == 'M')) else '0')


def parse_comp_part(parsed):
    comp_data = next(parsed.find_data('comp'))
    a_value = '1' if any(comp_data.scan_values(lambda x: x == 'M')) else '0'
    return a_value + COMP_TO_BINARY[comp_data.children[0].data]
