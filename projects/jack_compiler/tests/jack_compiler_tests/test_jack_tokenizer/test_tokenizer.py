from parametrization import Parametrization
from jack_compiler.jack_tokenizer.tokenizer import Tokenizer
from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol


@Parametrization.parameters('test_subject', 'expected_tokens')
@Parametrization.case('Single token in word', 'return', [JackKeyword('return')])
@Parametrization.case('Multiple tokens in word', 'return;', [JackKeyword('return'), JackSymbol(';')])
def test_tokenize_word(test_subject, expected_tokens):
    tokenizer = Tokenizer('/dummy/path')
    assert [token for token in tokenizer._tokenize_word(test_subject)] == expected_tokens
