from pathlib import Path

from xml.etree.ElementTree import Element, tostring

from .tokens import JackAlphanumeric, JackSymbol, JackString, JackIdentifier
from .tokens.utils import CLASS_TO_XML_TAG

_TOKEN_TYPES = [JackAlphanumeric, JackSymbol, JackString, JackIdentifier]


def tokenize_to_xml(f):
    with open(Path(f).with_suffix('.xml'), 'w') as output:
        output.write('<tokens>\n')
        for token in tokenize(f):
            e = Element(CLASS_TO_XML_TAG[token.__class__])
            e.text = f' {token.value} '
            output.write(tostring(e).decode('utf-8') + '\n')
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
            for line in input_:
                yield from self._tokenize_line(line)

    def _tokenize_line(self, line):
        for word in line.split():
            yield from self._tokenize_word(word)

    def _tokenize_word(self, word):
        for token_type in _TOKEN_TYPES:
            token, remainder = token_type.tokenize(word)
            if token:
                yield token
                if remainder:
                    yield from self._tokenize_word(remainder)
                return
