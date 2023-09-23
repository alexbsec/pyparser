from src import Parser


parser = Parser.Parser()
program = '''/(
    HI MOM
    )/
    1+2-3
'''
ast = parser.parse(program)
print(ast)