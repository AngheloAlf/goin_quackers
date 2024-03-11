_gp = main_SDATA_START + 0x7FF0;

_fbss = main_SBSS_START;

end = main_VRAM_END;
_end = end;

__static_init = main_CTOR_START;
__static_init_end = main_CTOR_END;

_stack = 0x01F80000;
_stack_size = 0x00080000;
_heap_size = 0xFFFFFFFF;

ENTRYPOINT = _start;
ENTRY(ENTRYPOINT);
