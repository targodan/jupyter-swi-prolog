#!/bin/env python3

import tempfile
import swipl

def main():
    with tempfile.NamedTemporaryFile(suffix=".pl") as kb_file:
        output, ok = swipl.run_cell("""
        man(socrates).

        ?- man(socrates).
        ?- man(socrates).
        """, kb_file)

        if ok:
            print("OK")
        else:
            print("NOT OK")

        print("\n".join(output))

if __name__ == "__main__":
    main()
