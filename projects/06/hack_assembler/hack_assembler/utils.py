from .instruction import create_instruction


def code_iterator(code, symbol_table):
    for line in code.splitlines():
        line = line[:line.index('//')] if '//' in line else line
        line = ''.join(line.split())

        if line:
            yield create_instruction(line, symbol_table)
