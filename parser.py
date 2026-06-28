from token import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def consume(self, token_type, error_msg=""):
        token = self.current_token()
        if token.type == token_type:
            self.pos += 1
            return token
        raise Exception(f"Parser Error di Baris {token.line}, Kolom {token.column}: {error_msg}. Dapat {token.type} ('{token.value}')")

    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.statement())
        return ProgramNode(statements)

    def statement(self):
        token = self.current_token()
        if token.type == TokenType.KEYWORD:
            if token.value == 'lamun':
                return self.lamun_statement()
            elif token.value == 'salila':
                return self.salila_statement()
        elif token.type == TokenType.BUILTIN:
            return self.builtin_statement()
        elif token.type == TokenType.IDENTIFIER:
            return self.assignment_statement()
        raise Exception(f"Pernyataan tidak dikenali: '{token.value}' di baris {token.line}")

    def assignment_statement(self):
        var_name = self.consume(TokenType.IDENTIFIER, "Mengharapkan nama variabel").value
        self.consume(TokenType.OPERATOR, "Mengharapkan '='")
        expr = self.expr()
        return AssignNode(var_name, expr)

    def builtin_statement(self):
        name = self.consume(TokenType.BUILTIN).value
        self.consume(TokenType.LPAREN, "Mengharapkan '('")
        args = []
        if self.current_token().type != TokenType.RPAREN:
            args.append(self.expr())
            while self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                args.append(self.expr())
        self.consume(TokenType.RPAREN, "Mengharapkan ')'")
        return BuiltinCallNode(name, args)

    def lamun_statement(self):
        self.consume(TokenType.KEYWORD)  # lamun
        condition = self.expr()
        self.consume(TokenType.LBRACE, "Mengharapkan '{'")
        then_branch = []
        while self.current_token().type != TokenType.RBRACE:
            then_branch.append(self.statement())
        self.consume(TokenType.RBRACE)
        
        else_branch = None
        if self.current_token().type == TokenType.KEYWORD and self.current_token().value == 'liyan':
            self.consume(TokenType.KEYWORD)  # liyan
            self.consume(TokenType.LBRACE, "Mengharapkan '{'")
            else_branch = []
            while self.current_token().type != TokenType.RBRACE:
                else_branch.append(self.statement())
            self.consume(TokenType.RBRACE)
        return LamunNode(condition, then_branch, else_branch)

    def salila_statement(self):
        self.consume(TokenType.KEYWORD)  # salila
        condition = self.expr()
        self.consume(TokenType.LBRACE, "Mengharapkan '{'")
        body = []
        while self.current_token().type != TokenType.RBRACE:
            body.append(self.statement())
        self.consume(TokenType.RBRACE)
        return SalilaNode(condition, body)

    def expr(self):
        node = self.term()
        while self.current_token().type in (TokenType.OPERATOR, TokenType.COMPARISON) and self.current_token().value in ('+', '-', '==', '!=', '<', '>', '<=', '>='):
            op = self.current_token().value
            self.pos += 1
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token().type == TokenType.OPERATOR and self.current_token().value in ('*', '/'):
            op = self.current_token().value
            self.pos += 1
            node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        token = self.current_token()
        if token.type == TokenType.NUMBER:
            self.pos += 1
            return NumNode(int(token.value))
        elif token.type == TokenType.STRING:
            self.pos += 1
            return StringNode(token.value[1:-1])
        elif token.type == TokenType.IDENTIFIER:
            self.pos += 1
            return VariableNode(token.value)
        elif token.type == TokenType.KEYWORD and token.value in ('bener', 'salah'):
            self.pos += 1
            # Diubah langsung menjadi True atau False bawaan Python
            return NumNode(True if token.value == 'bener' else False)
        elif token.type == TokenType.BUILTIN and token.value == 'tanya':
            return self.builtin_statement()
        raise Exception(f"Sintaks eror di dekat '{token.value}' baris {token.line}")