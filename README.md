# Tiny Languages

This repository contains code examples for a series of blog posts "Great Tiny Languages".

Here you may find micro-implementations of the most fundamental historical programming languages. Each implementation is in Python, code is deliberately terse to keep it under ~50 lines of code. Only Python standard library is used, and even that to a very humble extent (`sys`, sometimes `re`, rarely `itertool` etc).

I hope this project becomes a good starting point in implementing your own programming languages or learning about the history of programming.

## Languages

* `asm.py` - Assembly - compiles Python-ish assembly into bytecode and executes it.
* `basic.py` - BASIC - a subset of TinyBASIC, but it comes with a proper BASIC line editor!
* `lisp.py` - Lisp 1.5 - a classic, by John McCarthy, enough to interpret itself (meta-circular interpreter)
* `apl.py` - a k/simple interpreter, by Arthur Whitney, toy dialect of K (array processing programming language), which is a variant of APL itself.
* `mouse.py` - concatenative programming language MOUSE, as published in BYTE magazine from 1979.
* `pl0.py` - a PL/0 interpreter, by Niclaus Wirth.
* `tcl.py` - a tiny, tiny command language (TCL) interpreter.

## License

Code is distributed under MIT license. PRs are welcome!

