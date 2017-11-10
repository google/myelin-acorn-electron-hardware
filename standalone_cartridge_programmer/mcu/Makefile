BOARD_TAG = leonardo

# Not wanting to change the folder layout for libxsvf necessitates the following
# Makefile hackery.

# Predefine this so we can use it for libsxvf
OBJDIR = build-$(BOARD_TAG)

LIBXSVF_PATH := $(realpath ../../third_party/libxsvf)
LIBXSVF_OBJS = $(addprefix $(OBJDIR)/libxsvf/, \
  memname.c.o play.c.o scan.c.o statename.c.o svf.c.o tap.c.o xsvf.c.o \
	xsvftool-arduino.cpp.o)

# Add libxsvf to the include path
CPPFLAGS = -I$(LIBXSVF_PATH)
# Link libxsvf into target
OTHER_OBJS := $(LIBXSVF_OBJS)

# Build rules for libxsvf objects
$(OBJDIR)/libxsvf/%.c.o: $(LIBXSVF_PATH)/%.c
	@$(MKDIR) $(dir $@)
	$(CC) -MMD -c $(CPPFLAGS) $(CFLAGS) $< -o $@
$(OBJDIR)/libxsvf/%.cpp.o: $(LIBXSVF_PATH)/%.cpp
	@$(MKDIR) $(dir $@)
	$(CXX) -MMD -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

include ../../third_party/Arduino-Makefile/Arduino.mk
