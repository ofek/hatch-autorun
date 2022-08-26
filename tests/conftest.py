# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import errno
import os
import shutil
import stat
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest


def handle_remove_readonly(func, path, exc):  # no cov
    # TODO: remove when we drop Python 3.7
    # PermissionError: [WinError 5] Access is denied: '...\\.git\\...'
    if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise


@pytest.fixture(scope='session')
def plugin_dir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as d:
        directory = Path(d, 'plugin')
        shutil.copytree(Path.cwd(), directory)

        yield directory.resolve()

        shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)


@pytest.fixture
def new_project(plugin_dir, tmp_path) -> Generator[Path, None, None]:
    project_dir = tmp_path / 'my-app'
    project_dir.mkdir()

    project_file = project_dir / 'pyproject.toml'
    project_file.write_text(
        f"""\
[build-system]
requires = ["hatchling", "hatch-autorun @ {plugin_dir.as_uri()}"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]
requires-python = ">={sys.version_info[0]}"

[tool.hatch.version]
path = "my_app/__init__.py"

[tool.hatch.build.targets.wheel.hooks.autorun]
""",
        encoding='utf-8',
    )

    package_dir = project_dir / 'my_app'
    package_dir.mkdir()

    package_root = package_dir / '__init__.py'
    package_root.write_text('__version__ = "1.2.3"', encoding='utf-8')

    origin = os.getcwd()
    os.chdir(project_dir)
    try:
        yield project_dir
    finally:
        os.chdir(origin)
