import unittest

from on_rails.ResultDetails.Errors.ExceptionError import ExceptionError
from tests.helpers import assert_error_detail


class TestExceptionError(unittest.TestCase):
    def test_init_without_optional_args(self):
        exception = Exception("fake")
        detail = ExceptionError(exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="An exception occurred",
                            code=500, exception=exception)

    def test_init_required_args(self):
        self.assertRaises(ValueError, ExceptionError, exception=None)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = ExceptionError(title="title", message="message", code=100, more_data=["message"],
                                 errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="title",
                            code=100, message="message", more_data=["message"],
                            errors={"key": "message"}, exception=exception)


if __name__ == '__main__':
    unittest.main()
