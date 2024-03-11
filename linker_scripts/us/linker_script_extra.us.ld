_gp = main_SDATA_START + 0x7FF0;

_end = main_VRAM_END;
_fbss = main_SBSS_START;

_stack = 0x01F80000;
_stack_size = 0x00080000;
_heap_size = 0xFFFFFFFF;

ENTRYPOINT = _start;
ENTRY(ENTRYPOINT);
