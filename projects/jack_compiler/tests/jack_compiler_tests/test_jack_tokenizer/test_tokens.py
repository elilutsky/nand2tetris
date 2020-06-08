from parametrization import Parametrization

from jack_compiler.jack_tokenizer.tokens import JackKeyword


@Parametrization.parameters('keyword_type', 'test_subject', 'expected')
@Parametrization.case('JackKeyword valid word', JackKeyword, 'return', True)
@Parametrization.case('JackKeyword valid word', JackKeyword, 'function', True)
@Parametrization.case('JackKeyword invalid word', JackKeyword, 'nlul', False)
@Parametrization.case('JackKeyword invalid word', JackKeyword, 'retrun', False)
def test_is_of_type(keyword_type, test_subject, expected):
    assert keyword_type.is_of_type(test_subject) == expected
