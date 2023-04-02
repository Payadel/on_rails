from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class UnauthorizedError(ErrorDetail):
    """ An error that occurs when a user is not authorized to perform a certain action. Default code is 401.

    This error is a subclass of `ErrorDetail`, which provides additional details about the error.

    Inherits from ErrorDetail class.

    """

    def __init__(self, title: Optional[str] = "Unauthorized Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 401,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
