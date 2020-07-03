
from .tokenizer import tokenize

from .tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackString, JackIdentifier
from .symbol_table import SymbolTable
from .vm_writer import VMWriter
from .jack_to_vm_maps import JACK_BIN_OP_TO_VM_COMMAND_MAP, JACK_UNARY_OP_TO_VM_COMMAND_MAP, SegmentType, ArithmeticVMCommand


class CompilationEngine:
    def __init__(self, input_file_handle, output_file_handle):
        self._tokenizer = tokenize(input_file_handle).__iter__()
        self._vm_writer = VMWriter(output_file_handle)
        self._symbol_table = SymbolTable()

        self._current_token = None
        self._pre_read_token = None

        self._size_of_class_in_words = None
        self._jack_class_name = None

    def compile(self):
        self._compile_class()

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

    def _skip_expected_token(self, expected_token_value):
        self._next_token()

        if self._token != expected_token_value:
            raise Exception(f'Expected token: {expected_token_value} but got {self._token}')

    def _skip_token(self):
        self._next_token()

    def _get_token(self):
        self._next_token()
        return self._token

    def _compile_class(self):
        self._skip_expected_token(JackKeyword.CLASS)
        # className
        self._jack_class_name = self._get_token()
        self._skip_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._size_of_class_in_words = self._compile_class_var_dec()
        self._compile_subroutine_dec()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_class_var_dec_single(self):
        num_fields = 0

        # static | field
        symbol_kind_token = self._get_token()

        # type: int | char | boolean | identifier
        type_token = self._get_token()

        # varName: identifier
        identifier = self._get_token()

        def append_symbol(name):
            if symbol_kind_token == JackKeyword.FIELD:
                nonlocal num_fields
                num_fields += 1
                self._symbol_table.append_field(name, type_token.value)
            else:
                self._symbol_table.append_static(name, type_token.value)

        append_symbol(identifier)

        next_token = self._peek_token()
        while next_token == JackSymbol.COMMA:
            # comma
            self._skip_expected_token(JackSymbol.COMMA)

            # varName: identifier
            identifier = self._get_token()
            append_symbol(identifier)

            next_token = self._peek_token()

        self._skip_expected_token(JackSymbol.SEMICOLON)

        return num_fields

    def _compile_class_var_dec(self):
        num_fields = 0

        # match zero or more
        while self._peek_token() in [JackKeyword.STATIC, JackKeyword.FIELD]:
            num_fields += self._compile_class_var_dec_single()

        return num_fields

    def _compile_subroutine_dec_single(self):

        # TODO: handle 'this' variable in symbol table.

        # constructor | function | method
        subroutine_type_token = self._get_token()

        # void | type, ignored by our compiler
        self._get_token()

        # subroutineName
        name = self._get_token()

        self._skip_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_parameter_list()
        self._skip_expected_token(JackSymbol.RIGHT_BRACES)

        # subroutineBody
        self._skip_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        num_locals = self._compile_var_dec()

        self._vm_writer.write_function(f"{self._jack_class_name}.{name.value}", num_locals)

        if subroutine_type_token == JackKeyword.CLASS:
            self._vm_writer.write_constructor_entry(self._size_of_class_in_words)
        elif subroutine_type_token == JackKeyword.METHOD:
            self._vm_writer.write_method_entry()

        self._compile_statements()
        self._skip_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_subroutine_dec(self):

        # match zero or more
        while self._peek_token() in [JackKeyword.CONSTRUCTOR,
                                     JackKeyword.FUNCTION,
                                     JackKeyword.METHOD]:
            self._compile_subroutine_dec_single()

    def _compile_parameter_list(self):
        while self._peek_token() != JackSymbol.RIGHT_BRACES:
            # type
            type_token = self._get_token()

            # varName
            name_token = self._get_token()

            self._symbol_table.append_argument(name_token.value, type_token.value)

            if self._peek_token() == JackSymbol.COMMA:
                self._skip_token()
            else:
                assert self._peek_token() == JackSymbol.RIGHT_BRACES, \
                    f"unexpected token {self._peek_token()} encountered in parameter list"

    def _compile_var_dec_single(self):
        num_locals = 0

        # var
        self._skip_expected_token(JackKeyword.VAR)

        # type
        type_token = self._get_token()

        # varName
        name_token = self._get_token()

        num_locals += 1
        self._symbol_table.append_local(name_token.value, type_token.value)

        while self._peek_token() == JackSymbol.COMMA:
            # comma
            self._skip_expected_token(JackSymbol.COMMA)

            # varName
            name_token = self._get_token()

            self._symbol_table.append_local(name_token.value, type_token.value)
            num_locals += 1

        self._skip_expected_token(JackSymbol.SEMICOLON)
        return num_locals

    def _compile_var_dec(self):
        # match zero or more

        num_locals = 0
        while self._peek_token() == JackKeyword.VAR:
            num_locals += self._compile_var_dec_single()
        return num_locals

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

    def _compile_let(self):
        self._skip_expected_token(JackKeyword.LET)

        # varName
        symbol_name = self._get_token().value

        if self._peek_token() == JackSymbol.LEFT_SQUARE_BRACES:

            # TODO: implement this

            # [ expression ]
            self._skip_expected_token(JackSymbol.LEFT_SQUARE_BRACES)
            self._compile_expression()
            self._skip_expected_token(JackSymbol.RIGHT_SQUARE_BRACES)

        self._skip_expected_token(JackSymbol.EQUAL)
        self._compile_expression()
        self._skip_expected_token(JackSymbol.SEMICOLON)

        segment_type, offset = self._symbol_table.resolve_symbol(symbol_name)
        self._vm_writer.write_pop(segment_type, offset)

    def __compile_condition(self):
        assert self._peek_token().value in [JackKeyword.WHILE.value, JackKeyword.IF.value]
        self._compile_token()
        self._compile_expected_token(JackSymbol.LEFT_BRACES)
        self._compile_expression()
        self._compile_expected_token(JackSymbol.RIGHT_BRACES)
        self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
        self._compile_statements()
        self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_if(self):
        self.__compile_condition()

        if self._peek_token() == JackKeyword.ELSE:
            self._compile_expected_token(JackKeyword.ELSE)
            self._compile_expected_token(JackSymbol.LEFT_CURLY_BRACES)
            self._compile_statements()
            self._compile_expected_token(JackSymbol.RIGHT_CURLY_BRACES)

    def _compile_while(self):
        self.__compile_condition()

    def _compile_do(self):

        self._compile_expected_token(JackKeyword.DO)
        self._resolve_subroutine_and_target_names()
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

    def _compile_return(self):

        self._compile_expected_token(JackKeyword.RETURN)
        if self._peek_token() != JackSymbol.SEMICOLON:
            self._compile_expression()

        self._compile_expected_token(JackSymbol.SEMICOLON)

    def _compile_expression(self):
        # TODO: handle more than one term properly
        self._compile_term()
        while self._is_op(self._peek_token()):

            op_token = self._get_token()
            self._compile_term()

    def _compile_term(self):
        next_token = self._peek_token()
        if next_token == JackSymbol.LEFT_BRACES:
            self._skip_expected_token(JackSymbol.LEFT_BRACES)
            self._compile_expression()
            self._skip_expected_token(JackSymbol.RIGHT_BRACES)
        elif self._is_unary_op(next_token):
            unary_op_token = next_token
            self._skip_token()
            self._compile_term()
            self._vm_writer.write_arithmetic(JACK_UNARY_OP_TO_VM_COMMAND_MAP[unary_op_token])
        else:
            token = self._get_token()

            # check if still parsing either one of:
            # 1. foo[expression]
            # 2. foo.bar(expressionList)
            # 3. foo(expressionList)
            next_token = self._peek_token()
            if next_token == JackSymbol.LEFT_SQUARE_BRACES:
                self._skip_expected_token(JackSymbol.LEFT_SQUARE_BRACES)
                self._compile_expression()
                self._skip_expected_token(JackSymbol.RIGHT_SQUARE_BRACES)
            elif next_token == JackSymbol.DOT or next_token == JackSymbol.LEFT_BRACES:
                # subroutine call

                if next_token == JackSymbol.DOT:
                    self._skip_expected_token(JackSymbol.DOT)
                    function_name = self._get_token().value
                    call_target_name = token.value
                else:
                    function_name = token.value
                    call_target_name = None

                subroutine_name, target_object_name = self._resolve_subroutine_and_target_names(function_name,
                                                                                                call_target_name)

                num_arguments = 0
                if target_object_name is not None:
                    # need to push the address of the object first
                    segment, index, = self._symbol_table.resolve_symbol(target_object_name)
                    self._vm_writer.write_push(segment, index)
                    num_arguments = 1

                self._skip_expected_token(JackSymbol.LEFT_BRACES)
                num_arguments += self._compile_expression_list()
                self._skip_expected_token(JackSymbol.RIGHT_BRACES)

                self._vm_writer.write_call(subroutine_name, num_arguments)
            else:
                # integerConstant | stringConstant | keywordConstant | varName
                if isinstance(token, JackDecimal):
                    self._vm_writer.write_push(SegmentType.CONSTANT, token.value)
                elif isinstance(token, JackString):
                    # TODO: handle creating a string
                    raise NotImplementedError()
                elif isinstance(token, JackKeyword):
                    if token == JackKeyword.TRUE:
                        self._vm_writer.write_push(SegmentType.CONSTANT, 0)
                        self._vm_writer.write_arithmetic(ArithmeticVMCommand.NOT)
                    elif token == JackKeyword.FALSE or token == JackKeyword.NULL:
                        self._vm_writer.write_push(SegmentType.CONSTANT, 0)
                    else:
                        assert token == JackKeyword.THIS
                        # TODO: edge case in CTOR, this shouldn't be resolved as a parameter
                        self._write_identifier_push('this')
                else:
                    assert isinstance(token, JackIdentifier), f'{token}.value should be an identifier'
                    self._write_identifier_push(token.value)

    def _write_identifier_push(self, identifier):
        segment_type, index, = self._symbol_table.resolve_symbol(identifier)
        self._vm_writer.write_push(segment_type, index)

    def _resolve_subroutine_and_target_names(self, function_name, call_target_name=None):
        subroutine_full_name = None
        object_identifier = None

        if object_identifier is not None:
            # method call of form <identifier>.<identifier>(..)
            symbol_description_tuple = self._symbol_table.resolve_symbol(call_target_name)
            if symbol_description_tuple is None:
                # for a valid jack program, we assume that in this case this must be a class name
                # and thus this is a static function call
                subroutine_full_name = f"{call_target_name}.{function_name}"
            else:
                segment, index, symbol_type = symbol_description_tuple
                subroutine_full_name = f"{symbol_type}.{function_name}"
                object_identifier = call_target_name
        else:
            # function must be a local method
            subroutine_full_name = f"{self._jack_class_name}.{function_name}"
            object_identifier = 'this'

        # TODO: for a call of format <var_name>(..), is var_name necessarly a non-static method?
        return subroutine_full_name, object_identifier

    def _is_unary_op(self, token):
        return token.value in {JackSymbol.MINUS.value, JackSymbol.NOT.value}

    def _is_op(self, token):
        return token.value in [JackSymbol.PLUS.value, JackSymbol.MINUS.value, JackSymbol.MULT.value, JackSymbol.DIV.value,
                               JackSymbol.AND.value, JackSymbol.OR.value, JackSymbol.LOWER.value, JackSymbol.GREATER.value,
                               JackSymbol.EQUAL.value]

    def _compile_expression_list(self):
        num_paramters = 0

        while self._peek_token() != JackSymbol.RIGHT_BRACES:
            self._compile_expression()
            num_paramters += 1
            if self._peek_token() == JackSymbol.COMMA:
                self._skip_expected_token(JackSymbol.COMMA)
                assert self._peek_token() != JackSymbol.RIGHT_BRACES
        return num_paramters
