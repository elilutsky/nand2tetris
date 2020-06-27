import re

from .base import JackRegexToken


class JackSkip(JackRegexToken):
    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'^(//.*|\s+)')
