from cbuild.core import logger, paths

import os
import time
import fcntl
from contextlib import contextmanager

@contextmanager
def lock(path, pkg = None):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (IOError, OSError):
            pass
        else:
            break
        strf = f"waiting 1s for {path}..."
        if pkg:
            pkg.log(strf)
        else:
            logger.get().out(f"cbuild: {strf}")
        time.sleep(1)
    try:
        yield fd
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)

def repolock(arch):
    rpath = paths.repository()
    if not isinstance(arch, str):
        arch = arch.rparent.profile().arch
    return rpath / f"cbuild-{arch}.lock"
