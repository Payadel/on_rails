import unittest

from on_rails.ResultDetails.Errors.NotFoundError import NotFoundError
from tests.helpers import assert_error_detail


class TestNotFoundError(unittest.TestCase):
    def test_init_without_args(self):
        detail = NotFoundError()

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="NotFound Error",
                            expected_code=404)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = NotFoundError(title="title", message="message", code=100, more_data=["message"],
                               errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, target_error_detail=detail, expected_title="title",
                            expected_code=100, expected_message="message", expected_more_data=["message"],
                            expected_errors={"key": "message"}, expected_exception=exception)


if __name__ == '__main__':
    unittest.main()
