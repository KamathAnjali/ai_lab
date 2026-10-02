connected(a, b).
connected(b, a).
connected(b, c).
connected(c, b).

can_move(X, Y) :-
    connected(X, Y).