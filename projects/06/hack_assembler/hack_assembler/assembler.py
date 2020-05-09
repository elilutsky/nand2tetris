from .exceptions import LineParseException
from .instruction import parse_instruction
from .consts import LABEL_REGEX
from .symbol_table import SymbolTable


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


def assemble(f):
    """
    Creates a machine binary file from the given assembly file `f`. The output file will be named `f.hack`.
    """
    input_file = Path(f)
    if input_file.suffix != '.asm':
        raise Exception('Expected .asm file')

    result = parse_data(input_file.read_text())
    input_file.with_suffix('.hack').write_text(result)
