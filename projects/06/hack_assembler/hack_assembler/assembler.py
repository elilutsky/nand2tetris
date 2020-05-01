from pathlib import Path
from .parser import parse_data


def assemble(f):
    """
    Creates a machine binary file from the given assembly file `f`. The output file will be named `f.hack`.
    """
    input_file = Path(f)
    if input_file.suffix != '.asm':
        raise Exception('Expected .asm file')

    result = parse_data(input_file.read_text())
    input_file.with_suffix('.hack').write_text(result)
