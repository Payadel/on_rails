# pylint: disable=all

import unittest
from typing import Any, Dict, List, Optional

from on_rails.Result import Result
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail
from on_rails.ResultDetails.Errors import ExceptionError
from on_rails.ResultDetails.Errors.ValidationError import ValidationError


def assert_result(test_class: unittest.TestCase, result: Result, success: bool,
                  detail: Optional[ResultDetail] = None, value: Optional[Any] = None) -> None:
    test_class.assertEqual(success, result.success, msg="success")
    test_class.assertEqual(detail, result.detail, msg="detail")
    test_class.assertEqual(value, result.value, msg="value")


def assert_result_with_type(test_class: unittest.TestCase, result: Result, success: bool,
                            detail_type=None, value: Optional[Any] = None) -> None:
    test_class.assertEqual(success, result.success, msg="success")
    test_class.assertTrue(isinstance(result.detail, detail_type), msg="detail type")
    test_class.assertEqual(value, result.value, msg="value")


def assert_result_detail(test_class: unittest.TestCase, result_detail: ResultDetail, title: str,
                         message: Optional[str] = None, code: Optional[int] = None,
                         more_data: Optional[List[Any]] = None) -> None:
    if more_data is None:
        more_data = []
    test_class.assertEqual(title, result_detail.title, msg="title")
    test_class.assertEqual(message, result_detail.message, msg="message")
    test_class.assertEqual(code, result_detail.code, msg="code")

    test_class.assertIsNotNone(result_detail.more_data, msg="more data")  # It should never be None.
    test_class.assertEqual(result_detail.more_data, more_data, msg="more data")


def assert_error_detail(test_class: unittest.TestCase, error_detail: ErrorDetail, title: str,
                        message: Optional[str] = None, code: Optional[int] = None,
                        more_data: Optional[List[Any]] = None,
                        errors: Optional[Dict[str, str]] = None, exception: Optional[Exception] = None) -> None:
    if more_data is None:
        more_data = []
    assert_result_detail(test_class=test_class, result_detail=error_detail,
                         title=title, message=message, code=code, more_data=more_data)
    test_class.assertEqual(errors, error_detail.errors, msg="errors")
    test_class.assertEqual(exception, error_detail.exception, msg="exception")

    test_class.assertTrue(error_detail.stack_trace, msg="stack trace")


def assert_exception(test_class: unittest.TestCase, result: Result, exception_type=None):
    test_class.assertFalse(result.success, msg="success")
    detail: ExceptionError = result.detail
    test_class.assertTrue(isinstance(detail, ExceptionError), msg="detail type")
    if exception_type:
        test_class.assertTrue(isinstance(detail.exception, exception_type), msg="exception type")


def assert_invalid_func(test_class: unittest.TestCase, result: Result):
    assert_result_with_type(test_class=test_class, result=result, success=False, detail_type=ValidationError)
    assert_error_detail(test_class=test_class, error_detail=result.detail,
                        title='One or more validation errors occurred',
                        message="The input function is not valid.", code=400)
