# pylint: disable=all

import asyncio
import unittest
from typing import Optional

from on_rails.Result import (BreakRailsException, Result,
                             _get_num_of_function_parameters, try_func,
                             try_func_async)
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.ResultDetails.Errors.BadRequestError import BadRequestError
from on_rails.ResultDetails.Errors.ValidationError import ValidationError
from on_rails.ResultDetails.SuccessDetail import SuccessDetail
from on_rails.test_helpers import assert_result, assert_result_detail
from tests.helpers import (assert_error_detail, assert_exception,
                           assert_invalid_func, assert_result_with_type)

FAKE_EXCEPTION = Exception("fake")
FAKE_ERROR = ErrorDetail("fake")


def function_raise_exception():
    raise FAKE_EXCEPTION


async def function_raise_exception_async():
    raise FAKE_EXCEPTION


async def function_fails_async(error_detail: Optional[ErrorDetail] = None):
    await asyncio.sleep(0)
    return Result.fail(detail=error_detail)


async def async_function():
    await asyncio.sleep(0)
    return 5


async def async_function_with_parameter(number: int):
    await asyncio.sleep(0)
    return number + 1


class TestResult(unittest.TestCase):
    # region Generic

    def test_generic(self):
        # Simple
        result = Result.ok(1)
        assert_result(self, result, expected_success=True, expected_value=1)

        # Generic
        result = Result[int].ok(1)
        assert_result(self, result, expected_success=True, expected_value=1)

    # endregion

    # region __init__

    def test_init_without_optional_args(self):
        result = Result(True)

        assert_result(self, target_result=result, expected_success=True)

    def test_init_with_optional_args(self):
        detail = ResultDetail(title="test")
        value = 123
        result = Result(success=True, detail=detail, value=value)

        assert_result(self, target_result=result, expected_success=True, expected_detail=detail, expected_value=value)

    # endregion

    # region ok

    def test_ok_without_optional_args(self):
        result = Result.ok()

        assert_result(self, target_result=result, expected_success=True)

    def test_ok_with_optional_args(self):
        value = 123
        detail = ResultDetail(title="test")
        result = Result.ok(detail=detail, value=value)

        assert_result(self, target_result=result, expected_success=True, expected_detail=detail, expected_value=value)

    # endregion

    # region fail

    def test_fail_without_optional_args(self):
        result = Result.fail()

        assert_result(self, target_result=result, expected_success=False)

    def test_fail_with_optional_args(self):
        detail = ResultDetail(title="test")
        result = Result.fail(detail=detail)

        assert_result(self, target_result=result, expected_success=False, expected_detail=detail)

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

    def test_on_success_give_none(self):
        func_result = Result.ok().on_success(func=None)

        assert_result_with_type(test_class=self, target_result=func_result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(test_class=self, target_error_detail=func_result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.", expected_code=400)

    def test_on_success_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_success(lambda: Result.ok())

        self.assertEqual(fail_result, func_result)

    def test_on_success_with_success_result(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: Result.ok(5))

        assert_result(self, func_result, expected_success=True, expected_value=5)

    def test_on_success_with_None_result(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: None)

        assert_result(self, func_result, expected_success=True)

    def test_on_success_use_prev_value(self):
        func_result = Result.ok(1).on_success(lambda value: value + 1)

        assert_result(self, func_result, expected_success=True, expected_value=2)

    def test_on_success_use_prev_values(self):
        func_result = Result.ok(1).on_success(lambda value, result: value + result.value)

        assert_result(self, func_result, expected_success=True, expected_value=2)

    def test_on_success_give_func_fail(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(lambda: Result.fail())

        assert_result(self, func_result, expected_success=False)

    def test_on_success_give_too_many_args(self):
        func_result = Result.ok(1).on_success(lambda a, b, c: Result.ok())

        assert_result_with_type(self, func_result, expected_success=False, expected_detail_type=ValidationError)

    def test_on_success_give_func_raise_exception(self):
        success_result = Result.ok(1)

        func_result = success_result.on_success(function_raise_exception, num_of_try=2)

        self.assertFalse(func_result.success)
        assert_error_detail(self, func_result.detail, expected_title='An error occurred',
                            expected_message="Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.",
                            expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION],
                            expected_code=500)

    def test_on_success_give_builtin_functions(self):
        # The print is not supported function
        result = Result.ok(1).on_success(print)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="Function Parameter Detection Error",
                            expected_message='Can not recognize the number of function (print) parameters. '
                                             'You can wrap your built-in function with a python function like `lambda`.'
                            , expected_code=400)


    # endregion

    # region on_success_operate_when

    def test_on_success_operate_when_previous_failed(self):
        result = Result.fail().on_success_operate_when(True, lambda: Result.ok(1))

        assert_result(self, result, expected_success=False)

    def test_on_success_operate_when_use_previous_result(self):
        result = Result.ok(1).on_success_operate_when(lambda value, prev_result: value == prev_result.value,
                                                      lambda value, prev_result: Result.ok(value + prev_result.value))

        assert_result(self, result, expected_success=True, expected_value=2)

    def test_on_success_operate_when_break_rails_with_condition_false(self):
        result = Result.ok(1).on_success_operate_when(False, lambda: 5, break_rails=True)
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_success_operate_when_break_rails_with_condition_true(self):
        try:
            Result.ok(1).on_success_operate_when(True, lambda: 5, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result(self, e.result, expected_success=True, expected_value=5)

    def test_on_success_operate_when_break_rails_give_func_fail(self):
        try:
            Result.ok(1).on_success_operate_when(True, lambda: Result.fail(), break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result(self, e.result, expected_success=False)

    def test_on_success_operate_when_break_rails_give_func_raise_exception(self):
        try:
            Result.ok(1).on_success_operate_when(True, function_raise_exception, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result_with_type(self, e.result, expected_success=False, expected_detail_type=ErrorDetail)
            assert_error_detail(self, e.result.detail, expected_title='An error occurred',
                                expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in "
                                                 "the more_data field. At least one of the errors was an exception type, the "
                                                 "first exception being stored in the exception field.",
                                expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION],
                                expected_code=500)

    # endregion

    # region on_success_add_more_data

    def test_on_success_add_more_data_on_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_success_add_more_data("Data")

        assert_result(self, func_result, expected_success=False)
        self.assertIsNone(func_result.detail)

    def test_on_success_add_more_data_give_none(self):
        result = Result.ok(1)

        new_result = result.on_success_add_more_data(None)

        assert_result(self, new_result, expected_success=True, expected_value=1)
        self.assertIsNone(new_result.detail)

    def test_on_success_add_more_data_give_object(self):
        result = Result.ok(1)

        new_result = result.on_success_add_more_data("Data")

        assert_result_with_type(self, new_result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)
        self.assertEqual(["Data"], new_result.detail.more_data)

    def test_on_success_add_more_data_with_exist_detail(self):
        result = Result.ok(1, detail=SuccessDetail(more_data=["Data1"]))

        new_result = result.on_success_add_more_data("Data2")

        assert_result_with_type(self, new_result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)
        self.assertEqual(["Data1", "Data2"], new_result.detail.more_data)

    def test_on_success_add_more_data_give_func_ok(self):
        result = Result.ok(1).on_success_add_more_data(lambda: 5)
        assert_result_with_type(self, result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)
        assert_result_detail(test_class=self, target_result_detail=result.detail,
                             expected_title="Operation was successful",
                             expected_code=200, expected_more_data=[5])

        result = Result.ok(1).on_success_add_more_data(lambda value: value + 1)
        assert_result_with_type(self, result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)
        assert_result_detail(test_class=self, target_result_detail=result.detail,
                             expected_title="Operation was successful",
                             expected_code=200, expected_more_data=[2])

        result = Result.ok(1).on_success_add_more_data(lambda value, prev_result: value + prev_result.value)
        assert_result_with_type(self, result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)
        assert_result_detail(test_class=self, target_result_detail=result.detail,
                             expected_title="Operation was successful",
                             expected_code=200, expected_more_data=[2])

    def test_on_success_add_more_data_give_func_fail(self):
        result = Result.ok(1).on_success_add_more_data(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. "
                                             "The details of the 1 errors are stored in the more_data field. ",
                            expected_code=500, expected_more_data=[FAKE_ERROR])

        result = Result.ok(1).on_success_add_more_data(lambda: Result.fail(FAKE_ERROR), ignore_errors=True)
        assert_result(self, result, expected_success=True, expected_value=1)
        self.assertIsNone(result.detail)

    # endregion

    # region on_success_new_detail

    def test_on_success_new_detail_on_fail_result(self):
        result = Result.fail()

        new_result = result.on_success_new_detail(SuccessDetail)

        assert_result(self, new_result, expected_success=False)
        self.assertIsNone(new_result.detail)

    def test_on_success_new_detail(self):
        result = Result.ok(1, SuccessDetail())

        new_result = result.on_success_new_detail(None)

        assert_result(self, new_result, expected_success=True, expected_value=1)
        self.assertIsNone(new_result.detail)

    def test_on_success_new_detail_give_invalid_detail(self):
        result = Result.ok(1).on_success_new_detail(ErrorDetail())
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Type of new detail 'ErrorDetail' is not instance of 'SuccessDetail'",
                            expected_code=500)

        result = Result.ok(1).on_success_new_detail(lambda: ErrorDetail())
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Type of new detail 'ErrorDetail' is not instance of 'SuccessDetail'",
                            expected_code=500)

    def test_on_success_new_detail_give_func_ok(self):
        result = Result.ok(1).on_success_new_detail(lambda: SuccessDetail())

        assert_result_with_type(self, result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)

    def test_on_success_new_detail_give_func_fail(self):
        result = Result.ok(1).on_success_new_detail(lambda: Result.fail())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    # endregion

    # region on_success_tee

    def test_on_success_tee_give_invalid_func(self):
        # None
        result = Result.ok(1).on_success_tee(None)
        assert_invalid_func(self, result)

        # Not callable
        result = Result.ok(1).on_success_tee("Not callable")
        assert_invalid_func(self, result)

    def test_on_success_tee_on_fail_result(self):
        result = Result.fail().on_success_tee(lambda: 5)
        assert_result(self, result, expected_success=False)

    def test_on_success_tee_success_func(self):
        result = Result.ok(1).on_success_tee(lambda: 5)
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_success_tee_fail_func(self):
        result = Result.ok(1).on_success_tee(lambda: Result.fail())
        assert_result(self, result, expected_success=False)

    def test_on_success_tee_fail_func_set_ignore_errors(self):
        result = Result.ok(1).on_success_tee(lambda: Result.fail(), ignore_errors=True)
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_success_tee_use_prev_value(self):
        result = Result.ok(1).on_success_tee(lambda value: Result.fail(ErrorDetail(message=f"prev value: {value}")))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title='An error occurred',
                            expected_message="prev value: 1", expected_code=500)

    def test_on_success_tee_use_prev_value_and_result(self):
        result = Result.ok(1, SuccessDetail()).on_success_tee(
            lambda value, prev_result: Result.fail(ErrorDetail(
                message=f"prev value: {value}. prev detail type: {type(prev_result.detail).__name__}")))

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title='An error occurred',
                            expected_message="prev value: 1. prev detail type: SuccessDetail", expected_code=500)

    def test_on_success_tee_give_too_many_args(self):
        result = Result.ok(1, SuccessDetail()).on_success_tee(lambda a, b, c: Result.fail())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(test_class=self, target_error_detail=result.detail,
                            expected_title='One or more validation errors occurred',
                            expected_message="<lambda>() takes 3 arguments. It cannot be executed. "
                                             "maximum of 2 parameters is acceptable.", expected_code=400)

    # endregion

    # region on_success_new_detail

    def test_on_fail_new_detail_on_success_result(self):
        result = Result.ok(1, SuccessDetail())

        new_result = result.on_fail_new_detail(ErrorDetail())

        assert_result_with_type(self, new_result, expected_success=True, expected_value=1,
                                expected_detail_type=SuccessDetail)

    def test_on_fail_new_detail(self):
        result = Result.fail(ErrorDetail())

        new_result = result.on_fail_new_detail(None)

        assert_result(self, new_result, expected_success=False)
        self.assertIsNone(new_result.detail)

    def test_on_fail_new_detail_give_invalid_detail(self):
        result = Result.fail().on_fail_new_detail(SuccessDetail())
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Type of new detail 'SuccessDetail' is not instance of 'ErrorDetail'.",
                            expected_code=500)

        result = Result.fail().on_fail_new_detail(lambda: SuccessDetail())
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Type of new detail 'SuccessDetail' is not instance of 'ErrorDetail'.",
                            expected_code=500)

    def test_on_fail_new_detail_give_func_ok(self):
        result = Result.fail().on_fail_new_detail(lambda: ErrorDetail())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_on_fail_new_detail_give_func_fail(self):
        result = Result.fail().on_fail_new_detail(lambda: Result.fail())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    # endregion

    # region on_success_break

    def test_on_success_break_on_fail_result(self):
        result = Result.fail().on_success_break(True)

        assert_result(self, result, expected_success=False)

    def test_on_success_break_with_condition_false(self):
        result = Result.ok(1).on_success_break(False)
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.ok(1).on_success_break(lambda: False)
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.ok(1).on_success_break(lambda: Result.ok(False))
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_success_break_give_func_fails(self):
        result = Result.ok(1).on_success_break(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="fake", expected_code=500)

        result = Result.ok(1).on_success_break(function_raise_exception)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in the "
                                             "more_data field. At least one of the errors was an exception type, the first "
                                             "exception being stored in the exception field.", expected_code=500,
                            expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION])

    def test_on_success_break_with_condition_true(self):
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).on_success_break(True))
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).on_success_break(lambda: True))
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).on_success_break(lambda: Result.ok(True)))

    def test_on_success_break_use_prev_results(self):
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).on_success_break(lambda value: value == 1))
        self.assertRaises(BreakRailsException,
                          lambda: Result.ok(1).on_success_break(lambda value, prev_result: value == prev_result.value))

    # endregion

    # region on_success_fail_when

    def test_on_success_fail_when_on_fail_result(self):
        result = Result.fail().on_success_fail_when(True, ErrorDetail())

        assert_result(self, result, expected_success=False)
        self.assertIsNone(result.detail)

    def test_on_success_fail_when_condition_is_false(self):
        result = Result.ok(1).on_success_fail_when(False)

        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_success_fail_with_default_error_detail(self):
        result = Result.ok(1).on_success_fail_when(True)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_on_success_fail_when_default_custom_detail(self):
        result = Result.ok(1).on_success_fail_when(True, BadRequestError())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=BadRequestError)

    def test_on_success_fail_when_give_func_for_condition(self):
        result = Result.ok(1).on_success_fail_when(lambda value, prev_result: value and prev_result.success)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_on_success_fail_when_give_func_with_too_many_args(self):
        result = Result.ok(1).on_success_fail_when(lambda value, prev_result, b: prev_result.success)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_code=400, expected_message="<lambda>() takes 3 arguments. It cannot be executed. "
                                                                "maximum of 2 parameters is acceptable.")

    # endregion

    # region on_fail

    def test_on_fail_give_invalid_func(self):
        # None
        result = Result.fail().on_fail(None)
        assert_invalid_func(self, result)

        # Not callable
        result = Result.fail().on_fail("not callable")
        assert_invalid_func(self, result)

    def test_on_fail_with_success_result(self):
        success_result = Result.ok(5)

        func_result = success_result.on_fail(function_raise_exception)

        assert_result(self, func_result, expected_success=True, expected_value=5)

    def test_on_fail_with_fail_result(self):
        fail_result = Result.fail()

        func_result = fail_result.on_fail(lambda: Result.ok(5))

        assert_result(self, func_result, expected_success=True, expected_value=5)

    def test_on_fail_with_None_result(self):
        result = Result.fail()

        func_result = result.on_fail(lambda: None)

        assert_result(self, func_result, expected_success=True)

    def test_on_fail_use_prev_result(self):
        result = Result.fail()

        func_result = result.on_fail(lambda prev: prev)

        self.assertEqual(result, func_result)

    def test_on_fail_give_func_raise_exception(self):
        success_result = Result.fail()

        func_result = success_result.on_fail(function_raise_exception, num_of_try=2)

        self.assertFalse(func_result.success)
        assert_error_detail(self, func_result.detail, expected_title='An error occurred',
                            expected_message="Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.",
                            expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION],
                            expected_code=500)

    # endregion

    # region on_fail_operate_when

    def test_on_fail_operate_when_previous_success(self):
        result = Result.ok(1).on_fail_operate_when(True, lambda: Result.fail())

        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_fail_operate_when_use_previous_result(self):
        result = Result.fail().on_fail_operate_when(lambda prev_result: not prev_result.success,
                                                    lambda prev_result: Result.ok(prev_result.success))

        assert_result(self, result, expected_success=True, expected_value=False)

    def test_on_fail_operate_when_break_rails_with_condition_false(self):
        result = Result.fail().on_fail_operate_when(False, lambda: 5, break_rails=True)
        assert_result(self, result, expected_success=False)

    def test_on_fail_operate_when_break_rails_with_condition_true(self):
        try:
            Result.fail().on_fail_operate_when(True, lambda: 5, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result(self, e.result, expected_success=True, expected_value=5)

    def test_on_fail_operate_when_break_rails_give_func_fail(self):
        try:
            Result.fail().on_fail_operate_when(True, lambda: Result.fail(FAKE_ERROR), break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result_with_type(self, e.result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_on_fail_operate_when_break_rails_give_func_raise_exception(self):
        try:
            Result.fail().on_fail_operate_when(True, function_raise_exception, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result_with_type(self, e.result, expected_success=False, expected_detail_type=ErrorDetail)
            assert_error_detail(self, e.result.detail, expected_title='An error occurred',
                                expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in "
                                                 "the more_data field. At least one of the errors was an exception type, the "
                                                 "first exception being stored in the exception field.",
                                expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION],
                                expected_code=500)

    # endregion

    # region on_fail_add_more_data

    def test_on_fail_add_more_data_on_success_result(self):
        success_result = Result.ok()

        func_result = success_result.on_fail_add_more_data("Data")

        assert_result(self, func_result, expected_success=True)
        self.assertIsNone(func_result.detail)

    def test_on_fail_add_more_data_give_none(self):
        result = Result.fail()

        new_result = result.on_fail_add_more_data(None)

        assert_result(self, new_result, expected_success=False, )
        self.assertIsNone(new_result.detail)

    def test_on_fail_add_more_data_give_object(self):
        result = Result.fail()

        new_result = result.on_fail_add_more_data("Data")

        assert_result_with_type(self, new_result, expected_success=False, expected_detail_type=ErrorDetail)
        self.assertEqual(["Data"], new_result.detail.more_data)

    def test_on_fail_add_more_data_with_exist_detail(self):
        result = Result.fail(detail=ErrorDetail(more_data=["Data1"]))

        new_result = result.on_fail_add_more_data("Data2")

        assert_result_with_type(self, new_result, expected_success=False, expected_detail_type=ErrorDetail)
        self.assertEqual(["Data1", "Data2"], new_result.detail.more_data)

    def test_on_fail_add_more_data_give_func_ok(self):
        result = Result.fail().on_fail_add_more_data(lambda: 5)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_result_detail(test_class=self, target_result_detail=result.detail, expected_title="An error occurred",
                             expected_code=500, expected_more_data=[5])

        result = Result.fail().on_fail_add_more_data(lambda prev_result: f"Success: {prev_result.success}")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_result_detail(test_class=self, target_result_detail=result.detail, expected_title="An error occurred",
                             expected_code=500, expected_more_data=["Success: False"])

    def test_on_fail_add_more_data_give_func_fail(self):
        result = Result.fail().on_fail_add_more_data(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. "
                                             "The details of the 1 errors are stored in the more_data field. ",
                            expected_code=500, expected_more_data=[FAKE_ERROR])

    # endregion

    # region on_fail_tee

    def test_on_fail_tee_give_invalid_func(self):
        # None
        result = Result.fail().on_fail_tee(None)
        assert_invalid_func(self, result)

        # Not callable
        result = Result.fail().on_fail_tee("string")
        assert_invalid_func(self, result)

    def test_on_fail_tee_success_func(self):
        result = Result.fail().on_fail_tee(lambda: Result.ok())
        assert_result(self, result, expected_success=False)

    def test_on_fail_tee_fail_func(self):
        result = Result.fail().on_fail_tee(lambda: Result.fail(FAKE_ERROR))

        assert_result(self, result, expected_success=False, expected_detail=FAKE_ERROR)
        assert_error_detail(test_class=self, target_error_detail=result.detail, expected_title='fake',
                            expected_code=500)

    def test_on_fail_tee_fail_func_set_ignore_errors(self):
        result = Result.fail().on_fail_tee(lambda: Result.fail(FAKE_ERROR), ignore_errors=True)

        assert_result(self, result, expected_success=False)
        self.assertIsNone(result.detail)

    # endregion

    # region on_fail_raise_exception

    def test_on_fail_raise_exception_on_success(self):
        result = Result.ok()

        new_result = result.on_fail_raise_exception()

        self.assertEqual(result, new_result)

    def test_on_fail_raise_exception(self):
        result = Result.fail()

        try:
            result.on_fail_raise_exception()
            self.assertTrue(False)  # This code should not be executed.
        except Exception as e:
            self.assertEqual(Exception, type(e))
            self.assertEqual('', str(e))

    def test_on_fail_raise_exception_give_exception_type(self):
        result = Result.fail()

        try:
            result.on_fail_raise_exception(TypeError)
            self.assertTrue(False)  # This code should not be executed.
        except Exception as e:
            self.assertEqual(TypeError, type(e))
            self.assertEqual('', str(e))

    def test_on_fail_raise_exception_with_detail(self):
        result = Result.fail(ErrorDetail(message="fake"))

        try:
            result.on_fail_raise_exception()
            self.assertTrue(False)  # This code should not be executed.
        except Exception as e:
            self.assertEqual(Exception, type(e))
            self.assertTrue(str(e) != "" or None)

    # endregion

    # region on_fail_break

    def test_on_fail_break_on_success_result(self):
        result = Result.ok(1).on_fail_break(True)

        assert_result(self, result, expected_success=True, expected_value=1)

    def test_on_fail_break_with_condition_false(self):
        result = Result.fail().on_fail_break(False)
        assert_result(self, result, expected_success=False)

        result = Result.fail().on_fail_break(lambda: False)
        assert_result(self, result, expected_success=False)

        result = Result.fail().on_fail_break(lambda: Result.ok(False))
        assert_result(self, result, expected_success=False)

    def test_on_fail_break_give_func_fails(self):
        result = Result.fail().on_fail_break(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="fake", expected_code=500)

        result = Result.fail().on_fail_break(function_raise_exception)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in the "
                                             "more_data field. At least one of the errors was an exception type, the first "
                                             "exception being stored in the exception field.", expected_code=500,
                            expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION])

    def test_on_fail_break_with_condition_true(self):
        self.assertRaises(BreakRailsException, lambda: Result.fail().on_fail_break(True))
        self.assertRaises(BreakRailsException, lambda: Result.fail().on_fail_break(lambda: True))
        self.assertRaises(BreakRailsException, lambda: Result.fail().on_fail_break(lambda: Result.ok(True)))

    def test_on_fail_break_use_prev_results(self):
        self.assertRaises(BreakRailsException,
                          lambda: Result.fail().on_fail_break(lambda prev_result: not prev_result.success))

    # endregion

    # region fail_when

    def test_fail_when_condition_is_false(self):
        result = Result.ok(1).fail_when(False)

        assert_result(self, result, expected_success=True, expected_value=1)

    def test_fail_when_default_error_detail(self):
        result = Result.ok(1).fail_when(True)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_fail_when_default_custom_detail(self):
        result = Result.ok(1).fail_when(True, BadRequestError())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=BadRequestError)

    def test_fail_when_add_prev_detail(self):
        # Default
        result = Result.ok(1).fail_when(True)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_code=500)

        # Prev is None
        result = Result.ok(1).fail_when(True, add_prev_detail=True)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_code=500)

        result = Result.fail(FAKE_ERROR).fail_when(True, add_prev_detail=True)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_code=500,
                            expected_more_data=[{'prev_detail': FAKE_ERROR}])

    def test_fail_when_give_func_for_condition(self):
        result = Result.ok(1).fail_when(lambda prev_result: prev_result.success)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_fail_when_give_func_with_too_many_args(self):
        result = Result.ok(1).fail_when(lambda prev_result, b: prev_result.success)

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_code=400, expected_message="<lambda>() takes 2 arguments. It cannot be executed. "
                                                                "maximum of 1 parameters is acceptable.")

    # endregion

    # region convert_to_result

    def test_convert_to_result_give_none(self):
        result = Result.convert_to_result(None)
        assert_result(self, result, expected_success=True)

        result = Result.convert_to_result(None, none_means_success=False)
        assert_result(self, result, expected_success=False)

    def test_convert_to_result_give_result(self):
        result = Result.ok()
        self.assertEqual(result, Result.convert_to_result(result))

        result = Result.fail()
        self.assertEqual(result, Result.convert_to_result(result))

    def test_convert_to_result_give_value(self):
        result = Result.convert_to_result(5)
        assert_result(self, result, expected_success=True, expected_value=5)

    # endregion

    # region try_func

    def test_try_func_give_none(self):
        result = try_func(None)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.", expected_code=400)

    def test_try_func_give_func_with_parameters(self):
        result = try_func(lambda x: x)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='<lambda>() takes 1 arguments. It cannot be executed.', expected_code=400)

    def test_try_func_give_func_ok(self):
        result = try_func(lambda: Result.ok(5))
        assert_result(self, result, expected_success=True, expected_value=5)

        result = try_func(lambda: 5)
        assert_result(self, result, expected_success=True, expected_value=5)

        result = try_func(lambda: None)
        assert_result(self, result, expected_success=True)

        result = try_func(async_function)
        assert_result(self, result, expected_success=True, expected_value=5)

    def test_try_func_give_func_error(self):
        result = try_func(function_raise_exception, num_of_try=2)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. The details of the 2 errors are stored in the '
                                             'more_data field. At least one of the errors was an exception type, the first '
                                             'exception being stored in the exception field.',
                            expected_code=500, expected_exception=FAKE_EXCEPTION,
                            expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_try_only_on_exceptions(self):
        result = try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, expected_success=False)

        result = try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. There is no more information.',
                            expected_code=500)

        result = try_func(lambda: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. '
                                             'The details of the 2 errors are stored in the more_data field. ',
                            expected_code=500, expected_more_data=[FAKE_ERROR, FAKE_ERROR])

    def test_try_func_on_result_give_none(self):
        result = Result.ok().try_func(None)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='The input function is not valid.', expected_code=400)

    def test_try_func_without_parameters_on_success_result(self):
        result = Result.ok().try_func(lambda: 5)

        assert_result(self, result, expected_success=True, expected_value=5)

    def test_try_func_without_parameters_give_func_raise_exception(self):
        result = Result.ok().try_func(function_raise_exception, num_of_try=2)

        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            expected_code=500, expected_exception=FAKE_EXCEPTION,
                            expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_without_parameters_try_only_on_exceptions(self):
        result = Result.ok().try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, expected_success=False)

        result = Result.ok().try_func(lambda: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. There is no more information.',
                            expected_code=500)

        result = Result.ok().try_func(lambda: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. '
                                             'The details of the 2 errors are stored in the more_data field. ',
                            expected_code=500, expected_more_data=[FAKE_ERROR, FAKE_ERROR])

    def test_try_func_without_parameters_on_failed_result(self):
        result = Result.fail().try_func(lambda: 5)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message="The previous function failed. "
                                             "The new function does not have a parameter to get the previous result. "
                                             "Either define a function that accepts a parameter or set skip_previous_error to True.",
                            expected_code=400)

    def test_try_func_without_parameters_on_failed_result_with_skip_previous_error(self):
        result = Result.fail().try_func(lambda: 5, ignore_previous_error=True)

        assert_result(self, result, expected_success=True, expected_value=5)

    def test_try_func_with_parameters_try_only_on_exceptions(self):
        result = Result.ok().try_func(lambda x: Result.fail(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, expected_success=False)

        result = Result.ok().try_func(lambda x: Result.fail(), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. There is no more information.',
                            expected_code=500)

        result = Result.ok().try_func(lambda x: Result.fail(FAKE_ERROR), num_of_try=2, try_only_on_exceptions=False)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. '
                                             'The details of the 2 errors are stored in the more_data field. ',
                            expected_code=500, expected_more_data=[FAKE_ERROR, FAKE_ERROR])

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
        assert_error_detail(self, target_error_detail=func_result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            expected_code=500, expected_exception=FAKE_EXCEPTION,
                            expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

        result = Result.ok(5)
        func_result = result.try_func(lambda prev: function_raise_exception(), num_of_try=2)
        self.assertFalse(func_result.success)
        assert_error_detail(self, target_error_detail=func_result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. The details of the 2 errors are stored in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            expected_code=500, expected_exception=FAKE_EXCEPTION,
                            expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    def test_try_func_give_invalid_func(self):
        result = Result.ok().try_func(lambda x, y: x)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='<lambda>() takes 2 arguments. It cannot be executed.', expected_code=400)

    def test_try_func_give_BreakRailsException(self):
        result = Result.ok(1).try_func(lambda prev: prev \
                                       .on_success(lambda value: value + 1) \
                                       .break_rails(True) \
                                       .on_success(lambda value: value + 1)
                                       )
        assert_result(self, result, expected_success=True, expected_value=2)

    def test_try_func_give_builtin_functions(self):
        # The sum is supported builtin function
        result = Result.ok(1).try_func(sum)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='sum() takes 2 arguments. It cannot be executed.',
                            expected_code=400)

        # The print is not supported function
        result = Result.ok(1).try_func(print)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="Function Parameter Detection Error",
                            expected_message='Can not recognize the number of function (print) parameters. '
                                             'You can wrap your built-in function with a python function like `lambda`.'
                            , expected_code=400)

    # endregion

    # region operate_when

    def test_operate_when_give_bool_condition(self):
        result = Result.ok(1).operate_when(True, lambda: Result.fail())
        assert_result(self, result, expected_success=False)

        result = Result.ok(1).operate_when(False, lambda: Result.fail())
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_operate_when_give_func_as_condition_failed(self):
        result = Result.ok(1).operate_when(lambda: Result.fail(FAKE_ERROR), lambda: Result.fail())

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="fake", expected_code=500)

    def test_operate_when_give_func_as_condition(self):
        # True
        result = Result.ok(1).operate_when(lambda: True, lambda: Result.fail())
        assert_result(self, result, expected_success=False)
        result = Result.ok(1).operate_when(lambda: Result.ok(), lambda: Result.fail())
        assert_result(self, result, expected_success=False)
        result = Result.ok(1).operate_when(lambda: Result.ok("Value is not instance of bool"), lambda: Result.fail())
        assert_result(self, result, expected_success=False)
        result = Result.ok(1).operate_when(lambda: Result.ok(True), lambda: Result.fail())
        assert_result(self, result, expected_success=False)
        result = Result.ok(1).operate_when(lambda prev: Result.ok(prev.value), lambda: Result.fail())
        assert_result(self, result, expected_success=False)

        # False
        result = Result.ok(1).operate_when(lambda: False, lambda: Result.fail())
        assert_result(self, result, expected_success=True, expected_value=1)
        result = Result.ok(1).operate_when(lambda: Result.ok(False), lambda: Result.fail())
        assert_result(self, result, expected_success=True, expected_value=1)
        result = Result.ok(1).operate_when(lambda prev: Result.ok(not prev.value), lambda: Result.fail())
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_operate_when_give_func_with_too_many_args(self):
        result = Result.ok(1).operate_when(lambda a, b: True, lambda: Result.fail())

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='<lambda>() takes 2 arguments. It cannot be executed. '
                                             'maximum of 1 parameters is acceptable.', expected_code=400)

    def test_operate_when_give_invalid_condition_type(self):
        result = Result.ok(1).operate_when("This is not boolean or function", lambda: Result.fail())

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='The condition only can be a function or a boolean. '
                                             'str is not acceptable.', expected_code=400)

    def test_operate_when_break_rails_with_condition_false(self):
        result = Result.fail().operate_when(False, lambda: 5, break_rails=True)
        assert_result(self, result, expected_success=False)

    def test_operate_when_break_rails_with_condition_true(self):
        try:
            Result.fail().operate_when(True, lambda: 5, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result(self, e.result, expected_success=True, expected_value=5)

    def test_operate_when_break_rails_give_func_fail(self):
        try:
            Result.fail().operate_when(True, lambda: Result.fail(FAKE_ERROR), break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result_with_type(self, e.result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_operate_when_break_rails_give_func_raise_exception(self):
        try:
            Result.fail().operate_when(True, function_raise_exception, break_rails=True)
            self.assertTrue(False)  # should not reach here
        except BreakRailsException as e:
            assert_result_with_type(self, e.result, expected_success=False, expected_detail_type=ErrorDetail)
            assert_error_detail(self, e.result.detail, expected_title='An error occurred',
                                expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in "
                                                 "the more_data field. At least one of the errors was an exception type, the "
                                                 "first exception being stored in the exception field.",
                                expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION],
                                expected_code=500)

    # endregion

    # region finally_tee

    def test_finally_tee_ok(self):
        result = Result.ok(1).finally_tee(lambda: Result.ok(5))
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.fail().finally_tee(lambda: Result.ok(5))
        assert_result(self, result, expected_success=False)

    def test_finally_tee_use_prev_result_ok(self):
        result = Result.ok(1).finally_tee(lambda prev_result: Result.ok(prev_result.value + 1))
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.fail().finally_tee(lambda prev_result: Result.ok(prev_result.success))
        assert_result(self, result, expected_success=False)

    def test_finally_tee_fail(self):
        result = Result.ok(1).finally_tee(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

        result = Result.fail().finally_tee(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)

    def test_finally_tee_use_prev_result_fail(self):
        result = Result.ok(1).finally_tee(lambda prev_result: Result.fail(ErrorDetail(message=f"{prev_result.value}")))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="1", expected_code=500)

        result = Result.fail().finally_tee(
            lambda prev_result: Result.fail(ErrorDetail(message=f"{prev_result.success}")))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message="False", expected_code=500)

    # endregion

    # region BreakRails Exception

    def test_break_rails_ok(self):
        # Success
        result = Result.ok(1, SuccessDetail())
        exception = BreakRailsException(result)

        assert_exception(self, exception, BreakRailsException)
        self.assertEqual(result, exception.result)

        # Failure
        result = Result.fail(ErrorDetail())
        exception = BreakRailsException(result)

        assert_exception(self, exception, BreakRailsException)
        self.assertEqual(result, exception.result)

    def test_break_rails_give_none(self):
        self.assertRaises(ValueError, lambda: BreakRailsException(None))
        self.assertRaises(ValueError, lambda: BreakRailsException("Not result type"))

    # endregion

    # region break_rails

    def test_break_rails_with_condition_false(self):
        result = Result.ok(1).break_rails(False)
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.ok(1).break_rails(lambda: False)
        assert_result(self, result, expected_success=True, expected_value=1)

        result = Result.ok(1).break_rails(lambda: Result.ok(False))
        assert_result(self, result, expected_success=True, expected_value=1)

    def test_break_rails_give_func_fails(self):
        result = Result.ok(1).break_rails(lambda: Result.fail(FAKE_ERROR))
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="fake", expected_code=500)

        result = Result.ok(1).break_rails(function_raise_exception)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message="Operation failed with 1 attempts. The details of the 1 errors are stored in the "
                                             "more_data field. At least one of the errors was an exception type, the first "
                                             "exception being stored in the exception field.", expected_code=500,
                            expected_exception=FAKE_EXCEPTION, expected_more_data=[FAKE_EXCEPTION])

    def test_break_rails_with_condition_true(self):
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).break_rails(True))
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).break_rails(lambda: True))
        self.assertRaises(BreakRailsException, lambda: Result.ok(1).break_rails(lambda: Result.ok(True)))

    def test_break_rails_use_prev_results(self):
        self.assertRaises(BreakRailsException,
                          lambda: Result.ok(1).break_rails(lambda prev_result: prev_result.value == 1))

    # endregion

    # region get_num_of_function_parameters

    def test_get_num_of_function_parameters_normal_functions(self):
        result = _get_num_of_function_parameters(lambda: 5)
        assert_result(self, result, expected_success=True, expected_value=0)

        result = _get_num_of_function_parameters(function_raise_exception)
        assert_result(self, result, expected_success=True, expected_value=0)

        result = _get_num_of_function_parameters(lambda x: 5)
        assert_result(self, result, expected_success=True, expected_value=1)

        def function_with_parameters(a: int, b: int = 2):
            pass

        result = _get_num_of_function_parameters(function_with_parameters)
        assert_result(self, result, expected_success=True, expected_value=2)

    def test_get_num_of_function_parameters_supported_builtin_functions(self):
        result = _get_num_of_function_parameters(sum)
        assert_result(self, result, expected_success=True, expected_value=2)

    def test_get_num_of_function_parameters_unsupported_builtin_functions(self):
        result = _get_num_of_function_parameters(print)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="Function Parameter Detection Error",
                            expected_message="Can not recognize the number of function (print) parameters. "
                                             "You can wrap your built-in function with a python "
                                             "function like `lambda`.", expected_code=400)

    # endregion


class TestResultAsync(unittest.IsolatedAsyncioTestCase):
    # region try_func_async

    async def test_try_func_async_give_none(self):
        result = await try_func_async(None)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.", expected_code=400)

    async def test_try_func_async_give_func_with_parameters(self):
        result = await try_func_async(async_function_with_parameter)

        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='async_function_with_parameter() takes 1 arguments. It cannot be executed.',
                            expected_code=400)

    async def test_try_func_async_give_func_ok(self):
        result = await try_func_async(lambda: async_function())
        assert_result(self, result, expected_success=True, expected_value=5)

        result = await try_func_async(lambda: 5)
        assert_result(self, result, expected_success=True, expected_value=5)

        result = await try_func_async(lambda: None)
        assert_result(self, result, expected_success=True)

        result = await try_func_async(async_function)
        assert_result(self, result, expected_success=True, expected_value=5)

    async def test_try_func_async_give_func_error(self):
        result = await try_func_async(function_raise_exception_async, num_of_try=2)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. The details of the 2 errors are stored in the '
                                             'more_data field. At least one of the errors was an exception type, the first '
                                             'exception being stored in the exception field.',
                            expected_code=500, expected_exception=FAKE_EXCEPTION,
                            expected_more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION])

    async def test_try_func_async_try_only_on_exceptions(self):
        result = await try_func_async(lambda: function_fails_async(), num_of_try=2, try_only_on_exceptions=True)
        assert_result(self, result, expected_success=False)

        result = await try_func_async(lambda: function_fails_async(), num_of_try=2, try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. There is no more information.',
                            expected_code=500)

        result = await try_func_async(lambda: function_fails_async(FAKE_ERROR), num_of_try=2,
                                      try_only_on_exceptions=False)
        self.assertFalse(result.success)
        assert_error_detail(self, target_error_detail=result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 2 attempts. '
                                             'The details of the 2 errors are stored in the more_data field. ',
                            expected_code=500, expected_more_data=[FAKE_ERROR, FAKE_ERROR])

    async def test_try_func_async_give_builtin_functions(self):
        # The sum is supported builtin function
        result = await try_func_async(sum)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='sum() takes 2 arguments. It cannot be executed.',
                            expected_code=400)

        # The print is not supported function
        result = await try_func_async(print)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="Function Parameter Detection Error",
                            expected_message='Can not recognize the number of function (print) parameters. '
                                             'You can wrap your built-in function with a python function like `lambda`.'
                            , expected_code=400)

    def test_try_func_give_builtin_functions(self):
        # The sum is supported builtin function
        result = try_func(sum)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message='sum() takes 2 arguments. It cannot be executed.',
                            expected_code=400)

        # The print is not supported function
        result = try_func(print)
        assert_result_with_type(test_class=self, target_result=result, expected_success=False,
                                expected_detail_type=ErrorDetail)
        assert_error_detail(self, target_error_detail=result.detail,
                            expected_title="Function Parameter Detection Error",
                            expected_message='Can not recognize the number of function (print) parameters. '
                                             'You can wrap your built-in function with a python function like `lambda`.'
                            , expected_code=400)

    # endregion


if __name__ == "__main__":
    unittest.main()
