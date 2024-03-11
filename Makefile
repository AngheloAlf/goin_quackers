# Build options can be changed by modifying the makefile or by building with 'make SETTING=value'.
# It is also possible to override the settings in Defaults in a file called .make_options as 'SETTING=value'.

-include .make_options

MAKEFLAGS += --no-builtin-rules

SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -c

#### Defaults ####

COMPILER_VERBOSE ?= 0

# Set prefix to mips binutils binaries (mips-linux-gnu-ld => 'mips-linux-gnu-') - Change at your own risk!
# In nearly all cases, not having 'mips-linux-gnu-*' binaries on the PATH is indicative of missing dependencies
CROSS ?= mips-linux-gnu-


VERSION ?= us

BASEROM              := disk/$(VERSION)/SLUS_200.77
TARGET               := goin_quackers


### Output ###

BUILD_DIR := build/$(VERSION)
ROM       := $(BUILD_DIR)/$(TARGET).$(VERSION).rom
ELF       := $(BUILD_DIR)/$(TARGET).$(VERSION).elf
LD_MAP    := $(BUILD_DIR)/$(TARGET).$(VERSION).map
LD_SCRIPT := linker_scripts/$(VERSION)/$(TARGET).$(VERSION).ld


#### Setup ####

BUILD_DEFINES ?=

ifeq ($(VERSION),us)
    BUILD_DEFINES   += -DVERSION_US=1
else ifeq ($(VERSION),eu)
    BUILD_DEFINES   += -DVERSION_EU=1
$(error VERSION 'eu' is not currently supported, shorry)
else
$(error Invalid VERSION variable detected. Please use 'us')
endif

MAKE = make
CPPFLAGS += -fno-dollars-in-identifiers -P
LDFLAGS  := --no-check-sections --emit-relocs

UNAME_S := $(shell uname -s)
ifeq ($(OS),Windows_NT)
    DETECTED_OS := windows
else ifeq ($(UNAME_S),Linux)
    DETECTED_OS := linux
else ifeq ($(UNAME_S),Darwin)
    DETECTED_OS := mac
    MAKE := gmake
    CPPFLAGS += -xc++
endif


#### Tools ####
ifneq ($(shell type $(CROSS)ld >/dev/null 2>/dev/null; echo $$?), 0)
$(error Please install or build $(CROSS))
endif

CC              := 

AS              := $(CROSS)as
LD              := $(CROSS)ld
OBJCOPY         := $(CROSS)objcopy
OBJDUMP         := $(CROSS)objdump
GCC             := $(CROSS)gcc
CPP             := $(CROSS)cpp
STRIP           := $(CROSS)strip

PYTHON          ?= python3

SPLAT             ?= $(PYTHON) -m splat split
SPLAT_YAML        ?= config/$(VERSION)/$(TARGET).$(VERSION).yaml

SPLAT_FLAGS       ?=
ifneq ($(FULL_DISASM),0)
    SPLAT_FLAGS       += --disassemble-all
endif

export SPIMDISASM_PANIC_RANGE_CHECK="True"


IINC       := -Iinclude


## CC CHECK ##


## Compiler options ##

CFLAGS          += 

WARNINGS        := 
ASFLAGS         := -march=r5900 -mabi=eabi -G8 -no-pad-sections
COMMON_DEFINES  := 
AS_DEFINES      := 
C_DEFINES       := 
ENDIAN          := -EL

OPTFLAGS        := -O4
DBGFLAGS        :=
# DBGFLAGS        := -gdwarf
# MIPS_VERSION    := -mips3
# OUT_ENCODING    := Shift-JIS
# CHAR_SIGN       := -funsigned-char

ifneq ($(COMPILER_VERBOSE),0)
    COMP_VERBOSE_FLAG := -v
else
    COMP_VERBOSE_FLAG :=
endif


### OBJDUMP ###

# Use relocations and abi fpr names in the dump
# OBJDUMP_FLAGS := --disassemble --reloc --disassemble-zeroes -Mreg-names=32
OBJDUMP_FLAGS := --disassemble --reloc --disassemble-zeroes

ifneq ($(OBJDUMP_BUILD), 0)
    OBJDUMP_CMD = @$(OBJDUMP) $(OBJDUMP_FLAGS) $@ > $(@:.o=.dump.s)
else
    OBJDUMP_CMD = @:
endif


#### Files ####

# $(shell mkdir -p asm bin linker_scripts/$(VERSION)/auto)

SRC_DIRS      := $(shell find src -type d)
ASM_DIRS      := $(shell find asm/$(VERSION) -type d -not -path "asm/$(VERSION)/nonmatchings/*")
BIN_DIRS      := $(shell find bin/$(VERSION) -type d)

C_FILES       := $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.c))
CPP_FILES     := $(foreach dir,$(SRC_DIRS),$(wildcard $(dir)/*.cpp))
S_FILES       := $(foreach dir,$(ASM_DIRS) $(SRC_DIRS),$(wildcard $(dir)/*.s))

O_FILES       := $(foreach f,$(C_FILES:.c=.o),$(BUILD_DIR)/$f) \
                 $(foreach f,$(C_FILES:.cpp=.o),$(BUILD_DIR)/$f) \
                 $(foreach f,$(S_FILES:.s=.o),$(BUILD_DIR)/$f)

# LINKER_SCRIPTS   := $(LD_SCRIPT) $(BUILD_DIR)/linker_scripts/$(VERSION)/hardware_regs.ld $(BUILD_DIR)/linker_scripts/$(VERSION)/undefined_syms.ld $(BUILD_DIR)/linker_scripts/common_undef_syms.ld
LINKER_SCRIPTS   := $(LD_SCRIPT) $(BUILD_DIR)/linker_scripts/$(VERSION)/linker_script_extra.$(VERSION).ld linker_scripts/$(VERSION)/auto/undefined_funcs_auto.ld linker_scripts/$(VERSION)/auto/undefined_syms_auto.ld


### Automatic dependency files ###
DEP_FILES := $(LD_SCRIPT:.ld=.d)

#ifneq ($(DEP_ASM), 0)
#    DEP_FILES += $(O_FILES:.o=.asmproc.d)
#endif
#
#ifneq ($(DEP_INCLUDE), 0)
#    DEP_FILES += $(O_FILES:.o=.d)
#endif


##### Directory flags #####

##### Per-file flags #####

## Create build directories

$(shell mkdir -p $(BUILD_DIR)/linker_scripts/$(VERSION))
$(shell mkdir -p $(foreach dir,$(SRC_DIRS) $(ASM_DIRS) $(BIN_DIRS),$(BUILD_DIR)/$(dir)))


#### Main Targets ###

all: rom

rom: $(ROM)
ifneq ($(COMPARE),0)
	@md5sum $(ROM)
	@md5sum -c config/$(VERSION)/$(TARGET).$(VERSION).md5
endif

clean:
	$(RM) -r $(BUILD_DIR)/asm $(BUILD_DIR)/bin $(BUILD_DIR)/src $(ROM) $(ROMC) $(ELF)

libclean:
	$(RM) -r $(BUILD_DIR)/lib

distclean: clean
	$(RM) -r $(BUILD_DIR) asm/ bin/ .splat/
#	$(RM) -r linker_scripts/$(VERSION)/auto $(LD_SCRIPT)
	$(MAKE) -C tools distclean

setup:
	$(MAKE) -C tools

extract:
	$(RM) -r asm/$(VERSION) bin/$(VERSION) $(LD_SCRIPT) $(LD_SCRIPT:.ld=.d)
	$(SPLAT) $(SPLAT_YAML) $(SPLAT_FLAGS)

diff-init: all
	$(RM) -rf expected/$(BUILD_DIR)
	mkdir -p expected/$(BUILD_DIR)
	cp -r $(BUILD_DIR)/* expected/$(BUILD_DIR)

init:
	$(MAKE) distclean
	$(MAKE) setup
	$(MAKE) extract
	$(MAKE) all
	$(MAKE) diff-init

format:
	clang-format-11 -i -style=file $(C_FILES) $(CPP_FILES)

tidy:
	clang-tidy-11 -p . --fix --fix-errors $(C_FILES) $(CPP_FILES) -- $(CC_CHECK_FLAGS) $(IINC) -I build/$(VERSION)/src/main_segment $(CHECK_WARNINGS) $(BUILD_DEFINES) $(COMMON_DEFINES) $(C_DEFINES)


.PHONY: all rom clean distclean setup extract diff-init init format tidy
.DEFAULT_GOAL := all
# Prevent removing intermediate files
.SECONDARY:


#### Various Recipes ####

$(ROM): $(ELF)
	$(OBJCOPY) -O binary $< $@

$(ELF): $(LINKER_SCRIPTS)
	$(LD) $(ENDIAN) $(LDFLAGS) -G8 -Map $(LD_MAP) $(foreach ld, $(LINKER_SCRIPTS), -T $(ld)) -o $@ $(filter %.o, $^)


## Order-only prerequisites
# These ensure e.g. the PNG_INC_FILES are built before the O_FILES.
# The intermediate phony targets avoid quadratically-many dependencies between the targets and prerequisites.

o_files: $(O_FILES)

.PHONY: o_files


$(BUILD_DIR)/%.ld: %.ld
	$(CPP) $(CPPFLAGS) $(BUILD_DEFINES) $(IINC) $(COMP_VERBOSE_FLAG) $< > $@

$(BUILD_DIR)/%.o: %.s
	$(CPP) $(CPPFLAGS) $(BUILD_DEFINES) $(IINC) -I $(dir $*) -I $(BUILD_DIR)/$(dir $*) $(COMMON_DEFINES) $(AS_DEFINES) $(COMP_VERBOSE_FLAG) $< | $(AS) $(ASFLAGS) $(ENDIAN) $(IINC) -I $(dir $*) -I $(BUILD_DIR)/$(dir $*) $(COMP_VERBOSE_FLAG) -o $@
	$(PYTHON) tools/buildtools/elf_patcher.py $@
	$(OBJDUMP_CMD)



-include $(DEP_FILES)

# Print target for debugging
print-% : ; $(info $* is a $(flavor $*) variable set to [$($*)]) @true
