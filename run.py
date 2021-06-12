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

    return ast.node, ast.error
