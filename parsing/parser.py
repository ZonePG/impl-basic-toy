from error import InvalidSyntaxError
from parsing.parse_result import ParseResult
from parsing.node import BinOpNode, NumberNode, UnaryOpNode, VarAccessNode, VarAssignNode
from lex.token import (
    TT_DIV,
    TT_EOF,
    TT_EQ,
    TT_FLOAT,
    TT_IDENTIFIER,
    TT_INT,
    TT_KEYWORD,
    TT_LPAREN,
    TT_MINUS,
    TT_MUL,
    TT_PLUS,
    TT_POW,
    TT_RPAREN,
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

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'",
                    )
                )

        return res.failure(
            InvalidSyntaxError(tok.pos_start, tok.pos_end, " zpp Expected int, float, identifier, 'VAR', '+', '-' or '('")
        )

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))
        node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS)))

        if res.error:
            return res.failure(
                InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'VAR', int, float, identifier, '+', '-' or '('")
            )

        return res.success(node)

    # function term and expr use it
    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a
        res = ParseResult()
        left_node = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right_node = res.register(func_b())
            if res.error:
                return res
            left_node = BinOpNode(left_node, op_tok, right_node)

        return res.success(left_node)
