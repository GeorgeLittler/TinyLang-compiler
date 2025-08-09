from tinylang_ast import *
from lexer import lex
from codegen_c import CCodeGenerator

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def match(self, *expected):
        tok_type, _ = self.current()
        if tok_type in expected:
            self.pos += 1
            return True
        return False

    def expect(self, expected):
        tok_type, value = self.current()
        if tok_type == expected:
            self.pos += 1
            return value
        raise SyntaxError(f"Expected {expected}, got {tok_type}")

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match('LET'):
            name = self.expect('IDENTIFIER')
            self.expect('ASSIGN')
            expr = self.expression()
            self.expect('SEMICOLON')
            return LetStatement(name, expr)

        elif self.match('PRINT'):
            self.expect('LPAREN')
            expr = self.expression()
            self.expect('RPAREN')
            self.expect('SEMICOLON')
            return PrintStatement(expr)

        elif self.match('IF'):
            self.expect('LPAREN')
            cond = self.expression()
            self.expect('RPAREN')
            self.expect('LBRACE')
            true_block = self.block()
            self.expect('RBRACE')
            false_block = []
            if self.match('ELSE'):
                self.expect('LBRACE')
                false_block = self.block()
                self.expect('RBRACE')
            return IfStatement(cond, true_block, false_block)

        elif self.match('WHILE'):
            self.expect('LPAREN')
            cond = self.expression()
            self.expect('RPAREN')
            self.expect('LBRACE')
            body = self.block()
            self.expect('RBRACE')
            return WhileStatement(cond, body)

        elif self.current()[0] == 'IDENTIFIER':
            # Reassignment like: count = count + 1;
            name = self.expect('IDENTIFIER')
            self.expect('ASSIGN')
            expr = self.expression()
            self.expect('SEMICOLON')
            return LetStatement(name, expr)

        else:
            raise SyntaxError(f"Unexpected statement at {self.current()}")

    def block(self):
        statements = []
        while self.current()[0] not in ('RBRACE', 'EOF'):
            statements.append(self.statement())
        return statements

    def expression(self):
        left = self.term()
        while self.match('PLUS', 'MINUS', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'):
            op = self.tokens[self.pos - 1][1]
            right = self.term()
            left = BinaryOp(left, op, right)
        return left

    def term(self):
        if self.match('INTEGER'):
            return Integer(self.tokens[self.pos - 1][1])
        elif self.match('STRING'):
            return String(self.tokens[self.pos - 1][1])
        elif self.match('IDENTIFIER'):
            return Variable(self.tokens[self.pos - 1][1])
        elif self.match('LPAREN'):
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {self.current()}")

# === Test code ===
if __name__ == "__main__":
    code = """
    print("hello");
    let x = 5 + 3;
    print(x);
    let count = 0;
    while (count < 3) {
        print(count);
        count = count + 1;
    }
    """
    tokens = lex(code)
    parser = Parser(tokens)
    ast = parser.parse()

    gen = CCodeGenerator()
    c_code = gen.generate(ast)

    with open("output.c", "w") as f:
        f.write(c_code)

    print("✅ Generated C code written to output.c")
