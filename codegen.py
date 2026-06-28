from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.execute(stmt)
                
        elif isinstance(node, AssignNode):
            val = self.execute(node.expr)
            self.variables[node.var_name] = val
            return val
            
        elif isinstance(node, BinOpNode):
            left = self.execute(node.left)
            right = self.execute(node.right)
            if node.op == '+': return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left * right
            elif node.op == '/': return left // right
            elif node.op == '==': return left == right
            elif node.op == '!=': return left != right
            elif node.op == '<': return left < right
            elif node.op == '>': return left > right
            elif node.op == '<=': return left <= right
            elif node.op == '>=': return left >= right
            
        elif isinstance(node, NumNode):
            return node.value
            
        elif isinstance(node, StringNode):
            return node.value
            
        elif isinstance(node, VariableNode):
            if node.name in self.variables:
                return self.variables[node.name]
            raise Exception(f"Variabel '{node.name}' kagak ketemu rimbanya (belum dideklarasi)!")
            
        elif isinstance(node, BuiltinCallNode):
            if node.name == 'tulis':
                # Mengubah nilai boolean menjadi teks kearifan lokal saat dicetak
                evaluated_args = []
                for arg in node.args:
                    val = self.execute(arg)
                    if val is True:
                        evaluated_args.append("bener")
                    elif val is False:
                        evaluated_args.append("salah")
                    else:
                        evaluated_args.append(str(val))
                print(" ".join(evaluated_args))
                
            elif node.name == 'tanya':
                prompt = str(self.execute(node.args[0])) if node.args else ""
                return input(prompt)
                
        elif isinstance(node, LamunNode):
            if self.execute(node.condition):
                for stmt in node.then_branch: 
                    self.execute(stmt)
            elif node.else_branch:
                for stmt in node.else_branch: 
                    self.execute(stmt)
                    
        elif isinstance(node, SalilaNode):
            while self.execute(node.condition):
                for stmt in node.body: 
                    self.execute(stmt)