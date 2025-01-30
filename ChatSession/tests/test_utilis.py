import pytest
import pytest_asyncio
from .. import utilis


def test_async_Func():
   tmp = utilis.runAsyncFunction(aFunc, 2)
   assert tmp == 2
   
    
def test_async_callback():
    utilis.runCallback(aFunc, 2, v=2)
   
    
def test_callback():
   utilis.runCallback(callbackFunc, 4)
    
    
    
    
async def aFunc(t):
    return t
    
async def aCallbackFunc(t, v):
    assert t == v


def callbackFunc(t):
    assert t == 4
