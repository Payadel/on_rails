import inspect
from typing import Any, Optional

from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.Errors.ExceptionError import ExceptionError


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

    def on_success(self, func, *args, **kwargs):
        """
        If the result is a success, call the function with the given arguments

        :param func: The function to call
        :return: The result object is being returned.
        """
        if not self.success:
            return self
        return self._call_function(func, *args, **kwargs)

    def on_fail(self, func, *args, **kwargs):
        """
        If the result is not successful, call the function with the given arguments

        :param func: The function to call
        :return: The result object is being returned.
        """
        if self.success:
            return self
        return self._call_function(func, *args, **kwargs)

    def _call_function(self, func, *args, **kwargs):
        """
        If the function has no parameters, call it with no parameters. If the function has the same number of parameters as the number of arguments passed to the
        function, call it with the arguments. If the function has one more parameter than the number of arguments passed to
        the function, call it with the value of the Result as the first parameter and the arguments as the rest of the
        parameters

        :param func: The function to be called
        :return: A Result object
        """
        try:
            # Inputs
            num_of_inputs = len(args) + len(kwargs)
            function_sign = inspect.signature(func)
            num_of_function_params = len(function_sign.parameters)

            # Call function and get result
            if num_of_function_params == 0:
                result = func()
            elif num_of_function_params == num_of_inputs:
                result = func(*args, **kwargs)
            elif num_of_function_params == num_of_inputs + 1:
                result = func(self.value, *args, **kwargs)
            else:
                raise TypeError(
                    f"{func.__name__}() takes {num_of_function_params} positional arguments but {len(args)} were given")

            # Process result
            if isinstance(result, Result):
                return result
            if result is not None:
                return Result.ok(result)
            return self
        except Exception as e:
            return Result.fail(ExceptionError(message=str(e), exception=e))
