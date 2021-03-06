from .instruction import LabelInstruction
from .utils import code_iterator


class SymbolTable(object):

    def __init__(self):
        self._symbol_table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576
        }
        self._symbol_table.update({f'R{i}': i for i in range(16)})
        self._current_variable_location = 16

    def add_label(self, label, location):
        self._symbol_table[label] = location

    def add_variable(self, var):
        self._symbol_table[var] = self._current_variable_location
        self._current_variable_location += 1

    def __contains__(self, item):
        return item in self._symbol_table

    def __getitem__(self, item):
        return self._symbol_table[item]

    @staticmethod
    def build_symbol_table(code):
        symbol_table = SymbolTable()
        line_num = 0
        for instruction in code_iterator(code, symbol_table=None):
            if isinstance(instruction, LabelInstruction):
                symbol_table.add_label(instruction.variable_name, line_num)
            else:
                line_num += 1
        return symbol_table
