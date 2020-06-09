import re

from .base import JackToken


class JackString(JackToken):
    _TOKEN_REGEX = re.compile(r'\"(\w*)\"', re.UNICODE)
