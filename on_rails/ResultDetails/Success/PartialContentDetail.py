from typing import Any, List, Optional

from on_rails.ResultDetails.SuccessDetail import SuccessDetail


class PartialContentDetail(SuccessDetail):
    """
    Stores the details of a partial success operation. Default code is 206.

    Inherits from SuccessDetail class.
    """

    def __init__(self, title: Optional[str] = "Partial content",
                 message: Optional[str] = None,
                 code: Optional[int] = 206,
                 more_data: Optional[List[Any]] = None):
        """
        Initializes a new PartialContentDetail object.

        :param title: The title of the error.
        :param message: The error message.
        :param code: The error code.
        :param more_data: Additional data.
        """
        super().__init__(title=title, message=message, code=code, more_data=more_data)
