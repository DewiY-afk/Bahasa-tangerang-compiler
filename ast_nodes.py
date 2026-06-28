class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class AssignNode(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class LamunNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class SalilaNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BuiltinCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args