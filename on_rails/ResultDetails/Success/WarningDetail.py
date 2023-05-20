from typing import Any, List, Optional

from on_rails import SuccessDetail


class WarningDetail(SuccessDetail):
    """
    It shows the information of an operation that has been completed with a warning.
    """
    def __init__(self,
                 message: str,
                 title: Optional[str] = "The operation was completed successfully, but there is a warning.",
                 code: Optional[int] = 200,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title if title else "The operation was completed successfully, but there is a warning.",
                         message, code, more_data)
