CC ?= gcc
CFLAGS ?= -Wall -Wextra -std=c11 -O2

pm_sim: pm_sim.c pm_sim.h
	$(CC) $(CFLAGS) -o pm_sim pm_sim.c

clean:
	rm -f pm_sim

.PHONY: clean
