# pylint: disable=all
import asyncio
import unittest

from on_rails._utility import (await_func, generate_error, get_loop,
                               get_num_of_function_parameters, is_async)
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from tests.helpers import assert_error_detail


async def async_func():
    return "Hello, World!"


class TestUtility(unittest.TestCase):
    # region get_num_of_function_parameters

    def test_get_num_of_function_parameters_give_none(self):
        self.assertRaises(TypeError, get_num_of_function_parameters, None)

    def test_get_num_of_function_parameters(self):
        self.assertEqual(1, get_num_of_function_parameters(lambda x: x))
        self.assertEqual(2, get_num_of_function_parameters(lambda x, y: x))

    def test_get_num_of_function_parameters_builtin_functions(self):
        # Works for some builtin functions not all
        self.assertEqual(2, get_num_of_function_parameters(sum))

        self.assertRaises(AttributeError, get_num_of_function_parameters, print)

    # endregion

    # region is_async

    def test_is_async(self):
        self.assertFalse(is_async(lambda x: x))
        self.assertTrue(is_async(async_func))

    def test_is_async_give_none(self):
        self.assertFalse(is_async(None))

    # endregion

    # region generate_error

    def test_generate_error_none_or_empty_errors(self):
        error_detail = generate_error(None, 2)
        assert_error_detail(self, target_error_detail=error_detail, expected_title="An error occurred",
                            expected_code=500,
                            expected_message='Operation failed with 2 attempts. There is no more information.')

        error_detail = generate_error([], 2)
        assert_error_detail(self, target_error_detail=error_detail, expected_title="An error occurred",
                            expected_code=500,
                            expected_message='Operation failed with 2 attempts. There is no more information.')

    def test_generate_error_without_exception_error(self):
        error = ErrorDetail()
        error_detail = generate_error([error], 2)
        assert_error_detail(self, target_error_detail=error_detail, expected_title="An error occurred",
                            expected_code=500,
                            expected_message='Operation failed with 2 attempts. The details of the 1 errors '
                                             'are stored in the more_data field. ',
                            expected_more_data=[error])

    def test_generate_error_with_exception_error(self):
        exception = TypeError()
        error_detail = generate_error([exception], 2)
        assert_error_detail(self, target_error_detail=error_detail, expected_title="An error occurred",
                            expected_code=500,
                            expected_message='Operation failed with 2 attempts. The details of the 1 errors are stored in '
                                             'the more_data field. At least one of the errors was an exception type, '
                                             'the first exception being stored in the exception field.',
                            expected_more_data=[exception], expected_exception=exception)

    # endregion

    def test_get_loop(self):
        """
        This test case creates two event loops using the get_loop function and checks that they are both instances of
        the AbstractEventLoop class and that they are the same object. This tests that the function correctly returns
        the current event loop if one exists, or creates a new event loop if one doesn't exist, and sets it as the
        current event loop for the thread.
        """

        loop1 = get_loop()
        loop2 = get_loop()

        assert isinstance(loop1, asyncio.AbstractEventLoop)
        assert isinstance(loop2, asyncio.AbstractEventLoop)
        assert loop1 == loop2

    def test_await_func(self):
        result = await_func(async_func)
        self.assertEqual("Hello, World!", result)

        self.assertEqual(5, await_func(lambda: 5))


if __name__ == '__main__':
    unittest.main()
