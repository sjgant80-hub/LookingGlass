"""ISA-101 HMI navigation layers."""

HMI_LAYERS = {
    "L1": {"name": "Overview", "scope": "Plant/Site",
            "info": "KPIs, Status, Alarms"},
    "L2": {"name": "Area", "scope": "Process Area",
            "info": "Flows, States, Trends"},
    "L3": {"name": "Unit", "scope": "Equipment",
            "info": "Faceplate, Control"},
    "L4": {"name": "Detail", "scope": "Diagnostic",
            "info": "Config, Tuning"},
    "L5": {"name": "Support", "scope": "Maintenance",
            "info": "Calibration, History"},
}
