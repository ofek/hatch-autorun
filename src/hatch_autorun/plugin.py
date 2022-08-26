# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import os
import tempfile

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class AutoRunBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'autorun'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__config_file = None
        self.__config_code = None
        self.__config_template = None
        self.__temp_dir = None

    @property
    def config_file(self):
        if self.__config_file is None:
            file = self.config.get('file', '')
            if not isinstance(file, str):
                raise TypeError(f'Option `file` for build hook `{self.PLUGIN_NAME}` must be a string')

            self.__config_file = file

        return self.__config_file

    @property
    def config_code(self):
        if self.__config_code is None:
            code = self.config.get('code', '')
            if not isinstance(code, str):
                raise TypeError(f'Option `code` for build hook `{self.PLUGIN_NAME}` must be a string')

            self.__config_code = code

        return self.__config_code

    @property
    def config_template(self):
        if self.__config_template is None:
            template = self.config.get('template', 'import os, sys;exec({code!r})')
            if not isinstance(template, str):
                raise TypeError(f'Option `template` for build hook `{self.PLUGIN_NAME}` must be a string')

            self.__config_template = template

        return self.__config_template

    @property
    def temp_dir(self):
        if self.__temp_dir is None:
            self.__temp_dir = os.path.realpath(tempfile.mkdtemp())

        return self.__temp_dir

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
            f.write(self.config_template.format(code=code))

        if version == 'editable':  # no cov
            build_data['force_include_editable'][pth_file] = file_name
        else:
            build_data['force_include'][pth_file] = file_name

    def finalize(self, version, build_data, artifact_path):
        import shutil

        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
