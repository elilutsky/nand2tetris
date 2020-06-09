import re

from .base import JackToken


class JackIdentifier(JackToken):
    _TOKEN_REGEX = re.compile(r'^([^\d\W][\w_]*)')
