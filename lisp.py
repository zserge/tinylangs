#!/usr/bin/env python3

import sys

# Very simple lexer, split by parens and whitespace
def lex(code): return code.replace("(", " ( ").replace(")", " ) ").split()

# A simple parser: build nested lists from nested parenthesis
def parse(tokens):
    t = tokens.pop(0)
    if t == "(":
        sexp = []
        while tokens[0] != ")": sexp.append(parse(tokens))
        tokens.pop(0)
        return sexp
    try: return int(t)
    except: return t

#
# Add (x, y) pair to list L:
#
#   pairlis([3], [4], []) -> [[3, 4]]
#   pairlis([1, 2, 3], [4, 5, 6], [[7, 8]]) -> [[1, 4], [2, 5], [3, 6], [7, 8]]
#
def pairlis(x, y, L): return L if not x else [[x[0], y[0]]] + pairlis(x[1:], y[1:], L)

#
# Find value in associated list L by key x:
#
#   L = [["foo", 12], ["bar", 42], ["baz", 123]]
#   assoc("bar", L) -> 42
#
def assoc(x, L): return [] if not L else L[0][1] if L[0][0] == x else assoc(x, L[1:])

#
# Atom is not a list, or an empty list (nil)
#   atom([]) -> t
#   atom(42) -> t
#   atom([42, 'a']) -> []
#
def atom(x): return "t" if type(x) != type([]) or len(x) == 0 else []

#
#   apply[fn;x;a] =
#        [atom[fn] → [eq[fn;CAR] → caar[x];
#                    eq[fn;CDR] → cdar[x];
#                    eq[fn;CONS] → cons[car[x];cadr[x]];
#                    eq[fn;ATOM] → atom[car[x]];
#                    eq[fn;EQ] → eq[car[x];cadr[x]];
#                    T → apply[eval[fn;a];x;a]];
#        eq[car[fn];LAMBDA] → eval[caddr[fn]; pairlis[cadr[fn];x;a]]];
#
def apply(f, args, L):
    if f == "atom": return "t" if atom(args[0]) else []
    elif f == "car": return args[0][0]
    elif f == "cdr": return args[0][1:]
    elif f == "cons": return [args[0]] + args[1]
    elif f == "eq": return "t" if atom(args[0]) and args[0] == args[1] else []
    elif f == "+": return args[0] + args[1]
    elif f == "-": return args[0] - args[1]
    elif f == "*": return args[0] * args[1]
    elif f == "/": return args[0] / args[1]
    elif f[0] == "lambda": return eval(f[2], pairlis(f[1], args, L))
    else: return apply(eval(f, L), args, L)

# Evaluate "cond"
def evcon(x, L): return [] if len(x) == 0 else eval(x[0][1], L) if eval(x[0][0], L) else evcon(x[1:], L)

# Evaluate list of lambda arguments
def evlis(x, L): return [eval(x[0], L)] + evlis(x[1:], L) if x else []

#
# McCarthy's eval from the paper:
#
#   eval[e;a] =
#      [atom[e] → cdr[assoc[e;a]];
#       atom[car[e]] →
#             [eq[car[e],QUOTE] → cadr[e];
#              eq[car[e];COND] → evcon[cdr[e];a];
#              T → apply[car[e];evlis[cdr[e];a];a]];
#       T → apply[car[e];evlis[cdr[e];a];a]]
#
# ...with a few additions: nil, t, symbols and label
#
def eval(x, L):
    if x == "nil": return []
    elif x == "t" or type(x) == int: return x
    elif type(x) == str: return assoc(x, L)
    elif x[0] == "quote": return x[1]
    elif x[0] == "cond": return evcon(x[1:], L)
    elif x[0] == "label": L.insert(0, [x[1], x[2]]); return x[1]
    else: return apply(x[0], evlis(x[1:], L), L)

G = []
[print(eval(parse(lex(line.split(";", 1)[0])), G)) for line in sys.stdin if line.strip()]
