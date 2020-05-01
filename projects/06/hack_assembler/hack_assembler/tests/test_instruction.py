import pytest

from ..instruction import parse_instruction
from ..parser import SymbolTable
from parametrization import Parametrization


@Parametrization.parameters('test_input', 'expected')
@Parametrization.case('A instruction', '@17', '0000000000010001')
@Parametrization.case('A instruction', '@42', '0000000000101010')
@Parametrization.case('C instruction - branching', '0;JMP', '1110101010000111')
@Parametrization.case('C instruction - branching', 'M;JEQ', '1111110000000010')
@Parametrization.case('C instruction - branching', '-1;JLT', '1110111010000100')
@Parametrization.case('C instruction - branching', 'A;JNE', '1110110000000101')
@Parametrization.case('C instruction - branching', '-1;JGT', '1110111010000001')
@Parametrization.case('C instruction - branching', '!M;JGT', '1111110001000001')
@Parametrization.case('C instruction - branching', 'D|A;JMP', '1110010101000111')
@Parametrization.case('C instruction - branching', 'M-1;JLE', '1111110010000110')
@Parametrization.case('C instruction - assignment', 'M=D', '1110001100001000')
@Parametrization.case('C instruction - assignment', 'M=D+1', '1110011111001000')
@Parametrization.case('C instruction - assignment', 'M=D|M', '1111010101001000')
@Parametrization.case('C instruction - assignment', 'AM=D&M', '1111000000101000')
@Parametrization.case('C instruction - assignment', 'AMD=M-D', '1111000111111000')
@Parametrization.case('C instruction - assignment', 'D=D-A', '1110010011010000')
@Parametrization.case('C instruction - assignment', 'M=D-1', '1110001110001000')
@Parametrization.case('C instruction - assignment', 'D=0', '1110101010010000')
@Parametrization.case('C instruction - assignment', 'AMD=-1', '1110111010111000')
@Parametrization.case('C instruction - assignment', 'D=D+M', '1111000010010000')
def test_parse_instruction_valid_instruction(test_input, expected):
    assert parse_instruction(test_input, SymbolTable()) == expected


@Parametrization.parameters('test_input')
@Parametrization.case('A instruction - large literal', '@32768')
@Parametrization.case('A instruction - large literal', '@999999')
@Parametrization.case('A instruction - no literal', '@')
@Parametrization.case('C instruction - branching - invalid jump', '-1;GGT')
@Parametrization.case('C instruction - branching - invalid comp', 'MD;JMP')
@Parametrization.case('C instruction - assignment - invalid dest', '-1=M')
@Parametrization.case('C instruction - assignment - invalid dest', 'A-1=D')
@Parametrization.case('C instruction - assignment - invalid dest', '=D+1')
@Parametrization.case('C instruction - assignment - invalid comp', 'A=JMP')
@Parametrization.case('C instruction - assignment - invalid comp', 'M=M|D')
@Parametrization.case('C instruction - assignment - invalid comp', 'A=M+M')
@Parametrization.case('C instruction - assignment', 'M=D;JMP')
def test_parse_instruction_invalid_instruction(test_input):
    with pytest.raises(Exception):
        assert parse_instruction(test_input, SymbolTable())
