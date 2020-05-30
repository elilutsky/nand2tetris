import os

from pathlib import Path
from parametrization import Parametrization
from ..translator import translate

TESTS_BASE_DIR = Path(__file__).parent


@Parametrization.parameters('test_subject')
@Parametrization.case('Simple const push and arithmetic action', 'simple_add.vm')
@Parametrization.case('Arithmetic and logical stack operations', 'stack_test.vm')
@Parametrization.case('pop and push operations for most segment types', 'BasicTest.vm')
@Parametrization.case('pop and push operations for the pointer segment type', 'PointerTest.vm')
@Parametrization.case('static segment push and pop operations', 'StaticTest.vm')
@Parametrization.case('basic labeling scheme', 'BasicLoop.vm')
@Parametrization.case('advanced labeling scheme (goto, if-goto, label)', 'FibonacciSeries.vm')
@Parametrization.case('basic test of function and return commands', 'SimpleFunction.vm')
@Parametrization.case('tests calling functions in nested fashion', 'NestedCall.vm')
@Parametrization.case('fibonacci code flow test (directory)', 'FibonacciElement')
@Parametrization.case('static scope test (directory))', 'StaticsTest')
def test_translator(test_subject):

    input_ = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}')
    output_path = input_.with_suffix('.asm')
    expected_path = input_.with_suffix('.expected')

    translate(input_)

    actual_content = output_path.read_text()
    expected_content = expected_path.read_text()
    assert actual_content == expected_content
