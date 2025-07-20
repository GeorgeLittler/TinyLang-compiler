from tinylang_ast import *

class CCodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent_level = 1

    def indent(self):
        return '    ' * self.indent_level

    def emit(self, line):
        self.lines.append(self.indent() + line)

    def generate(self, program):
        self.lines = []
        self.lines.append('#include <stdio.h>')
        self.lines.append('int main() {')

        self.env = set()  # Keep track of declared variables

        for stmt in program:
            self.visit(stmt)

        self.lines.append('    return 0;')
        self.lines.append('}')
        return '\n'.join(self.lines)

    def visit(self, node):
        if isinstance(node, LetStatement):
            decl = '' if node.name in self.env else 'int '
            self.env.add(node.name)
            expr = self.expr(node.value)
            self.emit(f'{decl}{node.name} = {expr};')

        elif isinstance(node, PrintStatement):
            expr = self.expr(node.expression)
            self.emit(f'printf("%d\\n", {expr});')

        elif isinstance(node, IfStatement):
            cond = self.expr(node.condition)
            self.emit(f'if ({cond}) {{')
            self.indent_level += 1
            for stmt in node.true_block:
                self.visit(stmt)
            self.indent_level -= 1
            self.emit('}')
            if node.false_block:
                self.emit('else {')
                self.indent_level += 1
                for stmt in node.false_block:
                    self.visit(stmt)
                self.indent_level -= 1
                self.emit('}')

        elif isinstance(node, WhileStatement):
            cond = self.expr(node.condition)
            self.emit(f'while ({cond}) {{')
            self.indent_level += 1
            for stmt in node.body:
                self.visit(stmt)
            self.indent_level -= 1
            self.emit('}')

        else:
            raise RuntimeError(f'Unhandled statement type: {node}')

    def expr(self, e):
        if isinstance(e, Integer):
            return str(e.value)
        elif isinstance(e, Variable):
            return e.name
        elif isinstance(e, BinaryOp):
            return f'({self.expr(e.left)} {e.op} {self.expr(e.right)})'
        else:
            raise RuntimeError(f'Unhandled expression type: {e}')