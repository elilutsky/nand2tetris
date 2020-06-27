class JackToken:
    def __init__(self, token_value):
        self._token_value = token_value

    @classmethod
    def tokenize(cls, word) -> ('JackToken', str):
        """
        Returns The token and the remainder. If the word cannot be tokenized by the object then the
        returned value will be None, `word`.
        """
        raise NotImplementedError()

    @property
    def value(self):
        return self._token_value

    def __eq__(self, other: 'JackToken'):
        return self.__class__ == other.__class__ and self.value == other.value

    def __repr__(self):
        return f'<{self.__class__}: \'{self.value}\'>'


class JackRegexToken(JackToken):
    def __init__(self, token_value):
        super(JackRegexToken, self).__init__(token_value)

    @classmethod
    def tokenize(cls, word) -> ('JackToken', str):
        """
        A specific overload that uses a regex to match the token
        """
        match = cls._get_token_regex().match(word)
        if match:
            return cls(match.group(1)), word[len(match.group(0)):]
        else:
            return None, word

    @classmethod
    def _get_token_regex(cls):
        raise NotImplementedError()

