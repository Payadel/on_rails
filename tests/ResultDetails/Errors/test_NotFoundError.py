import unittest

from def_result.ResultDetails.Errors.NotFoundError import NotFoundError
from tests.helpers import assert_error_detail


class TestNotFoundError(unittest.TestCase):
    def test_init_without_args(self):
        detail = NotFoundError()

        assert_error_detail(test_class=self, error_detail=detail, title="NotFound Error",
                            code=404)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = NotFoundError(title="title", message="message", code=100, more_data=["message"],
                                 errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="title",
                            code=100, message="message", more_data=["message"],
                            errors={"key": "message"}, exception=exception)


if __name__ == '__main__':
    unittest.main()
