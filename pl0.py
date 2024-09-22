#!/usr/bin/env python3

import re, sys, operator


def parse(code):
    tok = ""; kind = ""; code = code + ";" # force terminate code to trick look-ahead lexer

    # A simple regex-based lexer for PL/0, cuts one token from the string
    def lex(expected=None):
        nonlocal code, tok, kind
        if expected and kind != expected: raise SyntaxError(f"Expected {expected} but got {kind}")
        m = re.match(r"(?P<num>[0-9]+)|(?P<op>[-+*/()<>=])|(?P<ws>\s+)|(?P<kw>begin|end\.|end|if|then|while|do|var|!|\?|call|procedure)|(?P<id>[a-zA-Z]+)|(?P<semi>;)|(?P<asgn>:=)|(?P<comma>,)", code)
        if not m: raise SyntaxError("unexpected character")
        if m.lastgroup == "ws": code = code[m.end():]; return lex()
        tok = code[:m.end()]; kind = m.lastgroup; code = code[m.end():]

    def block():
        var, proc = [], []
        # var <name> , ... ;
        while tok == "var":
            lex("kw")
            while tok != ";":
                var.append(tok); lex("id")
                if tok == ",": lex("comma")
            lex("semi")
        # procedure <name> ; begin ... end;
        while tok=='procedure': lex('kw'); n=tok; lex('id'); lex('semi'); proc.append((n, block())); lex('semi')
        # begin ... end (statement)
        return 'block',var,proc,stmt()

    def stmt():
        # <id> := <expr>
        if kind == "id": n = tok; lex("id"); lex("asgn"); return "asgn", n, expr()
        # call <id>
        elif tok == "call": lex("kw"); n = tok; lex("id"); return "call", n
        # ? <id>
        elif tok == "?": lex("kw"); n = tok; lex("id"); return "read", n
        # ! <expr>
        elif tok == "!": lex("kw"); return "write", expr()
        # begin <stmt...> end
        elif tok == "begin":
            lex("kw"); body = []
            while tok != "end" and tok != "end.":
                body.append(stmt())
                if tok == ";": lex("semi")
            lex("kw"); return "begin", body
        # if <cond> then <stmt>
        # while <cond> do <stmt>
        elif tok == "if" or tok == "while": cond = tok; lex("kw"); e = expr(); op = tok; lex("op"); c = ("op", op, e, expr()); lex("kw"); return (cond, c, stmt())

    def expr(tokens="+-", term=lambda: expr("*/", factor)):
        e = term()
        while tok in tokens: op = tok; lex("op"); e = ("op", op, e, term())
        return e

    def factor():
        if kind == "id": n = tok; lex("id"); return ("id", n)
        elif kind == "num": num = tok; lex("num"); return int(num)
        elif tok == "(": lex("op"); e = expr(); lex("op"); return e

    lex(); return block()

def eval(node, scope=(None, {}, {})):
    def find(x, i=1, frame=scope): return frame[i] if x in frame[i] else find(x, i, frame[0])

    if type(node) is int: return node
    elif node[0] == "id": return find(node[1], 1)[node[1]]
    elif node[0] == "asgn": env = find(node[1], 1); env[node[1]] = eval(node[2], scope)
    elif node[0] == "begin": [eval(n, scope) for n in node[1]]
    elif node[0] == "read": env = find(node[1], 1); env[node[1]] = int(input("> "))
    elif node[0] == "op": return {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, "<": operator.lt, ">": operator.gt, "=": operator.eq}[node[1]](eval(node[2], scope), eval(node[3], scope))
    elif node[0] == "if":
        if eval(node[1], scope): eval(node[2], scope)
    elif node[0] == "while":
        while eval(node[1], scope): eval(node[2], scope)
    elif node[0] == "write": print(eval(node[1], scope))
    elif node[0] == "block": eval(node[3], (scope, {v: 0 for v in node[1]}, {p[0]: p[1] for p in node[2]}))
    elif node[0] == "call": eval(find(node[1], 2)[node[1]], scope)
    return 0

eval(parse("\n".join([line for line in sys.stdin])))
