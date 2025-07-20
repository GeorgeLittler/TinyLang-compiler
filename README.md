# TinyLang Compiler

**TinyLang** is a minimal interpreted programming language designed and implemented from scratch in Python.

This project includes:
- A **manual lexer** (character-by-character tokeniser)
- A **recursive descent parser** that builds an Abstract Syntax Tree (AST)
- An **interpreter** that executes the AST with variables, expressions, conditionals, and loops

---

## ✨ Language Features

✅ Variable declarations (`let x = 5;`)  
✅ Arithmetic expressions (`+`, `-`, `*`, `/`, `%`)  
✅ Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`)  
✅ Control flow: `if`, `else`, `while`  
✅ Print statements (`print(x);`)  
✅ Reassignment (`x = x + 1;`)  
🚫 No functions or types (yet)

📖 **For full grammar and token rules, see** [`spec.md`](./spec.md)

---

## 🧪 Example TinyLang Program

```tiny
let x = 5 + 3;
print(x);

let count = 0;
while (count < 3) {
    print(count);
    count = count + 1;
}
