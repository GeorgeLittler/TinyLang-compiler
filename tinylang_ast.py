class Node:
    pass

# === EXPRESSIONS ===

class Integer(Node):
    def __init__(self, value):
        self.value = int(value)

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left = left    # expression (left-hand side)
        self.op = op        # operator: '+', '-', etc.
        self.right = right  # expression (right-hand side)

# === STATEMENTS ===

class LetStatement(Node):
    def __init__(self, name, value):
        self.name = name    # variable name (string)
        self.value = value  # expression (right-hand side)

class PrintStatement(Node):
    def __init__(self, expression):
        self.expression = expression

class IfStatement(Node):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition         # expression
        self.true_block = true_block       # list of statements
        self.false_block = false_block     # list of statements

class WhileStatement(Node):
    def __init__(self, condition, body):
        self.condition = condition         # expression
        self.body = body                   # list of statements