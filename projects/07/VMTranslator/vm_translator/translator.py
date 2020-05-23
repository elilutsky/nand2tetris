from pathlib import Path

from .parser import parse_code, SegmentType, CommandType, Commands


def translate(f):
    """
    Translate the given `.vm` file `f` to a Hack file. The result will be saved in `f.asm`
    """
    input_file = Path(f)
    if input_file.suffix != '.vm':
        raise Exception('Expected .vm file')

    translator = Translator(input_file.read_text())
    input_file.with_suffix('.asm').write_text(translator.translate_data())


class Translator(object):
    def __init__(self, vm_code):
        self._current_code = []
        self._vm_code = vm_code

    def translate_data(self):
        for vm_command in parse_code(self._vm_code):
            if vm_command.command_type == CommandType.ARITHMETIC:
                self._handle_arithmetic(vm_command)
            elif vm_command.command_type == CommandType.PUSH:
                self._handle_push(vm_command)
        return '\n'.join(self._current_code)

    def _handle_push(self, vm_command):
        if vm_command.arg1 == SegmentType.CONSTANT.value:
            self._push_constant(vm_command.arg2)

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

        # TODO: add eq, lt ...

    def _handle_unary(self, op):
        self._decrease_sp()
        self._load_from_stack('D')
        self._add_c_command(dest='D', comp=f'{op}D')
        self._push_to_stack('D')

    def _handle_binary(self, op):
        self._decrease_sp()
        self._load_from_stack('D')
        self._decrease_sp()
        self._load_from_stack('A')
        self._add_c_command(dest='D', comp=f'D{op}A')
        self._push_to_stack('D')

    def _push_constant(self, value):
        self._add_a_command(value)
        self._add_c_command(dest='D', comp='A')
        self._push_to_stack('D')

    def _load_from_stack(self, dest):
        self._load_sp()
        self._add_c_command(dest=dest, comp='M')

    def _push_to_stack(self, source):
        assert source.upper() not in ['A', 'M'], 'pushing to stack overrides A'
        self._load_sp()
        self._add_c_command(dest='M', comp=source)
        self._increase_sp()

    def _load_sp(self):
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
