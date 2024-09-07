nil                     ; []
42                      ; 42

(quote 42)              ; 42
(quote (a b))           ; ['a', 'b']
(quote ())              ; []

(+ 2 3)                 ; 5
(+ 2 (* 5 7))           ; 37

(atom 42)               ; t
(atom (quote t))        ; t
(atom (quote foo))      ; t
(atom (quote (foo bar))); []
(atom (quote ()))       ; t
(atom (quote (atom (quote a)))) ; []

(eq (quote a) (quote a))          ; t
(eq (quote (a b)) (quote (a b)))  ; []
(eq (quote ()) (quote ()))        ; t
(eq (quote a) (quote b))          ; []
(eq (+ 2 4) (* 2 3))              ; t

(car (quote (a b c)))               ; a
(cdr (quote (a b c)))               ; ['b', 'c']
(car (cdr (quote (a b c))))         ; b
(car (cdr (cdr (quote (a b c)))))   ; c

(cons (quote a) (quote (b c)))                         ; ['a', ['b', 'c']]
(cons (quote a) (cons (quote b) (cons (quote c) nil))) ; ['a', 'b', 'c']

(cond ((eq (quote a) (quote b)) (quote first)) ((atom (quote a)) (quote second))) ; second
(cond ((eq (quote a) (quote a)) (quote first)) ((atom (quote a)) (quote second))) ; first

((lambda (a b) (+ a b)) 2 3)        ; 5
((lambda (x) (cons x (quote (b)))) (quote a)) ; ['a', 'b']

(label five 5) ; five
five           ; 5

(label add (lambda (a b) (+ a b))) ; add
(add 3 five)   ; 8
