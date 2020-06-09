import re

from .base import JackToken


class JackIdentifier(JackToken):
    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'^([^\d\W][\w_]*)')
