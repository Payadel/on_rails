# pylint: disable=all

import unittest

from on_rails.Result import Result
from on_rails.ResultDetails.Errors.ValidationError import ValidationError
from on_rails.test_helpers import assert_error_detail, assert_result_with_type


def assert_invalid_func(test_class: unittest.TestCase, result: Result):
    assert_result_with_type(test_class=test_class, target_result=result, expected_success=False, expected_detail_type=ValidationError)
    assert_error_detail(test_class=test_class, target_error_detail=result.detail,
                        expected_title='One or more validation errors occurred',
                        expected_message="The input function is not valid.", expected_code=400)


def assert_exception(test_class: unittest.TestCase, exception, exception_type):
    test_class.assertTrue(isinstance(exception, Exception), msg="exception must be instance of Exception")
    test_class.assertTrue(isinstance(exception, exception_type), msg="exception type")
