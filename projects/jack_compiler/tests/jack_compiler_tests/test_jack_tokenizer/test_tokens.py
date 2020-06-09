from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword valid word', JackKeyword, 'return', (JackKeyword.RETURN, ''))
@Parametrization.case('Keyword valid word', JackKeyword, 'returnpasten', (JackKeyword.RETURN, 'pasten'))
@Parametrization.case('Keyword valid word', JackKeyword, 'function', (JackKeyword.FUNCTION, ''))
@Parametrization.case('Keyword invalid word', JackKeyword, 'nlul', (None, 'nlul'))
@Parametrization.case('Keyword invalid word', JackKeyword, 'retrun', (None, 'retrun'))
@Parametrization.case('Symbol valid word', JackSymbol, '*', (JackSymbol.MULT, ''))
@Parametrization.case('Symbol valid word', JackSymbol, '*hello', (JackSymbol.MULT, 'hello'))
@Parametrization.case('Symbol valid word', JackSymbol, '{', (JackSymbol.LEFT_CURLY_BRACES, ''))
@Parametrization.case('Symbol invalid word', JackSymbol, '_', (None, '_'))
@Parametrization.case('Symbol invalid word', JackSymbol, '%', (None, '%'))
@Parametrization.case('Decimal valid word', JackDecimal, '123', (JackDecimal('123'), ''))
@Parametrization.case('Decimal valid word', JackDecimal, '0', (JackDecimal('0'), ''))
@Parametrization.case('Decimal valid word', JackDecimal, '9999', (JackDecimal('9999'), ''))
@Parametrization.case('Decimal valid word', JackDecimal, '99999', (JackDecimal('9999'), '9'))
@Parametrization.case('Decimal valid word', JackDecimal, '32000abc', (JackDecimal('32000'), 'abc'))
def test_tokenize(keyword_type, test_subject, expected):
    assert keyword_type.tokenize(test_subject) == expected
