# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest


@pytest.fixture(scope='session')
def plugin_dir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as d:
        directory = Path(d, 'plugin')
        shutil.copytree(Path.cwd(), directory)

        yield directory.resolve()


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
