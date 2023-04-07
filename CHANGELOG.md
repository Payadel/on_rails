# Changelog

All notable changes to this project will be documented in this file.
See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [2.0.0](https://github.com/Payadel/on_rails/compare/v1.0.0...v2.0.0) (2023-04-07)

### ⚠ BREAKING CHANGES

* rename `def_result` to `on_rails`

### Features

* add `fail_when` ([9d2ca24](https://github.com/Payadel/on_rails/commit/9d2ca24f6bd55abc1d260d13b38de9d5aaeb9c2e))
* add `on_success` and `on_fail`
  functions ([d271141](https://github.com/Payadel/on_rails/commit/d271141d7016340a13e5cee5ff5d4ddd0e5396e0))
* add `try_only_on_exceptions` to `on_success` and `on_fail`
  functions ([5375b24](https://github.com/Payadel/on_rails/commit/5375b242c7d70ad988aa975020c249c7e83530db))
* add `try_only_on_exceptions` to `try_func`
  functions ([e445fce](https://github.com/Payadel/on_rails/commit/e445fce9fd90cad20f2378d4f85041b35f0c753a))
* **decorator:**
  supports `async` ([1a9f63d](https://github.com/Payadel/on_rails/commit/1a9f63dea611fbad8847cf7f4545be17d097235c))
* **result:** add `try_func`,
  add `convert_to_result` ([fd881cc](https://github.com/Payadel/on_rails/commit/fd881ccb9609732de41f59e1978aa0d43e1689d0))
* specify annotation for `func`
  parameters ([ec098f8](https://github.com/Payadel/on_rails/commit/ec098f8a3bda2178866fe6eb4900809c52a5bace))

### Fixes

* rename `def_result`
  to `on_rails` ([0215149](https://github.com/Payadel/on_rails/commit/0215149daad051e4459b4038b1e708e634e94275)
  , [4493029](https://github.com/Payadel/on_rails/commit/449302978795bacd12af2a963bab5084211df67e))

### Documents

* add description to
  pyproject.toml ([bf27a72](https://github.com/Payadel/on_rails/commit/bf27a723a17f4425d4bb5482f69c117a1a8cffc6))
* **readme:** update
  README.md ([04f99fe](https://github.com/Payadel/on_rails/commit/04f99fe64b98ac74e31280b29bb8b26f8a47fe25))

### Refactors

* minor updates ([28a3837](https://github.com/Payadel/on_rails/commit/28a38374cf942ded3ece3e43422aa42ffefe36c1))

### Development: CI/CD, Build, etc

* **coverage:** fix coverage
  action ([0873126](https://github.com/Payadel/on_rails/commit/0873126de8ba676b56ddac33415faabffa7bff68)
  , [ff03f77](https://github.com/Payadel/on_rails/commit/ff03f7791cc67b651602da085ef44f38a746bddf))
* **lock:** remove lock.yml
  action ([bbe562e](https://github.com/Payadel/on_rails/commit/bbe562e77da1b31c32fdf0858574e1a638ec73fb))

## [1.0.0](https://github.com/Payadel/on_rails/compare/v0.0.3...v1.0.0) (2023-04-02)

### Features

* **Result:**
  implement `Result.__str__` ([6647fb7](https://github.com/Payadel/on_rails/commit/6647fb7b4904fbe6ffe40eaf0158870823400953))
* **Result:**
  implement `ResultDetail.__repr__` ([baeec3e](https://github.com/Payadel/on_rails/commit/baeec3ecf13898e34add5a27a3dd3047a61cb7e7))

### Fixes

* add stack trace
  to `ErrorDetail.__str__` ([9142862](https://github.com/Payadel/on_rails/commit/91428625c6e1d35b6e1dc2e59488556e2e810649))
* fix Result.__str__ and add test
  case ([3470371](https://github.com/Payadel/on_rails/commit/3470371dcca4efa3418cc7b83f912c750e612bb1))
* fix ResultDetail.__repr__ and add test
  case ([f84c29b](https://github.com/Payadel/on_rails/commit/f84c29b717fd471ab4acaf73a6f25b4deee52f0f))
* update docstrings ([b3a5ab7](https://github.com/Payadel/on_rails/commit/b3a5ab7393e22450c63931d753ec422aceb2c836))

### Development: CI/CD, Build, etc

* add more data to
  pyproject.toml ([0e190d4](https://github.com/Payadel/on_rails/commit/0e190d4101994de46a6e9e5aab968001c4af32d2))

### Documents

* **readme:** add build status to
  README.md ([6948384](https://github.com/Payadel/on_rails/commit/6948384dfe60584ea2c1f308f19dfdaae6396d38))
* **readme:** update codes in
  README.md ([e56e770](https://github.com/Payadel/on_rails/commit/e56e7709b127e105df41ebad1d0382d6c7dc0d38))
* **readme:** use absolute links to fix links in package readme
  file ([b7b2041](https://github.com/Payadel/on_rails/commit/b7b204129d25b4bdd802b2eecf7c980061992617))

### [0.0.3](https://github.com/Payadel/on_rails/compare/v0.0.2...v0.0.3) (2023-04-02)

### Features

* import files in __init__
  files ([6e2ec3e](https://github.com/Payadel/on_rails/commit/6e2ec3e25ac9d193699702f08ca7cffbcf2dddf2))

### Development: CI/CD, Build, etc

* add .pyc files to
  .gitignore ([34dfc1f](https://github.com/Payadel/on_rails/commit/34dfc1f7b0b7517fbb5caf6716ffae21ca63ff31))
* update Makefile ([6b7f4f8](https://github.com/Payadel/on_rails/commit/6b7f4f8f1d1e68a001c0f3f8f9ac36ce328a500d))

### [0.0.2](https://github.com/Payadel/on_rails/compare/v0.0.1...v0.0.2) (2023-04-01)

### Fixes

* minor updates ([fb9db93](https://github.com/Payadel/on_rails/commit/fb9db937deab11535adf95867ef5bb97e11bda39))

### Development: CI/CD, Build, etc

* add `Update poetry version` to publish-test.yaml and
  fix `pypi_token` ([4a8fcaf](https://github.com/Payadel/on_rails/commit/4a8fcaf099bdd937e9dae7a9af01dffa0fd72f7f))
* add description to
  pyproject.toml ([60b6892](https://github.com/Payadel/on_rails/commit/60b689217b484a4e95079f401252d1366ab47bca))
* **coverage:** add coverage.yaml github
  action ([8106295](https://github.com/Payadel/on_rails/commit/8106295f21b44274b0456b53060cc068d7af71eb))
* **coverage:** update
  coverage.yaml ([2767351](https://github.com/Payadel/on_rails/commit/2767351ebf63f9a93c52199cbfe9648035c052c3))
* fix inputs in
  publish-test.yaml ([793e3f8](https://github.com/Payadel/on_rails/commit/793e3f8df92aa8a62e10f426c7918e27acd77624))
* **release:**
  fix `Update poetry version` ([c3e1db9](https://github.com/Payadel/on_rails/commit/c3e1db9e624875db89941e0a2558bc6324e177f5))
* **release:** fix
  pypi_token ([07bfc18](https://github.com/Payadel/on_rails/commit/07bfc1805d4080f5889b4a03dec9355b63412baf))
* remove excess section (scripts) from
  pyproject.toml ([daa7f36](https://github.com/Payadel/on_rails/commit/daa7f366764d855a711541b94058b20a4dcb5eb0))
* **requirements:** add `Install poetry` section to
  requirements.py ([ab09e1c](https://github.com/Payadel/on_rails/commit/ab09e1cb9e1fd0f7646aa4e839d7f6b271669a90))
* separate publish from
  release ([8cfb936](https://github.com/Payadel/on_rails/commit/8cfb9360b0409104891965da90361f0ad01a0557))
* update Makefile. supports more GitHub
  action ([5d65dda](https://github.com/Payadel/on_rails/commit/5d65ddad8ae119c5bde394c35ffd7a627ee10ce2))

### Documents

* **contributing:** update
  CONTRIBUTING.md ([d137023](https://github.com/Payadel/on_rails/commit/d1370237a0939c6dd57c1adec63072cee42fd0fb))
* **readme:** add code coverage
  badge ([59c5b97](https://github.com/Payadel/on_rails/commit/59c5b97d0f306501139e58b7be8a13ff368aa39d))
* **readme:** update
  README.md ([cb888fb](https://github.com/Payadel/on_rails/commit/cb888fbff103581b6b327efdc3acb5de086d6347))
* **readme:** update
  README.md ([67c9b71](https://github.com/Payadel/on_rails/commit/67c9b717f3b5296419386498f81fac0a6cccb01e))
* **readme:** update table of
  contents ([7afad9a](https://github.com/Payadel/on_rails/commit/7afad9addb9e31988271e89a2d2b7220418c381c))
* update
  PULL_REQUEST_TEMPLATE.md ([8cfc570](https://github.com/Payadel/on_rails/commit/8cfc570444fe4abc0d94570e64833f7d3902f23d))
* update README.md ([fe43dfd](https://github.com/Payadel/on_rails/commit/fe43dfd42028f028603f6de3de5df9375623b392))

### 0.0.1 (2023-03-31)

### Features

* add `on_rails`
  decorator ([98f9101](https://github.com/Payadel/on_rails/commit/98f91010c58f093596d4c9017a1680c34ba6a665))
* add BadRequestError ([59711c8](https://github.com/Payadel/on_rails/commit/59711c821cba16527c7654d34a5a7d8c90d745e2))
* add ConflictError ([c37b217](https://github.com/Payadel/on_rails/commit/c37b217ed2934fe38fae44d8fda5b885e7c52c48))
* add docstring to Result and
  ResultDetail ([381998e](https://github.com/Payadel/on_rails/commit/381998e7281e0ead1f7707215e7d28569d792d29))
* add ErrorDetail ([7fb0722](https://github.com/Payadel/on_rails/commit/7fb072264a37473ef02d5be459ad94bf320d0e48))
* add ExceptionError ([6ca9f3c](https://github.com/Payadel/on_rails/commit/6ca9f3cd57c83107a87ede7d5c97a204aa89a2e6))
* add ForbiddenError ([26575c9](https://github.com/Payadel/on_rails/commit/26575c9ef0b9dbf693a718b9c893c0418a7bd38c))
* add InternalError ([c6504fd](https://github.com/Payadel/on_rails/commit/c6504fdb236cd6a8264648e5e2ff4f60c0cfd1f2))
* add NotFoundError ([2321dc3](https://github.com/Payadel/on_rails/commit/2321dc3b7114aa10872d72536d0d0469f106c2f3))
* add Payadel python package
  template ([c8f21a7](https://github.com/Payadel/on_rails/commit/c8f21a7394309263b6c74f858e946158b26f8d0b))
* add Payadel readme
  template ([cb3e4e0](https://github.com/Payadel/on_rails/commit/cb3e4e0ba5559b2ca1756f4c1acb1cb6bfb36d20))
* Add Result and ResultDetail
  classes ([bab86c8](https://github.com/Payadel/on_rails/commit/bab86c8ab932e874266680c093cebcb3aa7dfffe))
* add some success
  details ([35ac92b](https://github.com/Payadel/on_rails/commit/35ac92b91c7329be0f51409f7c03055ca7e56dd3))
* add SuccessDetail.py ([261e631](https://github.com/Payadel/on_rails/commit/261e6313448dc3aa824e8bbe3d82fbaf9af3b21a))
* add UnauthorizedError ([a60234b](https://github.com/Payadel/on_rails/commit/a60234b16708c73d8e5041cd2e24dd825711fe00))
* add ValidationError ([fbf0ed7](https://github.com/Payadel/on_rails/commit/fbf0ed799f0effd6fa614f8df8402665c22d029d))
* **decorator:** support functions that return
  Result ([274bbd3](https://github.com/Payadel/on_rails/commit/274bbd33f478390a962160ea1dbee8b31f1c6a3c))

### Fixes

* fix more_data type in
  ErrorDetail.py ([c29b505](https://github.com/Payadel/on_rails/commit/c29b505c1dc7b5fa52985cb798fdde3d27afe75b))
* update docstrings ([122e667](https://github.com/Payadel/on_rails/commit/122e6673f5da26a01c6bc80aee8f0543448c02ca))

### Development: CI/CD, Build, etc

* **build:** update build.yaml
  events ([57bdafc](https://github.com/Payadel/on_rails/commit/57bdafc6876c5a2396262e5a03ef6d465c7836a3))
* **codeql:**
  fix `python-version` ([0b5f46a](https://github.com/Payadel/on_rails/commit/0b5f46ac51793773c25d0ae1d834148294256113))
* ignore some pylint
  errors ([234f870](https://github.com/Payadel/on_rails/commit/234f870c6fe585aa0d466cecda9f306e57306676))
* **makefile:** add
  Makefile ([5b9580f](https://github.com/Payadel/on_rails/commit/5b9580fbee927eda7e22508313e02b8233b55f63))
* update
  .pre-commit-config.yaml ([933234a](https://github.com/Payadel/on_rails/commit/933234ad0940d1fe37b708a7bcfa84cbc3644ab5))

### Refactors

* add `assert_more_data` function to
  helpers.py ([5be313d](https://github.com/Payadel/on_rails/commit/5be313d42a9ccda9aa9002e8261def3d9f6d45d0))

### Tests

* add __init__.py to test
  directories ([5516040](https://github.com/Payadel/on_rails/commit/5516040dd9f0e7f45f9adb04bcf56ac824cff356))
* add test_Result.py ([b82247b](https://github.com/Payadel/on_rails/commit/b82247b7dc1a703f28876a790c792bd6ec21aa39))
* fix test_decorator.py ([f1c4508](https://github.com/Payadel/on_rails/commit/f1c4508fdf4bb971c3f371a56140203f081904ce))
* refactor ([9808868](https://github.com/Payadel/on_rails/commit/98088680a55a64d2189dada04d44de75809a05cc))
* update
  test_ExceptionError.py ([1ba3ddd](https://github.com/Payadel/on_rails/commit/1ba3dddb9d8bd39fdc64b1cb8940fa785ae8582a))
