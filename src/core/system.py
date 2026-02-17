"""KonomiSystem - Top-level orchestrator."""
from .evgpu import eVGPU
from .block_array import BlockArray
from .cube import Cube


class KonomiSystem:
    """Main system: manages arrays and cubes."""

    def __init__(self, cores=4):
        self.evgpu = eVGPU(cores)
        self.arrays = {}
        self.cubes = {}

    def create_block_array(self, name, dims=(10, 10, 10)):
        ba = BlockArray(dims)
        self.arrays[name] = ba
        return ba

    def create_cube(self, cube_id):
        cube = Cube(cube_id)
        self.cubes[cube_id] = cube
        return cube

    def status(self):
        return {
            "arrays": list(self.arrays.keys()),
            "cubes": list(self.cubes.keys()),
            "cores": self.evgpu.cores,
        }
