import re
from lark import Lark

A_INSTRUCTION_MAX_LITERAL_SIZE = 32767

LABEL_REGEX = re.compile('\((?P<label_name>[A-Z_]+)\)')

JGT = "JGT"
JEQ = "JEQ"
JGE = "JGE"
JLT = "JLT"
JNE = "JNE"
JLE = "JLE"
JMP = "JMP"

ZERO = "zero"
ONE = "one"
MINUS_ONE = "minus_one"
DREGISTER = 'dregister'
SREGISTER = 'sregister'
NOT_DREGISTER = 'not_dregister'
NOT_SREGISTER = 'not_sregister'
MINUS_DREGISTER = 'minus_dregister'
MINUS_SREGISTER = 'minus_sregister'
DREGISTER_PLUS_ONE = 'dregister_plus_one'
SREGISTER_PLUS_ONE = 'sregister_plus_one'
DREGISTER_MINUS_ONE = 'dregister_minus_one'
SREGISTER_MINUS_ONE = 'sregister_minus_one'
DREGISTER_PLUS_SREGISTER = 'dregister_plus_sregister'
DREGISTER_MINUS_SREGISTER = 'dregister_minus_sregister'
SREGISTER_MINUS_DREGISTER = 'sregister_minus_dregister'
DREGISTER_AND_SREGISTER = 'dregister_and_sregister'
DREGISTER_OR_SREGISTER = 'dregister_or_sregister'

COMP_TO_BINARY = {
    ZERO: '101010',
    ONE: '111111',
    MINUS_ONE: '111010',
    DREGISTER: '001100',
    SREGISTER: '110000',
    NOT_DREGISTER: '001101',
    NOT_SREGISTER: '110001',
    MINUS_DREGISTER: '001111',
    MINUS_SREGISTER: '110011',
    DREGISTER_PLUS_ONE: '011111',
    SREGISTER_PLUS_ONE: '110111',
    DREGISTER_MINUS_ONE: '001110',
    SREGISTER_MINUS_ONE: '110010',
    DREGISTER_PLUS_SREGISTER: '000010',
    DREGISTER_MINUS_SREGISTER: '010011',
    SREGISTER_MINUS_DREGISTER: '000111',
    DREGISTER_AND_SREGISTER: '000000',
    DREGISTER_OR_SREGISTER: '010101',
}

JMP_TO_BINARY = {
    JGT: '001',
    JEQ: '010',
    JGE: '011',
    JLT: '100',
    JNE: '101',
    JLE: '110',
    JMP: '111',
}

lexer = Lark(f"""
            instruction : A_PREFIX value | dest EQUAL comp | comp SEMICOLON jump
            value: NUMBER | NAME
            dest : register~1..3
            register : {SREGISTER} | {DREGISTER}
            sregister : A_REGISTER | M_REGISTER
            dregister: D_REGISTER
            jump : {JGT} | {JEQ} | {JGE} | {JLT} | {JNE} | {JLE} | {JMP}
            {ZERO}: ZERO
            {ONE}: ONE
            {MINUS_ONE}: MINUS_ONE
            {NOT_DREGISTER}: NOT {DREGISTER}
            {NOT_SREGISTER}: NOT {SREGISTER}
            {MINUS_DREGISTER}: MINUS {DREGISTER}
            {MINUS_SREGISTER}: MINUS {SREGISTER}
            {DREGISTER_PLUS_ONE}: {DREGISTER} PLUS ONE
            {SREGISTER_PLUS_ONE}: {SREGISTER} PLUS ONE
            {DREGISTER_MINUS_ONE}: {DREGISTER} MINUS ONE
            {SREGISTER_MINUS_ONE}: {SREGISTER} MINUS ONE
            {DREGISTER_PLUS_SREGISTER}: {DREGISTER} PLUS {SREGISTER}
            {DREGISTER_MINUS_SREGISTER}: {DREGISTER} MINUS {SREGISTER}
            {SREGISTER_MINUS_DREGISTER}: {SREGISTER} MINUS {DREGISTER}
            {DREGISTER_AND_SREGISTER}: {DREGISTER} AND {SREGISTER}
            {DREGISTER_OR_SREGISTER}: {DREGISTER} OR {SREGISTER}
            comp : {ZERO} | {MINUS_ONE} | {ONE} | {SREGISTER} | {DREGISTER} | {NOT_DREGISTER} | {NOT_SREGISTER} | {MINUS_DREGISTER} | {NOT_SREGISTER} | {MINUS_DREGISTER} | {MINUS_SREGISTER} | {DREGISTER_PLUS_ONE} | {SREGISTER_PLUS_ONE} | {DREGISTER_MINUS_ONE} | {SREGISTER_MINUS_ONE} | {DREGISTER_PLUS_SREGISTER} | {DREGISTER_MINUS_SREGISTER} | {SREGISTER_MINUS_DREGISTER} | {DREGISTER_AND_SREGISTER} | {DREGISTER_OR_SREGISTER} 

            A_PREFIX: "@"
            EQUAL: "="
            SEMICOLON: ";"
            A_REGISTER: "A"
            D_REGISTER: "D"
            M_REGISTER: "M"
            ZERO: "0"
            ONE: "1"
            MINUS_ONE: "-1"
            PLUS: "+"
            MINUS: "-"
            NOT: "!"
            AND: "&"
            OR: "|" 
            {JGT}: "{JGT}"
            {JEQ}: "{JEQ}"
            {JGE}: "{JGE}"
            {JLT}: "{JLT}"
            {JNE}: "{JNE}"
            {JLE}: "{JLE}"
            {JMP}: "{JMP}"
            
            %import common.NUMBER
            %import common.CNAME -> NAME
            """
             , start='instruction')
