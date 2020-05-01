from assembler.exceptions import LineParseException
from assembler.instruction import parse_instruction


def parse_data(data):
    """
    Converts the given assembly string to machine binary code.
    """
    result = ''
    for line_num, line in enumerate(filter(None, data.splitlines())):
        try:
            result += parse_instruction(line) + '\n'
        except Exception as e:
            raise LineParseException(line, line_num, str(e))
    return result
