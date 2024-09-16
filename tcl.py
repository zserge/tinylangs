#!/usr/bin/env python3
import sys, re, operator

G = {}

def tcl_m(op): return lambda a: str(int(op(int(a[0]), int(a[1]))))
def tcl_puts(a): s = " ".join(a); print(s); return s
def tcl_set(a): G.update({a[0]: a[1]}) if len(a) > 1 else ""; return G.get(a[0], "")
def tcl_while(a):
    while int(tcl_eval(a[0])): tcl_eval(a[1])

FN = {
    "#": lambda a: "",
    "puts": tcl_puts,
    "+": tcl_m(operator.add),
    "*": tcl_m(operator.mul),
    "<=": tcl_m(operator.le),
    "set": tcl_set,
    "while": tcl_while,
}

def tcl_tok(code):
    if code[0] == "$": return "$" + tcl_tok(code[1:])
    elif code[0] in ";\n": return ";"
    elif code[0] == " ": return re.match(r"\s*", code).group(0)
    elif code[0] in "{[":
        level, i = 1, 1
        while level > 0 and i < len(code):
            if code[i] in "}]":
                level = level - 1
            elif code[i] in "{[":
                level = level + 1
            i = i + 1
        return code[:i]
    else: return re.match(r"[^;${}\[\]\n ]*", code).group(0)

def tcl_subst(s):
    if s and s[0] == "{": return s[1:-1]
    elif s and s[0] == "$": return tcl_eval("set " + s[1:] + ";")
    elif s and s[0] == "[": return tcl_eval(s[1:-1] + ";")
    return s

def tcl_eval(code):
    args, r = [""], ""
    while code:
        tok = tcl_tok(code)
        code = code[len(tok) :]
        if tok[0] == " ": args = (args + [""]) if args[0] else args
        elif tok != ";": args[-1] += tcl_subst(tok)
        if (tok == ";" or code == "") and len(args) > 0:
            r = FN[args[0]](args[1:]) if args[0] in FN else ""
            args = [""]
    return r

tcl_eval("\n".join([line for line in sys.stdin]))
