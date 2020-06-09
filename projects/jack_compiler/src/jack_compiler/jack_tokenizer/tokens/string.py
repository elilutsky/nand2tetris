import re

from .base import JackToken


class JackString(JackToken):

    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'\"(\w*)\"', re.UNICODE)
