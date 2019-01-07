BIN_NAME = main

# CXX = g++
# LD  = g++

CXX = gcc
LD  = icpc

CXXFLAGS =`pkg-config fuse3 --cflags --libs`

MDIR ?= tmp
SRC_DIR = src
BIN_DIR = bin
BUILD_DIR = build
LOG_DIR = logs
SRC = $(wildcard $(SRC_DIR)/*.c)
OBJ = $(patsubst src/%.c,build/%.o,$(SRC))
DEPS = $(patsubst build/%.o,build/%.d,$(OBJ))
BIN = $(BIN_NAME)

vpath %.c $(SRC_DIR)

.DEFAULT_GOAL = all

$(BUILD_DIR)/%.d: %.c
	$(CXX) -M -Wall $< $(CXXFLAGS) -o $@

$(BUILD_DIR)/%.o: %.c
	$(CXX) -c -Wall $< $(CXXFLAGS) -o $@

$(BIN_DIR)/$(BIN_NAME): $(DEPS) $(OBJ)
	$(CXX) -Wall $(OBJ) $(CXXFLAGS) -o $@

checkdirs:
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BIN_DIR)

all: checkdirs $(BIN_DIR)/$(BIN_NAME)

run: clean all
	./bin/main $(MDIR)
	echo Use fusermount3 -u $(MDIR) to unmount the filesystem.

clean:
	rm -f $(BUILD_DIR)/* $(BIN_DIR)/* $(LOG_DIR)/*
