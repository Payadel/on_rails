import unittest
from typing import Any, Dict, List, Optional

from on_rails.Result import Result
from on_rails.ResultDetail import ResultDetail
from on_rails.ResultDetails.ErrorDetail import ErrorDetail


def assert_result(test_class: unittest.TestCase, target_result: Result, expected_success: bool,
                  expected_detail: Optional[ResultDetail] = None, expected_value: Optional[Any] = None) -> None:
    """
    This function asserts that the given result matches the expected success, detail, and value.

    :param test_class: The test class that is calling this function. This is typically a subclass of
    unittest.TestCase
    :type test_class: unittest.TestCase

    :param target_result: The `result` parameter is of type `Result`, which is the result of some operation.
    It probably contains information such as whether the operation was successful (`success`), any
    details about the result (`detail`), and the actual value returned by the operation (`value`)
    :type target_result: Result

    :param expected_success: The expected value of `success`. It will check with `result.success`
    :type expected_success: bool

    :param expected_detail: The expected value of `detail`. It will check with `result.detail`
    :type expected_detail: Optional[ResultDetail]

    :param expected_value: The expected value of `value`. It will check with `result.value`
    :type expected_value: Optional[Any]
    """
    test_class.assertEqual(expected_success, target_result.success, msg="success")
    test_class.assertEqual(expected_detail, target_result.detail, msg="detail")
    test_class.assertEqual(expected_value, target_result.value, msg="value")


def assert_result_with_type(test_class: unittest.TestCase, target_result: Result, expected_success: bool,
                            expected_detail_type=None, expected_value: Optional[Any] = None) -> None:
    """
    This function asserts the success, detail type, and value of a given result object.

    :param test_class: The test class that is calling this function. This is typically a subclass of
    unittest.TestCase
    :type test_class: unittest.TestCase

    :param target_result: The `result` parameter is of type `Result`, which is the result of some operation.
    It probably contains information such as whether the operation was successful (`success`), any
    details about the result (`detail`), and the actual value returned by the operation (`value`)
    :type target_result: Result

    :param expected_success: The expected value of `success`. It will check with `result.success`
    :type expected_success: bool

    :param expected_detail_type: The `detail_type` parameter is an optional argument that
    specifies the expected type of the `detail`

    :param expected_value: The expected value of `value`. It will check with `result.value`
    :type expected_value: Optional[Any]
    """
    test_class.assertEqual(expected_success, target_result.success, msg="success")
    test_class.assertTrue(isinstance(target_result.detail, expected_detail_type), msg="detail type")
    test_class.assertEqual(expected_value, target_result.value, msg="value")


def assert_result_detail(test_class: unittest.TestCase, target_result_detail: ResultDetail, expected_title: str,
                         expected_message: Optional[str] = None, expected_code: Optional[int] = None,
                         expected_more_data: Optional[List[Any]] = None) -> None:
    """
    This function asserts that the given result detail object matches the expected title, message, code, and more data.

    :param test_class: The unittest.TestCase class that is being used to run the test
    :type test_class: unittest.TestCase

    :param target_result_detail: The object of type ResultDetail that we want to test against the expected values of
    its attributes (title, message, code, and more_data)
    :type target_result_detail: ResultDetail

    :param expected_title: A string representing the title of the result detail. It will check with `result_detail.title`
    :type expected_title: str

    :param expected_message: The expected value of `message`. It will check with `result_detail.message`
    :type expected_message: Optional[str]

    :param expected_code: The expected value of `code`. It will check with `result_detail.code`
    :type expected_code: Optional[int]

    :param expected_more_data: The expected value of `more_data`. It will check with `result_detail.more_data
    :type expected_more_data: Optional[List[Any]]
    """
    if expected_more_data is None:
        expected_more_data = []
    test_class.assertEqual(expected_title, target_result_detail.title, msg="title")
    test_class.assertEqual(expected_message, target_result_detail.message, msg="message")
    test_class.assertEqual(expected_code, target_result_detail.code, msg="code")

    test_class.assertIsNotNone(target_result_detail.more_data, msg="more data")  # It should never be None.
    test_class.assertEqual(expected_more_data, target_result_detail.more_data, msg="more data")


def assert_error_detail(test_class: unittest.TestCase, target_error_detail: ErrorDetail, expected_title: str,
                        expected_message: Optional[str] = None, expected_code: Optional[int] = None,
                        expected_more_data: Optional[List[Any]] = None,
                        expected_errors: Optional[Dict[str, str]] = None,
                        expected_exception: Optional[Exception] = None) -> None:
    """
    This function asserts the details of an error, including its title, message, code, additional data, errors, and
    exception.

    :param test_class: The unittest.TestCase class that the test is being run on
    :type test_class: unittest.TestCase

    :param target_error_detail: This is the ErrorDetail object that we want to test/assert against.
    It contains information about an error that occurred during the execution of a program or function
    :type target_error_detail: ErrorDetail

    :param expected_title: The expected title of the error detail.
    :type expected_title: str

    :param expected_message: The expected message string that should be present in the error detail
    :type expected_message: Optional[str]

    :param expected_code: The expected code that should be returned with the error detail
    :type expected_code: Optional[int]

    :param expected_more_data: The expected additional data that should be present in the error detail
    :type expected_more_data: Optional[List[Any]]

    :param expected_errors: The expected errors that should be present in the error detail
    :type expected_errors: Optional[Dict[str, str]]

    :param expected_exception: The expected exception that should be present in the error detail
    :type expected_exception: Optional[Exception]
    """
    if expected_more_data is None:
        expected_more_data = []
    assert_result_detail(test_class=test_class, target_result_detail=target_error_detail,
                         expected_title=expected_title, expected_message=expected_message, expected_code=expected_code,
                         expected_more_data=expected_more_data)
    test_class.assertEqual(expected_errors, target_error_detail.errors, msg="errors")
    test_class.assertEqual(expected_exception, target_error_detail.exception, msg="exception")

    test_class.assertTrue(target_error_detail.stack_trace, msg="stack trace")
