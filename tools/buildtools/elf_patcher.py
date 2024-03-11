#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import spimdisasm
from pathlib import Path
import struct

sections_to_realign = {
    ".text": 4,
    ".data": 4,
    ".rodata": 4,
    ".ctor": 4,
    ".init": 4,
    ".exceptix": 4,
    ".sdata": 4,
    ".sbss": 4,
    ".bss": 4,
}

parser = argparse.ArgumentParser()

parser.add_argument("elf_path")

args = parser.parse_args()

elf_path = Path(args.elf_path)

elf_bytes = bytearray(elf_path.read_bytes())

elf_file = spimdisasm.elf32.Elf32File(elf_bytes)

for i, sect in enumerate(elf_file.sectionHeaders):
    name = elf_file.shstrtab[sect.name]
    # print(name, sect)

    new_alignment = sections_to_realign.get(name)
    if new_alignment is not None:
        section_offset = elf_file.header.shoff + i * 0x28
        addralign = section_offset + 0x20

        fmt = spimdisasm.common.GlobalConfig.ENDIAN.toFormatString() + "I"
        struct.pack_into(fmt, elf_bytes, addralign, new_alignment)

        # print(name)
        # print(elf_bytes[section_offset:section_offset+0x28])

elf_path.write_bytes(elf_bytes)
