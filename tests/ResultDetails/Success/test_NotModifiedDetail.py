import unittest

from on_rails.ResultDetails.Success.NotModifiedDetail import NotModifiedDetail
from on_rails.test_helpers import assert_result_detail


class TestNotModifiedDetail(unittest.TestCase):
    def test_init_without_args(self):
        detail = NotModifiedDetail()

        assert_result_detail(test_class=self, target_result_detail=detail,
                             expected_title="The resource has not been modified since the last request", expected_code=304)

    def test_init_with_args(self):
        detail = NotModifiedDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, target_result_detail=detail, expected_title="title", expected_message="message", expected_code=100,
                             expected_more_data=["message"])


if __name__ == '__main__':
    unittest.main()
