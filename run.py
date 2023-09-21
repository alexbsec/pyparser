from src import Parser


parser = Parser.Parser()
program = '"asvb"'
ast = parser.parse(program)
print(ast)