import re

from .base import JackToken


class JackDecimal(JackToken):
    @classmethod
    def _get_token_regex(cls):
        return re.compile(
            '^(3276[0-7]|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9]|'  # Match 5 digit numbers
            '1000[0-9]|100[1-9][0-9]|10[1-9][0-9][0-9]|1[1-9][0-9][0-9][0-9]|[2-2][0-9][0-9][0-9][0-9]|'  # Match 5 digit numbers
            '999[0-9]|99[0-8][0-9]|9[0-8][0-9][0-9]|100[0-9]|10[1-9][0-9]|1[1-9][0-9][0-9]|[2-8][0-9][0-9][0-9]|'  # Match 4 digit numbers
            '99[0-9]|9[0-8][0-9]|10[0-9]|1[1-9][0-9]|[2-8][0-9][0-9]|'  # Match 3 digit numbers
            '9[0-9]|1[0-9]|[2-8][0-9]|[0-9])'  # Match 1-2 digit numbers
        )
