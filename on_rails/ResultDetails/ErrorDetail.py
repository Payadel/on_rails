import traceback
from typing import Any, Dict, List, Optional

from on_rails.ResultDetail import ResultDetail


class ErrorDetail(ResultDetail):
    """
    Stores the error details of a result.

    Inherits from ResultDetail class.
    """
    errors: Optional[Dict[str, str]]
    exception: Optional[Exception]
    stack_trace: traceback.StackSummary

    def __init__(self, title: Optional[str] = "An error occurred",
                 message: Optional[str] = None,
                 code: Optional[int] = 500,
                 errors: Optional[Dict[str, str]] = None,
                 exception: Optional[Exception] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title if title else "An error occurred", message, code, more_data)
        self.errors = errors
        self.exception = exception
        self.stack_trace = traceback.extract_stack()

    def add_or_update_error(self, key: str, value: str):
        """
        Add or update an error in the dictionary.
        """
        if self.errors is None:
            self.errors = {}
        self.errors[key] = value

    def __str__(self):
        error_details = super().__str__()

        if self.errors is not None:
            error_details += "Errors: " + str(self.errors) + "\n"

        if self.exception:
            error_details += "Exception: " + str(self.exception) + "\n"
        error_details += "Stack trace: " + ''.join(self.stack_trace.format()) + "\n"

        return error_details
