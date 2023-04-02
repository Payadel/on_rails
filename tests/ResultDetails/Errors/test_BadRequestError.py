import unittest

from on_rails.ResultDetails.Errors.BadRequestError import BadRequestError
from tests.helpers import assert_error_detail


class TestBadRequestError(unittest.TestCase):
    def test_init_without_args(self):
        detail = BadRequestError()

        assert_error_detail(test_class=self, error_detail=detail, title="BadRequest Error",
                            code=400)

    def test_init_with_args(self):
        exception = Exception("fake")
        detail = BadRequestError(title="title", message="message", code=100, more_data=["message"],
                                 errors={"key": "message"}, exception=exception)

        assert_error_detail(test_class=self, error_detail=detail, title="title",
                            code=100, message="message", more_data=["message"],
                            errors={"key": "message"}, exception=exception)


if __name__ == '__main__':
    unittest.main()
