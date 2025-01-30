from typing import Dict, List, Callable, Coroutine, TypeVar
import asyncio

def runAsyncFunction(func,*args, **kwargs) -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(func(*args, **kwargs))
    
def runCallback(func, *args, **kwargs) -> None:
    if asyncio.iscoroutinefunction(func):
        runAsyncFunction(func, *args, **kwargs)
    else:
       func(*args, **kwargs)
