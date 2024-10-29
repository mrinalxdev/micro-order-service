import functools
import inspect
import logging
import socket
import time
from contextlib import ContextManager
from datetime import datetime
from typing import Any, Callable, ContextManager, Dict, Type, Union

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger('callio')

class Timer:
    """Utility class for measuring execution time"""
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start the timer"""
        self.start_time = time.perf_counter()
        return self
    
    def stop(self):
        """Stop the Timer"""
        self.end_time = time.perf_counter()
        return self.elapsed

    @property
    def elapsed(self) -> float:
        """Return elapsed time in seconds"""
        if self.start_time is None:
            raise ValueError("Timer not started")
        end_time = self.end_time if self.end_time is not None else time.perf_counter()
        return end_time - self.start_time


@ContextManager
def timing_context(operation_name : str):
    """Context manager for timing operations"""
    timer = Timer().start()
    try:
        yield timer 
    finally:
        elapsed = timer.stop()
        logger.info(f"{operation_name} took {elapsed:.4f} seconds")

def validate_port(port : int) -> bool:
    """Validate if a port number is valid"""
    return isinstance(port, int) and 0 < port < 65536

def retry(max_attempts : int = 3, delay : float = 1.0):
    """Decorator for retrying operations with expotential backoff"""
    def decorator(func : Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try : 
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = delay * (2 ** attempt)
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {sleep_time:.2f}s...")
                        time.sleep(sleep_time)
            raise last_exception
        raise wrapper
    raise decorator

class RPCStats:
    """Class for tracking rpc statistics"""
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_time = 0.0
        self.__start_times: Dict[str, float] = {}
    
    def start_call(self, call_id : str):
        """Start timing a call"""
        self.__start_times[call_id] = time.perf_counter()
    
    def end_call(self, call_id : str, success : bool):
        """End timing a call and update statistics"""
        if call_id in self.__start_times:
            elapsed = time.perf_counter() - self.__start_times[call_id]
            self.total_calls += 1
            self.total_time += elapsed
            if success:
                self.successful_calls += 1
            else:
                self.failed_calls += 1
            del self.__start_times[call_id]
        
    @property
    def average_time(self) -> float:
        """Calculate average call time"""
        return self.total_time / self.total_calls if self.total_calls > 0 else 0.0

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        return (self.successful_calls / self.total_calls * 100) if self.total_calls > 0 else 0.0

    def __str__(self) -> str:
        return (
            f"RPC Stats : {self.total_calls} total calls, "
            f"{self.success_rate:.1f}% success rate,"
            f"{self.average_time*1000:.2f}ms average time"
        )
