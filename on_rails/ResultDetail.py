from typing import Any, List, Optional


class ResultDetail:
    """ Stores information about the result

    Attributes:
        title (str): A title for the result detail.
        message (str, optional): A message describing the result detail. Defaults to None.
        code (int, optional): A code associated with the result detail. Defaults to None.
        more_data (List[Any]): A list of additional data associated with the result detail. Defaults to an empty list.
    """
    title: str
    message: Optional[str]
    code: Optional[int]
    more_data: List[Any] = []

    def __init__(self, title: str,
                 message: Optional[str] = None,
                 code: Optional[int] = None,
                 more_data: Optional[List[Any]] = None):
        """
        Initializes a new instance of the ResultDetail class.

        :param title: The title of the error
        :type title: str
        :param message: The message to display to the user
        :type message: Optional[str]
        :param code: The status code
        :type code: Optional[int]
        :param more_data: This is a list of any data you want to pass along with the error
        :type more_data: Optional[List[Any]]

        :raises ValueError: If title is empty or None.
        """
        if title is None or title == '':
            raise ValueError("title is required")
        self.title = title
        self.message = message
        self.code = code
        if more_data is not None:
            self.more_data = more_data
        else:
            self.more_data = []

    def is_instance_of(self, cls):
        """
        The isinstance() function is used to determine whether an object is an instance of a class or a subclass

        :param cls: The class to check against
        :return: True or False
        """
        return isinstance(self, cls)

    def add_more_data(self, data: Any) -> None:
        """
        Adds additional data to the result detail

        :param data: The data to be added to the list
        :type data: Any
        :return: None.
        """
        if data is None:
            return
        if self.more_data is None:
            self.more_data = []
        self.more_data.append(data)

    def __str__(self):
        """
        The function returns a string that contains the title, message, and code of the exception
        :return: str
        """
        result: str = f"Title: {self.title}\n"

        if self.message:
            result += f"Message: {self.message}\n"
        if self.code:
            result += f"Code: {self.code}\n"

        return result

    def __repr__(self):
        result = self.__str__()
        if self.more_data and len(self.more_data) > 0:
            result += "More Data:\n"
            for data in self.more_data:
                result += f"\t{data}\n"
        return result
