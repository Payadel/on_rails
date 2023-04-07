<div align="center">
  <h1>on_rails</h1>
  <br />
  <a href="#getting-started"><strong>Getting Started »</strong></a>
  <br />
  <br />
  <a href="https://github.com/Payadel/on_rails/issues/new?assignees=&labels=scope-bug&template=BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/Payadel/on_rails/issues/new?assignees=&labels=scope-enhancement&template=FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/Payadel/on_rails/issues/new?assignees=&labels=help-wanted&template=SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![code with love by Payadel](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-Payadel-ff1414.svg?style=flat-square)](https://github.com/Payadel)

[![Build Status](https://img.shields.io/github/actions/workflow/status/Payadel/on_rails/build.yaml?branch=dev)](https://github.com/Payadel/on_rails/actions/workflows/build.yaml?query=branch%3Adev)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](coverage.md)
[![PyPI](https://img.shields.io/pypi/v/on_rails.svg)](https://pypi.org/project/on_rails/)

![GitHub](https://img.shields.io/github/license/Payadel/on_rails)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/Payadel/on_rails/issues?q=is%3Aissue+is%3Aopen)



</div>
<details>
<summary>Table of Contents</summary>

- [About](#about)
    - [Purpose](#Purpose)
    - [Motivation](#Motivation)
    - [What problems are solved?](#what-problems-are-solved)
- [Getting Started](#getting-started)
- [Usage](#usage)
    - [Documentation](#documentation)
- [CHANGELOG](#changelog)
- [Features](#features)
- [Roadmap](#roadmap)
- [Support](#support)
- [FAQ](#faq)
- [Project assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Security](#security)
- [License](#license)

</details>

## About

`on_rails` is a **Railway-Oriented** programming library for Python. It is designed to help developers write code that
is both easier to read and more resilient to errors. Railway-Oriented programming is a pattern that is similar to
functional programming, but with a focus on handling errors in a more elegant way.

### Railway Oriented

The Railway Oriented Programming (ROP) pattern separates the pure functional domain logic from the side effects, by
representing them as a **sequence of functions** that return an Either type, representing either a successful `Result`
or an error. This allows for better **composition** and **testing** of functions, as well as improving the code's **
maintainability** and **readability**.

It also facilitates the **handling of errors**, as the error handling logic is separated from the main logic, making it
easier to reason about and handle errors in a consistent and predictable manner. Overall, ROP can lead to more robust
and reliable software systems.

### Error Handling

In functional programming, it is not always appropriate to use traditional `try-except` blocks because they can lead to
code that is difficult to read, understand, and maintain.

`on_rails` supports functional error handling. The goal of this library is to make error handling **more explicit,
composable, and testable**. By using this library, developers can write code that is **more robust, maintainable, and
expressive**.

### Motivation

The motivation behind this library is the desire to write code that is **more reliable, easier to understand, and less
prone to errors**. In many cases, functional programming languages provide built-in abstractions for chaining functions
and handling errors. However, for languages that do not have built-in support, libraries like this can provide a useful
alternative.

### What problems are solved?

Railway Oriented Programming (ROP) solves several common problems in software development, such as:

- **Handling errors:** By using an Either (`Result`) type, ROP makes it easy to represent and handle errors in a
  consistent and predictable manner, avoiding errors being thrown and allowing for error handling logic to be separated
  from the main logic.

- **Composition:** ROP separates the pure functional domain logic from the side effects, such as I/O, by representing
  them as a sequence of functions. This makes it easy to compose and chain functions together, enabling better code
  reuse and maintainability.

- **Readability:** The separation of pure functional domain logic from the side effects makes the code more readable and
  understandable, as it makes it clear what each function does and how they relate to each other.

- **Testing:** The pure functional domain logic can be easily tested, as it does not depend on any external state or
  side effects. This simplifies testing and ensures that the code is correct.

Overall, ROP provides a structured approach to software development that makes it easier to handle errors, compose
functions, and test code, leading to more robust and reliable software systems.

Developers can spend less time debugging and more time writing code that adds value to their organization. Additionally,
by using functional programming concepts, developers can write code that is easier to reason about and understand, which
can lead to faster development cycles and better quality code.

## Getting Started

Use `pip` to install package:

`pip install on_rails`

## Usage

### Sample 1

```python
from on_rails import Result, def_result


@def_result()
def get_number() -> Result:
    number = int(input("Enter number: "))
    return Result.ok(number)


get_number()\
    .on_success(lambda prev: print(f"Number is valid: {prev.value}"))\
    .on_fail(lambda prev: print(prev.detail))
```

Within the `get_number` function, the user is prompted to enter an integer number. If the user enters a valid integer,
the number is returned as a successful result using `Result.ok()`, otherwise, an error message is returned as a failed
result.

When the number is **not valid**, that is, it cannot be converted to int, an **exception** is raised. Thanks to
the `def_result` decorator, all exceptions are handled and the error details are saved in the Result detail.

The `get_number()` function is then called and its result is **chained** with two methods: `on_success()`
and `on_fail()`. If the `get_number()` function returns a **successful** result, the lambda function passed
to `on_success()` is executed, which prints the valid number entered by the user. If the `get_number()` function returns
a **failed** result, the lambda function passed to `on_fail()` is executed, which prints the error message.

Sample output for **valid** number:

```text
Enter number: 5
Number is valid: 5
```

Sample output for **invalid** number:

```text
Enter number: a
Title: An exception occurred
Message: invalid literal for int() with base 10: 'a'
Code: 500
Exception: invalid literal for int() with base 10: 'a'
Stack trace: ...
```

### Sample 2:

```python
from on_rails import Result, def_result
from on_rails.ResultDetails.Errors import ValidationError


@def_result()
def divide_numbers(a: int, b: int):
    if b == 0:
        return Result.fail(ValidationError(message="Cannot divide by zero"))
    return Result.ok(a / b)


result = divide_numbers(10, 0)

if result.success:
    print(f"Operation was successful: {result.value}")
else:
    print("Operation failed:")
    if result.detail.is_instance_of(ValidationError):
        print("Ooo! This is a validation error!")
    print(result.detail)

```

For better error management, you can also specify the error type.

You can use [the implemented](https://github.com/Payadel/on_rails/tree/main/on_rails/ResultDetails) error types or
implement your own error type.

### Sample 3: Custom Error Detail

```python
from typing import Optional
from on_rails import Result, def_result, ErrorDetail


class CustomErrorDetail(ErrorDetail):
    custom_field: str = "custom field!"

    def __init__(self, message: Optional[str] = None):
        super().__init__(title="This is my custom detail", message=message)
        self.code = 600  # Custom error code

    def __str__(self):
        error_details = super().__str__()
        error_details += f"Custom Field: {self.custom_field}"
        return error_details


@def_result()
def divide_numbers(a: int, b: int):
    if b == 0:
        return Result.fail(CustomErrorDetail(message="Cannot divide by zero"))
    return Result.ok(a / b)

```

### Sample 4: Retry Operations

```python
from on_rails.ResultDetails.Success import CreatedDetail
from on_rails import Result, def_result
import requests


@def_result()
def create_data(url: str, data: dict[str, str]) -> Result:
    response = requests.post(url, data=data, timeout=2000)
    response.raise_for_status()  # Raise an exception if the status code indicates an error

    detail = CreatedDetail() if response.status_code == 201 else None
    return Result.ok(response.json(), detail)


def fake_operation():
    return Result.ok()


fake_operation().on_success(create_data, num_of_try=5)

```

In the example above, if the request goes wrong, an **exception** will be raised. By setting `num_of_try`, you can
specify how many times the operation should be repeated in case of an error.

### Sample 5: Async Decorator

By default, all operations are executed **synchronous**. If you want to be **asynchronous** set `is_async` to true.

```python
from on_rails import def_result


@def_result(is_async=True)
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

```

> Note: In asymmetric mode, **chain** of functions is not supported.

## CHANGELOG

Please see the [CHANGELOG](https://github.com/Payadel/on_rails/blob/main/CHANGELOG.md) file.

## Features

- **Easy to use:** `on_rails` is designed to be simple and easy to use, with a minimal API and clear documentation.
- **Compatibility with existing code:** `on_rails` can be easily added to existing codes without the need for major
  refactoring. You can use decorator for wrap old functions or write new functions without worrying about
  incompatibilities.
- **Save any details you like:** Thanks to
  the [ResultDetail](https://github.com/Payadel/on_rails/blob/main/on_rails/ResultDetail.py) class, you can store
  various information about the output of the function. Also, by inheriting from this class, you can write new and
  customized classes for your project.
- **Special details for errors:** With
  the [ErrorDetail](https://github.com/Payadel/on_rails/blob/main/on_rails/ResultDetails/ErrorDetail.py) class, you can
  store specific details about errors. For example, this class supports **stack trace** in a built-in way.
- **Support for common details by default:**
  In [this link](https://github.com/Payadel/on_rails/tree/main/on_rails/ResultDetails), you can see the different types
  of details that are supported.

## Roadmap

See the [open issues](https://github.com/Payadel/on_rails/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/Payadel/on_rails/issues?q=label%3Ascope-enhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/Payadel/on_rails/issues?q=is%3Aissue+is%3Aopen+label%3Ascope-bug+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/Payadel/on_rails/issues?q=is%3Aopen+is%3Aissue+label%3Ascope-bug)

## Support

Reach out to the maintainers at one of the following places:

- [GitHub issues](https://github.com/Payadel/on_rails/issues/new?assignees=&labels=help-wanted&template=SUPPORT_QUESTION.md&title=support%3A+)

## FAQ

#### Do I need rewrite all the functions in a new way?

**not necessarily.** You can add this library and write new functions without changing the previous codes.

Also for old functions, you can use **decorator**. By using decorator, The output of the function is converted
to `Result` format. This way, your code is wrap in a `try-except` block to handle all exceptions.

#### How to manage all function exceptions?

By using decorator, your code is wrap in a `try-except` block and the final output is converted to Result. In this way,
all exceptions are handled.

## Project assistance

If you want to say thank you or/and support active development of `on_rails`:

- Add a [GitHub Star](https://github.com/Payadel/on_rails) to the project.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your
  personal blog.

Together, we can make `on_rails` **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the free/open-source community such an
amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly
appreciated**.

Please read [our contribution guidelines](https://github.com/Payadel/on_rails/blob/main/docs/CONTRIBUTING.md), and thank
you for being involved!

> Please do not forget that this project uses [conventional commits](https://www.conventionalcommits.org), so please follow the specification in your commit messages. You can see valid types from [this file](https://github.com/Payadel/on_rails/blob/main/.configs/commitlint.config.js).

## Authors & contributors

The original setup of this repository is by [Payadel](https://github.com/Payadel).

For a full list of all authors and contributors,
see [the contributors page](https://github.com/Payadel/on_rails/contributors).

## Security

`on_rails` follows good practices of security, but 100% security cannot be assured. `on_rails` is provided **"as is"**
without any **warranty**.

_For more information and to report security issues, please refer to
our [security documentation](https://github.com/Payadel/on_rails/blob/main/docs/SECURITY.md)._

## License

This project is licensed under the **GPLv3**.

See [LICENSE](https://github.com/Payadel/on_rails/blob/main/LICENSE) for more information.
