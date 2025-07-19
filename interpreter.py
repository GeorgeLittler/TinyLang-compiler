from tinylang_ast import *

class Interpreter:
    def __init__(self):
        self.env = {}  # variable environment (symbol table)

    def run(self, program):
        for stmt in program:
            self.execute(stmt)

    def execute(self, node):
        if isinstance(node, LetStatement):
            value = self.eval_expr(node.value)
            self.env[node.name] = value

        elif isinstance(node, PrintStatement):
            value = self.eval_expr(node.expression)
            print(value)

        elif isinstance(node, IfStatement):
            cond = self.eval_expr(node.condition)
            if cond:
                for stmt in node.true_block:
                    self.execute(stmt)
            else:
                for stmt in node.false_block:
                    self.execute(stmt)

        elif isinstance(node, WhileStatement):
            while self.eval_expr(node.condition):
                for stmt in node.body:
                    self.execute(stmt)

        else:
            raise RuntimeError(f"Unknown statement: {node}")

    def eval_expr(self, expr):
        if isinstance(expr, Integer):
            return expr.value
        elif isinstance(expr, Variable):
            if expr.name in self.env:
                return self.env[expr.name]
            else:
                raise NameError(f"Undefined variable: {expr.name}")
        elif isinstance(expr, BinaryOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            op = expr.op

            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': return left // right  # integer division
            if op == '%': return left % right
            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<': return left < right
            if op == '<=': return left <= right
            if op == '>': return left > right
            if op == '>=': return left >= right

            raise RuntimeError(f"Unknown operator: {op}")

        else:
            raise RuntimeError(f"Unknown expression: {expr}")