#define _POSIX_C_SOURCE 200809L

#include "pm_sim.h"

#include <stdio.h>
#include <string.h>
#include <time.h>

static uint64_t now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return (uint64_t)ts.tv_sec * 1000ull + (uint64_t)(ts.tv_nsec / 1000000ull);
}

const char *pm_state_name(pm_state_t s) {
    switch (s) {
    case PM_IDLE: return "IDLE";
    case PM_CONNECTED: return "CONNECTED";
    case PM_DRX: return "DRX";
    case PM_DEEP_SLEEP: return "DEEP_SLEEP";
    default: return "UNKNOWN";
    }
}

double pm_default_score_mw(pm_state_t s) {
    switch (s) {
    case PM_CONNECTED: return 450.0;
    case PM_IDLE: return 120.0;
    case PM_DRX: return 45.0;
    case PM_DEEP_SLEEP: return 8.0;
    default: return 100.0;
    }
}

pm_state_t pm_state_from_event(const char *line) {
    if (strstr(line, "RegistrationAccept") || strstr(line, "RRCConnected")) {
        return PM_CONNECTED;
    }
    if (strstr(line, "DRX")) {
        return PM_DRX;
    }
    if (strstr(line, "DEEP_SLEEP") || strstr(line, "DeregistrationAccept")) {
        return PM_DEEP_SLEEP;
    }
    if (strstr(line, "enter IDLE") || strstr(line, "PM: state IDLE")) {
        return PM_IDLE;
    }
    if (strstr(line, "PM: state CONNECTED")) {
        return PM_CONNECTED;
    }
    if (strstr(line, "PM: state DRX")) {
        return PM_DRX;
    }
    return PM_IDLE;
}

int main(int argc, char **argv) {
    const char *events_path = (argc > 1) ? argv[1] : "-";
    const char *out_path = (argc > 2) ? argv[2] : "power_trace.jsonl";

    FILE *in = stdin;
    if (strcmp(events_path, "-") != 0) {
        in = fopen(events_path, "r");
        if (!in) {
            perror(events_path);
            return 1;
        }
    }

    FILE *out = fopen(out_path, "w");
    if (!out) {
        perror(out_path);
        if (in != stdin) fclose(in);
        return 1;
    }

    pm_state_t cur = PM_IDLE;
    char line[512];
    while (fgets(line, sizeof(line), in)) {
        pm_state_t next = pm_state_from_event(line);
        if (next != cur) {
            cur = next;
            fprintf(out,
                    "{\"ts_ms\":%llu,\"state\":\"%s\",\"score_mw\":%.1f,\"event\":",
                    (unsigned long long)now_ms(), pm_state_name(cur),
                    pm_default_score_mw(cur));
            fputc('"', out);
            for (char *p = line; *p; p++) {
                if (*p == '"' || *p == '\\') fputc('\\', out);
                if (*p == '\n' || *p == '\r') continue;
                fputc(*p, out);
            }
            fputs("\"}\n", out);
        }
    }

    if (in != stdin) fclose(in);
    fclose(out);
    fprintf(stderr, "[pm_sim] wrote %s\n", out_path);
    return 0;
}
