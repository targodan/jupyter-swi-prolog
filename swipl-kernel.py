import os
import os.path as op
import tempfile
import IPython
import jupyter_client
from IPython.utils.process import getoutput
import subprocess as sp
from queue import Queue, Empty
from threading import Thread

SWIPL_ENCODING = "utf-8"
SWIPL_READ_TIMEOUT = 30

def enqueue_output(out, queue):
    try:
        for line in iter(out.readline, b''):
            print('Q <- {0}'.format(line))
            queue.put(line.decode(SWIPL_ENCODING))
    finally:
        queue.put(None)
        out.close()

"""
Executes swipl with `knowledgebase_path` as script input and a list of `queries`
It returns the lines of output and True iff. the execution was successful.
"""
def run_swipl(queries, knowledgebase_path):
    with sp.Popen(["swipl", "-s", knowledgebase_path], stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE) as proc:
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

def run_cell(code, temp_path):
    output = []
    with open(temp_path, 'w') as kb:
        for line in code.split("\n"):
            line = line.strip()

            if line[:2] == "?-":
                # Is query => flush KB and execute
                kb.flush()

                line = line[2:]
                # TODO: batch queries in a list
                tmpOutput, ok = run_swipl([line], temp_path)
                output += tmpOutput

                if not ok:
                    return output, False
            else:
                # Is part of the knowledgebase
                kb.write(line+"\n")

    return output, True

def setup_env():
    dirpath =  tempfile.mkdtemp()
    temp_path = op.join(dirpath, 'temp.pl')
    output_path = op.join(dirpath, 'out.txt')
    code_path = op.join(dirpath, 'code.pl')
    return temp_path, output_path, code_path


"""SWI-Prolog kernel wrapper"""
from ipykernel.kernelbase import Kernel

class SwiplKernel(Kernel):
    implementation = 'SWI-Prolog'
    implementation_version = '0.0'
    language = 'Prolog'
    language_version = '1.0'
    language_info = {'name': 'swipl',
                     'mimetype': 'text/plain'}
    banner = "SWI-Prolog Kernel"

    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):
        """This function is called when a code cell is
        executed."""
        if not silent:
            # We run the Prolog code and get the output.
            output = run_cell(code)

            # We send back the result to the frontend.
            stream_content = {'name': 'stdout',
                              'text': output}
            self.send_response(self.iopub_socket,
                              'stream', stream_content)
        return {'status': 'ok',
                # The base class increments the execution
                # count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

if __name__ == '__main__':
    output, ok = run_cell("""man(socrates).
                            mortal(X) :- man(X).

                            ?- mortal(socrates).
                            ?- mortal(X).
                            ?- mortal(socrates2).
                            man(socrates2).
                            ?- mortal(socrates2).
                            """, "temp.pl")
    if ok:
        print("OK\n")
    else:
        print("NOT OK\n")

    print("\n".join(output))
    #from ipykernel.kernelapp import IPKernelApp
    #IPKernelApp.launch_instance(kernel_class=SwiplKernel)
