from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class ForbiddenError(ErrorDetail):
    """
    Represents a Forbidden error. Default code is 403.

    Inherits from ErrorDetail class.
    """

    def __init__(self, title: Optional[str] = "Forbidden Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 403,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
