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

`on_rails` is a library for **python**.

It is a library for functional error handling to improve **managing errors**.

It stores result of functions and provides a simple way to handle and manipulate the return values of functions, with built-in support for error
handling and more.

### Purpose

In functional programming, it is not always appropriate to use traditional `try-except` blocks because they can lead to code
that is difficult to read, understand, and maintain.

The purpose of Functional Error Handling Libraries is to provide developers with a set of abstractions and tools for
managing errors in a functional way.

`on_rails` is a functional error handling library. The goal of this library is to make error handling m**ore explicit, composable, and testable**. By using this library, developers can write code that is **more robust, maintainable, and expressive**.

### Motivation

The motivation behind this library is the desire to write code that is **more reliable, easier to understand, and less
prone to errors**. In many cases, functional programming languages provide built-in abstractions for handling errors.
However, for languages that do not have built-in support for functional error handling, libraries like this can provide
a useful alternative.

### What problems are solved?

This library can solve several problems, including:

- Ensuring that error handling is consistent across an application.
- Making it easier to test error handling code.
- Making error handling code more readable and maintainable.
- Encouraging developers to handle errors in a more functional way, which can lead to more reliable and robust code.

Developers
can spend less time debugging and more time writing code that adds value to their organization. Additionally, by using
functional programming concepts, developers can write code that is easier to reason about and understand, which can lead
to faster development cycles and better quality code.

## Getting Started

Use `pip` to install package:

`pip install on_rails`

## Usage

### Sample 1: use decorator for pure functions

In this example, `on_rails` is used as a decorator to wrap the `divide_numbers` function.

```python
from on_rails import on_rails


@on_rails
def divide_numbers(a: int, b: int):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


result = divide_numbers(10, 0)

if result.success:
    print(f"Operation was successful: {result.value}")
else:
    print(f"Operation failed: {str(result.detail)}")
```

### Sample 2: use `Result` in function

```python
from on_rails import Result
from on_rails.ResultDetails.Errors import ValidationError


def divide_numbers(a: int, b: int):
    if b == 0:
        return Result.fail(ValidationError(message="Cannot divide by zero"))
    return Result.ok(a / b)


result = divide_numbers(10, 0)

if result.success:
    print(f"Operation was successful: {result.value}")
else:
    print(f"Operation failed:")
    print(str(result.detail))

```

## CHANGELOG

Please see the [CHANGELOG](https://github.com/Payadel/on_rails/blob/main/CHANGELOG.md) file.

## Features

- **Easy to use:** `on_rails` is designed to be simple and easy to use, with a minimal API and clear documentation.
- **Compatibility with existing code:** `on_rails` can be easily added to existing codes without the need for major
  refactoring. You can use decorator for wrap old functions or write new functions without worrying about incompatibilities.
- **Save any details you like:** Thanks to the [ResultDetail](https://github.com/Payadel/on_rails/blob/main/on_rails/ResultDetail.py) class, you can store various information about the output of the function. Also, by inheriting from this class, you can write new and customized classes for your project.
- **Special details for errors:** With the [ErrorDetail](https://github.com/Payadel/on_rails/blob/main/on_rails/ResultDetails/ErrorDetail.py) class, you can store specific details about errors. For example, this class supports **stack trace** in a built-in way.
- **Support for common details by default:** In [this link](https://github.com/Payadel/on_rails/tree/main/on_rails/ResultDetails), you can see the different types of details that are supported.

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

Also for old functions, you can use **decorator**. By using decorator, The output of the function is converted to `Result` format. This way, your code is wrap in a `try-except` block to handle all exceptions.

#### How to manage all function exceptions?

By using decorator, your code is wrap in a `try-except` block and the final output is converted to Result. In this way, all exceptions are handled.

## Project assistance

**First of, thank you.**

If you want to say thank you or/and support active development of `on_rails`:

- Add a [GitHub Star](https://github.com/Payadel/on_rails) to the project.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your
  personal blog.

Together, we can make `on_rails` **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the free/open-source community such an
amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly
appreciated**.

Please read [our contribution guidelines](https://github.com/Payadel/on_rails/blob/main/docs/CONTRIBUTING.md), and thank you for being involved!

Please do not forget that this project uses [conventional commits](https://www.conventionalcommits.org), so please follow the specification in your commit messages.
You can see valid types from [this file](https://github.com/Payadel/on_rails/blob/main/.configs/commitlint.config.js).

## Authors & contributors

The original setup of this repository is by [Payadel](https://github.com/Payadel).

For a full list of all authors and contributors,
see [the contributors page](https://github.com/Payadel/on_rails/contributors).

## Security

`on_rails` follows good practices of security, but 100% security cannot be assured. `on_rails` is provided **"as
is"** without any **warranty**.

_For more information and to report security issues, please refer to our [security documentation](https://github.com/Payadel/on_rails/blob/main/docs/SECURITY.md)._

## License

This project is licensed under the **GPLv3**.

See [LICENSE](https://github.com/Payadel/on_rails/blob/main/LICENSE) for more information.
