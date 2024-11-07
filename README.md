# Tiny Languages

![ASM](https://img.shields.io/badge/ASM-38_LOC-green)
![BASIC](https://img.shields.io/badge/BASIC-50_LOC-green)
![MOUSE](https://img.shields.io/badge/MOUSE-50_LOC-green)
![LISP](https://img.shields.io/badge/LISP-39_LOC-green)
![TCL](https://img.shields.io/badge/TCL-48_LOC-green)
![APL/K](https://img.shields.io/badge/APL/K-45_LOC-green)
![PL/0](https://img.shields.io/badge/PL/0-50_LOC-green)

This repository contains code examples for [a](https://zserge.com/posts/langs-asm) [series](https://zserge.com/posts/langs-basic) [of](https://zserge.com/posts/langs-mouse) [blog](https://zserge.com/posts/langs-lisp) [posts](https://zserge.com/posts/langs-apl) ["Great Tiny Languages"](https://zserge.com/posts/langs-pl0/).

Here you may find micro-implementations of the most fundamental historical programming languages. Each implementation is in Python, code is deliberately terse to keep it under ~50 lines of code. Only Python standard library is used, and even that to a very humble extent (`sys`, sometimes `re`, rarely `itertool` etc).

I hope this project becomes a good starting point in implementing your own programming languages or learning about the history of programming.

## Languages

* `asm.py` - Assembly - compiles Python-ish assembly into bytecode and executes it.
* `basic.py` - BASIC - a subset of TinyBASIC, but it comes with a proper BASIC line editor!
* `lisp.py` - Lisp 1.5 - a classic, by John McCarthy, enough to interpret itself (meta-circular interpreter)
* `apl.py` - a k/simple interpreter, by Arthur Whitney, toy dialect of K (array processing programming language), which is a variant of APL itself.
* `mouse.py` - concatenative programming language MOUSE, as published in BYTE magazine from 1979.
* `pl0.py` - a PL/0 interpreter, by Niclaus Wirth.
* `tcl.py` - a tiny, tiny command language interpreter (TCL).

## License

Code is distributed under MIT license. PRs are welcome!

