#!/usr/bin/env python3
import sys

code, vars = {}, {"#": 0}

def num(s):
    n = 0
    while s and s[0].isdigit(): n, s = n * 10 + int(s[0]), s[1:]
    return n, s.strip()

def expr(s):
    res, s = term(s); op = ""
    while s and s[0] in "+-":
        op = s[0]
        n, s = term(s[1:])
        res += n if op == "+" else -n
    return res, s


def term(s):
    res, s = factor(s)
    while s and s[0] in "*/":
        op = s[0]
        n, s = factor(s[1:])
        res *= n if op == "*" else 1 / n if n != 0 else 0
    return res, s


def factor(s):
    if s and s[0] == "(": res, s = expr(s[1:]); return res, s[1:]
    elif s and s[0].isdigit(): return num(s)
    else:
        i = 0
        while i < len(s) and s[i].isalnum(): i += 1
        return vars.get(s[:i], 0), s[i:]


def stmt(s):
    def do_if(s):
        n, ln = expr(s)
        if n: stmt(ln)

    while s != None:
        cmd = s.split(None, 1)
        vars["#"] += 1 if vars["#"] else 0
        ops = {
            "rem": lambda args: None,
            "new": lambda args: code.clear(),
            "bye": lambda args: sys.exit(0),
            "list": lambda args: print("\n".join([f"{n:3} {ln}" for (n, ln) in sorted(code.items()) if ln])),
            "print": lambda args: print(args[1:-1] if args and args[0] == '"' else expr(args)[0]),
            "input": lambda args: vars.update({args[0]: int(input("] "))}),
            "goto": lambda args: vars.update({"#": expr(args)[0]}),
            "if": lambda args: do_if(args),
            "run": lambda args: vars.update({"#": 1}),
        }
        if cmd and cmd[0].lower() in ops: ops[cmd[0].lower()](cmd[1] if len(cmd) > 1 else "")
        elif s: assign = s.split("=", 1); vars[assign[0]], _ = expr(assign[1])
        if vars["#"] <= 0: break
        vars["#"], s = next(((n, ln) for (n, ln) in sorted(code.items()) if n >= vars["#"]), (0, None))


for line in sys.stdin:
    lineno, line = num(line)
    if lineno: code[lineno] = line.strip()
    else: stmt(line)
