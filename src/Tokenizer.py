import re  

spec = {
    r'^\d+': "NUMBER",
    r'^[\'"].*?[\'"]' : "STRING"
}

class Token:
    def __init__(self, _type=None, _value=None):
        self.type = _type
        self.value = _value

class Tokenizer:
    def initialize(self, string):
        self._string = string
        self._cursor = 0

    def isEOF(self):
        return self._cursor == len(self._string)

    def hasMoreTokens(self):
        return self._cursor < len(self._string)
    

    def _match(self, regex, string):
        matched = re.match(regex, string)
        if matched:
            val = matched.group()
            self._cursor += len(val)
            return val

        return None


    def assignToken(self, string):
        for regex, t_type in spec.items():
            t_value = self._match(regex, string)
            if t_value is not None:
                return Token(t_type, t_value)
            
        raise SyntaxError(
            f"Unexpected token: {string[0]}"
        )


    def getNextToken(self):
        if not self.hasMoreTokens():
            return Token()

        string = self._string[self._cursor:]
    
        return self.assignToken(string)