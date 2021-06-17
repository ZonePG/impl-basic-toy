from interpreter.number import Number
from interpreter.symbol_table import SymbolTable
from interpreter import Interpreter, Context
from lex import Lexer
from parsing import Parser

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))


def run(text):
    # Generate tokens
    lexer = Lexer("<stdin>", text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    print(tokens)

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error
    print(ast.node)

    # Run Program
    interpreter = Interpreter()
    context = Context('<program>')
    context.set_symbol_table(global_symbol_table)
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
