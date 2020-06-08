from enum import Enum

from .base import JackToken


class KeywordTypes(Enum):
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
    def has_value(cls, value):
        return value in set(item.value for item in cls)


class JackKeyword(JackToken):

    def __init__(self, word):
        self._word = word

    @staticmethod
    def is_of_type(word):
        return KeywordTypes.has_value(word)

    @property
    def value(self):
        return KeywordTypes(self._word)
