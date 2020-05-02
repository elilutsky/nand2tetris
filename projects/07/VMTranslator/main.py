import argparse
from vm_translator import translator

if __name__ == '__main__':
    argsparser = argparse.ArgumentParser(description='VMTranslator for the Hack language.')
    argsparser.add_argument('file', metavar='FILE', help='path to the .vm file')
    args = argsparser.parse_args()
    translator.translate(args.file)
