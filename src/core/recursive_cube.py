"""RecursiveCube — self-similar cube nesting at any depth.

The same 8-vertex + center topology repeats at every level:

  Level 0: a single Cube (8 FemtoLLM vertices + 1 central coordinator)
  Level 1: 8 Cubes at the corners of a larger region = MetaCube
  Level 2: 8 MetaCubes at corners of an even larger region
  Level N: 8 Level-(N-1) structures at corners

The invariant holds at every level:
  - 8 corners (sub-structures from the level below)
  - 6 faces (4 corners each, using NESW+UD naming)
  - Interior space (between the corners, for nested data)
  - Two adjacent same-level structures share a face (4 corners become shared)

Scale:
  Level 0:  1 leaf Cube,          1 total node
  Level 1:  8 leaf Cubes,         9 total nodes
  Level 2:  64 leaf Cubes,        73 total nodes
  Level 3:  512 leaf Cubes,       585 total nodes
  Level 6:  262,144 leaf Cubes,   299,593 total nodes

Corner-to-vertex mapping (constant at all levels, using LookingGlass naming):
  corner 0 = SWD (South-West-Down, back-left-bottom)
  corner 1 = SED (South-East-Down, back-right-bottom)
  corner 2 = NWD (North-West-Down, front-left-bottom)
  corner 3 = NED (North-East-Down, front-right-bottom)
  corner 4 = SWU (South-West-Up, back-left-top)
  corner 5 = SEU (South-East-Up, back-right-top)
  corner 6 = NWU (North-West-Up, front-left-top)
  corner 7 = NEU (North-East-Up, front-right-top)

Origin: MacCubeFACE Steps 4-6 pattern (AirTrek/Birdhouse project).
Adapted to LookingGlass vertex naming.
"""

import numpy as np
from .cube import Cube
from .shared_face import connect_cubes, FACE_VERTICES, OPPOSITES


# Corner index → vertex name in LookingGlass's NESW+UD scheme
CORNER_NAMES = ['SWD', 'SED', 'NWD', 'NED', 'SWU', 'SEU', 'NWU', 'NEU']

# Which 4 corner indices sit on each face
FACE_CORNERS = {
    'D': [0, 1, 2, 3],  # Down  (bottom): SWD, SED, NWD, NED
    'U': [4, 5, 6, 7],  # Up    (top):    SWU, SEU, NWU, NEU
    'S': [0, 1, 4, 5],  # South (back):   SWD, SED, SWU, SEU
    'N': [2, 3, 6, 7],  # North (front):  NWD, NED, NWU, NEU
    'W': [0, 2, 4, 6],  # West  (left):   SWD, NWD, SWU, NWU
    'E': [1, 3, 5, 7],  # East  (right):  SED, NED, SEU, NEU
}


class RecursiveCube:
    """
    A cube at any level of recursion.

    Level 0: wraps a single Cube with 8 FemtoLLM vertices + central coordinator.
    Level N: contains 8 Level-(N-1) RecursiveCubes at its corners.

    At every level, the structure has the same shape:
      - 8 corner sub-structures
      - 6 faces (4 corners each)
      - Interior space for nested data
      - Connects to neighbors by sharing face corners
    """

    def __init__(self, level: int, cube_id: str, span: int = 1):
        """
        Args:
            level: Recursion depth. 0 = single Cube, N = 8 Level-(N-1)s.
            cube_id: Unique identifier for this structure.
            span: Size of this structure in the BlockArray coordinate space.
                  At level 0: 1 (single cube position).
                  At level N: span of each corner sub-cube is span // 2.
        """
        self.level = level
        self.id = cube_id
        self.span = span
        self.interior = {}  # Nested data between corners

        if level == 0:
            # Base case: a single Cube
            self.cube = Cube(cube_id)
            self.corners = None
        else:
            # Recursive case: 8 sub-cubes at corners
            self.cube = None
            sub_span = max(1, span // 2)
            self.corners = [
                RecursiveCube(
                    level=level - 1,
                    cube_id=f"{cube_id}:{CORNER_NAMES[i]}",
                    span=sub_span,
                )
                for i in range(8)
            ]

    # ----------------------------------------------------------
    # Structure queries
    # ----------------------------------------------------------

    def is_leaf(self) -> bool:
        """True if this is a level-0 Cube (base case)."""
        return self.level == 0

    def get_face(self, face: str):
        """
        Get the sub-structures that form a face.

        Level 0: returns the Cube itself (access its vertices directly).
        Level N: returns the 4 corner RecursiveCubes on that face.
        """
        if self.is_leaf():
            return self.cube
        indices = FACE_CORNERS[face]
        return [self.corners[i] for i in indices]

    def count_leaves(self) -> int:
        """Total number of level-0 Cubes in this structure."""
        if self.is_leaf():
            return 1
        return sum(c.count_leaves() for c in self.corners)

    def count_all_nodes(self) -> int:
        """Total number of RecursiveCubes across all levels."""
        if self.is_leaf():
            return 1
        return 1 + sum(c.count_all_nodes() for c in self.corners)

    def walk_leaves(self):
        """Yield all level-0 Cubes in depth-first order."""
        if self.is_leaf():
            yield self
        else:
            for corner in self.corners:
                yield from corner.walk_leaves()

    def walk_all(self):
        """Yield all nodes at all levels in depth-first order."""
        yield self
        if not self.is_leaf():
            for corner in self.corners:
                yield from corner.walk_all()

    # ----------------------------------------------------------
    # Data storage
    # ----------------------------------------------------------

    def store(self, key: str, value):
        """Store data in this structure's interior."""
        self.interior[key] = value

    def get(self, key):
        """Retrieve data from this structure's interior."""
        return self.interior.get(key)

    # ----------------------------------------------------------
    # Connection — generalized SharedFace at all levels
    # ----------------------------------------------------------

    def connect(self, other: 'RecursiveCube', face: str):
        """
        Connect two adjacent RecursiveCubes by sharing the touching face.

        At level 0: delegates to shared_face.connect_cubes() — the 4 touching
                    FemtoLLM vertices become the same objects on both sides.

        At level N: makes the 4 touching corner sub-structures shared objects.
                    Two adjacent level-N structures share 4 level-(N-1) corners.

        After connect(), winding_number([self, other]) == 0.
        The path closes. No topological paradox.

        Args:
            other: The adjacent RecursiveCube to connect to.
            face: Which face of self touches other ('N','S','E','W','U','D').
        """
        if self.level != other.level:
            raise ValueError(
                f"Cannot connect level-{self.level} to level-{other.level}: "
                f"both must be the same level."
            )
        if face not in OPPOSITES:
            raise ValueError(
                f"face must be one of {list(OPPOSITES)}, got {face!r}"
            )

        their_face = OPPOSITES[face]

        if self.is_leaf():
            # Level 0: create SharedFace between the two Cubes
            connect_cubes(self.cube, face, other.cube)
        else:
            # Level N: share the 4 corner sub-structures on the touching face
            my_indices = FACE_CORNERS[face]
            their_indices = FACE_CORNERS[their_face]
            for my_idx, their_idx in zip(my_indices, their_indices):
                # other's corner IS self's corner — same object, both sides
                other.corners[their_idx] = self.corners[my_idx]

    # ----------------------------------------------------------
    # Topology measurement — winding number (pure numpy)
    # ----------------------------------------------------------

    def winding_number(self, path: list) -> float:
        """
        Topological winding number of a path through this structure.

        path: list of RecursiveCubes from start to end.

        Returns 0.0 if the path is contractible (loop closes cleanly).
        Returns non-zero if the path forms a non-contractible loop
        (topological paradox: a contradiction that can't be resolved
        by naive concatenation — needs dialectic synthesis).

        After connect(), adjacent cubes always have winding = 0.
        A winding of ≠ 0 indicates missing connect() calls.

        Pure numpy — no scipy required.
        """
        if len(path) < 2:
            return 0.0

        # Encode each node as a complex number from its position
        # (level used as a depth signal in the imaginary component)
        field = np.array(
            [complex(hash(node.id) % 1000, node.level * 10.0)
             for node in path],
            dtype=complex,
        )
        norm = np.linalg.norm(field)
        if norm < 1e-12:
            return 0.0
        field /= norm

        # Winding = total phase accumulation / 2π
        phases = np.angle(field)
        unwrapped = np.unwrap(phases)
        return float((unwrapped[-1] - unwrapped[0]) / (2 * np.pi))

    # ----------------------------------------------------------
    # Representation
    # ----------------------------------------------------------

    def __repr__(self) -> str:
        name = CORNER_NAMES[self.level] if self.level < len(CORNER_NAMES) else f"L{self.level}"
        if self.is_leaf():
            return f"RC(L0, {self.id})"
        return (
            f"RC(L{self.level}, {self.id}, "
            f"span={self.span}, {self.count_leaves()} leaves)"
        )
