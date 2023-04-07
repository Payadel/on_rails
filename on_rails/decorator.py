from typing import Coroutine

from on_rails._utility import await_func
from on_rails.Result import Result
from on_rails.ResultDetails.Errors.ExceptionError import ExceptionError


def def_result(is_async: bool = False):
    """
    A decorator that converts the output of a function into a Result, and can handle both
    synchronous and asynchronous functions.

    :param is_async: A boolean parameter that indicates whether the decorated function is an asynchronous function or not.
    If it is set to True, the decorator will return an asynchronous wrapper function that can be used with the asyncio
    library, defaults to False
    :type is_async: bool (optional)
    :return: The function `def_result` returns the inner decorator function `inner_decorator`.
    """

    def inner_decorator(func: callable):
        def wrapper(*args, **kwargs):
            try:
                result = await_func(lambda: func(*args, **kwargs))
                return Result.convert_to_result(result)
            except Exception as e:
                return Result.fail(detail=ExceptionError(message=str(e), exception=e))

        async def wrapper_async(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if isinstance(result, Coroutine):
                    result = await result
                return Result.convert_to_result(result)
            except Exception as e:
                return Result.fail(detail=ExceptionError(message=str(e), exception=e))

        return wrapper_async if is_async else wrapper

    return inner_decorator
