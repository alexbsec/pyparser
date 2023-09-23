import re  

spec = {
    ## NUMBERS:
    r'^\d+': "NUMBER",

    # STRINGS:
    r'^[\'"].*?[\'"]' : "STRING",

    ## WHITESPACES
    r'^\s+': None,

    ## COMMENTS:
    r'^\/\/.*': None,
    r'^\/\([\s\S]*?\)\/': None,

    ## Operators:
    r'[+-]': "OPERATOR",
}

class Token:
    def __init__(self, _type=None, _value=None):
        self.type = _type
        self.value = _value

class Tokenizer:
    def initialize(self, string: str):
        self._string = string
        self._cursor = 0

    def isEOF(self):
        return self._cursor == len(self._string)

    def hasMoreTokens(self):
        return self._cursor < len(self._string)
    

    def _match(self, regex: str, string: str):
        matched = re.match(regex, string)
        if matched:
            val = matched.group()
            self._cursor += len(val)
            return val

        return None


    def assignToken(self, string: str):
        for regex, t_type in spec.items():
            t_value = self._match(regex, string)
            if t_value is None:
                continue
            if t_type is None:
                return self.getNextToken()
            if t_value is not None:
                return Token(t_type, t_value)
            
        raise SyntaxError(
            f"Unexpected token: {string[0]}"
        )


    def getNextToken(self):
        if not self.hasMoreTokens():
            return Token()

        string = self._string[self._cursor:]
    
        token = self.assignToken(string)
        return token