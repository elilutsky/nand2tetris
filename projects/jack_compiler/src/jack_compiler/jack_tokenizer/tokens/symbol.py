import re
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
    def _get_token_regex(cls):
        return re.compile(rf'^(\{cls.LEFT_CURLY_BRACES}|\{cls.RIGHT_CURLY_BRACES}|\{cls.LEFT_BRACES}|'
                          rf'\{cls.RIGHT_BRACES}|\{cls.LEFT_SQUARE_BRACES}|\{cls.RIGHT_SQUARE_BRACES}|\{cls.DOT}|\{cls.COMMA}|\{cls.SEMICOLON}|'
                          rf'\{cls.PLUS}|\{cls.MINUS}|\{cls.MULT}|\{cls.DIV}|\{cls.AND}|\{cls.OR}|\{cls.LOWER}|\{cls.GREATER}|'
                          rf'\{cls.EQUAL}|\{cls.NOT})')
