from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('Keyword valid word', JackKeyword, 'return', (JackKeyword.RETURN, ''))
@Parametrization.case('Keyword valid word', JackKeyword, 'function', (JackKeyword.FUNCTION, ''))
@Parametrization.case('Keyword invalid word', JackKeyword, 'nlul', (None, 'nlul'))
@Parametrization.case('Keyword invalid word', JackKeyword, 'retrun', (None, 'retrun'))
@Parametrization.case('Symbol valid word', JackSymbol, '*', (JackSymbol.MULT, ''))
@Parametrization.case('Symbol valid word', JackSymbol, '{', (JackSymbol.LEFT_CURLY_BRACES, ''))
@Parametrization.case('Symbol invalid word', JackSymbol, '_', (None, '_'))
@Parametrization.case('Symbol invalid word', JackSymbol, '%', (None, '%'))
def test_tokenize(keyword_type, test_subject, expected):
    assert keyword_type.tokenize(test_subject) == expected
