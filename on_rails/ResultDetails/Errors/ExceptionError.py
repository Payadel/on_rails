from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.Errors.InternalError import InternalError


class ExceptionError(InternalError):
    """
    Represents an internal error caused by an exception. Default code is 500.

    Inherits from InternalError class.
    """

    def __init__(self, exception: Exception,
                 title: Optional[str] = "An exception occurred",
                 message: Optional[str] = None,
                 code: Optional[int] = 500,
                 errors: Optional[Dict[str, str]] = None,
                 more_data: Optional[List[Any]] = None):
        if not exception:
            raise ValueError("Exception must be provided")
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
