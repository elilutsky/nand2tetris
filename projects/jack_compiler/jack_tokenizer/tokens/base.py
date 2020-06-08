class JackToken:

    @staticmethod
    def is_of_type(word):
        """
        Returns true if the given string is a valid token of the type.
        """
        raise NotImplementedError()

    @property
    def value(self):
        raise NotImplementedError()
