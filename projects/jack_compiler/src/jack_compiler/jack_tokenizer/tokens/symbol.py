from enum import Enum

from .base import JackToken


class JackSymbol(JackToken, Enum):
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
    def tokenize(cls, word) -> ('JackToken', str):
        assert len(word) > 0
        if word[0] in set(item.value for item in cls):
            return cls(word[0]), word[1:]
        else:
            return None, word
