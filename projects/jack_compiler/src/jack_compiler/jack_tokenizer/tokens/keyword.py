from .base import JackToken

_POSSIBLE_KEYWORDS = ['class', 'constructor', 'function', 'method',
                      'field', 'static', 'var', 'int', 'char', 'boolean',
                      'void', 'true', 'false', 'null', 'this', 'let', 'do',
                      'if', 'else', 'while', 'return']


class JackKeyword(JackToken):

    def __init__(self, word):
        self._word = word

    @staticmethod
    def is_of_type(word):
        return word in _POSSIBLE_KEYWORDS

    @property
    def value(self):
        return self._word
