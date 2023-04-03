import unittest

from on_rails.ResultDetails.Errors.ConflictError import ConflictError
from tests.helpers import assert_error_detail


class TestConflictError(unittest.TestCase):
    def test_init_without_args(self):
        detail = ConflictError()

        assert_error_detail(test_class=self, error_detail=detail, title="Conflict Error",
                            code=409)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = ConflictError(title="title", message="message", code=100, more_data=["message"],
                               errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="title",
                            code=100, message="message", more_data=["message"],
                            errors={"key": "message"}, exception=exception)


if __name__ == '__main__':
    unittest.main()
