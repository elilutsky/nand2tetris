from .instruction import parse_instruction, LABEL_REGEX
from .symbol_table import SymbolTable
from .utils import code_iterator


def parse_data(code):
    """
    Converts the given assembly string to machine binary code.
    """
    result = ''
    symbol_table = SymbolTable.build_symbol_table(code)
    for line in code_iterator(code):
        label_match = LABEL_REGEX.match(line)
        if not label_match:
            result += parse_instruction(line, symbol_table) + '\n'
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
