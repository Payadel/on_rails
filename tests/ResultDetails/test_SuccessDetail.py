import unittest

from on_rails.ResultDetails.SuccessDetail import SuccessDetail
from tests.helpers import assert_result_detail


class TestSuccessDetail(unittest.TestCase):
    def test_init_without_args(self):
        success_detail = SuccessDetail()

        assert_result_detail(test_class=self, result_detail=success_detail, title="Operation was successful", code=200)

    def test_init_with_args(self):
        success_detail = SuccessDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, result_detail=success_detail, title="title", message="message", code=100,
                             more_data=["message"])


if __name__ == '__main__':
    unittest.main()
