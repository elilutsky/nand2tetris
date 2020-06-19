from pathlib import Path

from .tokens.utils import write_token_to_xml_output, TOKEN_TYPES


def tokenize_to_xml(f):
    with open(Path(f).with_suffix('.xml'), 'w') as output:
        output.write('<tokens>\n')
        for token in tokenize(f):
            write_token_to_xml_output(token, output)
        output.write('</tokens>\n')


def tokenize(f):
    """
    Returns a Tokenizer for the give .jack file path.
    """
    return Tokenizer(f)


class Tokenizer:
    def __init__(self, f):
        self._file_path = f

    def __iter__(self):
        with open(self._file_path, 'r') as input_:
            for line in self._skip_multiline_comments(input_):
                yield from self._tokenize_line(line)

    def _skip_multiline_comments(self, f):
        while True:
            line = f.readline()
            if not line:
                return
            if line.strip().startswith('/**'):
                while not line.strip().endswith('*/'):
                    line = f.readline()
                line = f.readline()
            yield line

    def _tokenize_line(self, line):
        for token_type in TOKEN_TYPES:
            token, remainder = token_type.tokenize(line)

            if token:
                if not isinstance(token, JackSkip):
                    yield token
                if remainder:
                    yield from self._tokenize_line(remainder)
                return

