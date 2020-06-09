from pathlib import Path
from parametrization import Parametrization
from jack_compiler.jack_tokenizer.tokenizer import Tokenizer, tokenize_to_xml
from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackIdentifier


@Parametrization.parameters('test_subject', 'expected_tokens')
@Parametrization.case('Multiple tokens in word', 'return;', [JackKeyword('return'), JackSymbol(';')])
@Parametrization.case('Multiple tokens in word', 'return function', [JackKeyword('return'), JackKeyword('function')])
@Parametrization.case('Multiple tokens in word', 'return3function', [JackKeyword('return'), JackDecimal('3'), JackKeyword('function')])
@Parametrization.case('Multiple tokens in word', 'let 3 = 2 * 2;', [JackKeyword('let'), JackDecimal('3'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')])
@Parametrization.case('Multiple tokens in word', 'let tst = 2 * 2;', [JackKeyword('let'), JackIdentifier('tst'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')])
def test_tokenize_line(test_subject, expected_tokens):
    tokenizer = Tokenizer('/dummy/path')
    assert [token for token in tokenizer._tokenize_line(test_subject)] == expected_tokens


def test_tokenize_to_xml():
    parent_dir = Path(__file__).parent
    input_ = Path(f'{parent_dir}/files/input.jack')

    tokenize_to_xml(input_)

    output = input_.with_suffix('.xml')
    expected = Path(f'{parent_dir}/files/expected.xml')

    assert output.read_text() == expected.read_text()

    output.unlink()
