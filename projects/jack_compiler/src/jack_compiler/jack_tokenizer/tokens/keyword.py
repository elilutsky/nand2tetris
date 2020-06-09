import re
from enum import Enum

from .base import JackToken


class JackKeyword(JackToken, Enum):
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
    def _get_token_regex(cls):
        return re.compile(f'^({cls.CLASS}|{cls.CONSTRUCTOR}|{cls.FUNCTION}|{cls.METHOD}|{cls.FIELD}|{cls.STATIC}|'
                          f'{cls.VAR}|{cls.INT}|{cls.CHAR}|{cls.BOOLEAN}|{cls.VOID}|{cls.TRUE}|{cls.FALSE}|{cls.NULL}|'
                          f'{cls.THIS}|{cls.LET}|{cls.DO}|{cls.IF}|{cls.ELSE}|{cls.WHILE}|{cls.RETURN})')
