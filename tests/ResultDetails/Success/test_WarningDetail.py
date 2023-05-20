import unittest

from on_rails.ResultDetails.Success.WarningDetail import WarningDetail
from on_rails.test_helpers import assert_result_detail


class TestWarningDetail(unittest.TestCase):
    def test_init(self):
        create_detail = WarningDetail(message="fake")

        assert_result_detail(test_class=self, target_result_detail=create_detail, expected_message="fake",
                             expected_title="The operation was completed successfully, but there is a warning.",
                             expected_code=200)


if __name__ == '__main__':
    unittest.main()
