import unittest

from on_rails.ResultDetails.SuccessDetail import SuccessDetail
from on_rails.test_helpers import assert_result_detail


class TestSuccessDetail(unittest.TestCase):
    def test_init_without_args(self):
        success_detail = SuccessDetail()

        assert_result_detail(test_class=self, target_result_detail=success_detail, expected_title="Operation was successful", expected_code=200)

    def test_init_with_args(self):
        success_detail = SuccessDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, target_result_detail=success_detail, expected_title="title", expected_message="message", expected_code=100,
                             expected_more_data=["message"])


if __name__ == '__main__':
    unittest.main()
