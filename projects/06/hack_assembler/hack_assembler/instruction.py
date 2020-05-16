from .consts import *


def create_instruction(cmd):
    for instruction_type in [LabelInstruction]:
        if instruction_type.is_of_type(cmd):
            return instruction_type(cmd)
    return Instruction(cmd)


class Instruction(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def to_binary(self):
        raise NotImplementedError()

    @staticmethod
    def is_of_type(cmd):
        raise NotImplementedError()


class LabelInstruction(Instruction):
    LABEL_REGEX = re.compile('((?P<label_name>.+))')

    def to_binary(self):
        raise Exception('Label instructions do not convert to binary')

    @staticmethod
    def is_of_type(cmd):
        return LABEL_REGEX.match(cmd)

    @property
    def variable_name(self):
        return LABEL_REGEX.match(self.cmd)['label_name']


def parse_instruction(line, symbol_table):
    """
    Parses the given assembly line into a machine binary instruction. The returned string is a 16-bit machine binary.
    """
    parsed = lexer.parse(line)
    if hasattr(parsed.children[0], 'value') and parsed.children[0].value == '@':
        return parse_a_instruction(parsed, symbol_table)
    else:
        return parse_c_instruction(parsed)


def parse_a_instruction(parsed, symbol_table):
    value = next(parsed.find_data('value')).children[0].value

    if not value.isdecimal():
        # Encountered variable
        if value not in symbol_table:
            symbol_table.add_variable(value)
        value = symbol_table[value]

    if int(value) > A_INSTRUCTION_MAX_LITERAL_SIZE:
        raise Exception('A instruction max literal size exceeded')
    return '0' + f'{int(value):b}'.zfill(15)


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
