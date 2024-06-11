from typing import Dict, List, Callable, Coroutine
import asyncio

def runAsyncFunction(func: Coroutine ,*args, **kwargs) -> any:
    try:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    except Exception as e:
        print(f"_runAsyncFunction Error: {e.args}")
        return None
    
def runCallback(func: Callable, *args, **kwargs) -> None:
    if asyncio.iscoroutinefunction(func):
        runAsyncFunction(func, *args, **kwargs)
    else:
        func(*args, **kwargs)