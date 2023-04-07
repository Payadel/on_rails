# pylint: disable=all

import asyncio
import unittest

from on_rails import ErrorDetail
from on_rails.Result import Result, try_func
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails import SuccessDetail
from on_rails.ResultDetails.Errors import BadRequestError
from tests.helpers import (assert_error_detail, assert_result,
                           assert_result_with_type)

FAKE_EXCEPTION = Exception("fake")
FAKE_ERROR = ErrorDetail("fake")


def function_raise_exception():
    raise FAKE_EXCEPTION


async def async_function():
    await asyncio.sleep(0)
    return 5


class TestResult(unittest.TestCase):
    # region __init__

    def test_init_without_optional_args(self):
        result = Result(True)

        assert_result(self, result=result, success=True)

    def test_init_with_optional_args(self):
        detail = ResultDetail(title="test")
        value = 123
        result = Result(success=True, detail=detail, value=value)

        assert_result(self, result=result, success=True, detail=detail, value=value)

    # endregion

    # region ok

    def test_ok_without_optional_args(self):
        result = Result.ok()

        assert_result(self, result=result, success=True)

    def test_ok_with_optional_args(self):
        value = 123
        detail = ResultDetail(title="test")
        result = Result.ok(detail=detail, value=value)

        assert_result(self, result=result, success=True, detail=detail, value=value)

    # endregion

    # region fail

    def test_fail_without_optional_args(self):
        result = Result.fail()

        assert_result(self, result=result, success=False)

    def test_fail_with_optional_args(self):
        detail = ResultDetail(title="test")
        result = Result.fail(detail=detail)

        assert_result(self, result=result, success=False, detail=detail)

    # endregion

    # region code

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

    # endregion

    # region __str__

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

    # endregion

    # region on_success

    def test_on_success_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_success(lambda: Result.ok())

        self.assertEqual(fail_result, func_result)

    def test_on_success_with_success_result(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: Result.ok(5))

        assert_result(self, func_result, success=True, value=5)

    def test_on_success_with_None_result(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: None)

        assert_result(self, func_result, success=True)

    def test_on_success_use_prev_result(self):
        result = Result.ok(1)

        func_result = result.on_success(lambda prev: prev)

        self.assertEqual(result, func_result)

    def test_on_success_give_func_fail(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: Result.fail())

        assert_result(self, func_result, success=False)

    def test_on_success_give_func_raise_exception(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(function_raise_exception, num_of_try=2)

        self.assertFalse(func_result.success)
        assert_error_detail(self, func_result.detail, title='An error occurred',
                            message="Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.",
                            exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION], code=500)

    # endregion

    # region on_success_add_more_data

    def test_on_success_add_more_data_on_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_success_add_more_data("Data")

        assert_result(self, func_result, success=False)
        self.assertIsNone(func_result.detail)

    def test_on_success_add_more_data_give_none(self):
        result = Result.ok(1)

        new_result = result.on_success_add_more_data(None)

        assert_result(self, new_result, success=True, value=1)
        self.assertIsNone(new_result.detail)

    def test_on_success_add_more_data_give_object(self):
        result = Result.ok(1)

        new_result = result.on_success_add_more_data("Data")

        assert_result_with_type(self, new_result, success=True, value=1, detail_type=SuccessDetail)
        self.assertEqual(["Data"], new_result.detail.more_data)

    def test_on_success_add_more_data_with_exist_detail(self):
        result = Result.ok(1, detail=SuccessDetail(more_data=["Data1"]))

        new_result = result.on_success_add_more_data("Data2")

        assert_result_with_type(self, new_result, success=True, value=1, detail_type=SuccessDetail)
        self.assertEqual(["Data1", "Data2"], new_result.detail.more_data)

    # endregion

    # region on_success_new_detail

    def test_on_success_new_detail_on_fail_result(self):
        result = Result.fail()

        new_result = result.on_success_new_detail(SuccessDetail)

        assert_result(self, new_result, success=False)
        self.assertIsNone(new_result.detail)

    def test_on_success_new_detail(self):
        result = Result.ok(1, SuccessDetail())

        new_result = result.on_success_new_detail(None)

        assert_result(self, new_result, success=True, value=1)
        self.assertIsNone(new_result.detail)

    # endregion

    # region on_success_tee

    def test_on_success_tee(self):
        result = Result.ok(1)
        new_result = result.on_success_tee(None)
        assert_result(self, new_result, success=True, value=1)

        result = Result.ok(1)
        new_result = result.on_success_tee(lambda: Result.fail())
        assert_result(self, new_result, success=True, value=1)

    # endregion

    # region on_fail

    def test_on_fail_with_success_result(self):
        success_result = Result.ok(5)

        func_result = success_result.on_fail(function_raise_exception)

        assert_result(self, func_result, success=True, value=5)

    def test_on_fail_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_fail(lambda: Result.ok(5))

        assert_result(self, func_result, success=True, value=5)

    def test_on_fail_with_None_result(self):
        result = Result.fail()

        func_result = result.on_fail(lambda: None)

        assert_result(self, func_result, success=True)

    def test_on_fail_use_prev_result(self):
        result = Result.fail()

        func_result = result.on_fail(lambda prev: prev)

        self.assertEqual(result, func_result)

    def test_on_fail_give_func_raise_exception(self):
        success_result = Result.fail()

        func_result = success_result.on_fail(function_raise_exception, num_of_try=2)

        self.assertFalse(func_result.success)
        assert_error_detail(self, func_result.detail, title='An error occurred',
                            message="Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.",
                            exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION], code=500)

    # endregion

    # region on_fail_add_more_data

    def test_on_fail_add_more_data_on_success_result(self):
        success_result = Result.ok()

        func_result = success_result.on_fail_add_more_data("Data")

        assert_result(self, func_result, success=True)
        self.assertIsNone(func_result.detail)

    def test_on_fail_add_more_data_give_none(self):
        result = Result.fail()

        new_result = result.on_fail_add_more_data(None)

        assert_result(self, new_result, success=False,)
        self.assertIsNone(new_result.detail)

    def test_on_fail_add_more_data_give_object(self):
        result = Result.fail()

        new_result = result.on_fail_add_more_data("Data")

        assert_result_with_type(self, new_result, success=False, detail_type=ErrorDetail)
        self.assertEqual(["Data"], new_result.detail.more_data)

    def test_on_fail_add_more_data_with_exist_detail(self):
        result = Result.fail(detail=ErrorDetail(more_data=["Data1"]))

        new_result = result.on_fail_add_more_data("Data2")

        assert_result_with_type(self, new_result, success=False, detail_type=ErrorDetail)
        self.assertEqual(["Data1", "Data2"], new_result.detail.more_data)

    # endregion

    # region on_success_new_detail

    def test_on_fail_new_detail_on_success_result(self):
        result = Result.ok(1, SuccessDetail())

        new_result = result.on_fail_new_detail(ErrorDetail())

        assert_result_with_type(self, new_result, success=True, value=1, detail_type=SuccessDetail)

    def test_on_fail_new_detail(self):
        result = Result.fail(ErrorDetail())

        new_result = result.on_fail_new_detail(None)

        assert_result(self, new_result, success=False)
        self.assertIsNone(new_result.detail)

    # endregion

    # region fail_when

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

        # Prev is None
        result = Result.ok(1).fail_when(True, add_prev_detail=True)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred", code=500)

        result = Result.fail(FAKE_ERROR).fail_when(True, add_prev_detail=True)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred", code=500,
                            more_data=[{'prev_detail': FAKE_ERROR}])

    # endregion

    # region convert_to_result

    def test_convert_to_result_give_none(self):
        result = Result.convert_to_result(None)
        assert_result(self, result, success=True)

        result = Result.convert_to_result(None, none_means_success=False)
        assert_result(self, result, success=False)

    def test_convert_to_result_give_result(self):
        result = Result.ok()
        self.assertEqual(result, Result.convert_to_result(result))

        result = Result.fail()
        self.assertEqual(result, Result.convert_to_result(result))

    def test_convert_to_result_give_value(self):
        result = Result.convert_to_result(5)
        assert_result(self, result, success=True, value=5)

    # endregion

    # region try_func

    def test_try_func_give_none(self):
        result = try_func(None)
        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message="The input function can not be None.", code=500)

    def test_try_func_give_func_with_parameters(self):
        result = try_func(lambda x: x)
        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='<lambda>() takes 1 arguments. It cannot be executed.', code=500)

    def test_try_func_give_func_ok(self):
        result = try_func(lambda: Result.ok(5))
        assert_result(self, result, success=True, value=5)

        result = try_func(lambda: 5)
        assert_result(self, result, success=True, value=5)

        result = try_func(lambda: None)
        assert_result(self, result, success=True)

        result = try_func(async_function)
        assert_result(self, result, success=True, value=5)

    def test_try_func_give_func_error(self):
        result = try_func(function_raise_exception, num_of_try=2)
        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. The details of the 2 errors are stored in the '
                                    'more_data field. At least one of the errors was an exception type, the first '
                                    'exception being stored in the exception field.',
                            code=500, exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_try_only_on_exceptions(self):
        result = try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, success=False)

        result = try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. There is no more information.', code=500)

        result = try_func(lambda: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. '
                                    'The details of the 2 errors are stored in the more_data field. ',
                            code=500, more_data=[FAKE_ERROR, FAKE_ERROR])

    def test_try_func_on_result_give_none(self):
        result = Result.ok().try_func(None)

        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='The input function can not be None.', code=500)

    def test_try_func_without_parameters_on_success_result(self):
        result = Result.ok().try_func(lambda: 5)

        assert_result(self, result, success=True, value=5)

    def test_try_func_without_parameters_give_func_raise_exception(self):
        result = Result.ok().try_func(function_raise_exception, num_of_try=2)

        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            code=500, exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_without_parameters_try_only_on_exceptions(self):
        result = Result.ok().try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, success=False)

        result = Result.ok().try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. There is no more information.',
                            code=500)

        result = Result.ok().try_func(lambda: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. '
                                    'The details of the 2 errors are stored in the more_data field. ',
                            code=500, more_data=[FAKE_ERROR, FAKE_ERROR])

    def test_try_func_without_parameters_on_failed_result(self):
        result = Result.fail().try_func(lambda: 5)

        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message="The previous function failed. "
                                    "The new function does not have a parameter to get the previous result. "
                                    "Either define a function that accepts a parameter or set skip_previous_error to True.",
                            code=500)

    def test_try_func_without_parameters_on_failed_result_with_skip_previous_error(self):
        result = Result.fail().try_func(lambda: 5, ignore_previous_error=True)

        assert_result(self, result, success=True, value=5)

    def test_try_func_with_parameters_try_only_on_exceptions(self):
        result = Result.ok().try_func(lambda x: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, success=False)

        result = Result.ok().try_func(lambda x: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. There is no more information.',
                            code=500)

        result = Result.ok().try_func(lambda x: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. '
                                    'The details of the 2 errors are stored in the more_data field. ',
                            code=500, more_data=[FAKE_ERROR, FAKE_ERROR])

    def test_try_func_use_prev_result_ok(self):
        result = Result.fail()
        func_result = result.try_func(lambda prev: prev)
        self.assertEqual(result, func_result)

        result = Result.ok(5)
        func_result = result.try_func(lambda prev: prev)
        self.assertEqual(result, func_result)

    def test_try_func_use_prev_result_error(self):
        result = Result.fail()
        func_result = result.try_func(lambda prev: function_raise_exception(), num_of_try=2)
        self.assertFalse(func_result.success)
        assert_error_detail(self, error_detail=func_result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            code=500, exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

        result = Result.ok(5)
        func_result = result.try_func(lambda prev: function_raise_exception(), num_of_try=2)
        self.assertFalse(func_result.success)
        assert_error_detail(self, error_detail=func_result.detail, title="An error occurred",
                            message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            code=500, exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_give_invalid_func(self):
        result = Result.ok().try_func(lambda x, y: x)

        self.assertFalse(result.success)
        assert_error_detail(self, error_detail=result.detail, title="An error occurred",
                            message='<lambda>() takes 2 arguments. It cannot be executed.', code=500)

    # endregion


if __name__ == "__main__":
    unittest.main()
