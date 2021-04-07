import os
from multiprocessing import Process
import psutil


def detachify(func):
    """Decorate a function so that its calls are async in a detached process.

    Usage
    -----

    .. code::
            import time

            @detachify
            def f(message):
                time.sleep(5)
                print(message)

            f('Async and detached!!!')
    """
    # Taken from: https://stackoverflow.com/a/58071119/1274908

    # create a process fork and run the function
    def forkify(*args, **kwargs):
        if os.fork() != 0:
            return
        func(*args, **kwargs)

    # wrapper to run the forkified function
    def wrapper(*args, **kwargs):
        proc = Process(target=lambda: forkify(*args, **kwargs))
        proc.start()
        proc.join()
        return

    return wrapper


def is_process_running(process_name: str):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Taken from: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
