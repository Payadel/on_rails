import unittest

from on_rails.ResultDetails.Errors.ValidationError import ValidationError
from tests.helpers import assert_error_detail


class TestValidationError(unittest.TestCase):
    def test_init_without_args(self):
        detail = ValidationError()

        assert_error_detail(test_class=self, error_detail=detail, title="One or more validation errors occurred",
                            code=400)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = ValidationError(title="title", message="message", code=100, more_data=["message"],
                                 errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="title",
                            code=100, message="message", more_data=["message"],
                            errors={"key": "message"}, exception=exception)


if __name__ == '__main__':
    unittest.main()
