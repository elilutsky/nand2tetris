import re


def create_instruction(cmd, symbol_table):
    for instruction_type in Instruction.__subclasses__():
        if instruction_type.is_of_type(cmd):
            return instruction_type(cmd, symbol_table)
    raise Exception('Invalid instruction')


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
    LABEL_REGEX = re.compile('^\((?P<label_name>.+)\)$')

    @staticmethod
    def is_of_type(cmd):
        return bool(LabelInstruction.LABEL_REGEX.match(cmd))

    def to_binary(self):
        raise Exception('Label instructions do not convert to binary')

    @property
    def variable_name(self):
        return LabelInstruction.LABEL_REGEX.match(self.cmd)['label_name']


class AInstruction(Instruction):
    A_REGEX = re.compile('^@(?P<value>[^@]+)$')
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


class CInstruction(Instruction):
    C_REGEX = re.compile('^((?P<dest>[AMD]{1,3})=)?(?P<comp>[^=;]+)(;(?P<jump>\w+))?$')
    JMP_TO_BINARY = {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    COMP_TO_BINARY = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'M': '110000',
        'A': '110000',
        '!D': '001101',
        '!M': '110001',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        '-M': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'M+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'M-1': '110010',
        'D+A': '000010',
        'D+M': '000010',
        'D-A': '010011',
        'D-M': '010011',
        'A-D': '000111',
        'M-D': '000111',
        'D&A': '000000',
        'D&M': '000000',
        'D|A': '010101',
        'D|M': '010101',
    }

    @staticmethod
    def is_of_type(cmd):
        m = CInstruction.C_REGEX.match(cmd)
        return bool(m) and bool(m.groupdict()['jump'] or m.groupdict()['dest'])

    @property
    def comp_part(self):
        return CInstruction.C_REGEX.match(self.cmd)['comp']

    @property
    def dest_part(self):
        return CInstruction.C_REGEX.match(self.cmd)['dest']

    @property
    def jump_part(self):
        return CInstruction.C_REGEX.match(self.cmd)['jump']

    def to_binary(self):
        return '111' + self._parse_comp() + self._parse_dest() + self._parse_jump()

    def _parse_comp(self):
        a_value = '1' if 'M' in self.comp_part else '0'
        return a_value + CInstruction.COMP_TO_BINARY[self.comp_part]

    def _parse_jump(self):
        if self.jump_part:
            return CInstruction.JMP_TO_BINARY[self.jump_part]
        else:
            return '000'

    def _parse_dest(self):
        if self.dest_part:
            return ('1' if 'A' in self.dest_part else '0') + \
                   ('1' if 'D' in self.dest_part else '0') + \
                   ('1' if 'M' in self.dest_part else '0')
        else:
            return '000'
