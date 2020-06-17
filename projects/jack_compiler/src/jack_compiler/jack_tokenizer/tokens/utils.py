from .alphanumeric import JackKeyword
from .symbol import JackSymbol
from .decimal import JackDecimal
from .string import JackString
from .identifier import JackIdentifier


CLASS_TO_XML_TAG = {
    JackKeyword: 'keyword',
    JackSymbol: 'symbol',
    JackDecimal: 'integerConstant',
    JackString: 'stringConstant',
    JackIdentifier: 'identifier'
}