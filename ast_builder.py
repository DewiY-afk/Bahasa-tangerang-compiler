# File ini berfungsi sebagai pembungkus parser utama untuk mengembalikan AST utuh
from parser import Parser

class ASTBuilder:
    def __init__(self, tokens):
        self.parser = Parser(tokens)

    def build(self):
        return self.parser.parse()