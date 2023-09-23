from .Tokenizer import Tokenizer

class Parser:

    def __init__(self):
        self._string = ''
        self._tokenizer = Tokenizer()
        self._tokens = []

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
        body = self.literal()
        if body is not None:
            return {
                "type": 'Program',
                "body": body,
            }
        else:
            return {
                "type": 'Program',
                "body": "Empty",
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
                explit = self.expressionLiteral()
                return explit
            case "STRING":
                return self.stringLiteral()
            case None:
                if not self._tokenizer.isEOF():
                    self._look_ahead_token = self._tokenizer.getNextToken()
                    return self.literal()
                
                return None
            
        raise SyntaxError(
            f"Unexpected literal {self._look_ahead_token.type}"
        )

####### EXPRESSIONS ###########################
#################################################


    def buildAST(self, exp):
        ast = {
                "type": "ExpressionStatement",
                "expression": exp
            }

        return ast

    def build_expression(self, tokens):
        if len(tokens) == 0 or len(tokens) % 2 != 1:
            return None  # No expression to build
        
        # Find the rightmost operator with the lowest precedence
        lowest_precedence = float('inf')
        lowest_precedence_index = -1
        current_precedence = 0

        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]
            if isinstance(token, str) and token in "+-":
                if current_precedence <= lowest_precedence:
                    lowest_precedence = current_precedence
                    lowest_precedence_index = i
            elif token == '+':
                current_precedence += 1
            elif token == '-':
                current_precedence += 1

        if lowest_precedence_index == -1:
            # No operators found, return the single value as an expression
            return {"type": "NumericalLiteral", "value": tokens[0]}

        left_tokens = tokens[:lowest_precedence_index]
        right_tokens = tokens[lowest_precedence_index + 1:]
        operator = tokens[lowest_precedence_index]

        left_expression = self.build_expression(left_tokens)
        right_expression = self.build_expression(right_tokens)

        return {
            "type": "BinaryExpression",
            "operator": operator,
            "left": left_expression,
            "right": right_expression,
        }



    def expressionLiteral(self):
        tokens = []  # Initialize an empty list to collect tokens

        # Loop to collect all NUMBER and OPERATOR tokens
        while self._look_ahead_token.type in ['NUMBER', 'OPERATOR']:
            print(self._look_ahead_token.value)
            token = self._eat(self._look_ahead_token.type)
            tokens.append(token)

        # Check if there are tokens to build an expression
        if not tokens:
            raise SyntaxError("Expected NUMBER or OPERATOR")

        # Convert tokens to a format suitable for building the AST
        expression_tokens = []
        for token in tokens:
            if token.type == 'NUMBER':
                expression_tokens.append(token.value)
            elif token.type == 'OPERATOR':
                expression_tokens.append(token.value)

        # Build the expression
        exp = self.build_expression(expression_tokens)

        if exp:
            ast = self.buildAST(exp)
            return ast
        else:
            raise SyntaxError(f"Expression could not be parsed correctly. What was interpreted: {' '.join(a for a in expression_tokens)}")

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



'''
AST
2 + 3 - 2

"type": "Program",
"body": {
    "type": "ExpressionStatement",
    "expression": {
        "type": "BinaryExpression",
        "operator": "+",
        "left": {
            "type": "NumericalLiteral",
            "value": 2,
        },
        "right": {
            "type": "BinaryOperator",
            "operator": "-",
            "left": {
                "type": "NumericalLiteral",
                "value": "3",
            },
            "right": {
                "type": "NumericalLiteral",
                "value": 2,
            },
        },
    },
}

'''