from typing import Any, List, Optional

from on_rails.ResultDetails.SuccessDetail import SuccessDetail


class CreatedDetail(SuccessDetail):
    """
    A new resource has been created. Default code is 201.

    Inherits from SuccessDetail class.
    """

    def __init__(self, title: Optional[str] = "A new resource has been created",
                 message: Optional[str] = None,
                 code: Optional[int] = 201,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title=title, message=message, code=code, more_data=more_data)
