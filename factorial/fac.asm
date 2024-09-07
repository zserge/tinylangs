CONST 1
CONST 10
VAR n
VAR result

LOAD_CONST 0         # result = 1
STORE_FAST 0         # store in result
LOAD_CONST 1         # n = CONST[1] (change this to calculate factorial of different numbers)
STORE_FAST 1         # store in n
loop:
LOAD_FAST 1          # load n
POP_JUMP_IF_FALSE end  # if n == 0, jump to end
LOAD_FAST 0          # load result
LOAD_FAST 1          # load n
MULTIPLY 0           # result *= n
STORE_FAST 0         # store result
LOAD_FAST 1          # load n
LOAD_CONST 0         # load 1
SUBTRACT 0           # n -= 1
STORE_FAST 1         # store n
JUMP_BACKWARD loop   # jump to start of loop
end:
LOAD_FAST 0          # load result
RETURN_VALUE 0       # return result
