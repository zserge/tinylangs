#!/usr/bin/env python3
import types,dis,sys

# A minimal two-pass assembler for CPythin VM bytecode.  It can handle assembly
# instructions (simple and extended BINARY_OPs), constants, variables and
# labels.  Assembly source file is read from stdin until EOF. Resulting
# function is compiled and executed immediately after.

# Some CPython VM opcodes, feel free to extend these
OPS = {'LOAD_CONST':100,'LOAD_FAST':124,'STORE_FAST':125,'RETURN_VALUE':83,'JUMP_FORWARD':110,'JUMP_BACKWARD':140,'POP_JUMP_IF_FALSE':114,'POP_JUMP_IF_TRUE':115,'BINARY_OP':122}

# BINARY_OP parameters for arithmetic operations
BINOPS = {'ADD':0,'SUBTRACT':10,'MULTIPLY':5,'DIVIDE':3}

# Two-pass assembler
def assemble(code):
     bytecode, consts, vars, labels = [], [], [], {}
     pos = 0
     # First pass: handle constants, variables and label addresses
     for line in code.split('\n'):
          parts = line.strip().split()
          if not parts: continue
          instr = parts[0]
          if instr.endswith(':'): labels[instr[:-1]] = pos
          elif instr == 'CONST': consts.append(int(parts[1]))
          elif instr == 'VAR': vars.append(parts[1])
          else: pos += 2 if instr not in BINOPS else 4
     # Second pass: translate instructions to bytecode 1:1 and fill in labels
     for line in code.split('\n'):
          parts = line.strip().split()
          if not parts: continue
          instr = parts[0]
          if instr.endswith(':') or instr == 'CONST' or instr == 'VAR': continue
          arg = parts[1] if len(parts) > 1 else 0
          # Replace labels with addresses
          if isinstance(arg, str) and arg in labels:
               if labels[arg] < len(bytecode): arg = (len(bytecode)-labels[arg])/2+1
               else: arg = (labels[arg]-len(bytecode))/2-1
          if instr in BINOPS:
              # BINARY_OP is a 4-byte command with a 2-byte parameter
              bytecode.append(OPS['BINARY_OP'])
              bytecode.append(BINOPS[instr]&255)
              bytecode.append(BINOPS[instr]>>8&255)
              bytecode.append(0)
          else:
              bytecode.append(OPS[instr])
              bytecode.append(int(arg))
     return tuple(consts), tuple(vars), bytes(bytecode)

code = ''.join([line for line in sys.stdin])
consts, v, bytecode = assemble(code)
code_obj = types.CodeType(0,0,0,len(v),128,64,bytecode,consts,(),v,'asm','mod','',1,b'',b'')
# Optionally, disassemble the bytecode for debugging
# dis.dis(ff)
print(types.FunctionType(code_obj, {})())
