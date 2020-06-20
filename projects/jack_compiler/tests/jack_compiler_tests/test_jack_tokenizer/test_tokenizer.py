from pathlib import Path
from parametrization import Parametrization
from jack_compiler.jack_tokenizer.tokenizer import Tokenizer, tokenize_to_xml
from jack_compiler.jack_tokenizer.tokens import JackKeyword, JackSymbol, JackDecimal, JackIdentifier, JackSkip


@Parametrization.parameters('test_subject', 'expected_tokens', 'debug_mode')
@Parametrization.case('Multiple tokens in word', 'return;', [JackKeyword('return'), JackSymbol(';')], False)
@Parametrization.case('Multiple tokens in word', 'return function', [JackKeyword('return'), JackKeyword('function')], False)
@Parametrization.case('Multiple tokens in word', 'return3function', [JackIdentifier('return3function')], False)
@Parametrization.case('Multiple tokens in word', 'let 3 = 2 * 2;', [JackKeyword('let'), JackDecimal('3'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')], False)
@Parametrization.case('Multiple tokens in word', 'let tst = 2 * 2;', [JackKeyword('let'), JackIdentifier('tst'), JackSymbol('='), JackDecimal('2'), JackSymbol('*'), JackDecimal('2'), JackSymbol(';')], False)
@Parametrization.case('Multiple tokens in word with skip', ' aaa', [JackSkip(' '), JackIdentifier('aaa')], True)
@Parametrization.case('Multiple tokens in word with skip', 'aaa // bbb;\n aaa', [JackIdentifier('aaa'), JackSkip(' '), JackSkip('// bbb;'), JackSkip('\n '), JackIdentifier('aaa')], True)
def test_tokenize_stream(test_subject, expected_tokens, debug_mode):
    tokenizer = Tokenizer('/dummy/path', debug=debug_mode)
    assert [token for token in tokenizer._tokenize_stream(test_subject)] == expected_tokens


@Parametrization.parameters('file_name')
@Parametrization.case('Square program', 'square_Main')
@Parametrization.case('Square program', 'square_Square')
@Parametrization.case('Square program', 'square_SquareGame')
@Parametrization.case('Expression less square program', 'expless_square_Main')
@Parametrization.case('Expression less square program', 'expless_square_Square')
@Parametrization.case('Expression less square program', 'expless_square_SquareGame')
@Parametrization.case('ArrayTest program', 'arraytest_Main')
def test_tokenize_to_xml(file_name):
    parent_dir = Path(__file__).parent
    input_ = Path(f'{parent_dir}/files/{file_name}.jack')

    tokenize_to_xml(input_)

    output = input_.with_suffix('.xml')
    expected = Path(f'{parent_dir}/files/{file_name}.xml')

    assert output.read_text() == expected.read_text()

    output.unlink()
