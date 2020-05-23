from pathlib import Path

from ..assembler import parse_data


def test_parser():
    input_ = Path('Pong.asm').read_text()
    expected = Path('Pong.hack').read_text()
    assert parse_data(input_) == expected
