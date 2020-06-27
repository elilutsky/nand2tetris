from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackString, JackIdentifier,\
    JackAlphanumeric, JackSkip


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword valid word', JackAlphanumeric, 'return', (JackKeyword.RETURN, ''))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'returnpasten', (JackIdentifier('returnpasten'), ''))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'returnpasten', (JackIdentifier('returnpasten'), ''))
@Parametrization.case('Keyword valid word', JackAlphanumeric, 'function', (JackKeyword.FUNCTION, ''))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'nlul', (JackIdentifier('nlul'), ''))
@Parametrization.case('Keyword invalid word', JackAlphanumeric, 'retrun', (JackIdentifier('retrun'), ''))
@Parametrization.case('Symbol valid word', JackSymbol, '*', (JackSymbol.MULT, ''))
@Parametrization.case('Symbol valid word', JackSymbol, '*hello', (JackSymbol.MULT, 'hello'))
@Parametrization.case('Symbol valid word', JackSymbol, '{', (JackSymbol.LEFT_CURLY_BRACES, ''))
@Parametrization.case('Symbol invalid word', JackSymbol, '_', (None, '_'))
@Parametrization.case('Symbol invalid word', JackSymbol, '%', (None, '%'))
@Parametrization.case('Decimal valid word', JackAlphanumeric, '123', (JackDecimal('123'), ''))
@Parametrization.case('Decimal valid word', JackAlphanumeric, '0', (JackDecimal('0'), ''))
@Parametrization.case('Decimal valid word', JackAlphanumeric, '9999', (JackDecimal('9999'), ''))
@Parametrization.case('Decimal valid word', JackAlphanumeric, '30000', (JackDecimal('30000'), ''))
@Parametrization.case('Decimal valid word', JackAlphanumeric, '33000', (None, '33000'))
@Parametrization.case('String valid word', JackString, '"32000abc"', (JackString('32000abc'), ''))
@Parametrization.case('String valid word', JackString, '"32000 abc \t"', (JackString('32000 abc \t'), ''))
@Parametrization.case('String valid word', JackString, '""asd', (JackString(''), 'asd'))
@Parametrization.case('String invalid word', JackString, '"test', (None, '"test'))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'pasten', (JackIdentifier('pasten'), ''))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'pasten_pastenino', (JackIdentifier('pasten_pastenino'), ''))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'pasten_pastenino123', (JackIdentifier('pasten_pastenino123'), ''))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'pasten_Pastenino123', (JackIdentifier('pasten_Pastenino123'), ''))
@Parametrization.case('Identifier valid word', JackAlphanumeric, 'pasten_Pastenino123;', (JackIdentifier('pasten_Pastenino123'), ';'))
@Parametrization.case('Identifier valid word', JackAlphanumeric, '_Pastenino123;', (JackIdentifier('_Pastenino123'), ';'))
@Parametrization.case('Identifier invalid word', JackAlphanumeric, '123pasten', (None, '123pasten'))
@Parametrization.case('Identifier invalid word', JackAlphanumeric, '&^%pasd_asd', (None, '&^%pasd_asd'))
@Parametrization.case('Skip token', JackSkip, '// bla bla bl$a_ 9', (JackSkip('// bla bla bl$a_ 9'), ''))
@Parametrization.case('Skip token until newline', JackSkip, '// bla bla bla\naa', (JackSkip('// bla bla bla'), '\naa'))
def test_tokenize(keyword_type, test_subject, expected):
    assert keyword_type.tokenize(test_subject) == expected
