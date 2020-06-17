from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackString, JackIdentifier, JackAlphanumeric


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword valid word', JackAlphanumeric, 'return', (JackKeyword.RETURN, ''))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'returnpasten', (None, 'returnpasten'))
@Parametrization.case('Keyword valid word', JackAlphanumeric, 'function', (JackKeyword.FUNCTION, ''))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'nlul', (None, 'nlul'))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'retrun', (None, 'retrun'))
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
@Parametrization.case('String valid word', JackString, '"32000abc"', (JackString('32000abc'), ''))
@Parametrization.case('String valid word', JackString, '""asd', (JackString(''), 'asd'))
@Parametrization.case('String invalid word', JackString, '"test', (None, '"test'))
@Parametrization.case('Identifier valid word', JackIdentifier, 'pasten', (JackIdentifier('pasten'), ''))
@Parametrization.case('Identifier valid word', JackIdentifier, 'pasten_pastenino', (JackIdentifier('pasten_pastenino'), ''))
@Parametrization.case('Identifier valid word', JackIdentifier, 'pasten_pastenino123', (JackIdentifier('pasten_pastenino123'), ''))
@Parametrization.case('Identifier valid word', JackIdentifier, 'pasten_Pastenino123', (JackIdentifier('pasten_Pastenino123'), ''))
@Parametrization.case('Identifier valid word', JackIdentifier, 'pasten_Pastenino123;', (JackIdentifier('pasten_Pastenino123'), ';'))
@Parametrization.case('Identifier valid word', JackIdentifier, '_Pastenino123;', (JackIdentifier('_Pastenino123'), ';'))
@Parametrization.case('Identifier invalid word', JackIdentifier, '123pasten', (None, '123pasten'))
@Parametrization.case('Identifier invalid word', JackIdentifier, '&^%pasd_asd', (None, '&^%pasd_asd'))
def test_tokenize(keyword_type, test_subject, expected):
    assert keyword_type.tokenize(test_subject) == expected
