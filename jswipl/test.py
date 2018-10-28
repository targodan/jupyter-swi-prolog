#!/bin/env python3

import tempfile
import swipl

europe_pl = """
neighbours(austria        , [czech_republic, germany, hungary, italy,
                         slovenia, slovakia]).
neighbours(belgium        , [france, netherlands, luxemburg, germany,
                         united_kingdom]).
neighbours(bulgaria       , [romania, greece]).
neighbours(croatia        , [slovenia, hungary]).
neighbours(cyprus         , [greece]).
neighbours(czech_republic , [germany, poland, slovakia, austria]).
neighbours(denmark        , [germany, sweden]).
neighbours(estonia        , [finland, latvia, lithuania]).
neighbours(finland        , [estonia, sweden]).
neighbours(france         , [spain, belgium, luxemburg, germany, italy,
                         united_kingdom]).
neighbours(germany        , [netherlands, belgium, luxemburg, denmark,
                         france, austria, poland]).
neighbours(greece         , [bulgaria, cyprus]).
neighbours(hungary        , [austria, slovakia, romania, croatia,
                         slovenia]).
neighbours(ireland        , [united_kingdom]).
neighbours(italy          , [france, austria, slovenia]).
neighbours(latvia         , [estonia, lithuania]).
neighbours(luxemburg      , [belgium, france, germany]).
neighbours(malta          , []).
neighbours(netherlands    , [belgium, germany , united_kingdom]).
neighbours(poland         , [germany, czech_republic, slovakia,
                         lithuania]).
neighbours(portugal       , [spain]).
neighbours(romania        , [hungary, bulgaria]).
neighbours(slovakia       , [czech_republic, poland, hungary, austria]).
neighbours(slovenia       , [austria, italy, hungary, croatia]).
neighbours(spain          , [france, portugal]).
neighbours(sweden         , [finland, denmark]).
neighbours(united_kingdom , [ireland, netherlands, belgium, france]).

colour_countries(Colours) :-
setof(Country/_, X^neighbours(Country,X), Colours),
colours(Colours).

colours([]).
colours([Country/Colour | Rest]):-
colours(Rest),
member(Colour, [green, yellow, red, purple]),
\+ (member(CountryA/Colour, Rest), neighbour(Country, CountryA)).

neighbour(Country, CountryA):-
neighbours(Country, Neighbours),
member(CountryA, Neighbours).

member(X, [X|_]).
member(X, [_|Tail]) :- member(X, Tail).

?- colour_countries(Map){1}.
"""

socrates_pl = """
man(socrates).
man(bob).
mortal(X) :- man(X).

?- mortal(socrates).
?- mortal(X).
?- mortal(socrates2).
"""

def main():
    output, ok = swipl.run(socrates_pl)
    output, ok = swipl.run(socrates_pl)

    if ok:
        print("OK")
    else:
        print("NOT OK")

    print("\n".join(output))

if __name__ == "__main__":
    main()
