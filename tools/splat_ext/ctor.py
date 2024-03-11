#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

from splat.segtypes.common.rodata import CommonSegRodata
from spimdisasm.mips.sections import SectionBase

class PS2SegCtor(CommonSegRodata):
    def get_linker_section(self) -> str:
        return ".ctor"

    def get_section_flags(self) -> str|None:
        return "a"

    def scan(self, rom_bytes: bytes):
        super().scan(rom_bytes)

        # assert self.spim_section is not None, str(self)
        if self.spim_section is None:
            return

        section = self.spim_section.get_section()
        assert isinstance(section, SectionBase)

        for sym in section.symbolList:
            sym.contextSym.isMaybeString = False
