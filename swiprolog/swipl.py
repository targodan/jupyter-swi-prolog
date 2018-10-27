import os
import os.path as op
import tempfile
import IPython
import subprocess as sp
from queue import Queue, Empty
from threading import Thread

SWIPL_ENCODING = "utf-8"
SWIPL_READ_TIMEOUT = 30

def enqueue_output(out, queue):
    try:
        for line in iter(out.readline, b''):
            queue.put(line.decode(SWIPL_ENCODING))
    finally:
        queue.put(None)
        out.close()

"""
Executes swipl with `kb_path` as script input and a list of `queries`
It returns the lines of output and True iff. the execution was successful.
"""
def run_swipl(queries, kb_path):
    with sp.Popen(["swipl", "-s", kb_path], stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE) as proc:
        out = Queue()
        t1 = Thread(target=enqueue_output, args=(proc.stdout, out))
        t1.start()
        t2 = Thread(target=enqueue_output, args=(proc.stderr, out))
        t2.start()

        output = []
        # Consume welcome message and check for errors in KB.
        while True:
            try:
                line = out.get(timeout=0.1)
                if line is None:
                    break
                if "ERROR:" in line:
                    output.append(line)
            except Empty:
                break

        if len(output) > 0:
            proc.stdin.close()
            t1.join()
            t2.join()
            return output, False

        # No errors => continue

        # Write all queries
        for query in queries:
            proc.stdin.write((query+"\n").encode(SWIPL_ENCODING))

        proc.stdin.flush()
        proc.stdin.close()

        # Assume success until we see an error.
        ok = True

        # Consume output
        while True:
            try:
                line = out.get(timeout=SWIPL_READ_TIMEOUT)
                if line is None:
                    # End of output
                    break

                line = line.strip()
                if line == "" or line[0] == "%":
                    # Empty line or comment (like "% halt")
                    continue

                # Save output
                output.append(line)

                if "ERROR:" in line:
                    # Error, this is not ok...
                    ok = False
            except Empty:
                break

        # Join the reader threads
        t1.join()
        t2.join()

        return output, ok

def run_cell(code, kb_file):
    output = []
    for line in code.split("\n"):
        line = line.strip()

        if line[:2] == "?-":
            # Is query => flush KB and execute
            kb_file.flush()

            line = line[2:]
            # TODO: batch queries in a list
            tmpOutput, ok = run_swipl([line], kb_file.name)
            output += tmpOutput

            if not ok:
                return output, False
        else:
            # Is part of the knowledgebase
            kb_file.write((line+"\n").encode(SWIPL_ENCODING))

    return output, True
