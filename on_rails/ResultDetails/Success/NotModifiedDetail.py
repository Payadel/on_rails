from typing import Any, List, Optional

from on_rails.ResultDetails.SuccessDetail import SuccessDetail


class NotModifiedDetail(SuccessDetail):
    """
    The resource has not been modified since the last request. Default code is 304.

    Inherits from SuccessDetail class.
    """

    def __init__(self, title: Optional[str] = "The resource has not been modified since the last request",
                 message: Optional[str] = None,
                 code: Optional[int] = 304,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, more_data=more_data)
