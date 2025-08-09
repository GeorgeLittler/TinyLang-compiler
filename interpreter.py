from tinylang_ast import *

class Interpreter:
    def __init__(self):
        # Variable environment (symbol table)
        self.env = {}

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
        # Literals
        if isinstance(expr, Integer):
            return expr.value
        if isinstance(expr, String):
            return expr.value

        # Variables
        if isinstance(expr, Variable):
            if expr.name in self.env:
                return self.env[expr.name]
            raise NameError(f"Undefined variable: {expr.name}")

        # Binary operations
        if isinstance(expr, BinaryOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            op = expr.op

            # If either side is a string and op is '+', do string concatenation
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right

            if op == '-':  return left - right
            if op == '*':  return left * right
            if op == '/':  return left // right  # integer division
            if op == '%':  return left % right

            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<':  return left < right
            if op == '<=': return left <= right
            if op == '>':  return left > right
            if op == '>=': return left >= right

            raise RuntimeError(f"Unknown operator: {op}")

        raise RuntimeError(f"Unknown expression: {expr}")
