from pathlib import Path
import re
import sys

ILLEGAL_FILENAME_CHARS = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]

regex = re.compile(r"[0-9]+: (?P<address>[0-9a-fA-F]{8})\s+(?P<size>[0-9]+)\s+(?P<type>[^ ]+)\s+(?P<bind>.+?)\s+DEFAULT.+5 (?P<name>.+)")

def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)

defined_elsewhere_names: set[str] = set()
defined_elsewhere_addrs: set[int] = set()

def parse_other_file(other_path: Path, do_addrs: bool):
    with other_path.open() as f:
        for line in f:
            line = line.split("//")[0]
            if "=" not in line:
                continue
            name, addr = line.split("=")
            name = name.strip()
            addr = addr.strip()[:-1].strip()
            defined_elsewhere_names.add(name)
            if do_addrs:
                defined_elsewhere_addrs.add(int(addr, 16))

parse_other_file(Path("config/us/symbol_addrs.txt"), True)
parse_other_file(Path("linker_scripts/us/linker_script_extra.us.ld"), False)


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
        if address not in defined_elsewhere_addrs and name not in defined_elsewhere_names:
            duped_addresses[bind].add(address)
    if name in known_names[bind]:
        if address not in defined_elsewhere_addrs and name not in defined_elsewhere_names:
            duped_names[bind].add(name)

    if address not in defined_elsewhere_addrs and name not in defined_elsewhere_names:
        known_addresses[bind].add(address)
    if address not in defined_elsewhere_addrs and name not in defined_elsewhere_names:
        known_names[bind].add(name)

for address, size, typ, bind, name in syms:
    if name in banned_names:
        continue
    if typ in {"SECTION"}:
        continue

    comment_out = ""

    if name.startswith("@"):
        comment_out = "// "
    elif name in defined_elsewhere_names or address in defined_elsewhere_addrs:
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
    prefix = "D_"
    if typ == "FUNC":
        typ_str = " type:func"
        prefix = "func_"
    bind = bind.replace(":", "")

    assert size >= 0, size
    size_str = ""
    if size > 0:
        size_str = f" size:0x{size:X}"

    filename_str = ""
    if len(name) > 253 or any(c in ILLEGAL_FILENAME_CHARS for c in name):
        filename_str = f" filename:{prefix}{address:08X}"

    print(f"{comment_out}{name} = 0x{address:08X}; //{size_str}{typ_str}{filename_str} bind = {bind}")

# for address in duped_addresses:
#     print(f"0x{address:08X}", file=sys.stderr)
# 
# for name in duped_names:
#     print(f"{name}", file=sys.stderr)
