from .tokens import JackKeyword

_TOKEN_TYPES = [JackKeyword]


def tokenize(f):
    """
    Returns a Tokenizer for the give .jack file path.
    """
    return Tokenizer(f)


class Tokenizer:
    def __init__(self, f):
        self._file_path = f

    def __iter__(self):
        with open(self._file_path, 'rb') as input_:
            for line in input_:
                yield from self._tokenize_line(line)

    def _tokenize_line(self, line):
        for word in line.split():
            yield self._tokenize_word(word)

    def _tokenize_word(self, word):
        for token_type in _TOKEN_TYPES:
            if token_type.is_of_type(word):
                return token_type(word)
