import re

from .base import JackToken


class JackSkip(JackToken):
    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'^(//.*)|^(\s+)')
