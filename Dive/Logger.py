"""
   Spencer Little (spencer@soursecurity.com)
"""
import os
from enum import Enum
import time

from ErrorMessages import UNABLE_TO_INITIALIZE_LOG_FILE

LOG_FILE_NAME = "DIVE_EXECUTION_AND_ERROR_LOG.txt"
LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), LOG_FILE_NAME)

ONE_MILLION = 1000000

class LogLevel(Enum):
    JUST_SAYING = "JUST_SAYING"
    STILL_EXECUTING = "STILL_EXECUTING"
    STOPPED_EXECUTING = "STOPPED_EXECUTING"

class Logger():

    # the epoch time since we last commited a log line to LOG_FILE
    _last_commit_time = None
    # the current number of log lines we have commited to the log file -1
    _current_dist = None
    _initialized = None

    def __init__(self):
        try:
            if not os.path.exists(LOG_FILE):
                with open(LOG_FILE, "w+") as log_f:
                    log_f.write(f"DIVE EXECUTION AND ERROR LOG INIT\n")
                    self._last_commit_time = (time.time_ns() / ONE_MILLION)
                    self._current_dist = 0
                    log_f.write(f"Log line format is:\n")
                    log_f.write(f"LEVEL (one of: JUST_SAYING|STILL_EXECUTING|STOPPED_EXECUTING) | message | integer distance away from first log message | milliseconds since last log message\n")
                    log_f.write(f"JUST_SAYING | Log file created | 0 | {self._last_commit_time}")
            else:
                with open(LOG_FILE, "r") as log_f:
                    self._last_commit_time = int(((log_f.read().split("\n")[-1]).split("|")[-1]).strip(' '))
                    self._current_dist = int((log_f.read().split("\n")[-1]).split("|")[2])
            self._initialized = True
        except Exception as e:
            print(UNABLE_TO_INITIALIZE_LOG_FILE(LOG_FILE))
            self._initialized = False

            

    def log_event(self, message, level=LogLevel.JUST_SAYING, do_assert=False, commit_to_file=True):
       
        if commit_to_file and self._initialized:
            try:
                with open(LOG_FILE, "a") as log_f:
                    self._current_dist += 1
                    log_f.write(f"{level.value} | {message} | {self._current_dist} | {(time.time_ns() / ONE_MILLION) - self._last_commit_time}")
                    self._last_commit_time = (time.time_ns() / ONE_MILLION)
            except Exception as e:
                print("An exception occurred while handling a log event! My best guess is that the file open above (in class Logger) failed.")
                print(f"We may have contention for the log file (is another process holding a handle to {LOG_FILE_NAME}?)")
                print(f"We may exceeded the max size for the log file or... something else may have occurred.")
                print(f"We'll continue on handling the log event below, but know we may be missing some log data.\n")
       
        print(f"{level.value} | {message} | {self._current_dist} | {(time.time_ns() / ONE_MILLION) - self._last_commit_time}")
       
        if do_assert and self._initialized:
            assert False, f"A critical error occurred and Dive is bailing... Please check {LOG_FILE} for details!"
        elif do_assert:
            assert False, f"A critical error occurred and Dive is bailing... Initialization failed so there are no log entrys in {LOG_FILE} for this session"

LOGGER = Logger()