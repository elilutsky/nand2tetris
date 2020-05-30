from pathlib import Path

from .parser import parse_code, SegmentType, CommandType, Commands, VMCommand


def translate(input_path):
    """
    Translate the given `.vm` file to a Hack file. The result will be saved in `<input_path>.asm`
    If input_path is a directory, then all the .vm files in the directory will be translated to a single .asm file
    named '<input_path>.asm'
    """
    input_path = Path(input_path)
    if not input_path.is_dir() and input_path.suffix != '.vm':
        raise Exception('Expected .vm file or a directory of .vm files')

    input_files = list(input_path.rglob('*.vm')) if input_path.is_dir() else [input_path]

    with open(input_path.with_suffix('.asm'), 'w') as output_file:
        write_bootstrap = input_path.is_dir()
        for input_file in input_files:
            with open(input_file, 'r') as input_file_handle:
                translator = Translator(input_file_handle, output_file, input_file.stem, write_bootstrap)
                translator.translate_data()

            # bootstrap code is only written for the first .vm file, and only when a directory was given
            write_bootstrap = False


class Translator(object):
    def __init__(self, vm_code_file, output_asm_file, vm_file_name, write_bootstrap):
        self._current_code = []
        self._vm_code_file = vm_code_file
        self._output_asm_file = output_asm_file

        self._vm_file_name = vm_file_name
        self._enter_function()

        if write_bootstrap:
            self._write_bootstrap_code()

    def _enter_function(self, function_name=None):
        """
        Informs the translator of a beginning of a new function
        This resets the counters and symbols used to generate the unique labels

        :param function_name: function name. If set to None then vm file name will be used as the base
        of symbol names instead
        """
        self._comparison_counter = 0
        self._return_label_counter = 0
        self._current_function_name = function_name if function_name else self._vm_file_name

    def _generate_return_label(self):
        label_name = f"{self._current_function_name}$ret.{self._return_label_counter}"
        self._return_label_counter += 1
        return label_name

    def _generate_comparsion_labels(self):
        true_label_name = f"{self._current_function_name}$_comparsion_true.{self._comparison_counter}"
        end_label_name = f"{self._current_function_name}$_comparsion_end.{self._comparison_counter}"

        self._comparison_counter += 1
        return true_label_name, end_label_name

    def _write_bootstrap_code(self):
        # SP = 256
        self._add_a_command('256')
        self._add_c_command('D', 'A')
        self._add_a_command('SP')
        self._add_c_command('M', 'D')

        self._handle_call(VMCommand('call Sys.init 0'))

        self._output_asm_file.write('\n'.join(self._current_code) + '\n')
        self._current_code = []

    def translate_data(self):
        for vm_command in parse_code(self._vm_code_file):
            if vm_command.command_type == CommandType.ARITHMETIC:
                self._handle_arithmetic(vm_command)
            elif vm_command.command_type == CommandType.PUSH:
                self._handle_push(vm_command)
            elif vm_command.command_type == CommandType.POP:
                self._handle_pop(vm_command)
            elif vm_command.command_type == CommandType.BRANCH:
                self._handle_branch(vm_command)
            elif vm_command.command_type == CommandType.CALL:
                self._handle_call(vm_command)
            elif vm_command.command_type == CommandType.FUNCTION:
                self._handle_function(vm_command)
            elif vm_command.command_type == CommandType.RETURN:
                self._handle_return()

            self._output_asm_file.write('\n'.join(self._current_code) + '\n')
            self._current_code = []

    def _handle_call(self, vm_command):
        function_name = vm_command.arg1
        num_args = vm_command.arg2
        return_address_label = self._generate_return_label()

        self._push_label_to_stack(return_address_label)
        self._push_register_to_stack('LCL')
        self._push_register_to_stack('ARG')
        self._push_register_to_stack('THIS')
        self._push_register_to_stack('THAT')

        # ARG = SP - num_args - 5
        self._add_a_command('SP')
        self._add_c_command('D', 'M')
        self._add_a_command(num_args)
        self._add_c_command('D', 'D-A')
        self._add_a_command('5')
        self._add_c_command('D', 'D-A')
        self._add_a_command('ARG')
        self._add_c_command('M', 'D')

        # LCL = SP
        self._add_a_command('SP')
        self._add_c_command('D', 'M')
        self._add_a_command('LCL')
        self._add_c_command('M', 'D')

        # jump
        self._add_a_command(function_name)
        self._add_c_command(comp='0', jump='JMP')

        # define return label
        self._add_label_command(return_address_label)

    def _handle_return(self):

        def _load_from_frame(num_subs, target):
            # target = *(FRAME - num_subs)
            # where FRAME is stored in R13

            self._add_a_command('R13')
            self._add_c_command('D', 'M')
            self._add_a_command(f'{num_subs}')
            self._add_c_command('A', 'D-A')
            self._add_c_command(target, 'M')

        def _restore_from_frame(num_subs, target_segment_register):
            # target_register = *(FRAME - num_subs)
            # where FRAME is stored in R13

            _load_from_frame(num_subs, 'D')

            self._add_a_command(target_segment_register)
            self._add_c_command('M', 'D')

        # store FRAME (LCL) in R13
        self._add_a_command('LCL')
        self._add_c_command('D', 'M')

        self._add_a_command('R13')
        self._add_c_command('M', 'D')

        # store RET in R14
        # R14 = *(FRAME-5)
        _load_from_frame(5, 'D')
        self._add_a_command('R14')
        self._add_c_command('M', 'D')

        # *ARG = pop()
        self._pop_stack('D')
        self._add_a_command('ARG')
        self._add_c_command('A', 'M')
        self._add_c_command('M', 'D')

        # SP = ARG + 1
        self._add_a_command('ARG')
        self._add_c_command('D', 'M+1')
        self._add_a_command('SP')
        self._add_c_command('M', 'D')

        #  THAT, THIS, ARG, LCL  =  *(FRAME-1), *(FRAME-2), *(FRAME-3), *(FRAME-4)
        _restore_from_frame(1, 'THAT')
        _restore_from_frame(2, 'THIS')
        _restore_from_frame(3, 'ARG')
        _restore_from_frame(4, 'LCL')

        # jump to saved return address
        self._add_a_command('R14')
        self._add_c_command('A', 'M')
        self._add_c_command(comp='0', jump='JMP')

    def _handle_function(self, vm_command):
        function_name = vm_command.arg1
        num_local_vars = vm_command.arg2

        self._return_label_counter = 0
        self._current_function_name = function_name

        self._add_label_command(function_name)

        for i in range(int(num_local_vars)):
            self._push_constant('0')

    def _handle_branch(self, vm_command):
        label = f"{self._current_function_name}${vm_command.arg1}"
        if vm_command.command == Commands.LABEL:
            self._add_label_command(label)
        elif vm_command.command == Commands.GOTO:
            self._add_a_command(label)
            self._add_c_command(comp='0', jump='JMP')
        elif vm_command.command == Commands.IF_GOTO:
            self._pop_stack('D')
            self._add_a_command(label)
            self._add_c_command(comp='D', jump='JNE')
        else:
            raise Exception(f'Unexpected branch command: {vm_command}')

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
        true_label, end_label = self._generate_comparsion_labels()

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

    def _push_label_to_stack(self, label):
        self._push_constant(label)

    def _push_register_to_stack(self, register):
        """
        :param symbol: a register identifier, e.g. R13, LCL, ARG.
        """
        self._add_a_command(register)
        self._add_c_command(dest='D', comp='M')
        self._push_to_stack('D')

    def _add_a_command(self, param):
        self._current_code.append(f'@{param}')

    def _add_c_command(self, dest=None, comp=None, jump=None):
        assert comp, 'Missing `comp` argument'

        assert not (dest and jump), 'function does not expect both dest and jump parameters'

        if dest:
            self._current_code.append(f'{dest}={comp}')
        elif jump:
            self._current_code.append(f'{comp};{jump}')
