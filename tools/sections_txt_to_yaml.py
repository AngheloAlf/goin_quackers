from pathlib import Path
import re

regex = re.compile(r"\s*[0-9]+: (?P<address>[0-9a-fA-F]{8}) .+5 (?P<section>[^ ]+)")

ADDRESS = 0x00200000
START = 0x000100

section_mapping = {
    ".text": "asm",
    ".data": "data",
    ".rodata": "rodata",
    ".bss": "bss",
    ".vutext": "vutext",
    ".vubss": "vubss",
}

noloads = {
    "bss",
    "vubss",
    "sbss",
}

sections: list[tuple[int, str]] = []

with Path("tools/elf_sections.us.txt").open() as f:
    for line in f:
        m = regex.match(line.strip())
        assert m is not None
        address = int(m["address"], 16)
        section = m["section"]
        # print(address, section)
        if address < ADDRESS:
            print(f"yeeting {section}")
            continue

        sections.append((address, section))

sections.sort()

for address, section in sections:
    start = address - ADDRESS + START
    splat_type = section_mapping[section]

    if splat_type in noloads:
        print(f"      - {{ type: {splat_type}, vram: 0x{address:08X}, name: main/{address:08X} }}")
    else:
        print(f"      - [0x{start:06X}, {splat_type}, main/{start:06X}]")
