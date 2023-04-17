"""
   Spencer Little (spencer@soursecurity.com)
"""

UNABLE_TO_READ_SOURCE_FILE = lambda file :  f"""
Unable to read source file {file}. Since you're here, I didn't know how to pre-emptively
deduce what went wrong, and handle it in the source, so now the burden is on you to figure
out the issue (:

Imaginary potential problems to check:

1. Encoding error: was the list of SUPPORTED_ENCODING's exhausted? Check Dive's log file (see
Logger.py) for a list of \"Encoding N raised M\" messages of length len(SUPPORTED_ENCODING) (
see FileProcess.py). If there were, there is a problem with the encoding of the source file.

2. Locking / handle retention: was someone holding a handle to {file} when open was called? If you're
using Windows you can check for open handles to processes via Resource Monitor. Under the CPU tab, you
can search for the top most file name {file} under \"Associated Handles\" to identify the process holding
the handle.

... if you've ruled out the above you will probably need further diagnostic data to deduce the issue, or
to simply try another path.
"""

UNABLE_TO_INITIALIZE_LOG_FILE = lambda file :  f"""
Unable to create or read from log file {file}.

Imaginary potential problems to check:

1. Locking / handle retention: was someone holding a handle to {file} when open was called? If you're
using Windows you can check for open handles to processes via Resource Monitor. Under the CPU tab, you
can search for the top most file name {file} under \"Associated Handles\" to identify the process holding
the handle.

... if you've ruled out the above you will probably need further diagnostic data to deduce the issue, or
to simply try another path. You'll be missing log data from the execution session in which the creation of
the Logger singleton failed, the alternative in this case would be proceeding without a sane _current_dist
or _last_commit_time, which could make the logs confusing, which is worse than non-existant.
"""