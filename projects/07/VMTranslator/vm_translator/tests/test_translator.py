import os

from pathlib import Path
from parametrization import Parametrization
from ..translator import Translator

TESTS_BASE_DIR = Path(__file__).parent


@Parametrization.parameters('test_subject')
@Parametrization.case('Simple const push and arithmetic action', 'simple_add')
@Parametrization.case('Arithmetic and logical stack operations', 'stack_test')
@Parametrization.case('pop and push operations for most segment types', 'BasicTest')
@Parametrization.case('pop and push operations for the pointer segment type', 'PointerTest')
@Parametrization.case('static segment push and pop operations', 'StaticTest')
@Parametrization.case('simple label and ifgoto operation', 'SimpleLoop')
def test_translator(test_subject):

    input_ = f'{TESTS_BASE_DIR}/test_files/{test_subject}.vm'
    temp = f'{TESTS_BASE_DIR}/test_files/{test_subject}.out'

    with open(input_, 'r') as input_file:
        with open(temp, 'w') as output_file:

            t = Translator(input_file, output_file, test_subject)
            t.translate_data()

    expected_content = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}.expected').read_text()
    actual_content = Path(temp).read_text()
    assert actual_content == expected_content

