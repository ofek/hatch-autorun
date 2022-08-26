# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import tempfile
from functools import cached_property

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class AutoRunBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'autorun'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__config_file = None
        self.__config_code = None

    @cached_property
    def config_file(self):
        file = self.config.get('file', '')
        if not isinstance(file, str):
            raise TypeError(f'Option `file` for build hook `{self.PLUGIN_NAME}` must be a string')

        return file

    @cached_property
    def config_code(self):
        code = self.config.get('code', '')
        if not isinstance(code, str):
            raise TypeError(f'Option `code` for build hook `{self.PLUGIN_NAME}` must be a string')

        return code

    @cached_property
    def temp_dir(self):
        return os.path.realpath(tempfile.mkdtemp())

    def initialize(self, version, build_data):
        if self.target_name != 'wheel':
            return
        elif not (self.config_file or self.config_code):
            raise ValueError(f'The build hook `{self.PLUGIN_NAME}` option `file` or `code` must be specified')
        elif self.config_file and self.config_code:
            raise ValueError(f'The build hook `{self.PLUGIN_NAME}` options `file` and `code` are mutually exclusive')
        elif self.config_file:
            with open(os.path.normpath(os.path.join(self.root, self.config_file)), 'r', encoding='utf-8') as f:
                code = f.read()
        else:
            code = self.config_code

        project_name = self.build_config.builder.metadata.core.name.replace('-', '_')
        file_name = f'hatch_{self.PLUGIN_NAME}_{project_name}.pth'
        pth_file = os.path.join(self.temp_dir, file_name)
        with open(pth_file, 'w', encoding='utf-8') as f:
            f.write(f'exec({code!r})')

        build_data['force_include'][pth_file] = file_name

    def finalize(self, version, build_data, artifact_path):
        import shutil

        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
