
% Fact
wet_road.

% Rules
slippery :-
    wet_road.

reduce_speed :-
    slippery.