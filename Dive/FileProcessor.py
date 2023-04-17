"""
   Spencer Little (spencer@soursecurity.com)
"""

from locale import getencoding
import os

from Logger import LOGGER
from ErrorMessages import UNABLE_TO_READ_SOURCE_FILE

# https://docs.python.org/3/library/functions.html#open
LOCALE_DEFAULT_ENCODING = getencoding()
# https://docs.python.org/3/library/codecs.html#standard-encodings
#
# A best effort to manage variable encodings. I have no reason to suspect
# there will be significant issues here. Testing locally interoperability
# between disparate encodings appeared fine. For now, try a few common ones
# and the platform default. Log if we have to bail.
#
SUPPORTED_ENCODING = [
    'utf-8',
    'ascii',
    LOCALE_DEFAULT_ENCODING,
]

class SourceFile():

    _encoding = None
    _source_as_string = None

    def __init__(self, source_path_as_string):
        if not os.path.exists(source_path_as_string):
            LOGGER.log_event(f"Provided path {path} does not os.path.exist(s)!", LogLevel.STOPPED_EXECUTING, do_assert=True)
        
        for enc in SUPPORTED_ENCODING:
            try:
                # https://docs.python.org/3/library/functions.html#open - see "strict" semantics
                with open(source_path_as_string, mode='r', encoding=enc, errors='strict') as f:
                    self._source_as_string = f.read()
                    read = True
            except ValueError as e:
                LOGGER.log_event(f"Encoding {enc} raised {e.args[0]}", LogLevel.JUST_SAYING)
            except Exception as e:
                LOGGER.log_event(f"Unexpected error occurred while reading {source_path_as_string} with encoding {enc}", LogLevel.JUST_SAYING)

            if read:
                break
        
        if not read:
            LOGGER.log_event(UNABLE_TO_READ_SOURCE_FILE(source_path_as_string), LogLevel.STILL_EXECUTING)
            self._source_as_string = None

