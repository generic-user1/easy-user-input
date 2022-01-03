
#Simulated Input/Output (simulatedIO)
#functions for simulating user input and output
#useful for testing functions that prompt a user for input and do something with it

from contextlib import contextmanager
from typing import Generator
from io import StringIO


#context-managed stdin redirection
#when passed a parameter, it is cast to a string and written to stdin
#this is useful for automated testing of functions that get input from the user
@contextmanager
def simulatedInput(inputValue: str):
    import sys
    
    originalStdin = sys.stdin

    with StringIO(initial_value=inputValue) as newStdin:
        try:
            sys.stdin = newStdin
            yield
        finally:
            sys.stdin = originalStdin


#context-managed stdout (or stderr) redirection
#redirects an output stream to a new StringIO object, which is yielded
#this is useful for automated verification of text normally output to users
#captures stdout by default, or stderr if the `stderr` param is set to True
@contextmanager
def simulatedOutput(stderr = False) -> Generator[StringIO, None, None]:
    if not stderr:
        from contextlib import redirect_stdout as redirect_stream
    else:
        from contextlib import redirect_stderr as redirect_stream

    with StringIO() as newStream, redirect_stream(newStream):
        yield newStream