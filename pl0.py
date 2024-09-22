#!/usr/bin/env python3

import re, sys, operator


# A simple regex-based lexer for PL/0, cuts one token from the string
def lex(s):
    m = re.match(r"(?P<num>[0-9]+)|(?P<op>[-+*/()<>=])|(?P<ws>\s+)|(?P<kw>begin|end\.|end|if|then|while|do|var|!|\?|call|procedure)|(?P<id>[a-zA-Z]+)|(?P<semi>;)|(?P<asgn>:=)|(?P<comma>,)", s)
    if not m: raise SyntaxError("unexpected character")
    if m.lastgroup == "ws": return lex(s[m.end():])
    return s[:m.end()], m.lastgroup, s[m.end():]


def parse(code):
    tok, kind, code = lex(code + ";") # force terminate code to trick look-ahead lexer

    def eat(expected):
        nonlocal code, tok, kind
        if kind != expected: raise SyntaxError(f"Expected {expected} but got {kind}")
        prevtok=tok; tok,kind,code=lex(code); return prevtok

    def block():
        var, proc = [], []
        # var <name> , ... ;
        while tok == "var":
            eat("kw")
            while tok != ";":
                var.append(eat("id"))
                if tok == ",": eat("comma")
            eat("semi")
        # procedure <name> ; begin ... end;
        while tok=='procedure': eat('kw'); n=eat('id'); eat('semi'); proc.append((n, block())); eat('semi')
        # begin ... end (statement)
        return 'block',var,proc,stmt()

    def stmt():
        # <id> := <expr>
        if kind == "id": n = eat("id"); eat("asgn"); return "asgn", n, expr()
        # call <id>
        elif tok == "call": eat("kw"); n = eat("id"); return "call", n
        # ? <id>
        elif tok == "?": eat("kw"); n = eat("id"); return "read", n
        # ! <expr>
        elif tok == "!": eat("kw"); return "write", expr()
        # begin <stmt...> end
        elif tok == "begin":
            eat("kw"); body = []
            while tok != "end" and tok != "end.":
                body.append(stmt())
                if tok == ";": eat("semi")
            eat("kw"); return "begin", body
        # if <cond> then <stmt>
        elif tok == "if": eat("kw"); c = cond(); eat("kw"); return ("if", c, stmt())
        # while <cond> do <stmt>
        elif tok == "while": eat("kw"); c = cond(); eat("kw"); return ("while", c, stmt())

    def cond(): e = expr(); op = eat("op"); return ("op", op, e, expr())

    def expr():
        e = term()
        while tok in "+-": op = eat("op"); e = ("op", op, e, term())
        return e

    def term():
        t = factor()
        while tok in "*/": op = eat("op"); t = ("op", op, t, factor())
        return t

    def factor():
        if kind == "id": n = eat("id"); return ("id", n)
        elif kind == "num": num = eat("num"); return int(num)
        elif tok == "(": eat("op"); e = expr(); eat("op"); return e

    return block()

def eval(node, scope=(None, {}, {})):
    def find(x, i=1):
        frame = scope
        while frame != None:
            if x in frame[i]: return frame[i]
            else: frame = frame[0]

    if type(node) is int: return node
    elif node[0] == "id": return find(node[1], 1)[node[1]]
    elif node[0] == "asgn": env = find(node[1], 1); env[node[1]] = eval(node[2], scope)
    elif node[0] == "begin": [eval(n, scope) for n in node[1]]
    elif node[0] == "read": env = find(node[1], 1); env[node[1]] = int(input("> "))
    elif node[0] == "op":
        return {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, "<": operator.lt, ">": operator.gt, "=": operator.eq}[node[1]](eval(node[2], scope), eval(node[3], scope))
    elif node[0] == "if":
        if eval(node[1], scope): eval(node[2], scope)
    elif node[0] == "while":
        while eval(node[1], scope): eval(node[2], scope)
    elif node[0] == "write": print(eval(node[1], scope))
    elif node[0] == "block": eval(node[3], (scope, {v: 0 for v in node[1]}, {p[0]: p[1] for p in node[2]}))
    elif node[0] == "call": eval(find(node[1], 2)[node[1]], scope)
    return 0

eval(parse("\n".join([line for line in sys.stdin])))
