from interpreter import Interpreter, Context
from lex import Lexer
from parsing import Parser


def run(text):
    # Generate tokens
    lexer = Lexer("<stdin>", text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    if ast.error:
        return None, ast.error

    # Run Program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
