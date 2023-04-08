# pylint: disable=all

import unittest

from on_rails.Result import Result
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.ResultDetails.Success.CreatedDetail import CreatedDetail
from tests.helpers import (assert_error_detail, assert_result,
                           assert_result_with_type)

FAKE_EXCEPTION = Exception("fake")


def raise_exception():
    raise FAKE_EXCEPTION


class TestCombined(unittest.TestCase):
    def test1(self):
        result = Result.ok() \
            .on_success(lambda value: 5) \
            .on_success_add_more_data("success data") \
            .on_success_new_detail(
            CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(
            ErrorDetail("fake")) \
            .on_fail_tee(lambda: 5)
        assert_result_with_type(self, result, success=True, value=5, detail_type=CreatedDetail)

    def test2(self):
        result = Result.convert_to_result(5) \
            .on_success(lambda value: value + 5) \
            .on_success_add_more_data(
            "success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(
            ErrorDetail("fake")) \
            .on_fail_tee(lambda: 5) \
            .on_success_add_more_data(
            "success data 2")
        assert_result_with_type(self, result, success=True, value=10, detail_type=CreatedDetail)
        self.assertEqual(["success data 2"], result.detail.more_data)

    def test3(self):
        result = Result.ok(5, CreatedDetail()).fail_when(False) \
            .on_success(raise_exception) \
            .on_success_add_more_data(
            "success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(
            ErrorDetail("fake")) \
            .on_fail_tee(lambda: 5)
        assert_result_with_type(self, result, success=False, detail_type=ErrorDetail)
        assert_error_detail(self, error_detail=result.detail, title="fake", code=500)

    def test4(self):
        result = Result.ok(5, CreatedDetail()).fail_when(False) \
            .on_success(raise_exception, num_of_try=2) \
            .on_success_add_more_data(
            "success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_tee(lambda: 5)
        assert_result_with_type(self, result, success=False, detail_type=ErrorDetail)
        assert_error_detail(self, error_detail=result.detail, title='An error occurred', code=500,
                            message='Operation failed with 2 attempts. The details of the 2 errors are stored '
                                    'in the more_data field. At least one of the errors was an exception type, the first exception being stored in the exception field.',
                            exception=FAKE_EXCEPTION, more_data=[FAKE_EXCEPTION, FAKE_EXCEPTION, "fail data"])

    def test5(self):
        result = Result.fail() \
            .on_success(raise_exception) \
            .on_success_add_more_data("success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(ErrorDetail("fake")) \
            .on_fail_tee(lambda: 5)
        assert_result_with_type(self, result=result, success=False, detail_type=ErrorDetail)
        assert_error_detail(self, error_detail=result.detail, title="fake", code=500)

    def test6(self):
        result = Result.fail() \
            .on_success(raise_exception) \
            .on_success_add_more_data("success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(ErrorDetail("fake")) \
            .on_fail(lambda: 5)
        assert_result(self, result=result, success=True, value=5)

    def test7(self):
        func = lambda: Result.fail(ErrorDetail()) \
            .on_success(raise_exception) \
            .on_success_add_more_data("success data") \
            .on_success_new_detail(CreatedDetail()) \
            .on_success_tee(raise_exception) \
            .on_fail_add_more_data("fail data") \
            .on_fail_new_detail(ErrorDetail("fake")) \
            .on_fail_tee(lambda: 5) \
            .on_fail_raise_exception()
        self.assertRaises(Exception, func)
