import unittest

from on_rails.ResultDetails.Success.PartialContentDetail import \
    PartialContentDetail
from tests.helpers import assert_result_detail


class TestPartialContentDetail(unittest.TestCase):
    def test_init_without_args(self):
        detail = PartialContentDetail()

        assert_result_detail(test_class=self, result_detail=detail, title="Partial content", code=206)

    def test_init_with_args(self):
        detail = PartialContentDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, result_detail=detail, title="title", message="message", code=100,
                             more_data=["message"])


if __name__ == '__main__':
    unittest.main()
