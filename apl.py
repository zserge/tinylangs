#!/usr/bin/env python3

#
# This is an implementation of k/simple language (https://github.com/kparc/ksimple/) in Python
# K/simple is a subset of K langauge, which belongs to the APL family, together with J and Q.
# This program illustrates how array languages work.
#

import sys, re, functools, itertools

G = {}  # global vars

def a(x): return type(x) == int  # is atom?
def err(msg="nyi"): raise f"error: {msg}"  # well, error
def sub(x): return -x if a(x) else list(map(lambda xi: -xi, x))  # negate atom or every element in list
def iota(x): return list(range(0, x)) if a(x) else err("rank/iota")  # iota 1..x or rank error for lists
def rank(x): return err("rank/rank") if a(x) else len(x)  # length of list, or rank error
def cat(x): return [x] if a(x) else x  # atom to list, or return list unchanged
def rev(x): return err("rank/rev") if a(x) else list(reversed(x))  # reverse list, or rank error

# dyad is a helper for high-level verbs.
# if x and y are both atoms: return "x OP y"
# if x is atom and y is a vector: flip them (operators are assumed to be commutative)
# if x is a vector and y is an atom: apply "x OP y" for every element of x
# if both are vectors (of the same length!) - apply OP pairwise
def dyad(x, y, op):
    if a(x): return op(x, y) if a(y) else dyad(y, x, op)
    elif a(y): return list(map(lambda n: op(n, y), x))
    elif len(x) != len(y): err("rank/opx")
    else: return list(map(lambda n: op(n[0], n[1]), zip(x, y)))

def Add(x, y): return dyad(x, y, lambda x, y: x + y)
def And(x, y): return dyad(x, y, lambda x, y: x & y)
def Or(x, y): return dyad(x, y, lambda x, y: x | y)
def Not(x, y): return dyad(x, y, lambda x, y: int(x != y))
def Eq(x, y): return dyad(x, y, lambda x, y: int(x == y))
def Prod(x, y): return dyad(x, y, lambda x, y: x * y)
def Sub(x, y): return Add(x, sub(y))
def Mod(x, y): return err("rank") if not a(x) else y % x if a(y) else list(map(lambda y: y % x, y))
def Take(x, y): return err("rank") if not a(x) else [y]*x if a(y) else y[:x]
def Cat(x, y): return cat(x) + cat(y)
def At(x, y): return x[y] if a(y) else list(map(lambda y: x[y], y))
def at(x): return At(x, 0)

def Over(op, x): return functools.reduce(lambda a, b: op(a, b), x)
def Scan(op, x): return list(itertools.accumulate(x, lambda a, b: op(a, b)))

V = {"+": (err, Add), "-": (sub, Sub), "!": (iota, Mod), "#": (rank, Take), ",": (cat, Cat), "@": (at, At), "=": (err, Eq), "~": (err, Not), "&": (err, And), "|": (rev, Or), "*": (err, Prod)}

def e(s):
    m = re.match(r"(?P<id>[a-zA-Z]+)|(?P<num>[0-9]+)|(?P<op>[-+!#,@=~&|*])", s)
    if not m: err(f"syntax: {s}")
    elif m.lastgroup == "id" or m.lastgroup == "num":
        x = int(s[: m.end()]) if m.lastgroup == "num" else G.get(s[: m.end()], 0)  # a noun
        if m.end() == len(s): return x  # if last in the string: return it
        if s[m.end()] == ":":  # if assignment: recursively evaluate the rest and assign a global
            x = e(s[m.end() + 1 :])
            G[s[: m.end()]] = x
            return x
        return V[s[m.end()]][1](x, e(s[m.end() + 1 :]))  # otherwise: apply dyadic function
    else:
        # If adverb (scan/over): evaluate the rest and apply verb to the resulting noun
        if len(s) > 1 and s[1] in "/\\": return (Over if s[1] == "/" else Scan)(V[s[0]][1], e(s[2:]))
        # Otherwise: apply a monadic verb to the rest of the expression
        return V[s[0]][0](e(s[1:]))

[print(e(line.split(";", 1)[0].strip().replace(" ", ""))) for line in sys.stdin if line.strip()]
