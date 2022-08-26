# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import pytest

from hatch_autorun.plugin import AutoRunBuildHook


class TestFile:
    def test_default(self, new_project):
        config = {}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_file == build_hook.config_file == ''

    def test_correct(self, new_project):
        config = {'file': 'foo'}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_file == build_hook.config_file == 'foo'

    def test_not_string(self, new_project):
        config = {'file': 9000}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        with pytest.raises(TypeError, match='Option `file` for build hook `autorun` must be a string'):
            _ = build_hook.config_file


class TestCode:
    def test_default(self, new_project):
        config = {}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_code == build_hook.config_code == ''

    def test_correct(self, new_project):
        config = {'code': 'foo'}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_code == build_hook.config_code == 'foo'

    def test_not_string(self, new_project):
        config = {'code': 9000}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        with pytest.raises(TypeError, match='Option `code` for build hook `autorun` must be a string'):
            _ = build_hook.config_code


class TestTemplate:
    def test_default(self, new_project):
        config = {}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_template == build_hook.config_template == 'import os, sys;exec({code!r})'

    def test_correct(self, new_project):
        config = {'template': 'foo'}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        assert build_hook.config_template == build_hook.config_template == 'foo'

    def test_not_string(self, new_project):
        config = {'template': 9000}
        build_dir = new_project / 'dist'
        build_hook = AutoRunBuildHook(str(new_project), config, None, None, str(build_dir), 'wheel')

        with pytest.raises(TypeError, match='Option `template` for build hook `autorun` must be a string'):
            _ = build_hook.config_template
