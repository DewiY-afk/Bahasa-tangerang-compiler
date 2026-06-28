from enum import Enum, auto

class TokenType(Enum):
    # Literal & Identifier
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Keywords & Builtins
    KEYWORD = auto()
    BUILTIN = auto()
    
    # Operators & Comparisons
    OPERATOR = auto()      # +, -, *, /, =
    COMPARISON = auto()    # ==, !=, <, >, <=, >=
    
    # Delimiters
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    COMMA = auto()         # ,
    
    # End of File
    EOF = auto()

class Token:
    def __init__(self, type: TokenType, value: str, line: int = 0, column: int = 0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', Line:{self.line}, Col:{self.column})"