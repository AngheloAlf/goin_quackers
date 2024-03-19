#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

# from splat.segtypes.ps2.asm import Ps2SegAsm
from splat.segtypes.common.data import CommonSegData
from splat.util import options

class PS2SegVutext(CommonSegData):
    def get_section_flags(self):
        return "ax"

    def get_linker_section(self) -> str:
        return ".vutext"

    def asm_out_path(self) -> Path:
        typ = self.type
        if typ.startswith("."):
            typ = typ[1:]

        # return options.opts.asm_path / self.dir / f"{self.name}.{typ}.s"
        return options.opts.data_path / self.dir / f"{self.name}.{typ}.s"

    """
    def out_path(self) -> Path|None:
        if self.type.startswith("."):
            if self.sibling:
                # C file
                return self.sibling.out_path()
            else:
                # Implied C file
                return options.opts.src_path / self.dir / f"{self.name}.c"
        else:
            # ASM
            return self.asm_out_path()
    """
