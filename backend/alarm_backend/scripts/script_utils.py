import fcntl
from contextlib import contextmanager
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCKS_DIR = os.path.join(CURRENT_DIR, "locks")


@contextmanager
def file_lock(lock_name: str):
    """ Locks FD before entering the context, always releasing the lock. """
    lock_name = f"{lock_name}.lock"
    lock_path = os.path.join(LOCKS_DIR, lock_name)
    lock_file = open(lock_path, "w")

    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
