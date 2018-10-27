#!/bin/env python3

import tempfile
import swipl

def main():
    output, ok = swipl.run("""
    man(socrates).
    mortal(X) :- man(X).

    just some stuff

    ?- man(socrates).
    ?- mortal(X).
    ?- mortal(yourMom).
    """)

    if ok:
        print("OK")
    else:
        print("NOT OK")

    print("\n".join(output))

if __name__ == "__main__":
    main()
