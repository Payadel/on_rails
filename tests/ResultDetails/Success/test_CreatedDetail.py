import unittest

from on_rails.ResultDetails.Success.CreatedDetail import CreatedDetail
from tests.helpers import assert_result_detail


class TestCreatedDetail(unittest.TestCase):
    def test_init_without_args(self):
        create_detail = CreatedDetail()

        assert_result_detail(test_class=self, result_detail=create_detail, title="A new resource has been created",
                             code=201)

    def test_init_with_args(self):
        create_detail = CreatedDetail(title="title", message="message", code=100, more_data=["message"])

        assert_result_detail(test_class=self, result_detail=create_detail, title="title", message="message", code=100,
                             more_data=["message"])


if __name__ == '__main__':
    unittest.main()
