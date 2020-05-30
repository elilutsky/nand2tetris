import argparse
from vm_translator import translator

if __name__ == '__main__':
    argsparser = argparse.ArgumentParser(description='VMTranslator for the Hack language.')
    argsparser.add_argument('file', metavar='FILE',
                            help='path to the .vm file or a directory containing one or more .vm files')
    args = argsparser.parse_args()
    translator.translate(args.file)
