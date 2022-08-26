# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import sys
import zipfile

import pytest

from .utils import build_project

CODE = """\
print('Starting coverage collection')
coverage.process_startup()
"""


def test_no_options(new_project):
    with pytest.raises(Exception, match='The build hook `autorun` option `file` or `code` must be specified'):
        build_project()


def test_multiple_options(new_project):
    project_file = new_project / 'pyproject.toml'
    contents = project_file.read_text(encoding='utf-8')
    contents += '\nfile = "code.emded"'
    contents += f'\ncode = """\n{CODE}"""'
    project_file.write_text(contents, encoding='utf-8')

    with pytest.raises(Exception, match='The build hook `autorun` options `file` and `code` are mutually exclusive'):
        build_project()


def test_target_not_wheel(new_project):
    project_file = new_project / 'pyproject.toml'
    contents = project_file.read_text(encoding='utf-8')
    contents = contents.replace('[tool.hatch.build.targets.wheel.hooks.autorun]', '[tool.hatch.build.hooks.autorun]')
    project_file.write_text(contents, encoding='utf-8')

    build_project('-s')

    build_dir = new_project / 'dist'
    assert build_dir.is_dir()

    artifacts = list(build_dir.iterdir())
    assert len(artifacts) == 1

    assert artifacts[0].name.endswith('.tar.gz')


def test_file(new_project):
    project_file = new_project / 'pyproject.toml'
    contents = project_file.read_text(encoding='utf-8')
    contents += '\nfile = "code.emded"'
    project_file.write_text(contents, encoding='utf-8')

    package_main = new_project / 'code.emded'
    package_main.write_text(CODE, encoding='utf-8')

    build_project()

    build_dir = new_project / 'dist'
    assert build_dir.is_dir()

    artifacts = list(build_dir.iterdir())
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file.name == f'my_app-1.2.3-py{sys.version_info[0]}-none-any.whl'

    extraction_directory = new_project.parent / '_archive'
    extraction_directory.mkdir()

    with zipfile.ZipFile(str(wheel_file), 'r') as zip_archive:
        zip_archive.extractall(str(extraction_directory))

    root_paths = list(extraction_directory.iterdir())
    assert len(root_paths) == 3

    pth_file = extraction_directory / 'hatch_autorun_my_app.pth'
    assert pth_file.is_file()
    assert pth_file.read_text() == f'import os, sys;exec({CODE!r})'


def test_code(new_project):
    project_file = new_project / 'pyproject.toml'
    contents = project_file.read_text(encoding='utf-8')
    contents += f'\ncode = """\n{CODE}"""'
    project_file.write_text(contents, encoding='utf-8')

    package_main = new_project / 'code.emded'
    package_main.write_text(CODE, encoding='utf-8')

    build_project()

    build_dir = new_project / 'dist'
    assert build_dir.is_dir()

    artifacts = list(build_dir.iterdir())
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file.name == f'my_app-1.2.3-py{sys.version_info[0]}-none-any.whl'

    extraction_directory = new_project.parent / '_archive'
    extraction_directory.mkdir()

    with zipfile.ZipFile(str(wheel_file), 'r') as zip_archive:
        zip_archive.extractall(str(extraction_directory))

    root_paths = list(extraction_directory.iterdir())
    assert len(root_paths) == 3

    pth_file = extraction_directory / 'hatch_autorun_my_app.pth'
    assert pth_file.is_file()
    assert pth_file.read_text() == f'import os, sys;exec({CODE!r})'


def test_file_and_template(new_project):
    project_file = new_project / 'pyproject.toml'
    contents = project_file.read_text(encoding='utf-8')
    contents += '\nfile = "code.emded"'
    contents += '\ntemplate = "import coverage;exec({code!r})"'
    project_file.write_text(contents, encoding='utf-8')

    package_main = new_project / 'code.emded'
    package_main.write_text(CODE, encoding='utf-8')

    build_project()

    build_dir = new_project / 'dist'
    assert build_dir.is_dir()

    artifacts = list(build_dir.iterdir())
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file.name == f'my_app-1.2.3-py{sys.version_info[0]}-none-any.whl'

    extraction_directory = new_project.parent / '_archive'
    extraction_directory.mkdir()

    with zipfile.ZipFile(str(wheel_file), 'r') as zip_archive:
        zip_archive.extractall(str(extraction_directory))

    root_paths = list(extraction_directory.iterdir())
    assert len(root_paths) == 3

    pth_file = extraction_directory / 'hatch_autorun_my_app.pth'
    assert pth_file.is_file()
    assert pth_file.read_text() == f'import coverage;exec({CODE!r})'
