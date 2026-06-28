from ast_nodes import *

class Optimizer:
    def optimize(self, node):
        if isinstance(node, ProgramNode):
            node.statements = [self.optimize(s) for s in node.statements]
            return node
        elif isinstance(node, AssignNode):
            node.expr = self.optimize(node.expr)
            return node
        elif isinstance(node, BinOpNode):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            # Constant folding optimization
            if isinstance(node.left, NumNode) and isinstance(node.right, NumNode):
                if node.op == '+': return NumNode(node.left.value + node.right.value)
                elif node.op == '-': return NumNode(node.left.value - node.right.value)
                elif node.op == '*': return NumNode(node.left.value * node.right.value)
                elif node.op == '/': return NumNode(node.left.value // node.right.value)
            return node
        elif isinstance(node, LamunNode):
            node.condition = self.optimize(node.condition)
            node.then_branch = [self.optimize(s) for s in node.then_branch]
            if node.else_branch:
                node.else_branch = [self.optimize(s) for s in node.else_branch]
            return node
        elif isinstance(node, SalilaNode):
            node.condition = self.optimize(node.condition)
            node.body = [self.optimize(s) for s in node.body]
            return node
        elif isinstance(node, BuiltinCallNode):
            node.args = [self.optimize(arg) for arg in node.args]
            return node
        return node