# this is a comment
set n 10

set i 1
set f 1
puts $i $f $n
while {<= $i $n} {
  puts $i $n $f
  set f [* $f $i]
  set i [+ $i 1]
}
puts
puts $n{!} is $f

