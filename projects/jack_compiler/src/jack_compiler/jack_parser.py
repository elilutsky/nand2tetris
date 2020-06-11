from pathlib import Path

from .jack_tokenizer import tokenize
from xml.etree.ElementTree import Element, tostring

from .jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackString, JackIdentifier
from .jack_tokenizer.tokens.utils import CLASS_TO_XML_TAG


class Parser:
    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file

        self._tokenizer = tokenize(self._input_file)
        self._current_token = None
        self._pre_read_token = None

    def parse(self):
        for token in self._tokenizer:
            self._current_token = token
            e = Element(CLASS_TO_XML_TAG[token.__class__])
            e.text = f' {token.value} '
            output.write(tostring(e).decode('utf-8') + '\n')
        output.write('</tokens>\n')

    def _next_token(self):
        if self._pre_read_token is not None:
            token = self._pre_read_token
            self._pre_read_token = None
            return token

        self._token = self._tokenizer.next()

    def _peek_token(self):
        self._next_token()
        self._pre_read_token = self._token
        return self._pre_read_token

    def _compile_expected_token(self, expected_token_value):
        self._next_token()

        if self._token.value != expected_token_value:
            raise Exception(f'Expected token: {expected_token_value} but got {self._token.value}')

        # todo, write self._token

    def _compile_token(self):
        self._next_token()

        # todo, write self._token

    def _compile_class(self):
        self._compile_expected_token(JackKeyword.CLASS)
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_class_var_dec()
        self._compile_subroutine_dec()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_class_var_dec(self):

        # match zero or more
        next_token = self._peek_token()
        while next_token.value in [JackKeyword.STATIC, JackKeyword.FIELD]:
            # static | field
            self._compile_token()

            # type: int | char | boolean | identifier
            self._compile_token()

            # varName: identifier
            self._compile_token()

            next_token = self._peek_token()
            while next_token.value == JackSymbol.COMMA:
                # comma
                self._compile_token()

                # varName: identifier
                self._compile_token()

                next_token = self._peek_token()

            self._compile_expected_token(JackSymbol.SEMICOLON)
            next_token = self._peek_token()

    def _compile_subroutine_dec(self):

        # match zero or more
        next_token = self._peek_token()
        while next_token in [JackKeyword.CONSTRUCTOR,
                             JackKeyword.FUNCTION,
                             JackKeyword.METHOD]:

            # constructor | function | method
            self._compile_token()

            # void | type
            self._compile_token()

            # subroutineName: identifier
            self._compile_token()

            self._compile_expected_token(JackSymbol.LEFT_BRACES)
            self._compile_parameter_list()
            self._compile_expected_token(JackSymbol.RIGHT_BRACES)
            self._compile_subroutine_body()

            next_token = self._peek_token()

    def _compile_parameter_list(self):
        next_token = self._peek_token()

        while next_token.value != JackSymbol.RIGHT_BRACES:
            # type
            self._compile_token()

            # varName
            self._compile_token()

            next_token = self._peek_token()
            if next_token.value == JackSymbol.COMMA:
                self._compile_token()
                next_token = self._peek_token()
            else:
                assert next_token.value == JackSymbol.RIGHT_BRACES, \
                    f"unexpected token {next_token.value} encountered in parameter list"

    def _compile_subroutine_body(self):
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_var_dec()
        self._compile_statements()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_var_dec(self):
        # match zero or more

        next_token = self._peek_token()
        while next_token.value == JackKeyword.VAR:
            # var
            self._compile_token()

            # type
            self._compile_token()

            # varName
            self._compile_token()

            next_token = self._peek_token()
            while next_token.value == JackSymbol.COMMA:
                # comma
                self._compile_token()

                # varName
                self._compile_token()

                next_token = self._peek_token()

            self._compile_expected_token(JackSymbol.SEMICOLON)

            next_token = self._peek_token()

    def _compile_statements(self):
        while True:
            next_token = self._peek_token()

            if next_token.value == JackKeyword.LET:
                self._compile_let()
            elif next_token.value == JackKeyword.IF:
                self._compile_if()
            elif next_token.value == JackKeyword.WHILE:
                self._compile_while()
            elif next_token.value == JackKeyword.DO:
                self._compile_do()
            elif next_token.value == JackKeyword.RETURN:
                self._compile_return()
            else:
                assert next_token.value == JackSymbol.RIGHT_CURLY_BRACES,\
                    "Unexpected token in statement: {next_token.value}"
                break

    def _compile_let(self):
        self._compile_expected_token(JackSymbol.LET)

        # varName
        self._compile_token()

        next_token = self._peek_token()
        if next_token.value == JackSymbol.LEFT_SQUARE_BRACES:
            # [ expression ]
            self._compile_expected_token(JackSymbol.LEFT_SQUARE_BRACES)
            self._compile_expression()
            self._compile_expected_token(JackSymbol.RIGHT_SQUARE_BRACES)

        self._compile_expected_token(JackSymbol.EQUAL)
        self._compile_expression()
        self._compile_expected_token(JackSymbol.SEMICOLON)

    def __compile_condition(self):
        assert self._peek_token().value in [JackSymbol.WHILE, JackSymbol.IF]
        self._compile_token()
        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_expression()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_statements()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_if(self):
        self.__compile_condition()

        next_token = self._peek_token()
        if next_token.value == JackSymbol.ELSE:
            self._compile_expected_token(JackSymbol.ELSE)
            self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
            self._compile_statements()
            self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_while(self):
        self.__compile_condition()

    def _compile_do(self):
        self._compile_expected_token(JackSymbol.DO)
        self._compile_subroutine_call()
        self._compile_expected_token(JackSymbol.SEMICOLON)

    def _compile_subroutine_call(self):

        # subroutineName, or className, or varName
        self._compile_token()

        next_token = self._peek_token()
        if next_token.value == JackSymbol.DOT:

            # subroutineName
            self._compile_token()

        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_expression_list()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)

    def _compile_return(self):
        self._compile_expected_token(JackSymbol.RETURN)
        while self._peek_token().value != JackSymbol.SEMICOLON:
            self._compile_expression()

    def _compile_expression(self):
        pass

    def _compile_term(self):
        pass

    def _compile_expression_list(self):
        next_token = self._peek_token()
        while next_token.value != JackSymbol.RIGHT_BRACES:
            self._compile_expression()
            next_token = self._peek_token()
            if next_token.value == JackSymbol.COMMA:
                self._compile_expected_token(JackSymbol.COMMA)
                next_token = self._peek_token()
