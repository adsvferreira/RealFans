import os
import sys
import signal
import psutil
import contextlib
from typing import NoReturn


def kill_process(pid: int):
    with contextlib.suppress(Exception):
        os.kill(pid, signal.SIGTERM)


def kill_process_and_children(pid: int):
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return

    children_processes = parent.children(recursive=True)
    for children in children_processes:
        kill_process(children.pid)
    kill_process(pid)


def cleanup_server() -> NoReturn:
    current_pid = os.getpid()
    try:
        kill_process_and_children(current_pid)
    finally:
        # in case it failed? idk. gg.
        sys.exit(0)
