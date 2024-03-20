#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 AngheloAlf
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import spimdisasm
from pathlib import Path
import struct

def align_up(x: int, a: int) -> int:
    return (x + (a-1)) & ~(a-1)

SECTIONS_TO_REALIGN_PER_TOOL: dict[str, dict[str, int]] = {
    "gas": {
        ".text": 4,
        ".data": 4,
        ".rodata": 4,
        ".ctor": 4,
        ".init": 4,
        ".exceptix": 4,
        ".vtables": 0x10,
        ".sdata": 4,
        ".sbss": 4,
        ".bss": 4,
    },
    "mwcc": {
        ".text": 0x10,
    }
}

parser = argparse.ArgumentParser()

parser.add_argument("elf_path")
parser.add_argument("mode", choices=["gas", "mwcc"])

args = parser.parse_args()

elf_path = Path(args.elf_path)

elf_bytes = bytearray(elf_path.read_bytes())

elf_file = spimdisasm.elf32.Elf32File(elf_bytes)

sections_to_realign = SECTIONS_TO_REALIGN_PER_TOOL[args.mode]

for i, sect in enumerate(elf_file.sectionHeaders):
    name = elf_file.shstrtab[sect.name]
    # print(name, sect)

    new_alignment = sections_to_realign.get(name)
    if new_alignment is not None:
        section_offset = elf_file.header.shoff + i * 0x28
        addralign_pointer = section_offset + 0x20
        size_pointer = section_offset + 0x14

        # Patch the alignment of the section
        fmt = spimdisasm.common.GlobalConfig.ENDIAN.toFormatString() + "I"
        struct.pack_into(fmt, elf_bytes, addralign_pointer, new_alignment)

        new_size = align_up(sect.size, new_alignment)
        # Patch the size of the section
        fmt = spimdisasm.common.GlobalConfig.ENDIAN.toFormatString() + "I"
        struct.pack_into(fmt, elf_bytes, size_pointer, new_size)

        # print(name)
        # print(elf_bytes[section_offset:section_offset+0x28])

elf_path.write_bytes(elf_bytes)
