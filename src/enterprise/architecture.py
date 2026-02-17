"""Enterprise Architecture → Cube mapping."""

LEVELS = {
    "L4": {"name": "Business", "maps_to": "enterprise_array"},
    "L3": {"name": "MOM/MES", "maps_to": "site_cluster"},
    "L2": {"name": "Control", "maps_to": "area_group"},
    "L1": {"name": "Sensing", "maps_to": "unit_cube"},
    "L0": {"name": "Process", "maps_to": "vertex_node"},
}


class EnterpriseMap:
    """Maps ISA-95 hierarchy to cube topology."""

    def __init__(self):
        self.levels = dict(LEVELS)
        self.nodes = {}

    def register(self, level, node_id, cube_ref):
        self.nodes[(level, node_id)] = cube_ref

    def lookup(self, level, node_id):
        return self.nodes.get((level, node_id))

    def cube_for_level(self, level):
        info = self.levels.get(level, {})
        return info.get("maps_to")

    def hierarchy(self):
        return {k: v["name"] for k, v in self.levels.items()}
