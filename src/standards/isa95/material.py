"""ISA-95 Material model."""


class Material:
    def __init__(self, id, name, lot=None):
        self.id = id
        self.name = name
        self.lot = lot
        self.properties = {}
        self.sublots = []

class MaterialClass:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.property_defs = []

    def add_prop(self, name, type_, uom, required=False):
        self.property_defs.append({
            "name": name, "type": type_,
            "uom": uom, "required": required,
        })
