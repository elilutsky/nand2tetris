from . import JackAlphanumeric, JackSkip, JackKeyword, JackDecimal, JackSymbol, JackString, JackIdentifier

from xml.etree.ElementTree import Element, tostring

CLASS_TO_XML_TAG = {
    JackKeyword: 'keyword',
    JackSymbol: 'symbol',
    JackDecimal: 'integerConstant',
    JackString: 'stringConstant',
    JackIdentifier: 'identifier'
}

TOKEN_HANDLER_TYPES = [JackSkip, JackAlphanumeric, JackSymbol, JackString, JackIdentifier]


def write_token_to_xml_output(token, output_file):
    e = Element(CLASS_TO_XML_TAG[token.__class__])
    e.text = f' {token.value} '
    output_file.write(tostring(e).decode('utf-8') + '\n')

