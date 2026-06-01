#ifndef PM_SIM_H
#define PM_SIM_H

#include <stdint.h>

typedef enum {
    PM_IDLE = 0,
    PM_CONNECTED,
    PM_DRX,
    PM_DEEP_SLEEP
} pm_state_t;

typedef struct {
    pm_state_t state;
    double score_mw;
    uint64_t timestamp_ms;
    char event[128];
} pm_trace_entry_t;

const char *pm_state_name(pm_state_t s);
pm_state_t pm_state_from_event(const char *line);
double pm_default_score_mw(pm_state_t s);

#endif
