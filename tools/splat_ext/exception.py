#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

from splat.segtypes.common.rodata import CommonSegRodata

class PS2SegException(CommonSegRodata):
    def get_linker_section(self) -> str:
        return ".exception"

    def get_section_flags(self) -> str|None:
        return "a"
