from parsing.node import BinOpNode, NumberNode
from lex.token import (
    TT_DIV,
    TT_FLOAT,
    TT_INT,
    TT_MINUS,
    TT_MUL,
    TT_PLUS,
)


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def parse(self):
        return self.expr()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    # function term and expr use it
    def bin_op(self, func, ops):
        left_node = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right_node = func()
            left_node = BinOpNode(left_node, op_tok, right_node)

        return left_node
