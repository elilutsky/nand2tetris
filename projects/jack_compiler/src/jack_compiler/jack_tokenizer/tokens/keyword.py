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
    def get_starting_keyword(cls, value):
        for keyword in cls:
            if value.startswith(keyword.value):
                return keyword
        return None  # Explicit return for readability

    @classmethod
    def tokenize(cls, word) -> ('JackKeyword', str):
        keyword = JackKeyword.get_starting_keyword(word)
        if keyword:
            return keyword, word[len(keyword.value):]
        else:
            return None, word
