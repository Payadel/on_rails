import unittest

from on_rails import ErrorDetail
from on_rails.Result import Result
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails import SuccessDetail
from on_rails.ResultDetails.Errors import BadRequestError
from tests.helpers import (assert_error_detail, assert_exception,
                           assert_result, assert_result_with_type)


def function_raise_exception():
    raise Exception("fake")


class TestResult(unittest.TestCase):
    def test_init_without_optional_args(self):
        result = Result(True)

        assert_result(self, result=result, success=True)

    def test_init_with_optional_args(self):
        detail = ResultDetail(title="test")
        value = 123
        result = Result(success=True, detail=detail, value=value)

        assert_result(self, result=result, success=True, detail=detail, value=value)

    def test_ok_without_optional_args(self):
        result = Result.ok()

        assert_result(self, result=result, success=True)

    def test_ok_with_optional_args(self):
        value = 123
        detail = ResultDetail(title="test")
        result = Result.ok(detail=detail, value=value)

        assert_result(self, result=result, success=True, detail=detail, value=value)

    def test_fail_without_optional_args(self):
        result = Result.fail()

        assert_result(self, result=result, success=False)

    def test_fail_with_optional_args(self):
        detail = ResultDetail(title="test")
        result = Result.fail(detail=detail)

        assert_result(self, result=result, success=False, detail=detail)

    def test_code_without_detail_and_without_args(self):
        # Success
        result = Result.ok()
        self.assertEqual(200, result.code())

        # Fail
        result = Result.fail()
        self.assertEqual(500, result.code())

    def test_code_without_detail_and_with_args(self):
        # Success
        result = Result.ok()
        self.assertEqual(0, result.code(default_success_code=0, default_error_code=1))

        # Fail
        result = Result.fail()
        self.assertEqual(1, result.code(default_success_code=0, default_error_code=1))

    def test_code_with_detail_and_without_args(self):
        detail = ResultDetail(title="test", code=100)
        # Success
        result = Result.ok(detail=detail)
        self.assertEqual(100, result.code())

        # Fail
        result = Result.fail(detail=detail)
        self.assertEqual(100, result.code())

    def test_code_with_detail_and_with_args(self):
        detail = ResultDetail(title="test", code=100)
        # Success
        result = Result.ok(detail=detail)
        self.assertEqual(100, result.code(default_success_code=0, default_error_code=1))

        # Fail
        result = Result.fail(detail=detail)
        self.assertEqual(100, result.code(default_success_code=0, default_error_code=1))

    def test_str_success_without_args(self):
        result = Result.ok()
        self.assertEqual("success: True\n", str(result))

    def test_str_fail_without_args(self):
        result = Result.fail()
        self.assertEqual("success: False\n", str(result))

    def test_str_with_value(self):
        result = Result.ok("123")
        self.assertEqual("success: True\nValue: 123\n", str(result))

    def test_str_with_detail_(self):
        result = Result.ok(detail=SuccessDetail(message="test"))
        self.assertTrue(str(result).startswith("success: True\nDetail:\n"))

    def test_call_function_give_function_without_parameters(self):
        result = Result.ok(1)

        func_result = result._call_function(lambda: Result.ok(2))
        assert_result(self, func_result, success=True, value=2)

        func_result = result._call_function(lambda: Result.fail())
        assert_result(self, func_result, success=False)

    def test_call_function_give_function_with_parameters(self):
        result = Result.ok(1)

        func_result = result._call_function(lambda x: Result.ok(x + 1), 5)
        assert_result(self, func_result, success=True, value=6)

        func_result = result._call_function(lambda a, b: Result.ok(a + b), 2, b=3)
        assert_result(self, func_result, success=True, value=5)

    def test_call_function_give_function_use_prev_arg(self):
        result = Result.ok(1)

        func_result = result._call_function(lambda prev, a, b: Result.ok(prev + a + b), 2, b=3)
        assert_result(self, func_result, success=True, value=6)

    def test_call_function_with_invalid_args(self):
        result = Result.ok(1)

        func_result = result._call_function(lambda x: x + 1, 1, 2, 3, 4)
        assert_exception(self, func_result, TypeError)

    def test_call_function_with_exception(self):
        result = Result.ok(1)

        func_result = result._call_function(function_raise_exception)
        assert_exception(self, func_result, Exception)

    def test_on_success_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_success(lambda: Result.ok())

        self.assertEqual(fail_result, func_result)

    def test_on_success_with_success_result(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: Result.ok(5))

        assert_result(self, func_result, success=True, value=5)

    def test_on_fail_with_success_result(self):
        success_result = Result.ok(5)

        func_result = success_result.on_fail(function_raise_exception)

        assert_result(self, func_result, success=True, value=5)

    def test_on_fail_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_fail(lambda: Result.ok(5))

        assert_result(self, func_result, success=True, value=5)

    def test_fail_when_condition_is_false(self):
        result = Result.ok(1).fail_when(False)

        assert_result(self, result, success=True, value=1)

    def test_fail_when_default_error_detail(self):
        result = Result.ok(1).fail_when(True)

        assert_result_with_type(self, result, success=False, detail_type=ErrorDetail)

    def test_fail_when_default_custom_detail(self):
        result = Result.ok(1).fail_when(True, BadRequestError())

        assert_result_with_type(self, result, success=False, detail_type=BadRequestError)

    def test_fail_when_add_prev_detail(self):
        # Default
        result = Result.ok(1).fail_when(True)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred", code=500)

        result = Result.ok(1).fail_when(True, add_prev_detail=True)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred", code=500, more_data=[{'prev_detail': None}])


if __name__ == "__main__":
    unittest.main()
