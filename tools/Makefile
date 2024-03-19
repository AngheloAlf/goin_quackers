VERSION ?= us


WIBO_DIR    := wibo
WIBO_BIN    := $(WIBO_DIR)/wibo

MWCPS2_DIR  := mwcps2/2.3-991202
MWCPS2_BIN  := $(MWCPS2_DIR)/mwccmips.exe


all: $(WIBO_BIN) $(MWCPS2_BIN)

clean:
	$(RM) -rf $(WIBO_DIR)

distclean: clean

.PHONY: all clean distclean

$(WIBO_BIN): | $(WIBO_DIR)
	wget https://github.com/decompals/wibo/releases/latest/download/wibo --directory-prefix=$(WIBO_DIR)
	chmod +x $(WIBO_DIR)/wibo

$(MWCPS2_BIN): | $(MWCPS2_DIR)
	wget https://github.com/AngheloAlf/mwcps2/releases/latest/download/mwcps2-2.3-991202.tar.gz
	tar xf mwcps2-2.3-991202.tar.gz -C $(MWCPS2_DIR)
	$(RM) mwcps2-2.3-991202.tar.gz

$(WIBO_DIR):
	mkdir -p $@

$(MWCPS2_DIR):
	mkdir -p $@
