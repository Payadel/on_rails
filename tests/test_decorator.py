# pylint: disable=all

import asyncio
import unittest
from typing import Coroutine

from on_rails.decorator import def_result
from on_rails.Result import BreakFunctionException, BreakRailsException, Result
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.ResultDetails.Errors.BadRequestError import BadRequestError
from on_rails.ResultDetails.SuccessDetail import SuccessDetail
from on_rails.test_helpers import (assert_error_detail, assert_result,
                                   assert_result_detail,
                                   assert_result_with_type)

FAKE_EXCEPTION = Exception("fake")


def divide_numbers(a: int, b: int):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def divide_numbers_support_result(a: int, b: int) -> Result:
    if b == 0:
        return Result.fail(BadRequestError(message="Cannot divide by zero"))
    return Result.ok(a / b)


def func_without_output_ok():
    pass


async def divide_numbers_async(a: int, b: int):
    await asyncio.sleep(0)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def raise_exception(exception: Exception):
    raise exception


async def raise_exception_async(exception: Exception):
    await asyncio.sleep(0)
    raise exception


class TestDefResultDecorator(unittest.TestCase):
    def test_def_result_on_simple_function_ok(self):
        result = def_result(is_async=False)(divide_numbers)(10, 2)
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=5)

    def test_def_result_on_simple_function_error(self):
        result = def_result(is_async=False)(divide_numbers)(10, 0)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored "
                                             "in the more_data field. At least one of the errors was an exception type, "
                                             "the first exception being stored in the exception field.",
                            expected_code=500, expected_more_data=result.detail.more_data,
                            expected_exception=result.detail.exception)
        self.assertTrue(isinstance(result.detail.exception, ValueError))
        self.assertEqual(str(result.detail.exception), "Cannot divide by zero")

    def test_def_result_on_result_function_ok(self):
        result = def_result(is_async=False)(divide_numbers_support_result)(10, 2)
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=5)

    def test_def_result_on_result_function_error(self):
        result = def_result(is_async=False)(divide_numbers_support_result)(10, 0)
        assert_result(test_class=self, target_result=result, expected_success=False, expected_detail=result.detail)
        assert_result_detail(test_class=self, target_result_detail=result.detail, expected_title="BadRequest Error",
                             expected_message="Cannot divide by zero", expected_code=400)

    def test_func_without_output_ok(self):
        result = def_result(is_async=False)(func_without_output_ok)()
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=None)

    def test_func_without_output_error(self):
        result = def_result(is_async=False)(raise_exception)(FAKE_EXCEPTION)
        assert_result(test_class=self, target_result=result, expected_success=False, expected_detail=result.detail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored "
                                             "in the more_data field. At least one of the errors was an exception type, "
                                             "the first exception being stored in the exception field.",
                            expected_code=500, expected_more_data=[FAKE_EXCEPTION], expected_exception=FAKE_EXCEPTION)

    def test_break_rails_with_result_ok(self):
        result_ok = Result.ok(1, SuccessDetail())
        break_rails = BreakRailsException(result_ok)

        result = def_result()(raise_exception)(break_rails)
        self.assertEqual(result_ok, result)

    def test_break_rails_with_result_fail(self):
        result_fail = Result.fail(ErrorDetail())
        break_rails = BreakRailsException(result_fail)

        result = def_result()(raise_exception)(break_rails)
        self.assertEqual(result_fail, result)

    def test_break_function_with_result_ok(self):
        result_ok = Result.ok(1, SuccessDetail())
        break_function = BreakFunctionException(result_ok)

        result = def_result()(raise_exception)(break_function)
        self.assertEqual(result_ok, result)

    def test_break_function_with_result_fail(self):
        result_fail = Result.fail(ErrorDetail())
        break_rails = BreakFunctionException(result_fail)

        result = def_result()(raise_exception)(break_rails)
        self.assertEqual(result_fail, result)


class TestDefResultDecoratorAsync(unittest.IsolatedAsyncioTestCase):
    async def test_def_result_on_simple_function_ok_async(self):
        result = await def_result(is_async=True)(divide_numbers)(10, 2)
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=5)

    async def test_def_result_on_simple_function_error_async(self):
        result = await def_result(is_async=True)(divide_numbers)(10, 0)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored "
                                             "in the more_data field. At least one of the errors was an exception type, "
                                             "the first exception being stored in the exception field.",
                            expected_code=500, expected_more_data=result.detail.more_data,
                            expected_exception=result.detail.exception)
        self.assertTrue(isinstance(result.detail.exception, ValueError))
        self.assertEqual(str(result.detail.exception), "Cannot divide by zero")

    async def test_def_result_on_result_function_ok_async(self):
        result = await def_result(is_async=True)(divide_numbers_support_result)(10, 2)
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=5)

    async def test_def_result_on_result_function_error_async(self):
        result = await def_result(is_async=True)(divide_numbers_support_result)(10, 0)
        assert_result(test_class=self, target_result=result, expected_success=False, expected_detail=result.detail)
        assert_result_detail(test_class=self, target_result_detail=result.detail, expected_title="BadRequest Error",
                             expected_message="Cannot divide by zero", expected_code=400)

    async def test_func_without_output_ok_async(self):
        result = await def_result(is_async=True)(func_without_output_ok)()
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=None)

    async def test_func_without_output_error(self):
        result = await def_result(is_async=True)(raise_exception_async)(FAKE_EXCEPTION)
        assert_result(test_class=self, target_result=result, expected_success=False, expected_detail=result.detail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored "
                                             "in the more_data field. At least one of the errors was an exception type, "
                                             "the first exception being stored in the exception field.",
                            expected_code=500, expected_more_data=[FAKE_EXCEPTION], expected_exception=FAKE_EXCEPTION)

    async def test_async(self):
        result = def_result(is_async=True)(divide_numbers_async)(10, 5)
        self.assertTrue(isinstance(result, Coroutine))
        result = await result
        assert_result(test_class=self, target_result=result, expected_success=True, expected_value=2)

    async def test_break_rails_with_result_async(self):
        result_ok = Result.ok(1, SuccessDetail())
        break_rails = BreakRailsException(result_ok)

        result = await def_result(is_async=True)(raise_exception_async)(break_rails)
        self.assertEqual(result_ok, result)

    async def test_break_rails_with_result_fail_async(self):
        result_fail = Result.fail(ErrorDetail())
        break_rails = BreakRailsException(result_fail)

        result = await def_result(is_async=True)(raise_exception_async)(break_rails)
        self.assertEqual(result_fail, result)

    async def test_break_function_with_result_async(self):
        result_ok = Result.ok(1, SuccessDetail())
        break_function = BreakFunctionException(result_ok)

        result = await def_result(is_async=True)(raise_exception_async)(break_function)
        self.assertEqual(result_ok, result)

    async def test_break_function_with_result_fail_async(self):
        result_fail = Result.fail(ErrorDetail())
        break_function = BreakFunctionException(result_fail)

        result = await def_result(is_async=True)(raise_exception_async)(break_function)
        self.assertEqual(result_fail, result)


if __name__ == '__main__':
    unittest.main()
