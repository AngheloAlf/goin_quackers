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

sections: list[tuple[int, str, str]] = []

current_text_name = f""

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

        if section in {".text", ".vutext"}:
            start = address - ADDRESS + START
            current_text_name = f"{start:06X}"

        sections.append((address, section, current_text_name))

sections.sort()

for address, section, filename in sections:
    start = address - ADDRESS + START
    splat_type = section_mapping[section]

    if splat_type in noloads:
        print(f"      - {{ type: {splat_type}, vram: 0x{address:08X}, name: main/{filename} }}")
    else:
        print(f"      - [0x{start:06X}, {splat_type}, main/{filename}]")
