from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword, KeywordTypes, JackSymbol, SymbolTypes


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword valid word', JackKeyword, 'return', True)
@Parametrization.case('Keyword valid word', JackKeyword, 'function', True)
@Parametrization.case('Keyword invalid word', JackKeyword, 'nlul', False)
@Parametrization.case('Keyword invalid word', JackKeyword, 'retrun', False)
@Parametrization.case('Symbol valid word', JackSymbol, '*', True)
@Parametrization.case('Symbol valid word', JackSymbol, '{', True)
@Parametrization.case('Symbol invalid word', JackSymbol, '_', False)
@Parametrization.case('Symbol invalid word', JackSymbol, '%', False)
def test_is_of_type(keyword_type, test_subject, expected):
    assert keyword_type.is_of_type(test_subject) == expected


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword', JackKeyword, 'return', KeywordTypes.RETURN)
@Parametrization.case('Keyword', JackKeyword, 'function', KeywordTypes.FUNCTION)
@Parametrization.case('Symbol', JackSymbol, '{', SymbolTypes.LEFT_CURLY_BRACES)
@Parametrization.case('Symbol', JackSymbol, '}', SymbolTypes.RIGHT_CURLY_BRACES)
@Parametrization.case('Symbol', JackSymbol, '*', SymbolTypes.MULT)
def test_value(keyword_type, test_subject, expected):
    assert keyword_type(test_subject).value == expected
