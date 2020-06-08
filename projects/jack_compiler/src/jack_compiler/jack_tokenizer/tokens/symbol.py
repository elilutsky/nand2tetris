from enum import Enum

from .base import JackToken


class SymbolTypes(Enum):
    LEFT_CURLY_BRACES = '{'
    RIGHT_CURLY_BRACES = '}'
    LEFT_BRACES = '('
    RIGHT_BRACES = ')'
    LEFT_SQUARE_BRACES = '['
    RIGHT_SQUARE_BRACES = ']'
    DOT = '.'
    COMMA = ','
    SEMICOLON = ';'
    PLUS = '+'
    MINUS = '-'
    MULT = '*'
    DIV = '/'
    AND = '&'
    OR = '|'
    LOWER = '<'
    GREATER = '>'
    EQUAL = '='
    NOT = '~'

    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in cls)


class JackSymbol(JackToken):

    def __init__(self, word):
        self._word = word

    @staticmethod
    def is_of_type(word):
        return SymbolTypes.has_value(word)

    @property
    def value(self):
        return SymbolTypes(self._word)
