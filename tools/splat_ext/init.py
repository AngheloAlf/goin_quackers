#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

from splat.segtypes.common.asm import CommonSegAsm
from splat.util import options

class PS2SegInit(CommonSegAsm):
    def get_linker_section(self) -> str:
        return ".init"

    def asm_out_path(self) -> Path:
        typ = self.type
        if typ.startswith("."):
            typ = typ[1:]

        return options.opts.asm_path / self.dir / f"{self.name}.{typ}.s"

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
