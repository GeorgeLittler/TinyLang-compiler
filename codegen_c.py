from tinylang_ast import *

class CCodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent_level = 1
        self.env = set()  # declared variables (ints only for now)

    def indent(self):
        return '    ' * self.indent_level

    def emit(self, line):
        self.lines.append(self.indent() + line)

    def generate(self, program):
        self.lines = []
        self.lines.append('#include <stdio.h>')
        self.lines.append('int main() {')

        self.env = set()

        for stmt in program:
            self.visit(stmt)

        self.lines.append('    return 0;')
        self.lines.append('}')
        return '\n'.join(self.lines)

    # ---------- helpers ----------

    def c_string_literal(self, s):
        # Escape for C string literal
        s = s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'"{s}"'

    def is_stringy(self, node):
        # literal String or any '+' tree containing a string
        if isinstance(node, String):
            return True
        if isinstance(node, BinaryOp) and node.op == '+':
            return self.is_stringy(node.left) or self.is_stringy(node.right)
        return False

    def flatten_concat(self, node):
        # turns a + (b + c) -> [a, b, c] for op '+'
        parts = []
        def dfs(n):
            if isinstance(n, BinaryOp) and n.op == '+':
                dfs(n.left)
                dfs(n.right)
            else:
                parts.append(n)
        dfs(node)
        return parts

    # ---------- visitors ----------

    def visit(self, node):
        if isinstance(node, LetStatement):
            # For now, only int variables in C backend
            if self.is_stringy(node.value):
                raise RuntimeError('C backend: string-valued variables not supported yet.')
            decl = '' if node.name in self.env else 'int '
            self.env.add(node.name)
            expr_c = self.expr(node.value)
            self.emit(f'{decl}{node.name} = {expr_c};')

        elif isinstance(node, PrintStatement):
            e = node.expression
            if self.is_stringy(e):
                # print concatenated pieces without newline, then newline
                for part in self.flatten_concat(e):
                    if self.is_stringy(part):
                        self.emit(f'printf("%s", {self.expr(part)});')
                    else:
                        self.emit(f'printf("%d", {self.expr(part)});')
                self.emit('printf("\\n");')
            else:
                self.emit(f'printf("%d\\n", {self.expr(e)});')

        elif isinstance(node, IfStatement):
            cond = self.expr(node.condition)
            self.emit(f'if ({cond}) {{')
            self.indent_level += 1
            for s in node.true_block:
                self.visit(s)
            self.indent_level -= 1
            self.emit('}')
            if node.false_block:
                self.emit('else {')
                self.indent_level += 1
                for s in node.false_block:
                    self.visit(s)
                self.indent_level -= 1
                self.emit('}')

        elif isinstance(node, WhileStatement):
            cond = self.expr(node.condition)
            self.emit(f'while ({cond}) {{')
            self.indent_level += 1
            for s in node.body:
                self.visit(s)
            self.indent_level -= 1
            self.emit('}')

        else:
            raise RuntimeError(f'Unhandled statement type: {node}')

    def expr(self, e):
        if isinstance(e, Integer):
            return str(e.value)
        elif isinstance(e, Variable):
            return e.name
        elif isinstance(e, String):
            return self.c_string_literal(e.value)
        elif isinstance(e, BinaryOp):
            # For non-concat ops, just emit infix — caller decides format spec
            return f'({self.expr(e.left)} {e.op} {self.expr(e.right)})'
        else:
            raise RuntimeError(f'Unhandled expression type: {e}')
