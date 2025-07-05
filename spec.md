# TinyLang Language Specification

## 🧱 Supported Features (Minimum Viable Language)

- **Variables**: declared using `let`, assigned using `=`
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Conditionals**: `if`, `else` blocks
- **Loops**: `while` loops
- **Print Statement**: `print(expression)`
- **Literals**: integers only (e.g., `42`)
- **Identifiers**: lowercase variable names (e.g., `x`, `total`)
- **Block structure**: uses `{}` for code blocks
- **End of statement**: semicolon (`;`)

---

## 🔤 Token Types and Examples

| Token Type   | Example          |
|--------------|------------------|
| `LET`        | `let`            |
| `PRINT`      | `print`          |
| `IF`         | `if`             |
| `ELSE`       | `else`           |
| `WHILE`      | `while`          |
| `IDENTIFIER` | `x`, `foo`       |
| `INTEGER`    | `5`, `42`        |
| `ASSIGN`     | `=`              |
| `PLUS`       | `+`              |
| `MINUS`      | `-`              |
| `MUL`        | `*`              |
| `DIV`        | `/`              |
| `MOD`        | `%`              |
| `EQ`         | `==`             |
| `NE`         | `!=`             |
| `LT`         | `<`              |
| `GT`         | `>`              |
| `LE`         | `<=`             |
| `GE`         | `>=`             |
| `LPAREN`     | `(`              |
| `RPAREN`     | `)`              |
| `LBRACE`     | `{`              |
| `RBRACE`     | `}`              |
| `SEMICOLON`  | `;`              |

---

## 🔁 Execution Model

- **Sequential execution** from top to bottom
- **Global variable scope only**
- **No functions** (in MVP)
- **Integer-only language**
- **No input handling** (just hardcoded code and `print()`)

---

## 📘 Example Program (Test Case)

```tiny
let x = 3;
let y = x + 2;

if (y > 4) {
  print(y);
} else {
  print(0);
}

let count = 0;
while (count < 3) {
  print(count);
  count = count + 1;
}