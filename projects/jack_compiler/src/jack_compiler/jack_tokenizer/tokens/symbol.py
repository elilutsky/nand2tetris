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
    def get_starting_symbol(cls, value):
        for symbol in cls:
            if value.startswith(symbol.value):
                return symbol
        return None  # Explicit return for readability

    @classmethod
    def tokenize(cls, word) -> ('JackSymbol', str):
        symbol = JackSymbol.get_starting_symbol(word)
        return (symbol, word[1:]) if symbol else (None, word)

