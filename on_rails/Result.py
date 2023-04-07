from typing import Any, Optional

from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.utility import (await_func, generate_error,
                              get_num_of_function_parameters)


class Result:
    """ Stores the result of a function.

    Attributes:
        success (bool): A flag indicating whether the result was successful.
        detail (ResultDetail, optional): The details of the result. Defaults to None.
        value (Any, optional): The value of the result. Defaults to None.
    """
    success: bool
    detail: Optional[ResultDetail] = None
    value: Optional[Any] = None

    def __init__(self, success: bool, detail: Optional[ResultDetail] = None, value: Optional[Any] = None):
        self.success = success
        self.detail = detail
        self.value = value

    @staticmethod
    def ok(value: Optional[Any] = None, detail: Optional[ResultDetail] = None):
        """
        Returns a successful result.

        :param value: The value to return if the result is ok
        :type value: Optional[Any]
        :param detail: Optional[ResultDetail] = None
        :type detail: Optional[ResultDetail]
        :return: A successful Result with the value. The detail and value are optional.
        """
        return Result(True, detail=detail, value=value)

    @staticmethod
    def fail(detail: Optional[ResultDetail] = None):
        """
        It returns a failed Result an optional detail

        :param detail: Optional[ResultDetail] = None
        :type detail: Optional[ResultDetail]
        :return: A failed Result object. The detail is optional.
        """
        return Result(False, detail)

    def code(self, default_success_code: int = 200, default_error_code: int = 500) -> int:
        """
        If the detail has a code, return that, otherwise return the default success code if the status is successful,
        otherwise return the default error code

        :param default_success_code: The default status code to return if the Result is successful, defaults to 200
        :type default_success_code: int (optional)
        :param default_error_code: The default error code to return if the Result is not successful, defaults to 500
        :type default_error_code: int (optional)
        :return: int
        """
        if self.detail and self.detail.code:
            return self.detail.code
        return default_success_code if self.success else default_error_code

    def __str__(self) -> str:
        result = f"success: {self.success}\n"
        if self.value:
            result += f"Value: {self.value}\n"
        if self.detail:
            result += f"Detail:\n{self.detail}\n"
        return result

    def on_success(self, func: callable, num_of_try: int = 1, try_only_on_exceptions=True):
        """
        This function executes a given function only if the previous attempts were successful.

        :param func: func is a function that will be executed if the previous operation was successful.
        :param num_of_try: num_of_try is an optional parameter that specifies the number of times the function should be
        tried in case of failure. If the function fails on the first try, it will be retried num_of_try times. If num_of_try
        is not specified, the function will only be tried once, defaults to 1 (optional)

        :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
        exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
        function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
        :type try_only_on_exceptions: bool (optional)

        :return: The method `on_success` returns either self or the result of given function.
        """
        if not self.success:
            return self
        return self.try_func(func, num_of_try, try_only_on_exceptions)

    def on_fail(self, func: callable, num_of_try: int = 1, try_only_on_exceptions=True):
        """
        If the result is not successful, call the function with the given arguments

        :param func: The function to call

        :param num_of_try: num_of_try is an optional parameter that specifies the number of times the function should be
        tried in case of failure. If the function fails on the first try, it will be retried num_of_try times. If num_of_try
        is not specified, the function will only be tried once, defaults to 1 (optional)

        :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
        exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
        function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
        :type try_only_on_exceptions: bool (optional)

        :return: The result object is being returned.
        """
        if self.success:
            return self
        return self.try_func(func, num_of_try, ignore_previous_error=True, try_only_on_exceptions=try_only_on_exceptions)

    def fail_when(self, condition: bool, error_detail: Optional[ErrorDetail] = None, add_prev_detail: bool = False):
        """
        If the condition is true, return a failure result with the given error detail

        :param condition: The condition to check. If it's True, the Result will be a failure
        :type condition: bool
        :param error_detail: This is the error detail that will be returned if the condition is true
        :type error_detail: Optional[ErrorDetail]
        :param add_prev_detail: If True, the previous error detail will be added to the new error detail, defaults to False
        :type add_prev_detail: bool (optional)
        :return: Result object
        """
        if not condition:
            return self

        error_detail = error_detail if error_detail else ErrorDetail()
        if add_prev_detail:
            error_detail.add_more_data({"prev_detail": self.detail})
        return Result.fail(error_detail)

    @staticmethod
    def convert_to_result(output: Any, none_means_success: bool = True):
        """
        The function converts a given output to a Result object, where None can indicate success or failure depending on the
        value of a boolean parameter.

        :param output: The output parameter is of type Any, which means it can be any Python object
        :type output: Any
        :param none_means_success: A boolean parameter that determines whether a `None` output should be considered a
        success or a failure. If `none_means_success` is `True`, then a `None` output will be considered a success and the
        function will return a `Result.ok()` instance. If `none_means_success` is, defaults to True
        :type none_means_success: bool (optional)
        :return: The function `convert_to_result` returns a `Result` object. If the `output` parameter is `None`, it returns
        a `Result` object with a success status if `none_means_success` is `True`, otherwise it returns a `Result` object
        with a failure status. If the `output` parameter is already a `Result` object, it returns it as is. Otherwise,
        """
        if output is None:
            return Result.ok() if none_means_success else Result.fail()
        if isinstance(output, Result):
            return output
        return Result.ok(output)

    def try_func(self, func: callable, num_of_try: int = 1,
                 ignore_previous_error: bool = False, try_only_on_exceptions: bool = True):
        """
        The function `try_func` attempts to execute a given function with a specified number of tries and handles errors.

        :param func: `func` is a function object that will be executed by the `try_func` method. It is the main parameter of
        the method and must be provided for the method to work
        :param num_of_try: The number of times the function should be attempted before returning a failure result. The
        default value is 1, meaning the function will be attempted once, defaults to 1 (optional)
        :param ignore_previous_error: By default, if the previous function fails, the Result is
         passed as a parameter to the new function. That is, the new function must accept
         1 parameter. If skip_previous_error is True, the new function can be with or without parameters.
        :type ignore_previous_error: bool (optional)
        the error.

    :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
    exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
    function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
    :type try_only_on_exceptions: bool (optional)

    :return: a `Result` object.
        :return: an instance of the `Result` class, which contains either a successful result or an error message.
        """
        if func is None:
            return Result.fail(ErrorDetail(message="The input function can not be None."))

        num_of_function_params = get_num_of_function_parameters(func)

        if num_of_function_params == 0:
            if self.success or ignore_previous_error:
                return try_func(func, num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
            return Result.fail(ErrorDetail(
                message="The previous function failed. "
                        "The new function does not have a parameter to get the previous result. "
                        "Either define a function that accepts a parameter or set skip_previous_error to True."))
        if num_of_function_params == 1:
            return try_func(lambda: func(self), num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
        return Result.fail(ErrorDetail(
            message=f"{func.__name__}() takes {num_of_function_params} arguments. It cannot be executed."))


def try_func(func: callable, num_of_try: int = 1, try_only_on_exceptions: bool = True) -> Result:
    """
    The function `try_func` attempts to execute a given function with a specified number of tries and handles errors.

    :param func: The input function that needs to be executed
    :param num_of_try: The number of times the input function will be attempted to execute in case of failure. The default
    value is 1, meaning the function will be executed only once by default, defaults to 1 (optional)
    :return: a `Result` object. The `Result` object can either be a successful result or a failed result with an
    `ErrorDetail` object containing information about the error.

    :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
    exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
    function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
    :type try_only_on_exceptions: bool (optional)
    :return: a `Result` object.
    """
    if func is None:
        return Result.fail(ErrorDetail(message="The input function can not be None."))

    num_of_function_params = get_num_of_function_parameters(func)
    if num_of_function_params > 0:
        return Result.fail(ErrorDetail(
            message=f"{func.__name__}() takes {num_of_function_params} arguments. It cannot be executed."))

    errors = []
    for _ in range(num_of_try):
        try:
            result = await_func(func)
            result = Result.convert_to_result(result)
            if result.success or try_only_on_exceptions:
                return result
            if result.detail:
                errors.append(result.detail)
        except Exception as e:
            errors.append(e)

    error_detail = generate_error(errors, num_of_try)
    return Result.fail(error_detail)
