#!/usr/bin/env python3
import sys

code, vars = {}, {"#": 0}

def num(s):
    n = 0
    while s and s[0].isdigit(): n, s = n * 10 + int(s[0]), s[1:]
    return n, s.strip()

def expr(s):
    res, s = term(s)
    while s and s[0] in "+-": res += (1 if s[0] == "+" else -1) * term(s[1:])[0]; s = term(s[1:])[1]
    return res, s

def term(s):
    res, s = factor(s)
    while s and s[0] in "*/": res *= factor(s[1:])[0] if s[0] == "*" else 1 / factor(s[1:])[0]; s = factor(s[1:])[1]
    return res, s

def factor(s):
    if s and s[0] == "(": return expr(s[1:])[0], s[1:]
    return num(s) if s[0].isdigit() else (vars.get(s.split()[0], 0), s[1:])

def stmt(s):
    ops = {
        "rem": lambda _: None, "bye": lambda _: sys.exit(0),
        "list": lambda _: print("\n".join([f"{n:3} {ln}" for n, ln in sorted(code.items())])),
        "print": lambda args: print(args[1:-1] if args[0] == '"' else expr(args)[0]),
        "input": lambda args: vars.update({args[0]: int(input("] "))}),
        "goto": lambda args: vars.update({"#": expr(args)[0]}),
        "if": lambda args: stmt(args.split("then", 1)[1]) if expr(args.split("then", 1)[0])[0] else None,
        "run": lambda _: vars.update({"#": 1}),
    }
    cmd, *args = s.split(None, 1)
    if cmd in ops: ops[cmd](args[0] if args else "")
    elif "=" in s: var, val = s.split("="); vars[var.strip()], _ = expr(val.strip())
    vars["#"] += 1

for line in sys.stdin:
    lineno, line = num(line)
    code[lineno] = line if lineno else stmt(line)
