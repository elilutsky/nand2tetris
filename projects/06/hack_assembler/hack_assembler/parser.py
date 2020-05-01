from .exceptions import LineParseException
from .instruction import parse_instruction
from .consts import LABEL_REGEX


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
        clean_code = []
        for line in code:
            label_match = LABEL_REGEX.match(line)
            if label_match:
                symbol_table.add_label(label_match['label_name'], line_num)
            else:
                line_num += 1
                clean_code.append(line)
        return symbol_table, clean_code


def filter_irrelevant_lines(data_lines):
    result = []
    for line in data_lines:
        if '//' in line:
            result.append(line[:line.index('//')])
        else:
            result.append(line)
    result = map(str.strip, result)
    return list(filter(None, result))


def parse_data(data):
    """
    Converts the given assembly string to machine binary code.
    """
    result = ''
    code = filter_irrelevant_lines(data.splitlines())
    symbol_table, clean_code = SymbolTable.build_symbol_table(code)
    for line_num, line in enumerate(clean_code):
        try:
            result += parse_instruction(line, symbol_table) + '\n'
        except Exception as e:
            raise LineParseException(line, line_num, str(e))
    return result
