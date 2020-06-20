from pathlib import Path
from parametrization import Parametrization
from jack_compiler.jack_tokenizer.tokenizer import Tokenizer, tokenize_to_xml
from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackIdentifier, JackSkip


@Parametrization.parameters('test_subject', 'expected_tokens')
@Parametrization.case('Multiple tokens in word', 'return;', [JackKeyword('return'), JackSymbol(';')])
@Parametrization.case('Multiple tokens in word', 'return function', [JackKeyword('return'), JackKeyword('function')])
@Parametrization.case('Multiple tokens in word', 'return3function', [JackIdentifier('return3function')])
@Parametrization.case('Multiple tokens in word', 'let 3 = 2 * 2;', [JackKeyword('let'), JackDecimal('3'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')])
@Parametrization.case('Multiple tokens in word', 'let tst = 2 * 2;', [JackKeyword('let'), JackIdentifier('tst'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')])
@Parametrization.case('Multiple tokens in word with skip', ' aaa', [JackSkip(' '), JackIdentifier('aaa')])
@Parametrization.case('Multiple tokens in word with skip', 'aaa // bbb;\n aaa', [JackIdentifier('aaa'), JackSkip(' '), JackSkip('// bbb;'), JackSkip('\n '), JackIdentifier('aaa')])
def test_tokenize_line(test_subject, expected_tokens, ):
    tokenizer = Tokenizer('/dummy/path')
    output_skip_tokens = any([isinstance(token, JackSkip) for token in expected_tokens])
    actual_tokens = [token for token in tokenizer._tokenize_line(test_subject, output_skip_tokens=output_skip_tokens)]
    assert actual_tokens == expected_tokens


def test_tokenize_to_xml():
    parent_dir = Path(__file__).parent
    input_ = Path(f'{parent_dir}/files/input.jack')

    tokenize_to_xml(input_)

    output = input_.with_suffix('.xml')
    expected = Path(f'{parent_dir}/files/expected.xml')

    assert output.read_text() == expected.read_text()

    output.unlink()
