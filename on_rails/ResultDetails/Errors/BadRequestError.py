from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class BadRequestError(ErrorDetail):
    """
    Represents a bad request error. Default code is 400.

    This error occurs when the request is invalid or improperly formatted.

    Inherits from ErrorDetail class.
    """

    def __init__(self, title: Optional[str] = "BadRequest Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 400,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
