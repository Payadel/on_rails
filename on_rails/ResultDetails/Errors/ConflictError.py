from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class ConflictError(ErrorDetail):
    """
      Represents a conflict error. Default code is 409.

      This error occurs when an operation cannot be completed due to conflicting data.

      Inherits from ErrorDetail class.
      """

    def __init__(self, title: Optional[str] = "Conflict Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 409,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
