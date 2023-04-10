import asyncio
import inspect
from asyncio import AbstractEventLoop
from typing import Any, Coroutine, List

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


def get_num_of_function_parameters(func: callable) -> int:
    """
    Returns the number of parameters of a given function.

    :param func: The `func` is a function object for which we want to determine the number of parameters it
    takes
    :return: Returns the number of parameters that the function takes.
    """
    return len(inspect.signature(func).parameters)


def is_async(func: callable):
    """
    The function checks if a given function is a coroutine function

    :param func: func is a parameter that represents a function. If the function is a coroutine function
    :return: Returns a boolean value indicating whether the
    function is a coroutine function or not. If the argument is not a function, it returns `False`.
    """
    return asyncio.iscoroutinefunction(func) if func else False


def await_func(func: callable):
    """
    Checks if the result of a function is a coroutine and runs it using asyncio if it is.

    :param func: The parameter `func` is a function that will be called and its result will be checked if it is a coroutine
    or not. If it is a coroutine, it will be run using the asyncio event loop until it completes and its result will be
    returned. If it is not a coroutine, its result will be returned as is.
    :return: Returns the result of the input function `func`. If the result is an instance of
    `Coroutine`, it will be run using the `asyncio` event loop until it completes, and the final result will be returned.
    Otherwise, the original result will be returned.
    """
    result = func()
    if isinstance(result, Coroutine):
        return get_loop().run_until_complete(result)
    return result


def generate_error(errors: List[Any], num_of_try: int) -> ErrorDetail:
    """
    This function generates an error detail object with information about the number of attempts made, any errors
    encountered, and whether any of the errors were exceptions.

    :param errors: The list of errors that occurred during the operation.
    :type errors: List[Any]
    :param num_of_try: The number of attempts made to perform an operation
    :type num_of_try: int
    :return: an instance of the `ErrorDetail` class, which contains information about any errors that occurred during an
    operation. The `message` field contains a string describing the errors, the `exception` field contains the first
    exception encountered (if any), and the `more_data` field contains a list of any additional errors encountered.
    """
    errors = [] if errors is None else errors
    message = f"Operation failed with {num_of_try} attempts. "
    if len(errors) > 0:
        message += f"The details of the {len(errors)} errors are stored in the more_data field. "
        exception = next((error for error in errors if isinstance(error, Exception)), None)
        if exception is not None:
            message += "At least one of the errors was an exception type, " \
                       "the first exception being stored in the exception field."
        return ErrorDetail(message=message, exception=exception, more_data=errors)

    message += "There is no more information."
    return ErrorDetail(message=message)


def is_func_valid(func):
    """
    Checks if a given input is a valid callable function or not.

    :param func: The parameter `func` is expected to be a function object. The `is_func_valid` function checks if the `func`
    parameter is not `None` and is callable (i.e., it can be called as a function). If both conditions are true, it returns
    `True`
    :return: Returns a boolean value. It returns `True` if the input `func` is not `None` and
    is callable (i.e. can be called as a function), and `False` otherwise.
    """
    return func is not None and callable(func)


def get_loop() -> AbstractEventLoop:
    """
    This function returns the current event loop or creates a new one if none exists in the current thread.

    :return: Returns an instance of the `AbstractEventLoop` class, which is the event loop used by
    asyncio for scheduling and executing coroutines and callbacks. If there is already an event loop running in the current
    thread, it returns that event loop. Otherwise, it creates a new event loop, sets it as the current event loop for the
    thread, and returns it.
    """

    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        raise  # pragma: no cover
