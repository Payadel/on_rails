# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [3.0.0](https://github.com/Payadel/on_rails/compare/v2.1.0...v3.0.0) (2023-04-10)


### ⚠ BREAKING CHANGES

* rename `ignore_error` to `ignore_errors` in `on_fail_add_more_data`
* rename `convert_to_result` parameter
* Previously, we ignore invalid `func` but now we validate it.
* For validation errors, `ValidationError` is used instead of `ErrorDetail`.
* Previously, only `Result` was passed, but now the first default param is `value`

### Features

* `on_success` accepts 2 params: `value` and `Result` ([7fa6d7b](https://github.com/Payadel/on_rails/commit/7fa6d7be6fe732caf807475480b077e97649145b))
* accept function as parameter in `on_fail_add_more_data` ([ccfc98d](https://github.com/Payadel/on_rails/commit/ccfc98d31bf4421eb3e8d1475ca2bf20a86b64b0))
* accept function as parameter in `on_success_add_more_data` ([54add78](https://github.com/Payadel/on_rails/commit/54add78fbca437d4d75f38f9a147a7d725d23df6))
* add `break_rails` ([12c8ca0](https://github.com/Payadel/on_rails/commit/12c8ca0895abfd91e3f3e1551cf296ace2da782b))
* add `break_rails` parameter to `operate_when` functions ([7e725d7](https://github.com/Payadel/on_rails/commit/7e725d7c8b8e129b1f60292a5659bf65bb17b725))
* add `BreakRails`. It breaks chaining of function ([1be17f4](https://github.com/Payadel/on_rails/commit/1be17f4e7635cc3a8c08079b3cf898e2c08a41f6))
* add `finally_tee` ([1c83d89](https://github.com/Payadel/on_rails/commit/1c83d8928a630ed0bf3d357e057d3629c9ffeb6d))
* add `ignore_errors` param to `tee` functions ([315bc53](https://github.com/Payadel/on_rails/commit/315bc5368586df62ca3f57d2f79f2b58e25791cd))
* add `ignore_errors` to `on_success_add_more_data` ([441ff03](https://github.com/Payadel/on_rails/commit/441ff035eb4a97226239c2963902bc3f638e9637))
* add `on_fail_break` ([4a20f37](https://github.com/Payadel/on_rails/commit/4a20f370d5a959ffe1decf9b441cbf61a3a60d5e))
* add `on_success_fail_when` ([ee7a5e3](https://github.com/Payadel/on_rails/commit/ee7a5e338851061342604efba09985da097edfa2))
* implement `on_fail_operate_when` ([36425cf](https://github.com/Payadel/on_rails/commit/36425cf891ab1d13194a90fda09a4cd807c10876))
* implement `on_success_operate_when` ([66111ea](https://github.com/Payadel/on_rails/commit/66111eafd5b8aa7ce76a328cc35deeace42c0ad2))
* implement `operate_when` ([56ded5b](https://github.com/Payadel/on_rails/commit/56ded5b0762ba6b14e1e01e41208450f19deaadd))
* support function in `fail_when` ([d4a62c5](https://github.com/Payadel/on_rails/commit/d4a62c589e8440fdc1c606ebfd64b427f4f4bac8))
* support function in `on_fail_new_detail` ([9b857b7](https://github.com/Payadel/on_rails/commit/9b857b79a6cb1078f8a9038136cb2925560a5eb0))
* support function in `on_success_new_detail` ([16d3824](https://github.com/Payadel/on_rails/commit/16d382428c208bdcba780372180586bfc37cfed3))
* support Generic ([a45799a](https://github.com/Payadel/on_rails/commit/a45799af2b13914569b2d89aba44589bc4dfd996))
* support prev result in `on_success_tee` like `on_success` ([fb85d2e](https://github.com/Payadel/on_rails/commit/fb85d2edd28413c474acb97306af553f96ae4427))
* validate `func` in `on_success` ([6ffcb59](https://github.com/Payadel/on_rails/commit/6ffcb596551c2466dbc14146177ca31e04f3b7e5))


### Development: CI/CD, Build, etc

* add verbose mode to local git hook ([57b6dda](https://github.com/Payadel/on_rails/commit/57b6ddaf4ef1b883eadabe6e8dac59b2be7372d6))
* check `tox` in pre-push git hook instead of `pytest` ([c4fb026](https://github.com/Payadel/on_rails/commit/c4fb026823348dfa2ee0690808f35362c03a69e3))
* **coverage:** update event ([0d3609f](https://github.com/Payadel/on_rails/commit/0d3609f79997677e242df0ec77ac068a6438f13c))
* fix check-tox.sh ([7b13058](https://github.com/Payadel/on_rails/commit/7b13058e48cdaaa3c9c67bbffda629e877584516))
* **pylint:** ignore `W0719: Raising too general exception: Exception` ([faa418a](https://github.com/Payadel/on_rails/commit/faa418ad8de024d4d76dc7dadda905ba15b376a2))
* update .pre-commit-config.yaml and git hook script ([80e6161](https://github.com/Payadel/on_rails/commit/80e6161330b37be42a8f522f0e603cd671e2a688))


### Documents

* **readme:** fix codes ([fd33c82](https://github.com/Payadel/on_rails/commit/fd33c827da9fc9c570c5ae1a891e3cc871c0b25e))
* update `Getting Started` section ([a378b0d](https://github.com/Payadel/on_rails/commit/a378b0d4143012f112aa9481cf463a3cdaa30756))


### Refactors

* add `__call_func` ([8ce6dec](https://github.com/Payadel/on_rails/commit/8ce6dec5398f965ffc4f55254aa7ebe575778c8c))
* refactor test. add `assert_invalid_func` ([ca3c64d](https://github.com/Payadel/on_rails/commit/ca3c64dcc1b5a2643b129376835cc186a7cdad99))
* use `on_fail` in `on_fail_tee` ([f5d5ea2](https://github.com/Payadel/on_rails/commit/f5d5ea2c4de087d9b4fc734fc3a1f3ec7d49e862))


### Tests

* add `test_on_fail_give_invalid_func` ([612ba2e](https://github.com/Payadel/on_rails/commit/612ba2e6ee85fac90f1ee3395073251a39046469))
* add combined tests ([0673d4c](https://github.com/Payadel/on_rails/commit/0673d4c86710970a58b8646f94f46ee5ca0b4681))
* add message to asserts ([bbd6d31](https://github.com/Payadel/on_rails/commit/bbd6d31c963e690cbf1057632750428a8e62a0c3))
* minor fix ([4bd2c17](https://github.com/Payadel/on_rails/commit/4bd2c17fb26a90290113acf86479f58ba7f0211d))


### Fixes

* add more validation for `func` param & update error types ([085fe9b](https://github.com/Payadel/on_rails/commit/085fe9beef411e68cb7731e6701032615d84e07b))
* fix exception `There is no current event loop in thread` for `get_event_loop` ([0b100d5](https://github.com/Payadel/on_rails/commit/0b100d55e2331e25af70f90640e9a734fccbe25b))
* rename `convert_to_result` parameter & use `Any` instead of `object` ([5cd552b](https://github.com/Payadel/on_rails/commit/5cd552becb8782359c3a38a2507bff4cf8434c7a))
* rename `ignore_error` to `ignore_errors` in `on_fail_add_more_data` ([92177a6](https://github.com/Payadel/on_rails/commit/92177a61a94a052103525c30687ad90d07a9adbd))
* use `Callable` type instead of `callable` ([61ebed3](https://github.com/Payadel/on_rails/commit/61ebed3dc5fa77f7b4a21893aecdf1c5b27af871))
* validate `func` in `tee` functions ([7196627](https://github.com/Payadel/on_rails/commit/71966279c057e41a26945434069c18620ac83367))

## [2.1.0](https://github.com/Payadel/on_rails/compare/v2.0.1...v2.1.0) (2023-04-07)

### Features

* add `on_fail_add_more_data` ([990ba33](https://github.com/Payadel/on_rails/commit/990ba33a59a2dce83b94b1d2d1ad87bd85cf1eb4))

* add `on_fail_new_detail` ([2f23e5e](https://github.com/Payadel/on_rails/commit/2f23e5e1b879fda46434f827d18fd0b780f69c44))
* add `on_fail_raise_exception` ([4ace02c](https://github.com/Payadel/on_rails/commit/4ace02c9c2aaf0cf1193b2eea3dccc6db979a5ef))
* add `on_fail_tee` ([248e486](https://github.com/Payadel/on_rails/commit/248e48678458935ac04e2cf67eb1aab838b43d7d))
* add `on_success_add_more_data` ([92021e4](https://github.com/Payadel/on_rails/commit/92021e4216318d0511075e2c3b95057475e74144))
* add `on_success_new_detail` ([6a02d12](https://github.com/Payadel/on_rails/commit/6a02d12a91d3cf9d6dadd9c16d9f20b9d0299c45))
* add `on_success_tee` ([6878755](https://github.com/Payadel/on_rails/commit/68787555178318eee1733fc154eb39af5ff63ce8))

### Fixes

* fix `ResultDetail.py`
  bugs ([eddc3ca](https://github.com/Payadel/on_rails/commit/eddc3cab3614ded20b8cb1d29b015c7f2c285f62))

### Refactors

* classify `Result.py`
  functions. ([2a0e18b](https://github.com/Payadel/on_rails/commit/2a0e18bb6cccf7d5e26977b61c503bf062fb6d6c))
* classify `test_Result.py`
  functions ([fca0f1e](https://github.com/Payadel/on_rails/commit/fca0f1e2ac241d2d805cc3097936cc8e98d47497))

### [2.0.1](https://github.com/Payadel/on_rails/compare/v2.0.0...v2.0.1) (2023-04-07)

### Documents

* fix codes in
  README.md ([e1bdff7](https://github.com/Payadel/on_rails/commit/e1bdff7b80b38f9b737f8284e506dbdfd3fcd21b))
* update README.md ([3abda37](https://github.com/Payadel/on_rails/commit/3abda3707a281f557337ca8a858bbb4d7666ea5f))

### Fixes

* make `utility.py`
  private ([1ad3e1a](https://github.com/Payadel/on_rails/commit/1ad3e1a2a334bf74868cfb0b7bd6d49fd5ad2abc))

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
