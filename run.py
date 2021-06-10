from lex import Lexer


def run(text):
    lexer = Lexer("<stdin>", text)
    tokens, error = lexer.make_tokens()

    return tokens, error
