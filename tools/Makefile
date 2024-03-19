VERSION ?= us


WIBO_DIR    := wibo
WIBO_BINARY := $(WIBO_DIR)/wibo


all: $(WIBO_BINARY)

clean:
	$(RM) -rf $(WIBO_DIR)

distclean: clean

.PHONY: all clean distclean

$(WIBO_BINARY): | $(WIBO_DIR)
	wget https://github.com/decompals/wibo/releases/latest/download/wibo --directory-prefix=$(WIBO_DIR)
	chmod +x $(WIBO_DIR)/*

$(WIBO_DIR):
	mkdir -p $@
