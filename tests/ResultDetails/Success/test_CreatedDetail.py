import unittest

from on_rails.ResultDetails.Success.CreatedDetail import CreatedDetail
from on_rails.test_helpers import assert_result_detail


class TestCreatedDetail(unittest.TestCase):
    def test_init_without_args(self):
        create_detail = CreatedDetail()

        assert_result_detail(test_class=self, target_result_detail=create_detail, expected_title="A new resource has been created",
                             expected_code=201)

    def test_init_with_args(self):
        create_detail = CreatedDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, target_result_detail=create_detail, expected_title="title", expected_message="message", expected_code=100,
                             expected_more_data=["message"])


if __name__ == '__main__':
    unittest.main()
