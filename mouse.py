#!/usr/bin/env python3

import sys

# Returns a position in string "s" of the unmatched delimiter "r" (skipping nested l+r pairs)
#
#     skip("2+(3+(4+5)))+6", "(", ")") -> 12 ("+6")
#     skip("a [ b  [] [] c]] d []", "[", "]") -> 16 (" d []")
#
def skip(s, l, r): return next(i + 1 for i, c in enumerate(s) if (c == r and (s[:i].count(l) - s[:i].count(r)) == 0))

def mouse(s):
    # We need to store macro definitons (they don't shadow variables),
    # data stack, return stack and memory for variables.
    # "i" is a code pointer, offset if the start of the first local variable
    # "A" in current environment (environments can be nested, so inner
    # function's "A" becomes 26, the other inner starts with 52 etc.
    defs, ds, rs, data, i, offset = {}, [], [], [0] * 200, 0, 0

    # First we loop over code and store starting addresses of all macros
    for n, c in enumerate(s):
        if c == "$": defs[s[n + 1]] = n + 2

    while i < len(s) and s[i] != "$":
        # Skip whitespace
        if s[i] in " \t\r\n]$": pass
        # Skip comments till the end of line
        elif s[i] == "'": i += s[i + 1 :].find("\n")
        # Parse numbers into integers
        elif s[i].isdigit():
            n = 0
            while s[i].isdigit(): n = n * 10 + ord(s[i]) - ord("0"); i = i + 1
            i = i - 1; ds.append(n)
        # Put variable address on data stack
        elif s[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": ds.append(ord(s[i]) - ord("A") + offset)
        # Read user input as a number
        elif s[i] == "?": ds.append(num(input("> ")))
        # Print value from data stack as a number
        elif s[i] == "!": print(ds.pop(), end="")
        # Print a literal string, "!" is newline
        elif s[i] == '"': j = skip(s[i + 1 :], '"', '"'); print(s[i + 1 : i + j].replace("!", "\n"), end=""); i = i + j
        # Common arithmetics and comparison (note the lack of == and != operators
        elif s[i] == "+": ds.append(ds.pop() + ds.pop())
        elif s[i] == "-": ds.append(-ds.pop() + ds.pop())
        elif s[i] == "*": ds.append(ds.pop() * ds.pop())
        elif s[i] == "/": ds.append(int(1 / (ds.pop() / ds.pop())))
        elif s[i] == ">": ds.append(int(ds.pop() < ds.pop()))
        elif s[i] == "<": ds.append(int(ds.pop() > ds.pop()))
        # Fetch/dereference variable
        elif s[i] == ".": ds.append(data[ds.pop()])
        # Store value into a variable
        elif s[i] == "=": x = ds.pop(); data[ds.pop()] = x
        # If data stack has non-positive value: execute the block, otherwise skip it
        elif s[i] == "[": i += skip(s[i + 1 :], "[", "]") if ds.pop() <= 0 else 0
        # Start of the loop: store it in return stack
        elif s[i] == "(": rs.append(("LOOP", i, offset))
        # Loop condition: if condition is non-positive - continue, otherwise skip until pairing ")"
        elif s[i] == "^":
            if ds.pop() <= 0: _, i, _ = rs.pop(); i += skip(s[i + 1 :], "(", ")")
        # End of loop: return to its start (which is stored on return stack)
        elif s[i] == ")": _, i, offset = rs[-1]
        # Call a macro: save current code pointer and variable offset, jump to the start of the macro
        elif s[i] == "#":
            if s[i + 1] in defs: rs.append(("MACRO", i, offset)); i = defs[s[i + 1]]; offset = offset + 26
            else: i += skip(s[i + 1 :], "#", ";")
        # End of macro: return to the macro call address and ignore until the last parameter (";")
        elif s[i] == "@": _, i, offset = rs.pop(); i += skip(s[i + 1 :], "#", ";")
        # Macro parameter delimiter: return back to the macro and continue execution from there
        elif s[i] == "," or s[i] == ";": _, i, offset = rs.pop()
        # Macro parameter inside macro: jump to the matching value from the macro call
        elif s[i] == "%":
            pn = ord(s[i + 1])-ord("A")+1; rs.append(("PARAM", i + 1, offset)); pb, tmp = 1, len(rs) - 1
            while pb:
                tmp = tmp - 1; tag, nn, off = rs[tmp]
                if tag == "MACRO": pb = pb - 1
                elif tag == "PARAM": pb = pb + 1
            _, i, offset = rs[tmp]
            while i < len(s) and pn and s[i] != ";":
                i = i + 1
                if s[i] == "#": i += skip(s[i:], "#", ";")
                if s[i] == ",": pn = pn - 1
            if s[i] == ";": _, i, offset = rs.pop()
        i = i + 1


mouse("\n".join([line for line in sys.stdin]))
