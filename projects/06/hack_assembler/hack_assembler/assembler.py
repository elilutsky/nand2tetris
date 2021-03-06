from .instruction import LabelInstruction
from .symbol_table import SymbolTable
from .utils import code_iterator

from pathlib import Path


def parse_data(code):
    """
    Converts the given assembly string to machine binary code.
    """
    result = ''
    symbol_table = SymbolTable.build_symbol_table(code)
    for instruction in code_iterator(code, symbol_table):
        if not isinstance(instruction, LabelInstruction):
            result += instruction.to_binary() + '\n'
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
