import re

from .base import JackToken

_IDENTIFIER_REGEX = re.compile(r'^([^\d\W][\w_]*)')


class JackIdentifier(JackToken):

    def __init__(self, identifier):
        self._identifier = identifier

    @staticmethod
    def tokenize(word) -> ('JackIdentifier', str):
        match = _IDENTIFIER_REGEX.match(word)
        if match:
            return JackIdentifier(match.group(1)), word[len(match.group(1)):]
        else:
            return None, word

    @property
    def value(self):
        return self._identifier

    def __eq__(self, other: 'JackIdentifier'):
        return self.value == other.value

    def __repr__(self):
        return f'<JackIdentifier.IDENTIFIER: \'{self.value}\'>'
