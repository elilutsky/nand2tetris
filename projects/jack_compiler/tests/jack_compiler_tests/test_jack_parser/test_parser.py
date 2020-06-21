from pathlib import Path
from JackAnalyzer import syntax_analyze
from parametrization import Parametrization


@Parametrization.parameters('file_name')
@Parametrization.case('Square program', 'square_Main')
@Parametrization.case('Square program', 'square_Square')
@Parametrization.case('Square program', 'square_SquareGame')
@Parametrization.case('arraytest', 'arraytest_Main')
@Parametrization.case('Expression less square program', 'expr_less_Main')
@Parametrization.case('Expression less square program', 'expr_less_Square')
@Parametrization.case('ArrayTest program', 'expr_less_SquareGame')
def test_tokenize_to_xml(file_name):
    parent_dir = Path(__file__).parent
    input_ = Path(f'{parent_dir}/files/{file_name}.jack')

    syntax_analyze(input_)

    output = input_.with_suffix('.xml')
    expected = Path(f'{parent_dir}/files/{file_name}_expected.xml')

    assert output.read_text() == expected.read_text()

    output.unlink()
