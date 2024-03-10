from pathlib import Path
import re
import sys

regex = re.compile(r"[0-9]+: (?P<address>[0-9a-fA-F]{8})\s+(?P<size>[0-9]+)\s+(?P<type>[^ ]+)\s+(?P<bind>.+?)\s+DEFAULT.+5 (?P<name>.+)")

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

sym_binds = ["NOTYPE", "LOCAL", "WEAK", "GLOBAL", "<processor specific>: 13", "<processor specific>: 15"]

known_addresses: dict[str, set[int]] = { bind: set() for bind in sym_binds }
duped_addresses: dict[str, set[int]] = { bind: set() for bind in sym_binds }

known_names: dict[str, set[str]] = { bind: set() for bind in sym_binds }
duped_names: dict[str, set[str]] = { bind: set() for bind in sym_binds }

banned_names = {
    "__gnu_compiled_c",
    "gcc2_compiled.",
    ".text",
    ".vutext",
    ".data",
    ".rodata",
    ".bss",
    ".vubss",
}

for address, size, typ, bind, name in syms:
    if name in banned_names:
        continue
    if typ in {"SECTION"}:
        continue

    # print(address, size, typ, bind, name, "\n", file=sys.stderr)

    if address in known_addresses[bind]:
        duped_addresses[bind].add(address)
    if name in known_names[bind]:
        duped_names[bind].add(name)

    known_addresses[bind].add(address)
    known_names[bind].add(name)

for address, size, typ, bind, name in syms:
    if name in banned_names:
        continue
    if typ in {"SECTION"}:
        continue

    comment_out = ""

    if name.startswith("@"):
        comment_out = "// "
    elif address in duped_addresses[bind] or name in duped_names[bind]:
        comment_out = "// "
    else:
        bind_index = sym_binds.index(bind)
        for i in range(bind_index+1, len(sym_binds)):
            cur_bind = sym_binds[i]
            if address in known_addresses[cur_bind] or name in known_names[cur_bind]:
                comment_out = "// "
                break

    # print(address, size, typ, bind, name)
    typ_str = ""
    if typ == "FUNC":
        typ_str = " type:func"
    bind = bind.replace(":", "")

    assert size >= 0, size
    size_str = ""
    if size > 0:
        size_str = f" size:0x{size:X}"

    print(f"{comment_out}{name} = 0x{address:08X}; //{size_str}{typ_str} bind = {bind}")

# for address in duped_addresses:
#     print(f"0x{address:08X}", file=sys.stderr)
# 
# for name in duped_names:
#     print(f"{name}", file=sys.stderr)
