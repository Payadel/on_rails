import unittest

from on_rails.ResultDetails.Errors.ValidationError import ValidationError
from tests.helpers import assert_error_detail


class TestValidationError(unittest.TestCase):
    def test_init_without_args(self):
        detail = ValidationError()

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="One or more validation errors occurred",
                            expected_code=400)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = ValidationError(title="title", message="message", code=100, more_data=["message"],
                                 errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="title",
                            expected_code=100, expected_message="message", expected_more_data=["message"],
                            expected_errors={"key": "message"}, expected_exception=exception)


if __name__ == '__main__':
    unittest.main()
