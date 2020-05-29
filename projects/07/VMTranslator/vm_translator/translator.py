from pathlib import Path

from .parser import parse_code, SegmentType, CommandType, Commands


def translate(f):
    """
    Translate the given `.vm` file `f` to a Hack file. The result will be saved in `f.asm`
    """
    input_file_path = Path(f)
    if input_file_path.suffix != '.vm':
        raise Exception('Expected .vm file')

    with open(f, 'r') as input_file:
        with open(input_file_path.with_suffix('.asm'), 'w') as output_file:
            translator = Translator(input_file, output_file, input_file_path.stem)
            translator.translate_data()


class Translator(object):
    def __init__(self, vm_code_file, output_asm_file, vm_file_name):
        self._current_code = []
        self._vm_code_file = vm_code_file
        self._output_asm_file = output_asm_file
        self._command_counter = 0
        self._vm_file_name = vm_file_name

    def translate_data(self):
        for vm_command in parse_code(self._vm_code_file):
            if vm_command.command_type == CommandType.ARITHMETIC:
                self._handle_arithmetic(vm_command)
            elif vm_command.command_type == CommandType.PUSH:
                self._handle_push(vm_command)
            elif vm_command.command_type == CommandType.POP:
                self._handle_pop(vm_command)

            self._command_counter += 1
            self._output_asm_file.write('\n'.join(self._current_code) + '\n')
            self._current_code = []

    def _handle_push(self, vm_command):
        segment_type = vm_command.arg1
        if segment_type == SegmentType.CONSTANT.value:
            self._push_constant(vm_command.arg2)
        elif segment_type == SegmentType.LOCAL.value:
            self._push_mapped_segment(vm_command.arg2, segment_register='LCL')
        elif segment_type == SegmentType.ARGUMENT.value:
            self._push_mapped_segment(vm_command.arg2, segment_register='ARG')
        elif segment_type == SegmentType.THIS.value:
            self._push_mapped_segment(vm_command.arg2, segment_register='THIS')
        elif segment_type == SegmentType.THAT.value:
            self._push_mapped_segment(vm_command.arg2, segment_register='THAT')
        elif segment_type == SegmentType.POINTER.value:
            self._push_mapped_segment(vm_command.arg2, segment_offset=3)
        elif segment_type == SegmentType.TEMP.value:
            self._push_mapped_segment(vm_command.arg2, segment_offset=5)
        elif segment_type == SegmentType.STATIC.value:
            self._push_static(vm_command.arg2)
        else:
            raise Exception(f'Unexpected push segment: {vm_command.arg1}')

    def _handle_pop(self, vm_command):
        segment_type = vm_command.arg1

        if segment_type == SegmentType.LOCAL.value:
            self._pop_mapped_segment(vm_command.arg2, segment_register='LCL')
        elif segment_type == SegmentType.ARGUMENT.value:
            self._pop_mapped_segment(vm_command.arg2, segment_register='ARG')
        elif segment_type == SegmentType.THIS.value:
            self._pop_mapped_segment(vm_command.arg2, segment_register='THIS')
        elif segment_type == SegmentType.THAT.value:
            self._pop_mapped_segment(vm_command.arg2, segment_register='THAT')
        elif segment_type == SegmentType.POINTER.value:
            self._pop_mapped_segment(vm_command.arg2, segment_offset=3)
        elif segment_type == SegmentType.TEMP.value:
            self._pop_mapped_segment(vm_command.arg2, segment_offset=5)
        elif segment_type == SegmentType.STATIC.value:
            self._pop_static(vm_command.arg2)
        else:
            raise Exception(f'Unexpected pop segment: {vm_command.arg1}')

    def _push_static(self, offset):
        self._add_a_command(f'{self._vm_file_name}.{offset}')
        self._add_c_command('D', 'M')
        self._push_to_stack('D')

    def _pop_static(self, offset):
        self._pop_stack('D')
        self._add_a_command(f'{self._vm_file_name}.{offset}')
        self._add_c_command('M', 'D')

    def _compute_address_in_segment(self, dest, offset, segment_register, segment_offset):
        assert (segment_register or segment_offset) and not (segment_register and segment_offset),\
            'exactly one of (segment register, fixed offset) should be provided'

        if segment_register:
            self._add_a_command(segment_register)
            self._add_c_command('D', 'M')
        else:
            self._add_a_command(segment_offset)
            self._add_c_command('D', 'A')
        self._add_a_command(offset)
        self._add_c_command(dest, 'D+A')

    def _push_mapped_segment(self, offset, segment_register=None, segment_offset=None):
        self._compute_address_in_segment('A', offset, segment_register, segment_offset)
        self._add_c_command('D', 'M')
        self._push_to_stack('D')

    def _pop_mapped_segment(self, offset, segment_register=None, segment_offset=None):
        self._compute_address_in_segment('D', offset, segment_register, segment_offset)

        # store address in first general purpose register
        self._add_a_command('R13')
        self._add_c_command('M', 'D')

        self._pop_stack('D')

        self._add_a_command('R13')
        self._add_c_command('A', 'M')
        self._add_c_command('M', 'D')

    def _handle_arithmetic(self, vm_command):
        if vm_command.command == Commands.NEG:
            self._handle_unary('-')
        elif vm_command.command == Commands.NOT:
            self._handle_unary('!')
        elif vm_command.command == Commands.ADD:
            self._handle_binary('+')
        elif vm_command.command == Commands.SUB:
            self._handle_binary('-')
        elif vm_command.command == Commands.AND:
            self._handle_binary('&')
        elif vm_command.command == Commands.OR:
            self._handle_binary('|')
        elif vm_command.command == Commands.LT:
            self._handle_comparison('JLT')
        elif vm_command.command == Commands.EQ:
            self._handle_comparison('JEQ')
        elif vm_command.command == Commands.GT:
            self._handle_comparison('JGT')
        else:
            raise Exception(f'Unexpected arithmetic command: {vm_command.command}')

    def _handle_unary(self, op):
        self._pop_stack('D')
        self._add_c_command(dest='D', comp=f'{op}D')
        self._push_to_stack('D')

    def _handle_binary(self, op):
        self._pop_stack('D')
        self._pop_stack('A')
        if op == '-':
            # The first parameter is pushed first
            self._add_c_command(dest='D', comp=f'A-D')
        else:
            # operator is symmetric
            self._add_c_command(dest='D', comp=f'D{op}A')
        self._push_to_stack('D')

    def _handle_comparison(self, branch_condition):
        true_label = f'_LOGICAL_SET_TRUE_{self._command_counter}'
        end_label = f'_LOGICAL_END_{self._command_counter}'

        self._pop_stack('D')
        self._pop_stack('A')
        self._add_c_command(dest='D', comp=f'A-D')
        self._add_a_command(true_label)
        self._add_c_command(comp='D', jump=branch_condition)

        # set result to false (represented as 0)
        self._add_c_command(dest='D', comp='0')
        self._add_a_command(end_label)
        self._add_c_command(comp='0', jump='JMP')

        # set result to true (represented as -1)
        self._add_label_command(true_label)
        self._add_c_command(dest='D', comp='-1')

        self._add_label_command(end_label)
        self._push_to_stack('D')

    def _add_label_command(self, label):
        self._current_code.append(f'({label})')

    def _push_constant(self, value):
        self._add_a_command(value)
        self._add_c_command(dest='D', comp='A')
        self._push_to_stack('D')

    def _pop_stack(self, dest):
        self._decrease_sp()
        self._load_sp_to_A()
        self._add_c_command(dest=dest, comp='M')

    def _push_to_stack(self, source):
        assert source.upper() not in ['A', 'M'], 'pushing to stack overrides A'
        self._load_sp_to_A()
        self._add_c_command(dest='M', comp=source)
        self._increase_sp()

    def _load_sp_to_A(self):
        self._add_a_command('SP')
        self._add_c_command(dest='A', comp='M')

    def _decrease_sp(self):
        self._add_a_command('SP')
        self._add_c_command('M', 'M-1')

    def _increase_sp(self):
        self._add_a_command('SP')
        self._add_c_command('M', 'M+1')

    def _add_a_command(self, param):
        self._current_code.append(f'@{param}')

    def _add_c_command(self, dest=None, comp=None, jump=None):
        assert comp, 'Missing `comp` argument'

        assert not (dest and jump), 'function does not expect both dest and jump parameters'

        if dest:
            self._current_code.append(f'{dest}={comp}')
        elif jump:
            self._current_code.append(f'{comp};{jump}')
