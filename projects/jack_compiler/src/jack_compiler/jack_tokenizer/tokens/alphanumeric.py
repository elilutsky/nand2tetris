import re
from enum import Enum

from .base import JackToken, JackRegexToken


class JackKeyword(Enum):
    CLASS = 'class'
    CONSTRUCTOR = 'constructor'
    FUNCTION = 'function'
    METHOD = 'method'
    FIELD = 'field'
    STATIC = 'static'
    VAR = 'var'
    INT = 'int'
    CHAR = 'char'
    BOOLEAN = 'boolean'
    VOID = 'void'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'

    @classmethod
    def does_exist(cls, value):
        return value in set(item.value for item in cls)

    def __eq__(self, other):
        return self.value == other.value


class JackDecimal(JackToken):
    pass


class JackIdentifier(JackToken):
    """
    Note: an identifier cannot start with the a digit
    """
    pass


class JackAlphanumeric(JackRegexToken):

    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'^([\w]+)')

    @classmethod
    def tokenize(cls, word) -> (JackToken, str):
        token, remainder = super(JackAlphanumeric, cls).tokenize(word)
        if not token:
            return None, word
        if JackKeyword.does_exist(token.value):
            return JackKeyword(token.value), remainder
        if token.value.isnumeric() and 0 <= int(token.value) < 32768:
            return JackDecimal(token.value), remainder
        if not token.value[0].isnumeric():
            return JackIdentifier(token.value), remainder

        return None, word
