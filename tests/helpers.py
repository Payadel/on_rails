import traceback
import unittest
from typing import Any, Dict, List, Optional

from on_rails.Result import Result
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail


def assert_result(test_class: unittest.TestCase, result: Result, success: bool,
                  detail: Optional[ResultDetail] = None, value: Optional[Any] = None) -> None:
    test_class.assertEqual(success, result.success)
    test_class.assertEqual(detail, result.detail)
    test_class.assertEqual(value, result.value)


def assert_result_detail(test_class: unittest.TestCase, result_detail: ResultDetail, title: str,
                         message: Optional[str] = None, code: Optional[int] = None,
                         more_data: Optional[List[Any]] = []) -> None:
    test_class.assertEqual(title, result_detail.title)
    test_class.assertEqual(message, result_detail.message)
    test_class.assertEqual(code, result_detail.code)

    test_class.assertIsNotNone(result_detail.more_data)  # It should never be None.
    test_class.assertEqual(result_detail.more_data, more_data)


def assert_error_detail(test_class: unittest.TestCase, error_detail: ErrorDetail, title: str,
                        message: Optional[str] = None, code: Optional[int] = None, more_data: Optional[List[Any]] = [],
                        errors: Optional[Dict[str, str]] = None, exception: Optional[Exception] = None) -> None:
    assert_result_detail(test_class=test_class, result_detail=error_detail,
                         title=title, message=message, code=code, more_data=more_data)
    test_class.assertEqual(errors, error_detail.errors)
    test_class.assertEqual(exception, error_detail.exception)

    test_class.assertTrue(error_detail.stack_trace)
