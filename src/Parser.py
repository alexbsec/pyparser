from .Tokenizer import Tokenizer

class Parser:

    def __init__(self):
        self._string = ''
        self._tokenizer = Tokenizer()

    def parse(self, string):
        self._tokenizer.initialize(string)
        self._look_ahead_token = self._tokenizer.getNextToken()


        return self.program()

    '''
        Main entry point:
        Program:
            : NumericalLiteral
            ;
    '''

    def program(self):
        return {
            "type": 'Program',
            "body": self.literal(),
        }

    
    '''
        Literal:
            : NumericalLiteral
            | StringLiteral
            ;
    '''

    '''
        NumericalLiteral:
            : NUMBER
            ;
    '''

    def literal(self):
        match self._look_ahead_token.type:
            case "NUMBER":
                return self.numericalLiteral()
            case "STRING":
                return self.stringLiteral()
            case None:
                self._look_ahead_token = self._tokenizer.getNextToken()
                return self.literal()
            
        raise SyntaxError(
            f"Unexpected literal {self._look_ahead_token.type}"
        )

    def numericalLiteral(self):
        token = self._eat('NUMBER')

        return {
            "type": "NumericalLiteral",
            "value": int(token.value)
        }

    def stringLiteral(self):
        token = self._eat('STRING')
        return {
            "type": "StringLiteral",
            "value": token.value[1:len(token.value)-1]
        }
    

    def _eat(self, token_type): 
        token = self._look_ahead_token

        if token.value == None:
            raise SyntaxError(
                f"Unexpected EoL, expected {token_type}."
            )

        if token.type != token_type:
            raise SyntaxError(
                f"Unexpected token: {token.value}, expected: {token_type}."
            )

        self._look_ahead_token = self._tokenizer.getNextToken()

        return token

