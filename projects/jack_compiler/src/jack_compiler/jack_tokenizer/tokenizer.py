from pathlib import Path

from .tokens.utils import write_token_to_xml_output, TOKEN_HANDLER_TYPES
from .tokens.skip import JackSkip


def tokenize_to_xml(jack_file_path):
    """
    A utility function accepting a file path to .jack file, and generating the tokens XML
    (step 1 of the project, does not use the parser)
    :param jack_file_path: the path to the .jack input file
    """
    with open(Path(jack_file_path).with_suffix('.xml'), 'w') as output:
        output.write('<tokens>\n')
        with open(jack_file_path, 'r') as input_jack_file:
            for token in tokenize(input_jack_file):
                write_token_to_xml_output(token, output)
        output.write('</tokens>\n')


def tokenize(jack_file_handle):
    """
    Returns a Tokenizer for the give .jack file path.

    :param jack_file_handle: the open jack file
    """
    return Tokenizer(jack_file_handle)


class Tokenizer:
    def __init__(self, input_file_handle, debug=False):
        self._input_file = input_file_handle
        self._debug = debug

    def __iter__(self):
        yield from self._tokenize_file()

    def _tokenize_file(self):
        while True:
            line = self._input_file.readline()
            if not line:
                return
            else:
                yield from self._tokenize_stream(line)

    def _tokenize_stream(self, line):
        if line.startswith('/**'):
            line = self._skip_multiline_comment(line)

        for token_type in TOKEN_HANDLER_TYPES:
            token, remainder = token_type.tokenize(line)

            if token:
                if not isinstance(token, JackSkip) or self._debug:
                    yield token
                if remainder:
                    yield from self._tokenize_stream(remainder)
                return

        raise Exception(f'The following input could not be resolved to a token:\n{line}')

    def _skip_multiline_comment(self, line):
        while '*/' not in line:
            line = self._input_file.readline()
        line = line[line.index('*/') + 2:]
        return line
