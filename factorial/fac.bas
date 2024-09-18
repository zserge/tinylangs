REM
REM Factorial program
REM

10  print "Enter N:"
20  input n
30  f=1
50  if n goto 70
60  goto 100
70  f=f*n
80  n=n-1
90  goto 50
100 print f

list
print ""
print "Try 10!..."
run
10
print "Try 8!..."
run
8

