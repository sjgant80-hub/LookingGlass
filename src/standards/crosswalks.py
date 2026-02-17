"""Cross-standard mappings (δ maps)."""

CROSSWALKS = {
    "ISA95_ISA88": {
        "WorkCenter": "ProcessCell",
        "WorkUnit": "Unit",
        "ProcessSegment": "Operation",
    },
    "ISA95_OPCUA": {
        "Equipment": "Object",
        "Property": "Variable",
        "Capability": "Method",
    },
    "ISA88_PackML": {
        "Phase.RUNNING": "EXECUTE",
        "Phase.HELD": "HELD",
        "Phase.ABORTED": "ABORTED",
    },
    "OPCUA_Sparkplug": {
        "Variable": "Metric",
        "Subscription": "NDATA/DDATA",
        "Method": "NCMD/DCMD",
    },
}


def crosswalk(entity, from_std, to_std):
    key = f"{from_std}_{to_std}"
    mapping = CROSSWALKS.get(key, {})
    return mapping.get(entity)
