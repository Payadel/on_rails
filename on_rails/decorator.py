from on_rails.Result import BreakFunctionException, try_func, try_func_async


def def_result(is_async: bool = False, num_of_try: int = 1, try_only_on_exceptions: bool = True):
    """
    A decorator that converts the output of a function into a Result type, and can handle both
    synchronous and asynchronous functions.
    This decorator wraps the function with `try-except` to handle all exceptions.
    Also, can be used to retry a function a specified number of times if it raises an exception or failed.

    :param is_async: A boolean flag indicating whether the decorated function is an asynchronous function or not. If set to
    True, the decorator will return an asynchronous wrapper function, defaults to False
    :type is_async: bool (optional)

    :param num_of_try: The number of times the decorated function should be retried if it fails, defaults to 1
    :type num_of_try: int (optional)

    :param try_only_on_exceptions: This parameter determines whether the function should only be retried if an exception is
    raised or for any error that occurs during operation. If set to True, the function will only be retried if an exception
    is raised. If set to False, the function will be retried for any error that occurs. defaults to True
    :type try_only_on_exceptions: bool (optional)
    """

    def inner_decorator(func: callable):
        def wrapper(*args, **kwargs):
            try:
                return try_func(lambda: func(*args, **kwargs),
                                num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
            except BreakFunctionException as e:
                return e.result

        async def wrapper_async(*args, **kwargs):
            try:
                return await try_func_async(lambda: func(*args, **kwargs),
                                            num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
            except BreakFunctionException as e:
                return e.result

        return wrapper_async if is_async else wrapper

    return inner_decorator
