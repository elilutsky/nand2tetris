import re

from .base import JackToken

_STRING_REGEX = re.compile(r'\"(\w*)\"', re.UNICODE)


class JackString(JackToken):

    def __init__(self, string_value):
        self._string_value = string_value

    @staticmethod
    def tokenize(word) -> ('JackString', str):
        match = _STRING_REGEX.match(word)
        if match:
            return JackString(match.group(1)), word[len(match.group(0)):]
        else:
            return None, word

    @property
    def value(self):
        return self._string_value

    def __eq__(self, other: 'JackString'):
        return self.value == other.value

    def __repr__(self):
        return f'<JackString.STRING: \'{self.value}\'>'
