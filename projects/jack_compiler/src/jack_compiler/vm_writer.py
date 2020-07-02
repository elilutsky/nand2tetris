from .jack_to_vm_maps import SegmentType, ArithmeticVMCommand




class VmWriter:
    def __init__(self, output_vm_file_handle):
        self._output_file_handle = output_vm_file_handle

    def _write(self, value):
        self._write(value + "\n")

    def write_push(self, segment_type, index):
        assert segment_type in SegmentType, f'{segment_type} invalid segment type '
        self._write(f'push {segment_type.value} {index}')

    def write_pop(self, segment_type, index):
        assert segment_type in SegmentType, f'{segment_type} invalid segment type'
        self._write(f'pop {segment_type.value} {index}')

    def write_arithmetic(self, command):
        assert command in ArithmeticVMCommand, f'{command} invalid arithmetic command'
        self._write(f'{command.value}')

    def write_label(self, label):
        self._write(f'{label}:')

    def write_goto(self, label):
        self._write(f'goto {label}')

    def write_if_goto(self, label):
        self._write(f'if-goto {label}')

    def write_call(self, name, num_arguments):
        self._write(f'call {name} {num_arguments}')

    def write_function(self, name, num_locals):
        self._write(f'function {name} {num_locals}')

    def write_return(self):
        self._write('return')
