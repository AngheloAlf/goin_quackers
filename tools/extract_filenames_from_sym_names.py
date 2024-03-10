from pathlib import Path
import re
import sys

regex = re.compile(r"[0-9]+: (?P<address>[0-9a-fA-F]{8})\s+(?P<size>[0-9]+)\s+(?P<type>[^ ]+)\s+(?P<bind>.+?)\s+DEFAULT.+5 (?P<name>.+)")

ADDRESS = 0x00200000
START = 0x000100

syms: list[tuple[int, int, str, str, str]] = []

with Path("tools/elf_syms.us.txt").open() as f:
    for line in f:
        m = regex.match(line.strip())
        if m is None:
            continue
        address = int(m["address"], 16)
        size = int(m["size"])
        typ = m["type"]
        bind = m["bind"]
        name = m["name"]

        if not name.endswith(".c") and not name.endswith(".cpp"):
            continue

        syms.append((address, size, typ, bind, name))

syms.sort()

for address, size, typ, bind, name in syms:
    start = address - ADDRESS + START
    # print(f"0x{address:08X}", f"0x{start:06X}", f"0x{size:X}", typ, bind, name)

    if name.startswith(".p__sinit_"):
        typ = "ctor"
        name = name.removeprefix(".p__sinit_")
    elif name.startswith("__sinit_"):
        typ = "init"
        name = name.removeprefix("__sinit_")
    else:
        assert False, (f"0x{address:08X}", f"0x{start:06X}", f"0x{size:X}", typ, bind, name)

    name, extension = name.split(".")

    print(f"      - [0x{start:06X}, {typ}, main/{name}] # {extension}")

