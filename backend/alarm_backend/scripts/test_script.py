import time

from script_utils import file_lock


with file_lock("test_script"):
    time.sleep(1000)
