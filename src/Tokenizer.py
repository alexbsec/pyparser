        
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

    def getNextToken(self):
        if not self.hasMoreTokens():
            return Token()

        # numbers
        string = self._string[self._cursor:]

        if string[0].isdigit():
            number = ''
            while self.hasMoreTokens() and string[self._cursor].isdigit():
                number += string[self._cursor]
                self._cursor += 1
            return Token("NUMBER", number)

        # strings

        if string[0] == '"' or string[0] == "'":
            s = ''
            while not self.isEOF():
                s += string[self._cursor]
                self._cursor += 1
            
            if self.isEOF() and s[self._cursor-1] != string[0]:
                return Token()


            return Token("STRING", s)

        
        return Token()