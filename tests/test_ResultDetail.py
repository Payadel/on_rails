import unittest

from on_rails.ResultDetail import ResultDetail
from tests.helpers import assert_result_detail


class TestResultDetail(unittest.TestCase):
    def test_init_without_optional_args(self):
        result_detail = ResultDetail(title='title')

        assert_result_detail(test_class=self, result_detail=result_detail, title='title')

    def test_init_with_optional_args(self):
        result_detail = ResultDetail(title='title', message='message', code=100, more_data=["more data"])

        assert_result_detail(test_class=self, result_detail=result_detail, title='title', message='message', code=100,
                             more_data=["more data"])

    def test_init_without_required_args(self):
        self.assertRaises(ValueError, ResultDetail, title=None)
        self.assertRaises(ValueError, ResultDetail, title='')

    def test_is_instance_of(self):
        test_detail = FakeDetail("title")

        self.assertTrue(test_detail.is_instance_of(FakeDetail))
        self.assertTrue(test_detail.is_instance_of(ResultDetail))

    def test_add_more_data(self):
        result_detail = ResultDetail(title='title')
        result_detail.more_data = None  # We use none to make sure that our function does not run into problems.

        result_detail.add_more_data("more data")
        self.assertEqual(["more data"], result_detail.more_data)

    def test_add_more_data_with_none(self):
        result_detail = ResultDetail(title='title')

        result_detail.add_more_data(None)
        self.assertEqual([], result_detail.more_data)

    def test_str_without_args(self):
        result_detail = ResultDetail(title='title')
        expected = "Title: title\n"

        self.assertEqual(expected, str(result_detail))

    def test_str_with_args(self):
        result_detail = ResultDetail(title='title', message='message', code=100)
        expected = "Title: title\nMessage: message\nCode: 100\n"

        self.assertEqual(expected, str(result_detail))

    def test_repr_without_more_data(self):
        result_detail = ResultDetail(title='title')
        self.assertEqual(str(result_detail), repr(result_detail))

    def test_repr_with_more_data(self):
        result_detail = ResultDetail(title='title', more_data=["more data"])
        expected = str(result_detail) + "More Data:\n\tmore data\n"

        self.assertEqual(expected, repr(result_detail))


class FakeDetail(ResultDetail):
    pass


if __name__ == "__main__":
    unittest.main()
