import asyncio
import unittest
from typing import Coroutine

from on_rails import Result, def_result
from on_rails.ResultDetails.Errors import BadRequestError
from tests.helpers import assert_result, assert_result_detail


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


def func_without_output_error():
    raise Exception("fake error")


async def divide_numbers_async(a: int, b: int):
    await asyncio.sleep(0)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class TestDefResultDecorator(unittest.TestCase):
    def test_def_result_on_simple_function_ok(self):
        """
        The function tests the `def_result` decorator on a simple synchronous and asynchronous function
        and checks if the result is as expected.
        """
        result = def_result(is_async=False)(divide_numbers)(10, 2)
        assert_result(test_class=self, result=result, success=True, value=5)

        result = def_result(is_async=True)(divide_numbers)(10, 2)
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=True, value=5)

    def test_def_result_on_simple_function_error(self):
        result = def_result(is_async=False)(divide_numbers)(10, 0)
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="An exception occurred",
                             message="Cannot divide by zero", code=500)

        result = def_result(is_async=True)(divide_numbers)(10, 0)
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="An exception occurred",
                             message="Cannot divide by zero", code=500)

    def test_def_result_on_result_function_ok(self):
        result = def_result(is_async=False)(divide_numbers_support_result)(10, 2)
        assert_result(test_class=self, result=result, success=True, value=5)

        result = def_result(is_async=True)(divide_numbers_support_result)(10, 2)
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=True, value=5)

    def test_def_result_on_result_function_error(self):
        result = def_result(is_async=False)(divide_numbers_support_result)(10, 0)
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="BadRequest Error",
                             message="Cannot divide by zero", code=400)

        result = def_result(is_async=True)(divide_numbers_support_result)(10, 0)
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="BadRequest Error",
                             message="Cannot divide by zero", code=400)

    def test_func_without_output_ok(self):
        result = def_result(is_async=False)(func_without_output_ok)()
        assert_result(test_class=self, result=result, success=True, value=None)

        result = def_result(is_async=True)(func_without_output_ok)()
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=True, value=None)

    def test_func_without_output_error(self):
        result = def_result(is_async=False)(func_without_output_error)()
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="An exception occurred",
                             message="fake error", code=500)

        result = def_result(is_async=True)(func_without_output_error)()
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=False, detail=result.detail)
        assert_result_detail(test_class=self, result_detail=result.detail, title="An exception occurred",
                             message="fake error", code=500)

    def test_async(self):
        result = def_result(is_async=True)(divide_numbers_async)(10, 5)
        self.assertTrue(isinstance(result, Coroutine))
        result = asyncio.get_event_loop().run_until_complete(result)
        assert_result(test_class=self, result=result, success=True, value=2)


if __name__ == '__main__':
    unittest.main()
