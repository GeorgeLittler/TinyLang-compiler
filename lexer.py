# Define keywords and tokens

KEYWORDS = {"let", "if", "else", "while", "print"}

SINGLE_CHAR_TOKENS = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '%': 'MOD',
    '=': 'ASSIGN',
    ';': 'SEMICOLON',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    '<': 'LT',
    '>': 'GT',
}

DOUBLE_CHAR_TOKENS = {
    '==': 'EQ',
    '!=': 'NE',
    '<=': 'LE',
    '>=': 'GE',
}

def is_whitespace(char):
    return char in ' \t\n'

def is_letter(char):
    return char.isalpha() or char == '_'

def is_digit(char):
    return char.isdigit()

def lex(source):
    tokens = []
    i = 0
    length = len(source)

    while i < length:
        char = source[i]

        if is_whitespace(char):
            i += 1
            continue

        # Double-char operators
        if i + 1 < length:
            two_char = char + source[i+1]
            if two_char in DOUBLE_CHAR_TOKENS:
                tokens.append((DOUBLE_CHAR_TOKENS[two_char], two_char))
                i += 2
                continue

        # Single-char operators/punctuation
        if char in SINGLE_CHAR_TOKENS:
            tokens.append((SINGLE_CHAR_TOKENS[char], char))
            i += 1
            continue

        # Numbers
        if is_digit(char):
            start = i
            while i < length and is_digit(source[i]):
                i += 1
            number = source[start:i]
            tokens.append(('INTEGER', number))
            continue

        # Identifiers and keywords
        if is_letter(char):
            start = i
            while i < length and (is_letter(source[i]) or is_digit(source[i])):
                i += 1
            word = source[start:i]
            if word in KEYWORDS:
                tokens.append((word.upper(), word))
            else:
                tokens.append(('IDENTIFIER', word))
            continue

        raise SyntaxError(f"Unexpected character: {char}")

    return tokens

# Testing
if __name__ == "__main__":
    code = """
    let x = 10;
    let y = x + 5;
    if (y >= 15) {
        print(y);
    }
    """
    result = lex(code)
    for token in result:
        print(token)