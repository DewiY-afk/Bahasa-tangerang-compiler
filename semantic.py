from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.declared_vars = set()

    def analyze(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, AssignNode):
            self.analyze(node.expr)
            self.declared_vars.add(node.var_name)
        elif isinstance(node, BinOpNode):
            self.analyze(node.left)
            self.analyze(node.right)
        elif isinstance(node, VariableNode):
            if node.name not in self.declared_vars:
                print(f"[Peringatan Semantik]: Variabel '{node.name}' digunakan sebelum diberi nilai!")
        elif isinstance(node, LamunNode):
            self.analyze(node.condition)
            for stmt in node.then_branch: self.analyze(stmt)
            if node.else_branch:
                for stmt in node.else_branch: self.analyze(stmt)
        elif isinstance(node, SalilaNode):
            self.analyze(node.condition)
            for stmt in node.body: self.analyze(stmt)
        elif isinstance(node, BuiltinCallNode):
            for arg in node.args: self.analyze(arg)