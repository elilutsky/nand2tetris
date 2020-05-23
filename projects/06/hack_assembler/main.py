import argparse
from hack_assembler import assembler

if __name__ == '__main__':
    argsparser = argparse.ArgumentParser(description='Assembler for Hack language.')
    argsparser.add_argument('file', metavar='FILE', help='path to the .asm file')
    args = argsparser.parse_args()
    assembler.assemble(args.file)
