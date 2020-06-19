from .alphanumeric import JackKeyword
from .alphanumeric import JackDecimal
from .symbol import JackSymbol
from .string import JackString
from .identifier import JackIdentifier


CLASS_TO_XML_TAG = {
    JackKeyword: 'keyword',
    JackSymbol: 'symbol',
    JackDecimal: 'integerConstant',
    JackString: 'stringConstant',
    JackIdentifier: 'identifier'
}