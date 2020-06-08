def tokenize(f):
    """
    Returns a Tokenizer for the give .jack file path.
    """
    pass


class Tokenizer:
    def __init__(self, f):
        self._file_path = f

    def __iter__(self):
        with open(self._file_path, 'rb') as input_:
            for line in input_:
                yield from self._tokenize_line(line)

    def _tokenize_line(self, line):
        pass
