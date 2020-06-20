
from .jack_tokenizer import tokenize

from .jack_tokenizer.tokens import JackKeyword, JackSymbol
from .jack_tokenizer.tokens.utils import write_token_to_xml_output


class CompilationEngine:
    def __init__(self, input_file_handle, output_file_handle):
        self._output_file_handle = output_file_handle
        self._tokenizer = tokenize(input_file_handle).__iter__()

        self._current_token = None
        self._pre_read_token = None

    def compile(self):
        self._compile_class()

    def write_xml_tag(tag_name):
        def decorator(compile_function):
            def wrapper(self):
                self._output_file_handle.write(f'<{tag_name}>\n')
                try:
                    ret = compile_function(self)
                finally:
                    self._output_file_handle.write(f'</{tag_name}>\n')
                return ret

            return wrapper
        return decorator

    def _next_token(self):
        if self._pre_read_token is not None:
            token = self._pre_read_token
            self._pre_read_token = None
            return token

        self._token = self._tokenizer.__next__()

    def _peek_token(self):
        self._next_token()
        self._pre_read_token = self._token
        return self._pre_read_token

    def _compile_expected_token(self, expected_token_value):
        self._next_token()

        if self._token != expected_token_value:
            raise Exception(f'Expected token: {expected_token_value} but got {self._token}')

        write_token_to_xml_output(self._token, self._output_file_handle)

    def _compile_token(self):
        self._next_token()

        write_token_to_xml_output(self._token, self._output_file_handle)

    @write_xml_tag('class')
    def _compile_class(self):
        self._compile_expected_token(JackKeyword.CLASS)
        # className
        self._compile_token()
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_class_var_dec()
        self._compile_subroutine_dec()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    @write_xml_tag('classVarDec')
    def _compile_class_var_dec_single(self):
        # static | field
        self._compile_token()

        # type: int | char | boolean | identifier
        self._compile_token()

        # varName: identifier
        self._compile_token()

        next_token = self._peek_token()
        while next_token == JackSymbol.COMMA:
            # comma
            self._compile_token()

            # varName: identifier
            self._compile_token()

            next_token = self._peek_token()

        self._compile_expected_token(JackSymbol.SEMICOLON)

    def _compile_class_var_dec(self):
        # match zero or more
        while self._peek_token() in [JackKeyword.STATIC, JackKeyword.FIELD]:
            self._compile_class_var_dec_single()

    @write_xml_tag('subroutineDec')
    def _compile_subroutine_dec_single(self):
        # constructor | function | method
        self._compile_token()

        # void | type
        self._compile_token()

        # subroutineName
        self._compile_token()

        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_parameter_list()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)
        self._compile_subroutine_body()

    def _compile_subroutine_dec(self):

        # match zero or more
        while self._peek_token() in [JackKeyword.CONSTRUCTOR,
                                     JackKeyword.FUNCTION,
                                     JackKeyword.METHOD]:
            self._compile_subroutine_dec_single()

    @write_xml_tag('parameterList')
    def _compile_parameter_list(self):
        while self._peek_token() != JackSymbol.RIGHT_BRACES:
            # type
            self._compile_token()

            # varName
            self._compile_token()

            if self._peek_token() == JackSymbol.COMMA:
                self._compile_token()
            else:
                assert self._peek_token() == JackSymbol.RIGHT_BRACES, \
                    f"unexpected token {self._peek_token()} encountered in parameter list"

    @write_xml_tag('subroutineBody')
    def _compile_subroutine_body(self):
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_var_dec()
        self._compile_statements()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    @write_xml_tag('varDec')
    def _compile_var_dec_single(self):
        # var
        self._compile_token()

        # type
        self._compile_token()

        # varName
        self._compile_token()

        while self._peek_token() == JackSymbol.COMMA:
            # comma
            self._compile_token()

            # varName
            self._compile_token()

        self._compile_expected_token(JackSymbol.SEMICOLON)

    def _compile_var_dec(self):
        # match zero or more

        while self._peek_token() == JackKeyword.VAR:
            self._compile_var_dec_single()

    @write_xml_tag('statements')
    def _compile_statements(self):
        while True:
            next_token = self._peek_token()

            if next_token == JackKeyword.LET:
                self._compile_let()
            elif next_token == JackKeyword.IF:
                self._compile_if()
            elif next_token == JackKeyword.WHILE:
                self._compile_while()
            elif next_token == JackKeyword.DO:
                self._compile_do()
            elif next_token == JackKeyword.RETURN:
                self._compile_return()
            else:
                break

    @write_xml_tag('letStatement')
    def _compile_let(self):
        self._compile_expected_token(JackKeyword.LET)

        # varName
        self._compile_token()

        if self._peek_token() == JackSymbol.LEFT_SQUARE_BRACES:
            # [ expression ]
            self._compile_expected_token(JackSymbol.LEFT_SQUARE_BRACES)
            self._compile_expression()
            self._compile_expected_token(JackSymbol.RIGHT_SQUARE_BRACES)

        self._compile_expected_token(JackSymbol.EQUAL)
        self._compile_expression()
        self._compile_expected_token(JackSymbol.SEMICOLON)

    def __compile_condition(self):
        assert self._peek_token().value in [JackKeyword.WHILE.value, JackKeyword.IF.value]
        self._compile_token()
        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_expression()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_statements()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    @write_xml_tag('ifStatement')
    def _compile_if(self):
        self.__compile_condition()

        if self._peek_token() == JackKeyword.ELSE:
            self._compile_expected_token(JackKeyword.ELSE)
            self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
            self._compile_statements()
            self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    @write_xml_tag('whileStatement')
    def _compile_while(self):
        self.__compile_condition()

    @write_xml_tag('doStatement')
    def _compile_do(self):

        self._compile_expected_token(JackKeyword.DO)
        self._compile_subroutine_call()
        self._compile_expected_token(JackSymbol.SEMICOLON)

    def _compile_subroutine_call(self):

        # subroutineName, or className, or varName
        self._compile_token()

        next_token = self._peek_token()
        if next_token == JackSymbol.DOT:
            self._compile_expected_token(JackSymbol.DOT)

            # subroutineName
            self._compile_token()

        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_expression_list()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)

    @write_xml_tag('returnStatement')
    def _compile_return(self):

        self._compile_expected_token(JackKeyword.RETURN)
        if self._peek_token() != JackSymbol.SEMICOLON:
            self._compile_expression()

        self._compile_expected_token(JackSymbol.SEMICOLON)

    @write_xml_tag('expression')
    def _compile_expression(self):
        # TODO: expand
        # self._compile_token()

        self._compile_term()
        while self._is_op(self._peek_token()):
            self._compile_token()
            self._compile_term()

    @write_xml_tag('term')
    def _compile_term(self):
        # '[', '(', '.'
        next_token = self._peek_token()
        if next_token == JackSymbol.LEFT_BRACES:
            self._compile_expected_token(JackSymbol.LEFT_BRACES)
            self._compile_expression()
            self._compile_expected_token(JackSymbol.RIGHT_BRACES)
        elif self._is_unary_op(next_token):
            self._compile_token()
            self._compile_term()
        else:
            self._compile_token()

            # check if still parsing either one of:
            # 1. foo[expression]
            # 2. foo.bar(expressionList)
            # 3. foo(expressionList)
            next_token = self._peek_token()
            if next_token == JackSymbol.LEFT_SQUARE_BRACES:
                self._compile_expected_token(JackSymbol.LEFT_SQUARE_BRACES)
                self._compile_expression()
                self._compile_expected_token(JackSymbol.RIGHT_SQUARE_BRACES)
            elif next_token == JackSymbol.DOT:
                self._compile_expected_token(JackSymbol.DOT)
                self._compile_token()
                self._compile_expected_token(JackSymbol.LEFT_BRACES)
                self._compile_expression_list()
                self._compile_expected_token(JackSymbol.RIGHT_BRACES)
            elif next_token == JackSymbol.LEFT_BRACES:
                self._compile_expected_token(JackSymbol.LEFT_BRACES)
                self._compile_expression_list()
                self._compile_expected_token(JackSymbol.RIGHT_BRACES)

    def _is_unary_op(self, token):
        return token.value in {JackSymbol.MINUS.value, JackSymbol.NOT.value}

    def _is_op(self, token):
        return token.value in [JackSymbol.PLUS.value, JackSymbol.MINUS.value, JackSymbol.MULT.value, JackSymbol.DIV.value,
                               JackSymbol.AND.value, JackSymbol.OR.value, JackSymbol.LOWER.value, JackSymbol.GREATER.value,
                               JackSymbol.EQUAL.value]

    @write_xml_tag('expressionList')
    def _compile_expression_list(self):
        while self._peek_token() != JackSymbol.RIGHT_BRACES:
            self._compile_expression()
            if self._peek_token() == JackSymbol.COMMA:
                self._compile_expected_token(JackSymbol.COMMA)
                assert self._peek_token() != JackSymbol.RIGHT_BRACES
