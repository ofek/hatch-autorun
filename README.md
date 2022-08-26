# hatch-autorun

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/ofek/hatch-autorun/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/hatch-autorun/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/hatch-autorun/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/hatch-autorun/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/hatch-autorun.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-autorun/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-autorun.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hatch-autorun/) |
| Meta | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |

-----

This provides a [build hook](https://hatch.pypa.io/latest/config/build/#build-hooks) plugin for [Hatch](https://github.com/pypa/hatch) that injects code into an installation that will automatically run before the first import.

**Table of Contents**

- [Configuration](#configuration)
  - [File](#file)
  - [Code](#code)
- [Conditional execution](#conditional-execution)
- [License](#license)

## Configuration

The [build hook plugin](https://hatch.pypa.io/latest/plugins/build-hook/) name is `autorun`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.build.targets.wheel.hooks.autorun]
    dependencies = ["hatch-autorun"]
    ```

- ***hatch.toml***

    ```toml
    [build.targets.wheel.hooks.autorun]
    dependencies = ["hatch-autorun"]
    ```

### File

You can select a relative path to a file containing the code with the `file` option:

```toml
[tool.hatch.build.targets.wheel.hooks.autorun]
file = "resources/code.emded"
```

### Code

You can define the code itself with the `code` option:

```toml
[tool.hatch.build.targets.wheel.hooks.autorun]
code = """
import coverage
coverage.process_startup()
"""
```

## Conditional execution

Sometimes you'll only want builds to induce auto-run behavior when installed under certain circumstances, like for tests. In such cases, set [`enable-by-default`](https://hatch.pypa.io/latest/config/build/#conditional-execution) to `false`:

```toml
[tool.hatch.build.targets.wheel.hooks.autorun]
enable-by-default = false
```

Then when the desired conditions are met, set the [`HATCH_BUILD_HOOK_ENABLE_AUTORUN`](https://hatch.pypa.io/latest/config/build/#environment-variables) environment variable to `true` or `1`.

## License

`hatch-autorun` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.