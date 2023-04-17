"""
   Spencer Little (spencer@soursecurity.com)

   Most of the repo was designed not to require extensive automated unit testing. This is just
   the most primoridial sanity check I though worth including, just for the sake of watching it
   work locally before tossing it up to the cloud.
"""

import os

from FileProcessor import SourceFile
from Blind import strip_comments, randomize_variables


TEST_FILE_NAME = "test_python.py"
TEST_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), TEST_FILE_NAME)

TEST_FILE_RANDOMIZED = "test_python_randomized.py"
TEST_FILE_RANDOMIZED_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), TEST_FILE_RANDOMIZED)

if __name__ == '__main__':
    source_file = SourceFile(TEST_FILE_PATH)
    print(f"Source as string:\n--------\n{source_file._source_as_string}")
    print("\n\n\n\n")
    comments_stripped = strip_comments(source_file._source_as_string)
    print(f"Comments stripped:\n--------\n{comments_stripped}")
    print("\n\n\n\n")
    souce_randomized = randomize_variables(source_file._source_as_string)
    print(f"Variales randomized:\n--------\n{souce_randomized}")
    with open(TEST_FILE_RANDOMIZED, "w+") as test_file_path:
        test_file_path.write(souce_randomized)