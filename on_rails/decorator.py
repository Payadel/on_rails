from on_rails.Result import Result
from on_rails.ResultDetails.Errors.ExceptionError import ExceptionError


def def_result(func):
    """
    A decorator function that wraps the return value of a function with a `Result`
    object containing additional information such as success status and error messages.

    :arg: `func`: The function to wrap.
    :return: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        """
        It wraps a function and returns a Result object.
        :return: a Result object.
        """
        try:
            result_value = func(*args, **kwargs)
            if isinstance(result_value, Result):
                return result_value
            result = Result.ok(value=result_value)
        except Exception as e:
            result = Result.fail(detail=ExceptionError(message=str(e), exception=e))
        return result

    return wrapper
