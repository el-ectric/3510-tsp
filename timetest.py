import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)


signal.alarm(TIMEOUT)    
try:
    foo()
except TimeoutException:
    print('function terminated')