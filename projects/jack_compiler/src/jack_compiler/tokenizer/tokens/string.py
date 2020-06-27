import re

from .base import JackRegexToken


class JackString(JackRegexToken):

    @classmethod
    def _get_token_regex(cls):
        return re.compile(r'\"([^\"]*)\"', re.UNICODE)
