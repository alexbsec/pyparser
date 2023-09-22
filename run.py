from src import Parser


parser = Parser.Parser()
program = '''
    /(
    bugbyte program
    )/
    'oi'

    // number
'''
ast = parser.parse(program)
print(ast)