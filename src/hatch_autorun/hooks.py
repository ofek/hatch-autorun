# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from hatch_autorun.plugin import AutoRunBuildHook


@hookimpl
def hatch_register_build_hook():
    return AutoRunBuildHook
