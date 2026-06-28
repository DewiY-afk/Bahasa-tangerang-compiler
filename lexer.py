import re
from token import Token, TokenType

KEYWORDS = {
    'lamun', 'lamun_ora', 'liyan', 'pilihan', 'basa',
    'salila', 'gawe', 'saban', 'pegat', 'teruskeun',
    'nyieun', 'balikeun', 'kosong', 'kelas', 'urang',
    'indung', 'anyar', 'bener', 'salah', 'jeung',
    'atawa', 'lain', 'ajal', 'cekel', 'pungkasan'
}

BUILTINS = {
    'tulis', 'tanya', 'angka', 'teks', 'panjang',
    'jumlah', 'urut', 'tambah', 'busiat'
}

class Lexer:
    def __init__(self, source):
        self.source = source
        self.rules = [
            ('SKIP', r'[ \t]+'),
            ('NEWLINE', r'\n'),
            ('COMMENT', r'#.*'),
            ('STRING', r'"[^"]*"'),
            ('NUMBER', r'\d+'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('COMPARISON', r'==|!=|<=|>=|<|>'),
            ('OPERATOR', r'\+|-|\*|/|='),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('MISMATCH', r'.')
        ]
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)
        self.scanner = re.compile(self.regex)

    def tokenize(self):
        tokens = []
        line_num = 1
        line_start = 0

        for match in self.scanner.finditer(self.source):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if kind in ['SKIP', 'COMMENT']:
                continue
            if kind == 'NEWLINE':
                line_num += 1
                line_start = match.end()
                continue
            if kind == 'MISMATCH':
                raise Exception(f"Karakter ilegal '{value}' di Baris {line_num}, Kolom {column}")

            if kind == 'ID':
                if value in KEYWORDS:
                    token_type = TokenType.KEYWORD
                elif value in BUILTINS:
                    token_type = TokenType.BUILTIN
                else:
                    token_type = TokenType.IDENTIFIER
            else:
                mapping = {
                    'STRING': TokenType.STRING,
                    'NUMBER': TokenType.NUMBER,
                    'OPERATOR': TokenType.OPERATOR,
                    'COMPARISON': TokenType.COMPARISON,
                    'LBRACE': TokenType.LBRACE,
                    'RBRACE': TokenType.RBRACE,
                    'LPAREN': TokenType.LPAREN,
                    'RPAREN': TokenType.RPAREN,
                    'COMMA': TokenType.COMMA
                }
                token_type = mapping[kind]

            tokens.append(Token(token_type, value, line_num, column))

        tokens.append(Token(TokenType.EOF, '', line_num, len(self.source) - line_start + 1))
        return tokens