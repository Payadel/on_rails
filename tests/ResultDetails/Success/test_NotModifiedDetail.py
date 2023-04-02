import unittest

from on_rails.ResultDetails.Success.NotModifiedDetail import NotModifiedDetail
from tests.helpers import assert_result_detail


class TestNotModifiedDetail(unittest.TestCase):
    def test_init_without_args(self):
        detail = NotModifiedDetail()

        assert_result_detail(test_class=self, result_detail=detail, title="The resource has not been modified since the last request", code=304)

    def test_init_with_args(self):
        detail = NotModifiedDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, result_detail=detail, title="title", message="message", code=100,
                             more_data=["message"])


if __name__ == '__main__':
    unittest.main()
