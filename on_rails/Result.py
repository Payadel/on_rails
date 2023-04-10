from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

from on_rails._utility import (await_func, generate_error,
                               get_num_of_function_parameters, is_func_valid)
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.ResultDetails.Errors.ValidationError import ValidationError
from on_rails.ResultDetails.SuccessDetail import SuccessDetail

T = TypeVar('T')


class Result(Generic[T]):
    """ Stores the result of a function.

    Attributes:
        success (bool): A flag indicating whether the result was successful.
        detail (ResultDetail, optional): The details of the result. Defaults to None.
        value (T, optional): The value of the result. Defaults to None.
    """

    success: bool
    detail: Optional[ResultDetail] = None
    value: Optional[T] = None

    def __init__(self, success: bool, detail: Optional[ResultDetail] = None, value: Optional[T] = None):
        self.success = success
        self.detail = detail
        self.value = value

    def __str__(self) -> str:
        result = f"success: {self.success}\n"
        if self.value:
            result += f"Value: {self.value}\n"
        if self.detail:
            result += f"Detail:\n{self.detail}\n"
        return result

    # region Static Methods

    @staticmethod
    def ok(value: Optional[T] = None, detail: Optional[ResultDetail] = None):
        """
        Returns a successful result.

        :param value: The value to return if the result is ok
        :type value: Optional[T]
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

    @staticmethod
    def convert_to_result(value: Any, none_means_success: bool = True):
        """
        The function converts a given output to a Result object, where None can indicate success or failure depending on the
        value of a boolean parameter.

        :param value: The output parameter is of type Any, which means it can be any Python object
        :type value: Any
        :param none_means_success: A boolean parameter that determines whether a `None` output should be considered a
        success or a failure. If `none_means_success` is `True`, then a `None` output will be considered a success and the
        function will return a `Result.ok()` instance. If `none_means_success` is, defaults to True
        :type none_means_success: bool (optional)
        :return: The function `convert_to_result` returns a `Result` object. If the `output` parameter is `None`, it returns
        a `Result` object with a success status if `none_means_success` is `True`, otherwise it returns a `Result` object
        with a failure status. If the `output` parameter is already a `Result` object, it returns it as is. Otherwise,
        """
        if value is None:
            return Result.ok() if none_means_success else Result.fail()
        if isinstance(value, Result):
            return value
        return Result.ok(value)

    # endregion

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

    # region on_success

    def on_success(self, func: Callable, num_of_try: int = 1, try_only_on_exceptions=True):
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

        return self.__call_func(func, optional_args=[self.value, self],
                                num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)

    def on_success_add_more_data(self, object_or_func: Union[Any, Callable], ignore_errors: bool = False):
        """
        This function adds more data to a success response object.

        :param object_or_func: The parameter `object_or_fuc` can be either an object or a function.
        If it is a function, it will be called with `self.value` and `self` as optional arguments.
        Then if operation was successful, result of function will be added to more_data field. Otherwise, the error details are returned.
        If it is an object, it will be added to the `SuccessDetail` object
        :type object_or_func: Any or Callable

        :param ignore_errors: `ignore_error` is a boolean parameter that determines whether or not to ignore any errors that occur during the execution of the function. If `ignore_error` is set to `True`,
        any errors that occur will be ignored. If `ignore_error` is set to False, any errors that occur during the execution of the function will be returned.
        :type ignore_errors: bool (optional)
        """
        if not self.success or object_or_func is None:
            return self

        if callable(object_or_func):
            result = self.__call_func(object_or_func, optional_args=[self.value, self])
            if not result.success:
                return self if ignore_errors else result
            obj = result.value
        else:
            obj = object_or_func

        if not self.detail:
            self.detail = SuccessDetail()

        result = try_func(lambda: self.detail.add_more_data(obj))
        if result.success or ignore_errors:
            return self
        return result  # pragma: no cover

    def on_success_new_detail(self, new_detail_or_func: Union[SuccessDetail, Callable]):
        """
        This function updates the success detail of a result object with either a new detail or the result of a callable
        function.

        :param new_detail_or_func: The parameter `new_detail_or_func` can either be an instance of `SuccessDetail` or a
        callable function that takes two optional arguments: `previous.value` and `previous result`.
        If it is a callable function, it will be called with these arguments and the result will be used as the new detail
        :type new_detail_or_func: Union[SuccessDetail, Callable]
        """

        if not self.success:
            return self

        new_detail = None
        if callable(new_detail_or_func):
            result = self.__call_func(new_detail_or_func, optional_args=[self.value, self])
            if not result.success:
                return result
            new_detail = result.value
        else:
            new_detail = new_detail_or_func

        if new_detail is not None and not isinstance(new_detail, SuccessDetail):
            return Result.fail(
                ErrorDetail(message=f"Type of new detail '{type(new_detail).__name__}' "
                                    "is not instance of 'SuccessDetail'"))
        self.detail = new_detail
        return self

    def on_success_tee(self, func: Callable, num_of_try: int = 1, try_only_on_exceptions=True,
                       ignore_errors: bool = False):
        """
        This function executes a given function and returns the previous result if successful, or the result of the given
        function if it fails.

        :param func: The function that will be executed
        :type func: Callable

        :param num_of_try: The number of times the function should be attempted if it fails, defaults to 1
        :type num_of_try: int (optional)

        :param try_only_on_exceptions: If set to True, the function will only be tried if an exception is raised,
        otherwise it also will try if the result is not success, defaults to True

        :param ignore_errors: If it is false, it will return the error result when the result of the function fails, otherwise it will be ignored.
        :type ignore_errors: bool (optional)
        """
        result = self.on_success(func, num_of_try, try_only_on_exceptions)
        if result.success or ignore_errors:
            return self  # ignore result
        return result

    def on_success_operate_when(self, condition_or_func: Union[Callable, bool], func: Callable,
                                num_of_try: int = 1, try_only_on_exceptions=True, break_rails: bool = False):
        """
        This function operates a given function when a specified condition is met and the previous operation was successful.

        :param condition_or_func: The condition or function that needs to be checked before calling the main function. It
        can be either a boolean value or a callable function that returns a boolean value
        :type condition_or_func: Union[Callable, bool]

        :param func: `func` is a callable object (function, method, lambda function, etc.) that will be executed if the
        `condition_or_func` parameter evaluates to `True`.
        The `self` parameter is passed as the first argument to `func` optionally.
        :type func: Callable

        :param num_of_try: The `num_of_try` parameter is an optional integer parameter that specifies the number of times to
        try executing the function `func` if it fails due to an exception. If `num_of_try` is not specified, the function
        will only be executed once, defaults to 1
        :type num_of_try: int (optional)

        :param try_only_on_exceptions: `try_only_on_exceptions` is a boolean parameter that determines whether the `func`
        should only be retried if an exception is raised or not.

        :param break_rails: If `condition_or_func` is passed, break the chain of functions or not? Defaults to `False`
        :type break_rails: bool (optional)

        :return: If condition pass, returns result of function as Result object.
        If condition not pass, returns previous Result object.
        """
        if not self.success:
            return self
        return self.__operate_when(condition_or_func, func, [self.value, self],
                                   num_of_try, try_only_on_exceptions, break_rails)

    def on_success_break(self, condition_or_func: Union[Callable, bool]):
        """
        The function raises a BreakRails exception if a given condition is true.

        :param condition_or_func: The parameter `condition_or_func` can be either a callable function or a boolean value.
        It is used to determine whether to break chaining of functions or not. If it is a callable function, it
        will be called with two optional arguments: the value and the result of the previous operation.
        :type condition_or_func: Union[Callable, bool]

        :return: If `condition_or_func` is callable function and fails, it returns error result.
        Otherwise, raise BreakRails exception

        :raise BreakRails
        """
        if not self.success:
            return self

        result = self.__is_condition_pass(condition_or_func, [self.value, self])
        if not result.success:
            return result  # return error result
        if not result.value:  # The condition is not true
            return self

        self.__break_rails()
        return Result.fail(ErrorDetail(message="The BreakRails exception not raised."))  # pragma: no cover

    def on_success_fail_when(self, condition_or_func: Union[Callable, bool],
                             error_detail: Optional[ErrorDetail] = None):
        """
        If the previous result is successful and condition is true, return a failure result with the given error detail

        :param condition_or_func: The condition or function that needs to be checked before calling the main function. It
        can be either a boolean value or a callable function that returns a boolean value
        :type condition_or_func: Union[Callable, bool]

        :param error_detail: This is the error detail that will be returned if the condition is true
        :type error_detail: Optional[ErrorDetail]
        """

        return self.on_success_operate_when(condition_or_func, lambda: self.__fail_when(error_detail))

    # endregion

    # region on_fail

    def on_fail(self, func: Callable, num_of_try: int = 1, try_only_on_exceptions=True):
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
        if not is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))
        if self.success:
            return self
        return self.try_func(func, num_of_try, ignore_previous_error=True,
                             try_only_on_exceptions=try_only_on_exceptions)

    def on_fail_add_more_data(self, object_or_func: Union[Any, Callable], ignore_errors: bool = False):
        """
        This function adds more data to an error detail object, and returns the original object or a new one
        with the added data.

        :param object_or_func: The parameter `object_or_fuc` can be either an object or a function.
        If it is a function, it will be called with `self` as optional arguments.
        Then if operation was successful, result of function will be added to more_data field. Otherwise, the error details are returned.
        If `object_or_fuc` is an object, it will be added to the `ErrorDetail` object
        :type object_or_func: Any or Callable

        :param ignore_errors: `ignore_error` is a boolean parameter that determines whether or not to ignore any errors that occur during the execution of the function. If `ignore_error` is set to `True`,
        any errors that occur will be ignored. If `ignore_error` is set to False, any errors that occur during the execution of the function will be returned.
        :type ignore_errors: bool (optional)
        """
        if self.success or object_or_func is None:
            return self

        if callable(object_or_func):
            result = self.__call_func(object_or_func, optional_args=[self])
            if not result.success:
                return self if ignore_errors else result
            obj = result.value
        else:
            obj = object_or_func

        if not self.detail:
            self.detail = ErrorDetail()

        result = try_func(lambda: self.detail.add_more_data(obj))
        if result.success or ignore_errors:
            return self

        result.detail.add_more_data(f"previous error: {self.detail}")  # pragma: no cover
        return result  # pragma: no cover

    def on_fail_new_detail(self, new_detail_or_func: Union[ErrorDetail, Callable]):
        """
        This function updates the error detail of a result object with either a new detail or the result of a callable
        function.

        :param new_detail_or_func: The parameter `new_detail_or_func` can either be an instance of `ErrorDetail` or a
        callable function that takes `previous result` as optional argument.
        If it is a callable function, it will be called with these arguments and the result will be used as the new detail
        :type new_detail_or_func: Union[ErrorDetail, Callable]
        """

        if self.success:
            return self

        if callable(new_detail_or_func):
            result = self.__call_func(new_detail_or_func, optional_args=[self])
            if not result.success:
                return result
            new_detail = result.value
        else:
            new_detail = new_detail_or_func

        if new_detail is not None and not isinstance(new_detail, ErrorDetail):
            return Result.fail(
                ErrorDetail(message=f"Type of new detail '{type(new_detail).__name__}' "
                                    f"is not instance of '{ErrorDetail.__name__}'."))
        self.detail = new_detail
        return self

    def on_fail_tee(self, func: Callable, num_of_try: int = 1, try_only_on_exceptions=True,
                    ignore_errors: bool = False):
        """
        This function executes a given function only if the previous operation was not successful and returns the original
        object. the function result will be ignored.

        :param func: func is a Callable object, which means it is a function or a method that can be called. It is the
        function that will be executed if the previous operation was not successful
        :type func: Callable
        :param num_of_try: The parameter `num_of_try` is an integer that specifies the number of times the `func` should be
        tried in case of failure. If `num_of_try` is not specified, it defaults to 1
        :type num_of_try: int (optional)
        :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
        exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
        function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
        :type try_only_on_exceptions: bool (optional)
        :param ignore_errors: If it is false, it will return the error result when the result of the function fails, otherwise it will be ignored.
        :return: an instance of the class that it belongs to (presumably named `self`).
        """
        result = self.on_fail(func, num_of_try, try_only_on_exceptions)
        if result.success or ignore_errors:
            return self  # ignore result
        return result

    def on_fail_raise_exception(self, exception_type: Optional[type] = None):
        """
        Request to raise the exception when the previous function failed.

        :param exception_type: The `exception_type` parameter is an optional argument that specifies the type of exception
        to be raised if the previous function fails. If this parameter is not provided, a generic `Exception` will be raised.
        If it is provided, the specified exception type will be raised.
        :type exception_type: Optional[type]
        :return: Returns self or raise Exception
        """
        if self.success:
            return self
        detail = self.detail if self.detail else ""
        if exception_type:
            raise exception_type(str(detail))
        raise Exception(str(detail))

    def on_fail_operate_when(self, condition_or_func: Union[Callable, bool], func: Callable,
                             num_of_try: int = 1, try_only_on_exceptions=True, break_rails: bool = False):
        """
        This function operates a given function when a specified condition is met and the previous operation was not successful.

        :param condition_or_func: The condition or function that needs to be checked before calling the main function. It
        can be either a boolean value or a callable function that returns a boolean value
        :type condition_or_func: Union[Callable, bool]

        :param func: `func` is a callable object (function, method, lambda function, etc.) that will be executed if the
        `condition_or_func` parameter evaluates to `True`.
        The `self` parameter is passed as the first argument to `func` optionally.
        :type func: Callable

        :param num_of_try: The `num_of_try` parameter is an optional integer parameter that specifies the number of times to
        try executing the function `func` if it fails due to an exception. If `num_of_try` is not specified, the function
        will only be executed once, defaults to 1
        :type num_of_try: int (optional)

        :param try_only_on_exceptions: `try_only_on_exceptions` is a boolean parameter that determines whether the `func`
        should only be retried if an exception is raised or not.

        :param break_rails: If `condition_or_func` is passed, break the chain of functions or not? Defaults to `False`
        :type break_rails: bool (optional)

        :return: If condition pass, returns result of function as Result object.
        If condition not pass, returns previous Result object.
        """

        if self.success:
            return self
        return self.__operate_when(condition_or_func, func, [self],
                                   num_of_try, try_only_on_exceptions, break_rails)

    def on_fail_break(self, condition_or_func: Union[Callable, bool]):
        """
        The function raises a BreakRails exception if a given condition is true.

        :param condition_or_func: The parameter `condition_or_func` can be either a callable function or a boolean value.
        It is used to determine whether to break chaining of functions or not. If it is a callable function, it
        will be called with two optional arguments: the value and the result of the previous operation.
        :type condition_or_func: Union[Callable, bool]

        :return: If `condition_or_func` is callable function and fails, it returns error result.
        Otherwise, raise BreakRails exception

        :raise BreakRails
        """
        if self.success:
            return self

        return self.break_rails(condition_or_func)

    # endregion

    def fail_when(self, condition_or_func: Union[Callable, bool],
                  error_detail: Optional[ErrorDetail] = None, add_prev_detail: bool = False):
        """
        If the condition is true, return a failure result with the given error detail

        :param condition_or_func: The condition or function that needs to be checked before calling the main function. It
        can be either a boolean value or a callable function that returns a boolean value
        :type condition_or_func: Union[Callable, bool]

        :param error_detail: This is the error detail that will be returned if the condition is true
        :type error_detail: Optional[ErrorDetail]
        :param add_prev_detail: If True, the previous error detail will be added to the new error detail, defaults to False
        :type add_prev_detail: bool (optional)
        :return: Result object
        """

        return self.operate_when(condition_or_func, lambda: self.__fail_when(error_detail, add_prev_detail))

    def __fail_when(self, error_detail: Optional[ErrorDetail] = None, add_prev_detail: bool = False):
        error_detail = error_detail if error_detail else ErrorDetail()

        if add_prev_detail and self.detail:
            error_detail.add_more_data({"prev_detail": self.detail})

        return Result.fail(error_detail)

    def operate_when(self, condition_or_func: Union[Callable, bool], func: Callable,
                     num_of_try: int = 1, try_only_on_exceptions=True, break_rails: bool = False):
        """
        This function takes a condition or function, and if it passes, it calls another function

        :param condition_or_func: The condition or function that needs to be checked before calling the main function. It
        can be either a boolean value or a callable function that returns a boolean value
        :type condition_or_func: Union[Callable, bool]

        :param func: `func` is a callable object (function, method, lambda function, etc.) that will be executed if the
        `condition_or_func` parameter evaluates to `True`.
        The `self` parameter is passed as the first argument to `func` optionally.
        :type func: Callable

        :param num_of_try: The `num_of_try` parameter is an optional integer parameter that specifies the number of times to
        try executing the function `func` if it fails due to an exception. If `num_of_try` is not specified, the function
        will only be executed once, defaults to 1
        :type num_of_try: int (optional)

        :param try_only_on_exceptions: `try_only_on_exceptions` is a boolean parameter that determines whether the `func`
        should only be retried if an exception is raised or not.

        :param break_rails: If `condition_or_func` is passed, break the chain of functions or not? Defaults to `False`
        :type break_rails: bool (optional)

        :return: If condition pass, returns result of function as Result object.
        If condition not pass, returns previous Result object.
        """

        return self.__operate_when(condition_or_func=condition_or_func,
                                   func=func, optional_args=[self],
                                   num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions,
                                   break_rails=break_rails)

    def try_func(self, func: Callable, num_of_try: int = 1,
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
        if not is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))

        num_of_function_params = get_num_of_function_parameters(func)

        if num_of_function_params == 0:
            if self.success or ignore_previous_error:
                return try_func(func, num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
            return Result.fail(ValidationError(
                message="The previous function failed. "
                        "The new function does not have a parameter to get the previous result. "
                        "Either define a function that accepts a parameter or set skip_previous_error to True."))
        if num_of_function_params == 1:
            return try_func(lambda: func(self), num_of_try=num_of_try, try_only_on_exceptions=try_only_on_exceptions)
        return Result.fail(ValidationError(
            message=f"{func.__name__}() takes {num_of_function_params} arguments. It cannot be executed."))

    def finally_tee(self, func: Callable, num_of_try: int = 1, try_only_on_exceptions: bool = True):
        """
        Whether the previous operation was successful or not, this function is executed.
        If the `func` result is successful, the previous result will be returned.
        But if it fails, the result of the function will be returned as Result.

        :param func: func is a parameter that expects a callable function as input. This function will be called by the
        finally_tee method
        :type func: Callable

        :param num_of_try: The parameter "num_of_try" is an integer that specifies the number of times the function should
        try to execute the given function "func". If the function execution fails, it will retry the execution for the
        specified number of times. The default value of this parameter is 1
        :type num_of_try: int (optional)

        :param try_only_on_exceptions: `try_only_on_exceptions` is a boolean parameter that determines whether the `func`
        should only be retried if an exception is raised or not.
        """
        result = self.__call_func(func, [self], num_of_try, try_only_on_exceptions)
        if result.success:
            return self
        return result

    def break_rails(self, condition_or_func: Union[Callable, bool]):
        """
        The function raises a BreakRails exception if a given condition is true.

        :param condition_or_func: The parameter `condition_or_func` can be either a callable function or a boolean value.
        It is used to determine whether to break chaining of functions or not. If it is a callable function, it
        will be called with previous result as optional parameter.
        :type condition_or_func: Union[Callable, bool]

        :return: If `condition_or_func` is callable function and fails, it returns error result.
        Otherwise, raise BreakRails exception

        :raise BreakRails
        """
        result = self.__is_condition_pass(condition_or_func, [self])
        if not result.success:
            return result  # return error result
        if not result.value:  # The condition is not true
            return self

        self.__break_rails()
        return Result.fail(ErrorDetail(message="The BreakRails exception not raised."))  # pragma: no cover

    # region private methods

    @staticmethod
    def __call_func(func: callable, optional_args: List[Any] = None,
                    num_of_try: int = 1, try_only_on_exceptions: bool = False):
        if not is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))

        optional_args = optional_args if optional_args else []
        num_of_function_params = get_num_of_function_parameters(func)
        if num_of_function_params > len(optional_args):
            return Result.fail(ValidationError(
                message=f"{func.__name__}() takes {num_of_function_params} arguments. It cannot be executed. "
                        f"maximum of {len(optional_args)} parameters is acceptable."))

        return try_func(lambda: func(*optional_args[:num_of_function_params]), num_of_try, try_only_on_exceptions)

    def __is_condition_pass(self, condition_or_func: Union[Callable, bool],
                            optional_args: List[Any] = None,
                            num_of_try: int = 1, try_only_on_exceptions: bool = True):
        """
        This function checks if a given condition or function is true or false and returns a result accordingly.
        If `condition_or_func` is a boolean value, it returns condition.
        If `condition_or_func` is a callable function, it calls the function, then if function fails, returns error result,
        otherwise checks the value of result function. if it exists and be boolean value, it returns value,
        otherwise returns True.
        """

        if isinstance(condition_or_func, bool):
            return Result.ok(condition_or_func)

        if not callable(condition_or_func):
            return Result.fail(ValidationError(message=f"The condition only can be a function or a boolean. "
                                                       f"{type(condition_or_func).__name__} is not acceptable."))

        result = self.__call_func(condition_or_func, optional_args, num_of_try, try_only_on_exceptions)
        if not result.success:
            return result
        if result.value is not None and isinstance(result.value, bool):
            return Result.ok(result.value)
        return Result.ok(True)

    def __operate_when(self, condition_or_func: Union[Callable, bool],
                       func: Callable, optional_args: List[Any] = None,
                       num_of_try: int = 1, try_only_on_exceptions=True, break_rails: bool = False):
        result = self.__is_condition_pass(condition_or_func, optional_args, num_of_try, try_only_on_exceptions)
        if not result.success:
            return result  # Return error result
        if not result.value:  # The condition is not true
            return self
        return self.__call_func(func, optional_args, num_of_try, try_only_on_exceptions) \
            .break_rails(break_rails)

    def __break_rails(self):
        raise BreakRailsException(result=self)

    # endregion


def try_func(func: Callable, num_of_try: int = 1, try_only_on_exceptions: bool = True) -> Result:
    """
    The function `try_func` attempts to execute a given function with a specified number of tries and handles errors.

    :param func: The input function that needs to be executed
    :param num_of_try: The number of times the input function will be attempted to execute in case of failure. The default
    value is 1, meaning the function will be executed only once by default, defaults to 1 (optional)
    :return: a `Result` object. The `Result` object can either be a successful result or a failed result with an
    `ValidationError` object containing information about the error.

    :param try_only_on_exceptions: A boolean parameter that determines whether the function should only be retried if an
    exception is raised. If set to True, the function will only be retried if an exception is raised. If set to False, the
    function will be retried regardless of whether an exception is raised or Result is not success, defaults to True
    :type try_only_on_exceptions: bool (optional)
    :return: a `Result` object.
    """
    if not is_func_valid(func):
        return Result.fail(ValidationError(message="The input function is not valid."))

    num_of_function_params = get_num_of_function_parameters(func)
    if num_of_function_params > 0:
        return Result.fail(ValidationError(
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


# The class `BreakRails` defines an exception that takes a `Result` object as input.
class BreakRailsException(Exception):
    """
    An exception for break fast chaining of functions.
    It stores the last result.
    """
    result: Result

    def __init__(self, result: Result):
        """
        This function initializes an object with a non-null and valid instance of the Result class.

        :param result: The `result` parameter is an instance of the `Result` class. The constructor checks if
        the `result` parameter is not `None` and is an instance of the `Result` class
        :type result: Result
        """
        super().__init__()
        if result is None:
            raise ValueError("The result cannot be None")
        if not isinstance(result, Result):
            raise ValueError("The result must be an instance of Result")
        self.result = result
