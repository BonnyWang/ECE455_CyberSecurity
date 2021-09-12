CC := gcc
CCFLAGS := -m32 -static -g -Wno-deprecated-declarations -fno-stack-protector
LDFLAGS :=

SOURCES := read_data.c
TARGET := read_data

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $< -o $@ $(CCFLAGS)

clean:
	rm -f $(TARGET)
