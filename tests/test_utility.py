import asyncio
import unittest

from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.utility import (await_func, generate_error,
                              get_num_of_function_parameters, is_async)
from tests.helpers import assert_error_detail


async def async_func():
    await asyncio.sleep(1)
    return "Hello, World!"


class TestUtility(unittest.TestCase):
    def test_get_num_of_function_parameters_give_none(self):
        self.assertRaises(TypeError, get_num_of_function_parameters, None)

    def test_get_num_of_function_parameters(self):
        self.assertEqual(get_num_of_function_parameters(lambda x: x), 1)
        self.assertEqual(get_num_of_function_parameters(lambda x, y: x), 2)

    def test_is_async(self):
        self.assertFalse(is_async(lambda x: x))
        self.assertTrue(is_async(async_func))

    def test_is_async_give_none(self):
        self.assertFalse(is_async(None))

    def test_await_func(self):
        result = await_func(async_func)
        self.assertEqual("Hello, World!", result)

        self.assertEqual(5, await_func(lambda: 5))

    def test_generate_error_none_or_empty_errors(self):
        error_detail = generate_error(None, 2)
        assert_error_detail(self, error_detail=error_detail, title="An error occurred", code=500,
                            message='Operation failed with 2 attempts. ')

        error_detail = generate_error([], 2)
        assert_error_detail(self, error_detail=error_detail, title="An error occurred", code=500,
                            message='Operation failed with 2 attempts. ')

    def test_generate_error_without_exception_error(self):
        error = ErrorDetail()
        error_detail = generate_error([error], 2)
        assert_error_detail(self, error_detail=error_detail, title="An error occurred", code=500,
                            message='Operation failed with 2 attempts. The details of the 1 errors '
                                    'are stored in the more_data field. ',
                            more_data=[error])

    def test_generate_error_with_exception_error(self):
        exception = TypeError()
        error_detail = generate_error([exception], 2)
        assert_error_detail(self, error_detail=error_detail, title="An error occurred", code=500,
                            message='Operation failed with 2 attempts. The details of the 1 errors are stored in '
                                    'the more_data field. At least one of the errors was an exception type, '
                                    'the first exception being stored in the exception field.',
                            more_data=[exception], exception=exception)


if __name__ == '__main__':
    unittest.main()
