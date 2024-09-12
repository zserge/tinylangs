var max, arg, ret;
var foo;

procedure isprime;
var i;
begin
  ret := 1;
  i := 2;
  while i < arg do
  begin
    if arg / i * i = arg then
    begin
      ret := 0;
      i := arg;
    end;
    i := i + 1;
  end;
end;

procedure primes;
begin
  arg := 2;
  while arg < max do
  begin
    call isprime;
    if ret = 1 then ! arg;
    arg := arg + 1;
  end;
end;

begin
  max := 100;
  call primes;
end.
