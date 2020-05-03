import os

from pathlib import Path
from parametrization import Parametrization
from ..translator import Translator

TESTS_BASE_DIR = Path(__file__).parent


@Parametrization.parameters('test_subject')
@Parametrization.case('Simple const push and arithmetic action', 'simple_add')
def test_translator(test_subject):
    input_ = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}.vm').read_text()
    expected = Path(f'{TESTS_BASE_DIR}/test_files/{test_subject}.expected').read_text()

    t = Translator(input_)
    assert t.translate_data() == expected
