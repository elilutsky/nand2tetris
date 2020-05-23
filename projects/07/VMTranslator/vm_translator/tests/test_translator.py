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
def test_translator(test_subject):
    input_ = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}.vm').read_text()
    expected = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}.expected').read_text()

    t = Translator(input_, test_subject)
    assert t.translate_data() == expected
