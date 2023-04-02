from typing import Any, Dict, List, Optional

from on_rails.ResultDetails.ErrorDetail import ErrorDetail


class NotFoundError(ErrorDetail):
    """
    Represent the error details of a not found error. Default code is 404.

    Inherits from ErrorDetail class.
    """

    def __init__(self, title: Optional[str] = "NotFound Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 404,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        """
        Initializes a new instance of the NotFoundError class.

        :param title: The title of the error.
        :param message: The message associated with the error.
        :param code: The HTTP status code associated with the error.
        :param errors: The dictionary of errors associated with the error.
        :param exception: The exception associated with the error.
        :param more_data: Any additional data associated with the error.
        """
        super().__init__(title=title, message=message, code=code, errors=errors, exception=exception,
                         more_data=more_data)
