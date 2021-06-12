from error.error import InvalidSyntaxError
from parsing.parse_result import ParseResult
from parsing.node import BinOpNode, NumberNode
from lex.token import (
    TT_DIV,
    TT_EOF,
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
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        return res

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        return res.failure(
            InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected int or float")
        )

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    # function term and expr use it
    def bin_op(self, func, ops):
        res = ParseResult()
        left_node = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right_node = res.register(func())
            if res.error:
                return res
            left_node = BinOpNode(left_node, op_tok, right_node)

        return res.success(left_node)
