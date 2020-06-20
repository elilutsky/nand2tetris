import argparse
from pathlib import Path

from jack_compiler.compilation_engine import CompilationEngine


def syntax_analyze(input_param):
    """
    Executes the Jack analyzer.
    Executes the jack parser for each .jack file specified by the input

    :param input_param: either a .jack file path, or a directory containing .jack files
    """
    input_path = Path(input_param)
    if not input_path.is_dir() and input_path.suffix != '.jack':
        raise Exception('Expected .jack file or a directory of .jack files')

    input_files = list(input_path.rglob('*.jack')) if input_path.is_dir() else [input_path]

    for input_file_path in input_files:
        with open(input_file_path.with_suffix('.xml'), 'w') as output_file_handle:
            with open(input_file_path, 'r') as input_file_handle:
                print(f'Compiling file {input_file_path}')
                compiler = CompilationEngine(input_file_handle, output_file_handle)
                compiler.compile()


if __name__ == '__main__':
    argsparser = argparse.ArgumentParser(description='JackAnalyzer for the Jack language.')
    argsparser.add_argument('file', metavar='FILE',
                            help='path to a .jack file or a directory of .jack files')
    args = argsparser.parse_args()
    syntax_analyze(args.file)
