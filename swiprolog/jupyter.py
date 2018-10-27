import os
import os.path as op
import tempfile
import IPython
import subprocess as sp
from queue import Queue, Empty
from threading import Thread
from swiprolog import swipl

def main():
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SwiplKernel)


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
            with tempfile.NamedTemporaryFile(suffix=".pl") as kb_file:
                output, ok = swipl.run_cell(code, kb_file)

            # We send back the result to the frontend.
            stream_content = {'name': 'stdout',
                              'text': "\n".join(output)}
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
    main()
