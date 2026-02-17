"""ISA-88 State machines."""
from ..meta import StateMachine

PhaseState = StateMachine("PhaseState", [
    "IDLE", "RUNNING", "COMPLETE",
    "HOLDING", "HELD", "RESTARTING",
    "STOPPING", "STOPPED",
    "ABORTING", "ABORTED",
], initial="IDLE")

PhaseState.add("IDLE", "RUNNING", "start")
PhaseState.add("RUNNING", "COMPLETE", "done")
PhaseState.add("RUNNING", "HOLDING", "hold")
PhaseState.add("HELD", "RESTARTING", "restart")
PhaseState.add("RUNNING", "STOPPING", "stop")
PhaseState.add("RUNNING", "ABORTING", "abort")

BatchState = StateMachine("BatchState", [
    "Created", "Scheduled", "Running",
    "Complete", "Held", "Aborted",
], initial="Created")

BatchState.add("Created", "Scheduled", "schedule")
BatchState.add("Scheduled", "Running", "start")
BatchState.add("Running", "Complete", "done")
BatchState.add("Running", "Held", "hold")
BatchState.add("Running", "Aborted", "abort")
