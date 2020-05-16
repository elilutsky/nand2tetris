def code_iterator(code):
    for line in code.splitlines():
        line = line[:line.index('//')] if '//' in line else line
        line = ''.join(line.split())

        if line:
            yield line
