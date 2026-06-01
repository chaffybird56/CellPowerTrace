CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c11 -O2
LDFLAGS ?=
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
  LDFLAGS += -lrt
endif

pm_sim: pm_sim.c pm_sim.h
	$(CC) $(CFLAGS) -o pm_sim pm_sim.c $(LDFLAGS)

clean:
	rm -f pm_sim

.PHONY: clean
