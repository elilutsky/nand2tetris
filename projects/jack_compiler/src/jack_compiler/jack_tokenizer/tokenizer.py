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
        for token in tokenize(jack_file_path):
            write_token_to_xml_output(token, output)
        output.write('</tokens>\n')


def tokenize(jack_file_handle):
    """
    Returns a Tokenizer for the give .jack file path.

    :param jack_file_handle: the open jack file
    """
    return Tokenizer(jack_file_handle)


class Tokenizer:
    def __init__(self, input_file_handle):
        self._input_file = input_file_handle

    def __iter__(self):
        for line in self._skip_multiline_comments(self._input_file):
            yield from self._tokenize_line(line)

    def _skip_multiline_comments(self):
        while True:
            line = self._input_file.readline()
            if not line:
                return
            if line.strip().startswith('/**'):
                while not line.strip().endswith('*/'):
                    line = self._input_file.readline()
                line = self._input_file.readline()
            yield line

    def _tokenize_line(self, line):
        for token_type in TOKEN_HANDLER_TYPES:
            token, remainder = token_type.tokenize(line)

            if token:
                if not isinstance(token, JackSkip):
                    yield token
                if remainder:
                    yield from self._tokenize_line(remainder)
                return

        raise Exception(f"The following input could not be resolved to a token:\n{line}")

