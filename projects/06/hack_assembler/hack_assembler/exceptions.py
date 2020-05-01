class LineParseException(Exception):
    def __init__(self, line, line_num, msg):
        self.line = line
        self.line_num = line_num
        self.msg = msg

    def __str__(self):
        return f'Failed to parse line {self.line_num} {self.line}\n{self.msg}'
