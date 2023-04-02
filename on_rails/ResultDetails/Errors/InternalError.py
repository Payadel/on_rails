from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class InternalError(ErrorDetail):
    """
    Represents an internal error. Default code is 500.

    Inherits from ErrorDetail class.
    """

    def __init__(self, title: Optional[str] = "Internal Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 500,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
