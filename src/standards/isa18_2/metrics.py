"""ISA-18.2 Alarm performance metrics."""

TARGETS = {
    "alarm_rate": {"max": 6, "unit": "alarms/op/hr"},
    "peak_rate": {"max": 12, "unit": "alarms/op/hr"},
    "flood": {"threshold": 10, "window_min": 10},
    "stale_hours": 24,
    "chatter": {"transitions_per_min": 3},
    "priority_pct": {1: 5, 2: 15, 3: 25, 4: 55},
}


def alarm_metrics(alarms):
    total = len(alarms)
    if total == 0:
        return {"total": 0, "healthy": True}
    by_pri = {}
    for a in alarms:
        by_pri[a.priority] = by_pri.get(a.priority, 0) + 1
    return {
        "total": total,
        "by_priority": by_pri,
        "healthy": total <= TARGETS["alarm_rate"]["max"],
    }
