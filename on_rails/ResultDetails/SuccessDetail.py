from typing import Any, List, Optional

from on_rails.ResultDetail import ResultDetail


class SuccessDetail(ResultDetail):
    """ Stores the details of a successful operation.

    This class inherits from the `ResultDetail` class

    Inherits from ResultDetail class.

    Args:
        title (str, optional): The title of the successful operation. If None, defaults to "Operation was successful".
        message (str, optional): The message of the successful operation. Defaults to None.
        code (int, optional): The HTTP status code of the successful operation. Defaults to 200.
        more_data (List[Any], optional): Additional data related to the successful operation. Defaults to None.
    """

    def __init__(self, title: Optional[str] = "Operation was successful",
                 message: Optional[str] = None,
                 code: Optional[int] = 200,
                 more_data: Optional[List[Any]] = None):
        super().__init__(title if title else "Operation was successful", message, code, more_data)
