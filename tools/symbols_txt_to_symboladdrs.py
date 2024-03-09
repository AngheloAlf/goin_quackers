from pathlib import Path
import re
import sys

regex = re.compile(r"[0-9]+: (?P<address>[0-9a-fA-F]{8})\s+(?P<size>[0-9]+)\s+(?P<type>[^ ]+)\s+(?P<bind>.+)\s+DEFAULT.+5 (?P<name>.+)")

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

        syms.append((address, size, typ, bind, name))

syms.sort()

known_addresses: set[int] = set()
duped_addresses: set[int] = set()

known_names: set[str] = set()
duped_names: set[str] = set()

for address, size, typ, bind, name in syms:
    if address in known_addresses:
        duped_addresses.add(address)
    if name in known_names:
        duped_names.add(name)

    known_addresses.add(address)
    known_names.add(name)

for address, size, typ, bind, name in syms:
    comment_out = ""
    if address in duped_addresses or name in duped_names:
        comment_out = "// "
    # print(address, size, typ, bind, name)
    typ_str = ""
    if typ == "FUNC":
        typ_str = " type:func"
    bind = bind.replace(":", "")
    print(f"{comment_out}{name} = 0x{address:08X}; // size:0x{size:X}{typ_str} bind = {bind}")

# for address in duped_addresses:
#     print(f"0x{address:08X}", file=sys.stderr)
# 
# for name in duped_names:
#     print(f"{name}", file=sys.stderr)
