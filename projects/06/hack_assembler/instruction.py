from consts import *


def parse_instruction(line):
    """
    Parses the given assembly line into a machine binary instruction. The returned string is a 16-bit machine binary.
    """
    parsed = lexer.parse(line)
    if hasattr(parsed.children[0], 'value') and parsed.children[0].value == '@':
        return parse_a_instruction(parsed)
    else:
        return parse_c_instruction(parsed)


def parse_a_instruction(parsed):
    value = next(parsed.find_data('value')).children[0].value
    if int(value) > A_INSTRUCTION_MAX_LITERAL_SIZE:
        raise Exception('A instruction max literal size exceeded')
    return '0' + f'{int(value):b}'.zfill(15)


def parse_c_instruction(parsed):
    if any(parsed.find_data('jump')):
        result = parse_jump_instruction(parsed)
    else:
        result = parse_assign_instruction(parsed)

    return '111' + result


def parse_jump_instruction(parsed):
    comp = parse_comp_part(parsed)
    jmp = next(parsed.find_data('jump'))
    return comp + '000' + JMP_TO_BINARY[jmp.children[0].value]


def parse_assign_instruction(parsed):
    comp = parse_comp_part(parsed)
    dest = next(parsed.find_data('dest'))
    return comp + \
           ('1' if any(dest.scan_values(lambda x: x == 'A')) else '0') + \
           ('1' if any(dest.scan_values(lambda x: x == 'D')) else '0') + \
           ('1' if any(dest.scan_values(lambda x: x == 'M')) else '0') \
           + '000'


def parse_comp_part(parsed):
    comp_data = next(parsed.find_data('comp'))
    a_value = '1' if any(comp_data.scan_values(lambda x: x == 'M')) else '0'
    return a_value + COMP_TO_BINARY[comp_data.children[0].data]
