# Compila la librería JNI contra cabeceras de OpenJDK de Termux.
# Termux exporta CC=clang y CFLAGS en el entorno: por eso se fijan aquí.
# Uso: make [-C bin/native_lib] [CC=...] [JAVA_HOME=...] [EXTRA_CFLAGS=...]
CC := aarch64-linux-android-clang
REQUIRED_CFLAGS := -O2 -fPIC -shared -Wall -Wextra
EXTRA_CFLAGS ?=

JAVA_HOME ?= $(or $(wildcard $(PREFIX)/lib/jvm/java-21-openjdk),$(firstword $(wildcard $(PREFIX)/lib/jvm/java-*)))
INCLUDES = -I$(JAVA_HOME)/include -I$(JAVA_HOME)/include/linux

TARGET = liblogger.so
SRC = native_logger.c
ABI ?= arm64-v8a
DEST_DIR = ../../build_payloads/lib/$(ABI)

all: install

$(TARGET): $(SRC)
	@test -f "$(JAVA_HOME)/include/jni.h" || \
		{ echo "JAVA_HOME inválido: $(JAVA_HOME)" >&2; exit 1; }
	$(CC) $(REQUIRED_CFLAGS) $(EXTRA_CFLAGS) -o $@ $< $(INCLUDES)

install: $(TARGET)
	mkdir -p $(DEST_DIR)
	install -m 0644 $(TARGET) $(DEST_DIR)/$(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all install clean
