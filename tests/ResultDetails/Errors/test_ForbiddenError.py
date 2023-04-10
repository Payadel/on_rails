import unittest

from on_rails.ResultDetails.Errors.ForbiddenError import ForbiddenError
from tests.helpers import assert_error_detail


class TestForbiddenError(unittest.TestCase):
    def test_init_without_args(self):
        detail = ForbiddenError()

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="Forbidden Error",
                            expected_code=403)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = ForbiddenError(title="title", message="message", code=100, more_data=["message"],
                                errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="title",
                            expected_code=100, expected_message="message", expected_more_data=["message"],
                            expected_errors={"key": "message"}, expected_exception=exception)


if __name__ == '__main__':
    unittest.main()
